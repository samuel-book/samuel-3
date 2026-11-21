# SAMueL-3: Stroke Audit Machine Learning

Causal machine learning and target trial emulation to estimate the effects of intravenous thrombolysis (IVT) and mechanical thrombectomy (MT) on outcomes at hospital discharge after ischaemic stroke, and how those effects vary with stroke severity and patient characteristics. The analyses use national stroke audit (SSNAP) data for England and Wales.

Project repository: https://github.com/samuel-book/samuel-3

Unless stated otherwise, a **good outcome** is a discharge modified Rankin Scale (mRS) of 0–2, or a discharge mRS no worse than the pre-stroke mRS. Notebooks also report mRS 0–2 alone and other outcome definitions as sensitivity analyses.

Within each folder, notebooks are numbered in the order they are intended to be run.

## Folders

### `1_descriptive_stats/`

Descriptive statistics.

- `01_correlations.ipynb`: correlations between variables in the data.
- `02_thrombctomy.ipynb`: descriptive statistics for thrombectomy.

### `2_feature_selection/`

Forward feature selection for outcomes and for treatment use, for all patients and for untreated patients.

- `01_feature_selection_disability.ipynb`: disability (mRS) at discharge.
- `02_feature_selection_disability_no_treatment.ipynb`: disability (mRS) at discharge, untreated patients.
- `03_feature_selection_los.ipynb`: length of stay.
- `04_feature_selection_los_no_treatmnent.ipynb`: length of stay, untreated patients.
- `05_feature_selection_thrombolysis.ipynb`: use of thrombolysis.
- `06_feature_selection_thrombectomy.ipynb`: use of thrombectomy.
- `07_feature_selection_thrombolysis_induced_haemorrhage.ipynb`: thrombolysis-induced haemorrhage.
- `08_feature_selection_disability_less_3.ipynb`: mRS 0–2 at discharge.
- `08_feature_selection_disability_less_3_or_not_worse.ipynb`: good outcome (mRS 0–2, or not worse than pre-stroke) at discharge.
- `09_feature_selection_disability_less_6.ipynb`: mRS 0–5 (survival) at discharge.
- `10_feature_selection_disability_less_3_no_treatment.ipynb`: good outcome (mRS 0–2, or not worse than pre-stroke) at discharge, untreated patients.
- `11_feature_selection_disability_less_6_no_treatment.ipynb`: mRS 0–5 (survival) at discharge, untreated patients.
- `90_plot_feature_selection.ipynb`: plots the feature selection results.

### `3_SHAP/`

Outcome and treatment-use models explained with SHAP values.

- `01_shap_survival_all_patients.ipynb`: survival, all patients.
- `02_shap_mrs_0_2_all_patients.ipynb`: mRS 0–2 at discharge, all patients.
- `02a_shap_good_outcome_all_patients.ipynb`: good outcome at discharge, all patients.
- `03_shap_mrs_3_5_all_patients.ipynb`: mRS 3–5 at discharge, all patients.
- `04_shap_mrs_3_5_all_patients_survivers.ipynb`: mRS 3–5 at discharge, all surviving patients.
- `05_thrombolysis_use_all_patients.ipynb`: use of thrombolysis.
- `06_thrombectomy_use_all_patients.ipynb`: use of thrombectomy.
- `07_thrombolysis_induced_haemorrhages.ipynb`: thrombolysis-induced haemorrhage.
- `08_shap_los_all_patients.ipynb`: length of stay, all patients.
- `09_shap_survival_untreated_patients.ipynb`: survival, untreated patients.
- `10_shap_mrs_0_2_untreated_patients.ipynb`: mRS 0–2 at discharge, untreated patients.
- `10a_shap_good_outcome_untreated_patients.ipynb`: good outcome at discharge, untreated patients.
- `11_shap_mrs_3_5_untreated_patients.ipynb`: mRS 3–5 at discharge, untreated patients.
- `12_shap_los_surviving_patients.ipynb`: length of stay, surviving patients.

### `4_target_trial_emulation/`

Target trial emulation, matching treated and untreated patients exactly. `trial_groups.csv` defines the trial groups; `output/` holds result tables and charts.

- `01_non_mild_thrombolysis_thrombectomy_target_trial_good_outcome.ipynb`: IVT and MT strategies in non-mild stroke arriving within 6 hours.
- `02_mild_thrombolysis_by_nihss_1_to_5_target_trial_good_outcome.ipynb`: thrombolysis in mild stroke (NIHSS 1–5) arriving within 4 hours, by individual NIHSS score.
- `03_target_trials_all_patients_treatments.ipynb`: IVT and MT across all stroke severities, with good outcome, death, length of stay and discharge disability as outcomes, plus sensitivity analyses.

### `5_ml_s_learner/`

S-learner analyses: a single outcome model with treatment as a feature, with effects estimated by switching treatment on and off.

- `01_non_mild_thrombolysis_thrombectomy_s_learner_good_outcome.ipynb`: IVT and MT in non-mild stroke arriving within 6 hours.
- `02_mild_thrombolysis_s_learner_mRS_2.ipynb`: thrombolysis in mild stroke (NIHSS 1–5) arriving within 4 hours.

### `6_ml_double_robust_causal_forest/`

Doubly robust causal forest analyses (EconML) of heterogeneous treatment effects. Results can be compared with folders 4 and 5.

- `01_non_mild_thrombolysis_thrombectomy_causal_forest_good_outcome.ipynb`: IVT and MT in non-mild stroke arriving within 6 hours.
- `02_mild_thrombolysis_causal_forest_good_outcome.ipynb`: thrombolysis in mild stroke (NIHSS 1–5) arriving within 4 hours.

### `9_DAGs/`

Directed acyclic graphs (DAGs) of the key determinants of treatment use and outcome.

- `01_thrombolysis_thrombectomy_dag.ipynb`: draws the DAGs with Graphviz and saves them as PNGs for non-mild and mild stroke with early arrival.

### `methods/`

A written description of the causal methods ([PDF](methods/samuel_3_causal_methods_description.pdf)) and a plain-language [glossary](methods/causal_methods_glossary.md) of the terms and abbreviations used.

### `data/`

Input data: SSNAP-derived datasets (`sam2/`, `sam3/`) and SSNAP annual reports. The patient-level data come from the Sentinel Stroke National Audit Programme (SSNAP) and are not publicly available; access is through the data controller, the Healthcare Quality Improvement Partnership (HQIP). Some files are read with `cryptpandas` (encrypted DataFrames), which needs the corresponding password.

### `output/`

Shared outputs.

## Setting up the environment

The conda environment is defined in `sam_3_environment.yml` (Python 3.12):

```bash
conda env create -f sam_3_environment.yml
conda activate sam3
jupyter lab
```

## Licence

MIT — see [LICENSE](LICENSE).
