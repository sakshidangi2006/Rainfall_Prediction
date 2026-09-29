import joblib
import numpy as np
import pandas as pd
from pathlib import Path


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Model path
MODEL_PATH = (
    BASE_DIR
    / "models"
    / "linear_regression_rainfall.joblib"
)

# Load model once
model = joblib.load(MODEL_PATH)


def predict_rainfall(
    annual_lag1,
    annual_lag2,
    annual_lag3,
    annual_lag4,
    annual_lag5
):
    """
    Predict next year's annual rainfall using
    the previous five years of annual rainfall.
    """

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

    input_data = pd.DataFrame([{
        'annual_lag1': annual_lag1,
        'annual_lag2': annual_lag2,
        'annual_lag3': annual_lag3,
        'annual_lag4': annual_lag4,
        'annual_lag5': annual_lag5,
        'rolling_mean_3': rolling_mean_3,
        'rolling_mean_5': rolling_mean_5
    }])

    prediction = model.predict(input_data)[0]

    return prediction