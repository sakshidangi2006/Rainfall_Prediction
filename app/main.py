from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from source.predict import predict_rainfall

app = FastAPI(
title="Rainfall Prediction API",
description="API for predicting next year's annual rainfall",
version="1.0.0"
)

# Allow the frontend to communicate with FastAPI

app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)

class RainfallInput(BaseModel):
    annual_lag1: float
    annual_lag2: float
    annual_lag3: float
    annual_lag4: float
    annual_lag5: float
    
@app.get("/")
def home():
    return {
        "message": "Rainfall Prediction API is running"
    }

@app.post("/predict")
def predict(data: RainfallInput):

    prediction = predict_rainfall(
        data.annual_lag1,
        data.annual_lag2,
        data.annual_lag3,
        data.annual_lag4,
        data.annual_lag5
)

    return {
        "predicted_annual_rainfall_mm": prediction
    }

