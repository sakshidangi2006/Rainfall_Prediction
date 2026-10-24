
import joblib
import numpy as np
import pandas as pd
from pathlib import Path


# --------------------------------------------------
# 1. LOAD THE TRAINED MODEL
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "linear_regression_subdivision.joblib"
)

model = joblib.load(MODEL_PATH)


# --------------------------------------------------
# 2. NORMALIZE SUBDIVISION NAME
# --------------------------------------------------

def normalize_subdivision(subdivision):
    """
    Match user input to the exact subdivision name
    used during model training.

    Example:
        'Kerala' -> 'KERALA'
        'KERALA' -> 'KERALA'
        ' kerala ' -> 'KERALA'
    """

    if not isinstance(subdivision, str):
        raise ValueError("Subdivision must be a string.")

    location_encoder = (
        model.named_steps["preprocessor"]
        .named_transformers_["location"]
    )

    valid_names = location_encoder.categories_[0]

    lookup = {
        name.strip().casefold(): name
        for name in valid_names
    }

    key = subdivision.strip().casefold()

    if key not in lookup:
        raise ValueError(
            f"Unknown subdivision: {subdivision}. "
            "Please use a valid subdivision name."
        )

    return lookup[key]


# --------------------------------------------------
# 3. PREDICT NEXT YEAR'S ANNUAL RAINFALL
# --------------------------------------------------

def predict_rainfall(
    subdivision,
    annual_lag1,
    annual_lag2,
    annual_lag3,
    annual_lag4,
    annual_lag5
):
    """
    Predict next year's annual rainfall in millimetres.

    Parameters:
        subdivision: Meteorological subdivision name
        annual_lag1: Rainfall from the most recent year
        annual_lag2: Rainfall from two years ago
        annual_lag3: Rainfall from three years ago
        annual_lag4: Rainfall from four years ago
        annual_lag5: Rainfall from five years ago

    Returns:
        Predicted annual rainfall in millimetres.
    """

    # Normalize the subdivision before prediction
    subdivision = normalize_subdivision(subdivision)

    # Calculate rolling averages
    rolling_mean_3 = np.mean([
        annual_lag1,
        annual_lag2,
        annual_lag3
    ])

    rolling_mean_5 = np.mean([
        annual_lag1,
        annual_lag2,
        annual_lag3,
        annual_lag4,
        annual_lag5
    ])

    # Prepare input features in the expected format
    input_data = pd.DataFrame([{
        "SUBDIVISION": subdivision,
        "annual_lag1": annual_lag1,
        "annual_lag2": annual_lag2,
        "annual_lag3": annual_lag3,
        "annual_lag4": annual_lag4,
        "annual_lag5": annual_lag5,
        "rolling_mean_3": rolling_mean_3,
        "rolling_mean_5": rolling_mean_5
    }])

    # Generate prediction
    prediction = model.predict(input_data)[0]

    return float(prediction)
