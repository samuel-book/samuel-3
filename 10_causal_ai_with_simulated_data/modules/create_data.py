# Function to create synthetic stroke data with causal treatment effect size

import numpy as np
import pandas as pd

def create_stroke_data(n=1000, seed=42):
    """
        Generates synthetic stroke patient data with a predefined causal treatment effect.

        This function simulates patient demographics, clinical characteristics, treatment 
        assignment (thrombolysis), and mortality outcomes. It explicitly constructs the 
        causal relationships and temporal treatment effects, making it ideal for testing 
        causal inference algorithms.

        Args:
            n (int, optional): The number of synthetic patients to generate. Defaults to 1000.
            seed (int, optional): The random seed for reproducibility. Defaults to 42.

        Returns:
            pd.DataFrame: A DataFrame containing the synthetic patient data, including 
            demographics, treatment assignments, true probabilities, causal effects, 
            and final observed outcomes.

        Calculations Performed:
            1. Patient Characteristics
                * Age: Uniformly distributed between 60 and 89.
                * Ethnicity: Randomly assigned as White (70%), Asian (20%), or Black (10%).
                * Sex (Male): Binomial distribution (50% probability).
                * Warfarin Use: Binomial distribution (20% probability).
                * NIHSS (Stroke Severity): Triangular distribution (min=0, mode=10, max=30).
                * Shoe Size (Noise): Triangular distribution (min=5, mode=9, max=13).

            2. Base Mortality Probability (Without Treatment)
                * Starts at a base probability of 0.05.
                * Adds 0.005 for every year of age over 60.
                * Adds 0.05 for male patients.
                * Adds 0.01 for each NIHSS point.
                * Adds 0.10 for Black patients and 0.05 for Asian patients.
                * Adds 0.10 if the patient was treated in the year 2020 (e.g. COVID-19 effect).
                * The sum is clipped to [0.001, 0.999] to prevent mathematical errors.
                * The probability is then converted to odds and log-odds.

            3. Thrombolysis Treatment Assignment
                * Base probability of receiving treatment is 0.50, modified by an NIHSS weight:
                    - NIHSS < 5: Weight is 0.0.
                    - NIHSS 5 to 9: Ramps linearly from 0.0 to 1.0.
                    - NIHSS 10 to 20: Weight remains 1.0.
                    - NIHSS 21 to 30: Decreases linearly from 1.0 to 0.0.
                * Probability is forced to 0.0 if the patient is on Warfarin.
                * Final treatment status is drawn from a binomial distribution.

            4. Treatment Effect (Log-Odds Ratio)
                * Time to thrombolysis is drawn uniformly between 30 and 360 minutes 
                (set to 99999 if the patient was not treated).
                * A base log-odds ratio of 2.0 is established for the treatment effect.
                * Time decay multiplier: The effect linearly decays to zero at 360 minutes 
                using the formula (360 - time) / 360.
                * Ethnicity modifier: The resulting log-odds ratio is halved for Asian patients.

            5. Final Outcome (Mortality)
                * Treated Log-Odds: Calculated by subtracting the log-odds ratio from the 
                base log-odds without treatment.
                * Treated Probability: The treated log-odds are converted back to a probability.
                * Final Probability: The algorithm assigns the treated probability if the 
                patient received thrombolysis, otherwise it assigns the base untreated probability.
                * Mortality ('died'): A final binomial draw determines if the patient survives 
                or dies based on their final probability.
        """
    
    np.random.seed(seed)

    # ---------------------------------- Patient characteristics -----------------------------------

    # --- Demographics
    age = np.random.randint(60, 90, size=n)

    ethnicity = np.random.choice(['white', 'asian', 'black'], size=n, p=[0.70, 0.20, 0.10])

    male = np.random.binomial(1, 0.50, size=n)

    # --- Warfarin (20% prevalence) ---
    warfarin = np.random.binomial(1, 0.20, size=n)

    # --- Noise variables (no causal role) ---
    shoe_size = np.random.triangular(5, 9, 13, size=n).astype(int)

    # set year as uniformly distributed between 2018 and 2024
    year = np.random.randint(2018, 2025, size=n)

    # --- NIHSS stroke severity (triangular distribution, 0–30, mode 10) ---
    nihss = np.random.triangular(0, 10, 30, size=n).astype(int)

    # --- Mortality probability without treatment ---
    mortality_prob_no_treatment = np.full(n, 0.05)
    mortality_prob_no_treatment += (age - 60) * 0.005
    mortality_prob_no_treatment[male == 1] += 0.05
    mortality_prob_no_treatment += nihss * 0.01
    mortality_prob_no_treatment[ethnicity == 'black'] += 0.1
    mortality_prob_no_treatment[ethnicity == 'asian'] += 0.05

    # Add 0.1 if year is 2020
    mortality_prob_no_treatment[year == 2020] += 0.1

    # Clip the mortality probabilities to ensure they are between 0 and 1
    mortality_prob_no_treatment = np.clip(mortality_prob_no_treatment, 0.001, 0.999)

    # Calculate odds and log-odds for mortality probability
    odds_no_treatment = (
        mortality_prob_no_treatment / (1 - mortality_prob_no_treatment))
    log_odds_no_treatment = np.log(odds_no_treatment)

    #  ------------------------- Probability of receiving thrombolysis -----------------------------

    prob_thrombolysis = np.full(n, 0.50)

    # NIHSS effect on thrombolysis probability:
    #   - eligibility of thrombolysis (zero below 5, ramps 5-10, stable 10-20, ramps down 20-30)

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

    #  --------------------------------- Treatment assignment --------------------------------------

    thrombolysis = np.random.binomial(1, prob_thrombolysis, size=n)

    #  ----------------------------------- Treatment effect ----------------------------------------

    base_log_odds_ratio = 2

    # Set time to thrombolysis as uniformly distributed between 30- 360 minutes
    thrombolysis_time = np.random.uniform(30, 360, size=n)
    # If thrombolysis is not given, set time to thrombolysis to 99999
    thrombolysis_time[thrombolysis == 0] = 99999

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

    #  ------------------------------------ Mortality outcome --------------------------------------
    mortality_prob = np.where(
        thrombolysis == 1, mortality_prob_with_treatment, mortality_prob_no_treatment)

    died = np.random.binomial(1, mortality_prob, size=n)

    # -----------------------------------  Return DataFrame ----------------------------------------

    # --- DataFrame ---
    df = pd.DataFrame({
        "patient_id": np.arange(1, n + 1),
        "year": year,
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
        "mortality_prob_treated": np.round(mortality_prob_with_treatment, 4),
        "mortality_odds_treated": np.round(adjusted_odds, 4),
        "mortality_log_odds_treated": np.round(adjusted_log_odds, 4),
        "odds_ratio_treated": np.round(np.exp(log_odds_ratio), 4),
        "log_odds_ratio_treated": np.round(log_odds_ratio, 4),
        "probability_difference": np.round(prob_diff, 4),
        "mortality_probability": np.round(mortality_prob, 4),
        "died": died
    })

    return df