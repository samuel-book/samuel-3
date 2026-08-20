# Function to create synthetic stroke data with causal treatment effect size

import numpy as np
import pandas as pd

def create_stroke_data(N=1000, seed=42):

    np.random.seed(seed)

    # ------------------------ Patient characteristics -------------------------

    # --- Demographics
    age = np.random.randint(60, 96, size=N)
    ethnicity = np.random.choice(['white', 'asian', 'black'], size=N, 
                                 p=[0.70, 0.20, 0.10])
    male = np.random.randint(0, 2, size=N)

    # --- Warfarin (20% prevalence) ---
    warfarin = np.random.binomial(1, 0.20, size=N)

    # --- Noise variables (no causal role) ---
    shoe_size = np.random.triangular(5, 9, 13, size=N).astype(int)

    # --- NIHSS stroke severity (triangular distribution, 0–30, mode 10) ---
    nihss = np.random.triangular(0, 10, 30, size=N).astype(int)

    # --- Mortality probability without treatment ---
    mortality_prob_no_treatment = np.full(N, 0.10)
    mortality_prob_no_treatment += (age - 60) * 0.01
    mortality_prob_no_treatment[male == 1] += 0.10
    mortality_prob_no_treatment += nihss * 0.01
    mortality_prob_no_treatment = np.clip(mortality_prob_no_treatment, 0, 1)
    mortality_prob_no_treatment[ethnicity == 'black'] += 0.2
    mortality_prob_no_treatment[ethnicity == 'asian'] += 0.1

    # Clip the mortality probabilities to ensure they are between 0 and 1
    mortality_prob_no_treatment = np.clip(mortality_prob_no_treatment, 0, 1)

    # Calculate odds and log-odds for mortality probability
    odds_no_treatment = (
        mortality_prob_no_treatment / (1 - mortality_prob_no_treatment))
    log_odds_no_treatment = np.log(odds_no_treatment)
    

    #  --------------- Probability of receiving thrombolysis -------------------

    prob_thrombolysis = np.full(N, 0.50)

    # NIHSS effect on thrombolysis probability:
    #   - eligibility/probability of thrombolysis (zero below 5, ramps 5-10, 
    #   - stable 10-20, ramps down 20-30)

    def nihss_weight(n):
        """Returns a 0–1 weight encoding the NIHSS-driven profile."""
        if n < 5:
            return 0.0
        elif n < 10:
            return (n - 5) / 5.0
        elif n <= 20:
            return 1.0
        elif n <= 30:
            return (30 - n) / 10.0
        else:
            return 0.0

    nihss_wt = np.array([nihss_weight(n) for n in nihss])
    prob_thrombolysis *= nihss_wt

    # Set the probability of thrombolysis to 0 for patients on warfarin
    prob_thrombolysis[warfarin == 1] = 0.0

    #  ------------------------- Treatment effect ------------------------------

    base_log_odds_ratio = 2

    # Set time to thrombolysis as uniiformly distributed between 30- 360 minutes
    thrombolysis_time = np.random.uniform(30, 360, size=N)

    # Scale log odds ratio based on time to thrombolysis (zero at 360 minutes)
    multiplier = np.clip((360 - thrombolysis_time) / 360, 0, 1)
    log_odds_ratio = base_log_odds_ratio * multiplier

    # Halve the log odds ratio for asian patients
    log_odds_ratio[ethnicity == 'asian'] *= 0.5

    # Calculate adjusted mortality log odds with treatment effect
    adjusted_log_odds = log_odds_no_treatment - log_odds_ratio

    # Calculate adjusted mortality probability with treatment effect
    adjusted_odds = np.exp(adjusted_log_odds)
    mortality_prob_with_treatment = adjusted_odds / (1 + adjusted_odds)

    prob_diff = mortality_prob_no_treatment - mortality_prob_with_treatment

    #  ------------------------- Treatment assignment --------------------------
    thrombolysis = np.random.binomial(1, prob_thrombolysis, size=N)


    #  ------------------------- Mortality outcome -----------------------------
    mortality_prob = np.where(thrombolysis == 1, mortality_prob_with_treatment,
                              mortality_prob_no_treatment)
    
    died = np.random.binomial(1, mortality_prob, size=N)


    # ------------------------  Return DataFrame -------------------------------

    # --- DataFrame ---
    df = pd.DataFrame({
        "patient_id": np.arange(1, N + 1),
        "age": age,
        "ethnicity": ethnicity,
        "male": male,
        "warfarin": warfarin,
        "shoe_size": shoe_size,
        "nihss": nihss,
        "thrombolysis_time": np.round(thrombolysis_time, 0),
        "thrombolysis": thrombolysis,
        "mortality_prob_no_treatment": mortality_prob_no_treatment,
        "mortality_odds_no_treatment": np.round(odds_no_treatment, 4),
        "mortality_log_odds_no_treatment": np.round(log_odds_no_treatment, 4),
        "mortality_prob_with_treatment": np.round(mortality_prob_with_treatment, 4),
        "mortality_odds_with_treatment": np.round(adjusted_odds, 4),
        "mortality_log_odds_with_treatment": np.round(adjusted_log_odds, 4),
        "odds_ratio_if_treated": np.round(np.exp(log_odds_ratio), 4),
        "log_odds_ratio_if_treated": np.round(log_odds_ratio, 4),
        "probability_difference": np.round(prob_diff, 4),
        "mortality_probability": np.round(mortality_prob, 4),
        "died": died
    })

    return df