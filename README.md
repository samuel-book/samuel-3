# SAMueL-3: Stroke Audit Machine Learning

Causal machine learning and target trial emulation to estimate the effects of thrombolysis and thrombectomy on outcomes after ischaemic stroke, using national stroke audit (SSNAP) data for England and Wales.

Project repository: https://github.com/samuel-book/samuel-3

## Aims

SAMueL-3 asks how much intravenous thrombolysis (IVT) and mechanical thrombectomy (MT) change outcomes at hospital discharge, and how that effect varies with stroke severity and patient characteristics. The main questions are:

- **Non-mild stroke arriving within 6 hours:** the effect of IVT and MT treatment strategies on a good outcome at discharge.
- **Mild stroke (NIHSS 1–5) arriving within 4 hours:** whether thrombolysis improves outcome, including by individual NIHSS score.
- **All ischaemic stroke:** treatment effects across the range of stroke severity, with death, length of stay and discharge disability as outcomes.

Unless stated otherwise, a **good outcome** is a discharge modified Rankin Scale (mRS) of 0–2, or a discharge mRS no worse than the pre-stroke mRS. Notebooks also report mRS 0–2 alone and other outcome definitions as sensitivity analyses.

## Methods

The same questions are answered with complementary methods, so that results can be compared across approaches:

| Method | Folder | Notes |
|---|---|---|
| Target trial emulation | `4_target_trial_emulation/` | Exact matching of treated and untreated patients (plus a non-exact matching variant) |
| S-learner | `5_ml_s_learner/` | A single outcome model with treatment as a feature; effects estimated by switching treatment on and off |
| Doubly robust causal forest | `6_ml_double_robust_causal_forest/` | Heterogeneous treatment effects using EconML |

A written description of the causal methods is in [`methods/samuel_3_causal_methods_description.pdf`](methods/samuel_3_causal_methods_description.pdf). A plain-language glossary of the terms and abbreviations used is in [`methods/causal_methods_glossary.md`](methods/causal_methods_glossary.md).

## Repository structure

| Folder | Contents |
|---|---|
| `1_descriptive_stats/` | Correlations in the data; thrombectomy descriptive statistics |
| `2_feature_selection/` | Forward feature selection for each outcome (disability, mRS 0–2, good outcome, length of stay, survival) and for treatment use (thrombolysis, thrombectomy, thrombolysis-induced haemorrhage), for all patients and for untreated patients; `90_plot_feature_selection.ipynb` plots the results |
| `3_SHAP/` | Outcome and treatment-use models explained with SHAP values: survival, mRS 0–2, good outcome, mRS 3–5, length of stay, thrombolysis and thrombectomy use, thrombolysis-induced haemorrhage |
| `4_target_trial_emulation/` | Target trial emulations (see below); `trial_groups.csv` defines the trial groups and `output/` holds result tables and charts |
| `5_ml_s_learner/` | S-learner analyses for non-mild stroke (IVT and MT) and mild stroke (IVT) |
| `6_ml_double_robust_causal_forest/` | Doubly robust causal forest analyses for non-mild stroke (IVT and MT) and mild stroke (IVT) |
| `9_DAGs/` | Directed acyclic graph (DAG) of the key determinants of thrombolysis use and outcome, drawn with Graphviz |
| `methods/` | Methods description (PDF) and glossary (Markdown) |
| `data/` | Input data (SSNAP-derived datasets and SSNAP annual reports); see *Data* below |
| `output/` | Shared outputs |

### Target trial emulation notebooks

- **IVT and MT strategies in non-mild stroke arriving within 6 hours (exact matching)**  
  [`01_non_mild_thrombolysis_thrombectomy_target_trial_good_outcome.ipynb`](4_target_trial_emulation/01_non_mild_thrombolysis_thrombectomy_target_trial_good_outcome.ipynb)

- **IVT and MT strategies in non-mild stroke arriving within 6 hours (non-exact matching)**  
  [`01a_non_mild_thrombolysis_thrombectomy_target_trial_non_exact_good_outcome.ipynb`](4_target_trial_emulation/01a_non_mild_thrombolysis_thrombectomy_target_trial_non_exact_good_outcome.ipynb)

- **Thrombolysis in mild stroke (NIHSS 1–5) arriving within 4 hours, by individual NIHSS score**  
  [`02_mild_thrombolysis_by_nihss_1_to_5_target_trial_good_outcome.ipynb`](4_target_trial_emulation/02_mild_thrombolysis_by_nihss_1_to_5_target_trial_good_outcome.ipynb)

- **IVT and MT across all stroke severities: good outcome, death, length of stay and discharge disability, with sensitivity analyses**  
  [`03_target_trials_all_patients_treatments.ipynb`](4_target_trial_emulation/03_target_trials_all_patients_treatments.ipynb)

Notebooks are numbered in the order they are intended to be run within each folder.

## Data

The analyses use patient-level data from the Sentinel Stroke National Audit Programme (SSNAP). These data are not publicly available; access is through the data controller, the Healthcare Quality Improvement Partnership (HQIP). Code in this repository expects the data in `data/`, and some files are read with `cryptpandas` (encrypted DataFrames), which needs the corresponding password.

## Setting up the environment

The conda environment is defined in `sam_3_environment.yml` (Python 3.12):

```bash
conda env create -f sam_3_environment.yml
conda activate sam3
jupyter lab
```

Main packages: pandas, NumPy, scikit-learn, XGBoost, LightGBM, SHAP, statsmodels, EconML, DoWhy, causal-learn, gCastle, miceforest, Optuna, PyTorch, Graphviz and NetworkX.

## Licence

MIT — see [LICENSE](LICENSE).
