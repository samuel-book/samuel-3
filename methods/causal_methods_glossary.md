# Glossary

*From: Allen, M. (2026). Causal Inference Methods Guide: Measuring treatment effects from observational data. Zenodo. https://doi.org/10.5281/zenodo.24426809*

Plain-language definitions of the technical terms used in this guide, in alphabetical order. Abbreviations have their own entries that point to the main entry.

[A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · [Q](#q) · [R](#r) · [S](#s) · [T](#t) · [U](#u) · [W](#w) · [X](#x)

## A

**Abadie–Imbens standard error**  
A standard error for matching estimators that allows for the matching itself, including controls used more than once.

**AIPW**  
See [Augmented inverse-probability weighting (AIPW)](#gl-aipw).

<a id="gl-auc"></a>
**Area under the ROC curve (AUC)**  
A measure of discrimination: the probability that a model gives a higher predicted risk to a randomly chosen patient with the outcome than to one without it. 0.5 is no better than chance; 1 is perfect.

**Arm**  
One of the groups compared in a trial or emulated trial, such as the treated arm and the untreated (control) arm.

**ATE**  
See [Average treatment effect (ATE)](#gl-ate).

**ATT**  
See [Average treatment effect in the treated (ATT)](#gl-att).

**AUC**  
See [Area under the ROC curve (AUC)](#gl-auc).

<a id="gl-aipw"></a>
**Augmented inverse-probability weighting (AIPW)**  
A doubly robust estimator that combines an outcome model with propensity-score weights. It corrects the outcome model's predictions using weighted residuals, so the estimate is correct if either model is correct.

<a id="gl-ate"></a>
**Average treatment effect (ATE)**  
The average effect if everyone in the population received the treatment, compared with no one receiving it.

<a id="gl-att"></a>
**Average treatment effect in the treated (ATT)**  
The average effect of treatment among the patients who actually received it: how their outcomes compare with what would have happened to them without treatment. Our default estimand.

## B

**Balance**  
How similar treated and untreated groups are on baseline characteristics, usually measured by the standardised mean difference.

**BART**  
See [Bayesian additive regression trees (BART)](#gl-bart).

<a id="gl-bart"></a>
**Bayesian additive regression trees (BART)**  
A Bayesian model that predicts the outcome as the sum of many small decision trees. Used to estimate treatment effects and their uncertainty (Section 8).

**Benchmark bounds**  
In sensemakr, the adjusted estimate if an unmeasured confounder were one, two or three times as strongly related to treatment and outcome as a named measured covariate.

<a id="gl-blp"></a>
**Best linear predictor (BLP) test**  
A check on heterogeneity: the doubly robust effect for each patient is regressed on the model's predicted individual effect. A slope above 0 means real variation in benefit has been detected; a slope near 1 means the individual predictions are well calibrated.

**Bias**  
A systematic difference between an estimate and the true value that does not shrink as the sample grows.

**BLP**  
See [Best linear predictor (BLP) test](#gl-blp).

**Bootstrap**  
Repeating the whole analysis on many samples drawn with replacement from the data, to estimate how much the result would vary from sample to sample. Used to build confidence intervals.

## C

**Calibration**  
Agreement between predicted probabilities and observed outcome rates. A well-calibrated model that predicts 30% risk sees the outcome in about 30% of such patients. Summarised by the calibration intercept (ideally 0) and slope (ideally 1).

**Caliper**  
The largest difference allowed between a treated patient and their match, usually on the propensity score. Treated patients with no untreated patient within the caliper are left unmatched.

**CATE**  
See [Conditional average treatment effect (CATE)](#gl-cate).

**Causal forest**  
A random forest adapted to estimate treatment effects rather than outcomes. Each tree splits patients into groups whose treatment effects differ.

**CausalForestDML**  
The EconML class that fits a causal forest within the double machine learning framework.

**CI**  
See [Confidence interval (CI)](#gl-ci).

**CLAN**  
See [Group average treatment effects (GATES) and classification analysis (CLAN)](#gl-gates).

**Class weighting**  
Giving more weight to the rarer outcome class when training a classifier. It improves accuracy-type metrics but distorts predicted probabilities, so it is avoided when effects are computed from probabilities.

**Clipping (of propensity scores)**  
Replacing propensity scores below a small threshold (for example, 0.01) with that threshold, so that no patient receives an extreme weight.

**Clone-censor-weight**  
A design for strategies defined by timing or duration: each patient is copied into every strategy they are compatible with at time zero, censored when they deviate from it, and the censoring is corrected by weighting. It avoids immortal-time bias.

**Cluster-robust confidence interval**  
A confidence interval that allows observations within a cluster (for example, matched pairs sharing the same control) to be correlated.

**Coarsened exact matching**  
Exact matching on coarsened (banded) versions of variables, which allows more variables to be matched while keeping most patients.

**Comparator**  
The strategy that treatment is compared against, often “no treatment”.

**Complier**  
In an instrumental-variable analysis, a patient whose treatment depends on the instrument: they would be treated with one value of the instrument but not with another. Instrumental-variable estimates apply to compliers.

<a id="gl-cate"></a>
**Conditional average treatment effect (CATE)**  
The average effect for patients with a given set of characteristics. Estimated for each patient by the causal forest and the S-learner; also called the individual or heterogeneous treatment effect.

<a id="gl-ci"></a>
**Confidence interval (CI)**  
A range of values, calculated from the data, that would contain the true value in a stated proportion (usually 95%) of repeated studies.

**Confounder**  
A variable that affects both which treatment a patient receives and their outcome. Unadjusted confounding biases the estimated effect.

**Confounding by indication**  
Confounding that arises because clinicians choose treatment based on the patient's prognosis or condition, so treated and untreated patients differ systematically.

**Consistency**  
The assumption that “treatment” means the same thing for everyone given it, so that a patient's observed outcome equals their potential outcome under the treatment they received.

**Contour plot (sensitivity)**  
In sensemakr, a plot of the adjusted estimate for every combination of a hypothetical confounder's partial R² with treatment and with outcome.

**Control (matched control)**  
An untreated patient selected as the comparison for a treated patient.

**Control reuse**  
Allowing one untreated patient to serve as the matched control for more than one treated patient (matching with replacement). It raises the matching rate but makes pairs less independent.

**Counterfactual (potential outcome)**  
The outcome a patient would have had under a treatment they did not actually receive. It is never observed and must be estimated.

**Cross-fitting**  
Splitting the data into folds and predicting each fold with a model trained on the other folds, so that no patient's prediction comes from a model that has seen them. It prevents overfitting from biasing effect estimates.

**Cross-validation**  
Splitting the data into folds, training on some and testing on the rest in turn, to estimate how well a model performs on new data or to choose its settings.

## D

**DAG**  
See [Directed acyclic graph (DAG)](#gl-dag).

**Decile**  
One of ten equal-sized groups formed by ranking patients, for example by predicted risk.

**Delta method**  
An approximation for the variance of a function of estimated quantities, such as the time at which predicted benefit reaches zero.

**Difference-in-differences**  
Estimating the effect of a change by comparing the change in outcomes over time in places that made it with the change in places that did not.

<a id="gl-dag"></a>
**Directed acyclic graph (DAG)**  
A diagram of assumed causal relationships between variables, used to decide which variables to adjust for.

**Discrimination**  
How well a model separates patients who have the outcome from those who do not, usually measured by the AUC.

**DML**  
See [Double/debiased machine learning (DML)](#gl-dml).

<a id="gl-dml"></a>
**Double/debiased machine learning (DML)**  
A framework that estimates causal effects using machine-learning nuisance models, with cross-fitting and residualisation so that errors in the nuisance models have only a small effect on the final estimate.

<a id="gl-dr"></a>
**Doubly robust**  
An estimator that remains consistent if either the outcome model or the treatment (propensity) model is correctly specified, not necessarily both.

**DR**  
See [Doubly robust](#gl-dr).

**DR-learner**  
A meta-learner that estimates individual effects by regressing doubly robust pseudo-outcomes on patient characteristics.

## E

**EconML**  
A Python package from Microsoft Research implementing double machine learning, causal forests and meta-learners.

**Effect modifier**  
A characteristic across which the size of the treatment effect varies (in the causal forest, the variables *X*).

**Eligibility criteria**  
The conditions a patient must meet at time zero to be included in a trial or emulated trial.

**Entropy balancing**  
A weighting method that chooses weights for untreated patients so that the means (and, optionally, variances) of the confounders exactly equal those of the treated patients.

**Estimand**  
The precise quantity an analysis aims to estimate: which effect, in which population, on which scale (for example, the ATT as a difference in percentage points).

**E-value**  
The minimum strength of association, on the risk-ratio scale, that an unmeasured confounder would need with both treatment and outcome to fully explain away an observed effect.

**Exact matching**  
Pairing each treated patient with an untreated patient who has identical values on every matching variable.

**Exchangeability (no unmeasured confounding)**  
The assumption that, after adjusting for measured variables, treated and untreated patients are comparable, so that the untreated represent what would have happened to the treated without treatment.

**Exclusion restriction**  
The instrumental-variable assumption that the instrument affects the outcome only through the treatment.

**Extrapolation**  
Making predictions for patients unlike any in the data used to fit the model, so that the estimate relies on modelling assumptions rather than data.

## F

**First stage and second stage**  
In double machine learning, the first stage fits the nuisance models (outcome and propensity); the second stage estimates the treatment effect from their residuals.

**Fold**  
One of the equal parts into which data are split for cross-validation or cross-fitting.

**Follow-up**  
The period from time zero over which outcomes are recorded.

**Full matching**  
Matching that places every eligible patient in a subclass with at least one treated and one untreated patient, and uses weights, so that no eligible patient is discarded.

## G

**GATES**  
See [Group average treatment effects (GATES) and classification analysis (CLAN)](#gl-gates).

**G-formula (g-computation)**  
Estimating a treatment effect by modelling the outcome, predicting each patient's outcome under each treatment strategy, and averaging the predictions. The S-learner is a version of this for treatment at a single time.

**Gradient boosting**  
A machine-learning method that builds many small decision trees in sequence, each correcting the errors of the previous ones (implemented in XGBoost and LightGBM).

<a id="gl-gates"></a>
**Group average treatment effects (GATES) and classification analysis (CLAN)**  
Group average treatment effects (GATES) compare average effects across groups defined by predicted benefit; classification analysis (CLAN) describes the characteristics of the most and least affected groups.

## H

**Heterogeneity (of treatment effect)**  
Variation in the size of the treatment effect between patients or subgroups.

**Holm adjustment**  
A step-down method for controlling the chance of any false-positive finding when many hypotheses are tested.

**Honest tree**  
A tree that uses one half of its sample to choose splits and the other half to estimate effects within the resulting groups, which reduces overfitting and supports valid confidence intervals.

**Hyperparameter tuning**  
Choosing a model's settings (for example, tree depth or learning rate) by testing many combinations and keeping the one that performs best on held-out data.

## I

**Immortal-time bias**  
Bias that arises when a period during which the outcome cannot occur, such as the time before a treatment is given, is credited to the treated group.

**Influence function**  
A description of how much each observation contributes to an estimate, used to calculate standard errors for doubly robust estimators.

**Instrumental variable**  
A variable that affects which treatment is received but affects the outcome only through treatment (for example, a site's treatment rate). It can address unmeasured confounding under its own assumptions.

**Interference**  
When one patient's treatment affects another patient's outcome. Most analyses assume there is none.

**Interrupted time series**  
Estimating the effect of a change by comparing the trend in outcomes before and after it.

<a id="gl-ipw"></a>
**Inverse probability weighting (IPW)**  
Weighting each patient by the inverse of their probability of receiving the treatment they actually received, so that the weighted groups resemble each other.

**IPW**  
See [Inverse probability weighting (IPW)](#gl-ipw).

## L

**Landmark analysis**  
Restricting an analysis to patients still alive and in follow-up at a fixed time after time zero, as a crude check on immortal-time bias.

**Leave-one-out (of confounders)**  
Re-estimating the effect with one measured confounder removed, to show how much the result depends on it.

**LightGBM**  
A fast gradient-boosting library, used here for the first-stage models of the causal forest.

**Linear probability model**  
A linear regression with a binary (0/1) outcome, whose coefficients are differences in probability. Used as a simple stand-in model for sensemakr.

**Logistic regression**  
A regression model for a binary outcome that models the log-odds of the outcome as a linear combination of predictors.

**Log loss**  
A measure of probabilistic prediction error that penalises confident wrong predictions. Used for tuning because it rewards both discrimination and calibration.

**Log-odds**  
The logarithm of the odds, log{p/(1 − p)}. Effects on this scale are log odds ratios.

## M

**Mahalanobis distance**  
A measure of how far apart two patients are on several variables at once, allowing for the scale of each variable and the correlations between them.

**Marginal structural model**  
A model of outcomes under different treatment strategies, fitted with inverse probability weights. Often used when treatments and confounders change over time.

**Matching rate**  
The percentage of treated patients for whom a matched control was found.

**Matching variables**  
The confounders on which treated and untreated patients must be identical to form a matched pair.

**McNemar's test**  
A test for paired binary outcomes that compares the numbers of pairs in which only the treated, or only the control, patient had the outcome.

**Mediator**  
A variable on the causal pathway between treatment and outcome. Adjusting for it removes part of the effect being estimated.

**Meta-learner**  
A general recipe for estimating treatment effects using any prediction model; examples are the S-, T-, X- and DR-learners.

**Meta-model**  
A model fitted to individual estimated benefits, used to describe which characteristics are associated with larger or smaller benefit.

**Missing as its own category**  
Coding missing values of a categorical variable as a separate category, so that patients with missing data are kept in the analysis.

**Multiclass model**  
A classification model that predicts the probability of each of more than two categories, such as several treatment strategies.

**Multiple imputation**  
Filling in missing values several times by drawing from a model of the missing data, analysing each completed dataset and combining the results.

**Multiplicity**  
The increased chance of false-positive findings when many statistical tests are carried out.

## N

**Nearest-neighbour matching**  
Matching each treated patient to the untreated patient closest to them on a distance measure, such as the propensity score or Mahalanobis distance.

**Negative control**  
An outcome that the treatment cannot affect, or an exposure that cannot affect the outcome. An apparent effect on a negative control signals residual confounding or bias.

**Nested tuning**  
Repeating hyperparameter tuning inside each training fold, so that the chosen settings never see the patients they are evaluated on.

**Non-exact matching**  
Matching treated patients to untreated patients who are similar but not identical, using a distance measure, a propensity score or both (Section 3.5).

**Nuisance model**  
A model needed to estimate the effect but not itself of interest, such as the outcome and propensity models in the first stage of double machine learning.

## O

**Observational data**  
Data collected during routine care or in registries, where treatment was not assigned at random.

<a id="gl-or"></a>
**Odds ratio (OR)**  
The ratio of the odds of the outcome in treated versus untreated patients. It is further from 1 than the risk ratio when the outcome is common.

**Omitted variable bias**  
Bias in a regression estimate caused by leaving out a variable related to both treatment and outcome; the basis of sensemakr.

**Optimism**  
The amount by which a model's performance on the data used to build it overstates its performance on new data.

**Optuna**  
A Python library for hyperparameter tuning that searches efficiently and stops unpromising trials early.

**OR**  
See [Odds ratio (OR)](#gl-or).

**Out-of-bag estimate**  
In a forest, a prediction for a patient made only by the trees that did not use that patient in their training sample.

**Out-of-fold prediction**  
A prediction for a patient made by a model trained on other folds of the data (see cross-fitting).

**Overfitting**  
When a model learns noise in the training data, so that it performs well on those data but poorly on new data.

**Overlap weights**  
Propensity-score weights that give most weight to patients who could plausibly have received either treatment and little to those almost certain to receive one, which avoids extreme weights.

## P

**Paired analysis**  
An analysis that compares outcomes within matched pairs, such as McNemar's test, the paired *t*-test or the Wilcoxon signed-rank test.

**Parallel trends**  
The difference-in-differences assumption that, without the change, outcomes in the compared groups would have followed the same path over time.

**Partial R²**  
The share of the remaining variance of a variable explained by another variable after accounting for the covariates; the scale used by sensemakr.

**Percentage points**  
The unit of an absolute difference between two percentages (for example, 40% versus 30% is a difference of 10 percentage points).

**Placebo test**  
An analysis in which the treatment or its timing is deliberately scrambled; any apparent effect points to bias in the method.

**Policy learning**  
Using estimated treatment effects to derive and evaluate a rule for deciding whom to treat.

**Policy tree**  
A shallow decision tree that assigns treatment based on a few patient characteristics, chosen to maximise estimated benefit.

**Positivity (overlap)**  
The assumption that patients with each combination of characteristics have some chance of receiving each treatment, so comparable treated and untreated patients exist.

**Probability scale**  
Expressing effects as differences in the probability of the outcome (in percentage points), as opposed to odds or log-odds.

**Propensity score**  
A patient's probability of receiving a treatment given their characteristics.

**Propensity-score matching**  
Matching treated and untreated patients on their propensity scores, rather than on each confounder separately.

**Protocol**  
The written specification of a trial or emulated trial: eligibility, strategies, assignment, time zero, follow-up, outcomes, causal contrast and analysis.

**Pseudo-outcome**  
A constructed outcome for each patient whose average equals the treatment effect, used as the target in a second-stage regression (for example, in the DR-learner).

## Q

**Quantitative bias analysis**  
Estimating how much a specified source of bias, such as a named unmeasured confounder with assumed strength and prevalence, would change the result.

## R

**Random forest**  
A prediction method that averages many decision trees, each grown on a random sample of patients and features.

<a id="gl-rct"></a>
**Randomised controlled trial (RCT)**  
A study in which treatment is assigned by chance, so that treated and untreated groups are comparable on average in both measured and unmeasured characteristics.

**Random seed**  
A number that fixes the sequence of random choices in an analysis, so that results can be reproduced.

**RCT**  
See [Randomised controlled trial (RCT)](#gl-rct).

**Regression adjustment**  
Including covariates in a regression model of the outcome to remove remaining differences between groups.

**Regression discontinuity design**  
Comparing patients just above and just below a threshold that decides treatment (such as a time limit), who are otherwise similar.

**Regularisation**  
Penalising model complexity during fitting to reduce overfitting.

**Residual**  
The difference between an observed value and a model's prediction of it.

**Residual confounding**  
Confounding that remains after adjustment, for example because a variable was grouped into broad bands or measured imperfectly.

**Residualisation**  
Removing the part of a variable that can be predicted from covariates, leaving only its residual.

<a id="gl-rr"></a>
**Risk ratio (RR)**  
The proportion with the outcome in treated patients divided by the proportion in untreated patients.

**Risk-set matching**  
Matching each patient treated at a given time to a patient who is still untreated and still eligible at that time. Used when treatment strategies are defined by the timing of treatment.

**R-learner**  
A meta-learner that estimates individual treatment effects from the residuals of the outcome and treatment models, which makes it robust to errors in those models.

<a id="gl-rv"></a>
**Robustness value (RV)**  
In sensemakr, the minimum partial R² an unmeasured confounder would need with both treatment and outcome to reduce the estimate to zero (RV<sub>α</sub>: to make it no longer statistically significant).

**ROC**  
See [Area under the ROC curve (AUC)](#gl-auc).

**RR**  
See [Risk ratio (RR)](#gl-rr).

**RV**  
See [Robustness value (RV)](#gl-rv).

## S

**Selection by indication**  
When the patients who undergo a test or receive a treatment are chosen because of their clinical features, so they differ systematically from those who do not.

**Sensemakr**  
A sensitivity-analysis method that describes the strength of a hypothetical unmeasured confounder by its partial R² with treatment and outcome, benchmarked against measured covariates.

**Sensitivity analysis**  
Repeating an analysis with one choice or assumption changed, to see whether the conclusions still hold.

**Sentinel value**  
A value far outside the real range (for example, 99,999 minutes) used to code “treatment not given” in a continuous variable.

**SHAP**  
See [SHapley Additive exPlanations (SHAP)](#gl-shap).

<a id="gl-shap"></a>
**SHapley Additive exPlanations (SHAP)**  
A method that attributes a model's prediction for each patient to the contributions of individual features.

**S-learner (single learner)**  
A meta-learner that fits one model to predict outcome from characteristics and treatment, then estimates effects by changing the treatment input.

**SMD**  
See [Standardised mean difference (SMD)](#gl-smd).

**SSNAP**  
Sentinel Stroke National Audit Programme: the national audit of stroke care in England, Wales and Northern Ireland, and the source of the data analysed in the SAMueL-3 project.

**Standard error**  
The estimated standard deviation of an estimate across repeated samples; used to build confidence intervals.

<a id="gl-smd"></a>
**Standardised mean difference (SMD)**  
The difference in means between two groups divided by their pooled standard deviation; absolute values below 0.1 usually indicate good balance.

**Stratum (plural strata)**  
A subgroup of patients who share the same values of the stratifying (for example, matching) variables.

**Super Learner**  
A method that combines several machine-learning models, weighted by their cross-validated performance. Often used with TMLE.

**Synthetic control**  
A weighted combination of places (such as regions or hospitals) without a change, chosen to match a changed place's outcomes before the change, and used as its comparison afterwards.

## T

<a id="gl-tmle"></a>
**Targeted maximum likelihood estimation (TMLE)**  
A doubly robust method that updates an initial outcome model in a targeted way to reduce bias in the effect estimate.

**TARGET statement**  
Reporting guidance for observational studies that emulate a target trial.

**Target trial**  
The hypothetical randomised trial that would answer the causal question, whose protocol an observational analysis is designed to emulate.

**Time zero**  
The point at which eligibility is met, treatment strategies are assigned and follow-up begins. It must be the same for all compared groups.

**Time-varying confounding**  
Confounding by factors that change during follow-up and may themselves be affected by earlier treatment.

**T-learner (two learner)**  
A meta-learner that fits separate outcome models for treated and untreated patients and takes the difference in their predictions.

**TMLE**  
See [Targeted maximum likelihood estimation (TMLE)](#gl-tmle).

**Transportability**  
Re-weighting an effect estimate so that it applies to a different target population, such as a trial population or another region.

**Treatment strategy**  
A precisely defined plan of treatment, including what is given and when (for example, “thrombolysis within 270 minutes”).

**Trimming**  
Excluding patients with extreme propensity scores (for example, outside 0.05–0.95) so that estimates do not rely on extrapolation or extreme weights.

**TRIPOD**  
Reporting guidance for studies that develop or validate prediction models.

## U

**Unmeasured confounding**  
Confounding by variables that are not recorded in the data, which no adjustment method can remove directly.

## W

**Wilcoxon signed-rank test**  
A non-parametric test comparing paired continuous measurements.

## X

**XGBoost**  
A widely used gradient-boosting library, used here for the S-learner outcome model.

**X-learner**  
A meta-learner that imputes individual effects using models for each group, then combines them with weights based on the propensity score; useful when treatment groups differ greatly in size.
