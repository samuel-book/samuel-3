# The Double-Robust Causal Forest

## Overview

This document describes the method implemented in `wip_causal_forest_with_sampling.ipynb`,
which uses EconML's `CausalForestDML` to estimate heterogeneous treatment effects of
thrombolysis and thrombectomy on stroke outcomes (discharge mRS 0–2).

The **double-robust causal forest** combines three ideas:

1. **Double / Debiased Machine Learning (DML)** — for confounding removal via orthogonalization.
2. **Generalized Random Forests (GRF)** — for adaptive, local, honest estimation of heterogeneous effects.
3. **An augmented (doubly-robust / AIPW-style) score** — which makes the estimator forgiving of nuisance-model errors.

The target estimand is the **Conditional Average Treatment Effect (CATE)**:

\[
\tau(x) = \mathbb{E}\!\left[\,Y(1) - Y(0) \mid X = x\,\right]
\]

In the strategy analysis this is the risk difference in \(P(\text{mRS } 0\text{–}2)\) for a given
treatment arm versus "neither," as a function of pre-treatment clinical covariates \(X\).

---

## 1. Motivation

The naive **S-learner** approach (train one outcome model on treatment + covariates, flip the
treatment feature, re-predict, and subtract) conflates predictive accuracy with causal estimation
and provides no honest confidence intervals. The causal forest addresses both problems: it
isolates the causal signal through orthogonalization and delivers asymptotically valid interval
estimates through forest honesty.

---

## 2. Orthogonalization (the DML / R-learner residual-on-residual trick)

Rather than modelling \(Y\) directly, two **nuisance models** first partial out the confounders \(W\):

- **Outcome model:** \(m(W) = \mathbb{E}[Y \mid W]\) (in the notebook: `model_y`, an `LGBMClassifier`).
- **Treatment / propensity model:** \(e(W) = \mathbb{E}[T \mid W]\) (in the notebook: `model_t`, a
  classifier for discrete arms, a regressor for continuous timing).

Residuals are then formed:

\[
\tilde{Y} = Y - \hat{m}(W), \qquad \tilde{T} = T - \hat{e}(W)
\]

and the treatment effect is estimated from the relationship between these residuals. This is
Robinson's partialling-out, generalized by Chernozhukov et al. (2018), and generalized to
heterogeneous effects by the R-learner (Nie & Wager, 2021). It renders the estimator
**Neyman-orthogonal**: small errors in the nuisance estimates have only a *second-order* effect on
\(\hat{\tau}\). This is the mathematical core of "debiasing."

---

## 3. Cross-fitting

The nuisances \(\hat{m}\) and \(\hat{e}\) must be estimated on data disjoint from the fold where
residuals are evaluated; otherwise overfitting reintroduces bias. In the notebook, `cv=5` performs
K-fold cross-fitting so that each patient's residuals come from nuisance models that never saw that
patient. Passing `groups=stroke_team` makes the folds **cluster-robust**, preventing
hospital-level correlation from leaking across the train/evaluation split.

> Note: resampling with replacement (the balanced-bootstrap debug option) duplicates patients.
> Duplicates landing in different folds break honesty and narrow confidence intervals. Cluster
> grouping only mitigates this if duplicates share a cluster id.

---

## 4. The doubly-robust (augmented) score

The forest does not split on raw residuals; it targets a **doubly-robust pseudo-outcome** that
combines both nuisance models. Schematically, for the binary-treatment case:

\[
\Gamma_i =
\hat{\mu}(1, X_i) - \hat{\mu}(0, X_i)
+ \frac{T_i\,\bigl(Y_i - \hat{\mu}(1, X_i)\bigr)}{\hat{e}(X_i)}
- \frac{(1 - T_i)\,\bigl(Y_i - \hat{\mu}(0, X_i)\bigr)}{1 - \hat{e}(X_i)}
\]

The defining property: \(\mathbb{E}[\Gamma_i \mid X] = \tau(X)\) provided that **either** the
outcome model **or** the propensity model is correctly specified — not necessarily both. With
flexible ML learners neither is exactly correct, but the orthogonal score means their errors
*multiply*, so each need only converge at the mild \(n^{1/4}\) rate for \(\hat{\tau}\) to be
\(\sqrt{n}\)-consistent and asymptotically normal. This is what yields valid confidence intervals.

---

## 5. The forest as an adaptive kernel (GRF + honesty)

The **generalized random forest** grows trees that split to maximize *heterogeneity in the
treatment effect* rather than outcome MSE. The forest is then interpreted not as a predictor but as
an **adaptive weighting function**: for a target point \(x\), the trees define weights
\(\alpha_i(x)\) — how often patient \(i\) falls in the same leaf as \(x\) — and \(\hat{\tau}(x)\)
solves a local moment equation weighted by those \(\alpha_i(x)\). The forest thus learns a
data-driven neighbourhood in which to solve the DML residual regression.

**Honesty** (`honest=True`) is the key GRF ingredient for inference: within each tree, one
subsample decides the splits while a *separate* subsample estimates the leaf effects. This
decorrelates split selection from estimation and underpins the asymptotic normality — and hence the
validity of `ate_interval` and `const_marginal_effect_interval`. In the notebook,
`min_samples_leaf=25` and `n_estimators=2000` control the bias/variance trade-off and the stability
of the weights.

---

## 6. Continuous treatment (the timing forests)

For the timing analysis (`discrete_treatment=False`) there is no per-arm propensity; instead
`model_t` is a regressor estimating \(\mathbb{E}[T \mid W]\), and the forest estimates a
**constant marginal effect** — the local slope \(\partial\,\mathbb{E}[Y] / \partial T\) — through
the same residual-on-residual local regression. This is reported as `const_marginal_effect`: the
per-minute (scaled to per-hour) partial effect of treatment delay on \(P(\text{mRS } 0\text{–}2)\).

---

## 7. Pipeline summary

| Stage | Concept | Notebook implementation |
|---|---|---|
| Nuisances | \(\hat{m}(W)\), \(\hat{e}(W)\) via ML | `make_nuisances` (LightGBM) |
| Orthogonalization | residual-on-residual (R-learner) | `CausalForestDML` internals |
| Cross-fitting | out-of-fold nuisances | `cv=5`, `groups=` |
| DR score | AIPW pseudo-outcome | discrete/continuous score inside EconML |
| Adaptive local fit | GRF weighting + honesty | `n_estimators=2000`, `honest=True`, `min_samples_leaf=25` |
| Inference | asymptotically normal CIs | `ate_interval`, `const_marginal_effect_interval` |
| Effect modification | honest test, not just importance | `best_linear_projection` (BLP) |

---

## 8. Effect modification via the Best Linear Projection

The best linear projection (BLP) of the estimated CATE onto interpretable covariates provides an
*honest test* of effect modification (whether the treatment effect genuinely varies with a
covariate), as opposed to a mere importance measure such as a SHAP dependence plot. A significant
BLP coefficient indicates that the treatment effect changes with that covariate. See Semenova &
Chernozhukov (2021).

---

## 9. Practical note on the balanced-bootstrap smoke test

Because the DR score is orthogonal, a weaker outcome model (e.g. AUC ≈ 0.74 on the balanced
bootstrap versus ≈ 0.82 for the S-learner) is tolerable provided the propensity model is
reasonable. However, the balanced resample distorts the true propensity distribution \(e(x)\) and
narrows the confidence intervals, so those numbers should be treated as a smoke test. The
doubly-robust guarantee holds on the full cohort (`BOOTSTRAP_BALANCED = False`), where both
nuisances are estimated under the natural treatment prevalences.

---

## References

- Wager, S., & Athey, S. (2018). Estimation and Inference of Heterogeneous Treatment Effects using
  Random Forests. *Journal of the American Statistical Association*, 113(523), 1228–1242.
  https://www.tandfonline.com/doi/full/10.1080/01621459.2017.1319839

- Athey, S., Tibshirani, J., & Wager, S. (2019). Generalized Random Forests. *The Annals of
  Statistics*, 47(2), 1148–1178.
  https://projecteuclid.org/journals/annals-of-statistics/volume-47/issue-2/Generalized-random-forests/10.1214/18-AOS1709.full

- Chernozhukov, V., Chetverikov, D., Demirer, M., Duflo, E., Hansen, C., Newey, W., & Robins, J.
  (2018). Double/Debiased Machine Learning for Treatment and Structural Parameters. *The
  Econometrics Journal*, 21(1), C1–C68.
  https://academic.oup.com/ectj/article/21/1/C1/5056401

- Nie, X., & Wager, S. (2021). Quasi-Oracle Estimation of Heterogeneous Treatment Effects (the
  R-learner). *Biometrika*, 108(2), 299–319.
  https://academic.oup.com/biomet/article/108/2/299/5911092

- Semenova, V., & Chernozhukov, V. (2021). Debiased Machine Learning of Conditional Average
  Treatment Effects and Other Causal Functions (Best Linear Projection). *The Econometrics
  Journal*, 24(2), 264–289.
  https://academic.oup.com/ectj/article/24/2/264/5899048

- Robinson, P. M. (1988). Root-N-Consistent Semiparametric Regression. *Econometrica*, 56(4),
  931–954. https://www.jstor.org/stable/1912705

- EconML `CausalForestDML` documentation. Microsoft Research.
  https://econml.azurewebsites.net/_autosummary/econml.dml.CausalForestDML.html
