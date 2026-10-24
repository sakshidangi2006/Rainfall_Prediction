
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from source.predict import predict_rainfall, model


# --------------------------------------------------
# 1. CREATE FASTAPI APPLICATION
# --------------------------------------------------

app = FastAPI(
    title="Regional Rainfall Prediction API",
    description=(
        "API for predicting next year's annual rainfall "
        "by meteorological subdivision."
    ),
    version="2.0.0"
)


# --------------------------------------------------
# 2. CONFIGURE CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# 3. GET VALID SUBDIVISIONS FROM THE TRAINED MODEL
# --------------------------------------------------

location_encoder = (
    model.named_steps["preprocessor"]
    .named_transformers_["location"]
)

VALID_SUBDIVISIONS = list(
    location_encoder.categories_[0]
)

# Map case-insensitive names to their exact training names
SUBDIVISION_LOOKUP = {
    name.strip().casefold(): name
    for name in VALID_SUBDIVISIONS
}


# --------------------------------------------------
# 4. DEFINE REQUEST SCHEMA
# --------------------------------------------------

class RainfallInput(BaseModel):
    subdivision: str = Field(min_length=1)

    annual_lag1: float = Field(ge=0, allow_inf_nan=False)
    annual_lag2: float = Field(ge=0, allow_inf_nan=False)
    annual_lag3: float = Field(ge=0, allow_inf_nan=False)
    annual_lag4: float = Field(ge=0, allow_inf_nan=False)
    annual_lag5: float = Field(ge=0, allow_inf_nan=False)


# --------------------------------------------------
# 5. HOME ENDPOINT
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Regional Rainfall Prediction API is running",
        "version": "2.0.0"
    }


# --------------------------------------------------
# 6. GET AVAILABLE SUBDIVISIONS
# --------------------------------------------------

@app.get("/subdivisions")
def get_subdivisions():
    return {
        "subdivisions": sorted(VALID_SUBDIVISIONS)
    }


# --------------------------------------------------
# 7. PREDICT RAINFALL
# --------------------------------------------------

@app.post("/predict")
def predict(data: RainfallInput):

    # Normalize the user's subdivision name
    submitted_name = data.subdivision.strip()
    canonical_name = SUBDIVISION_LOOKUP.get(
        submitted_name.casefold()
    )

    if canonical_name is None:
        raise HTTPException(
            status_code=422,
            detail=(
                "Unsupported subdivision. "
                "Check GET /subdivisions for valid names."
            )
        )

    try:
        prediction = predict_rainfall(
            canonical_name,
            data.annual_lag1,
            data.annual_lag2,
            data.annual_lag3,
            data.annual_lag4,
            data.annual_lag5
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc)
        ) from exc

    return {
        "subdivision": canonical_name,
        "predicted_next_year_annual_rainfall_mm": prediction
    }
