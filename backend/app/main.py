from __future__ import annotations

import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from . import insights
from .model import get_trained_state

app = FastAPI(title="RenewCast API", version="1.0.0")

# Allow the Vite dev server + any deployed frontend origin(s) to call this API.
# Set ALLOWED_ORIGINS as a comma-separated env var in production
# (e.g. "https://your-app.vercel.app,https://your-custom-domain.com").
_origins = os.environ.get("ALLOWED_ORIGINS", "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if _origins == "*" else _origins.split(","),
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ForecastRequest(BaseModel):
    countryCode: str
    targetYear: int


class PredictRequest(BaseModel):
    countryCode: str
    year: int | None = None


@app.get("/")
def root():
    return {"status": "ok", "service": "RenewCast API"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/country")
def get_countries():
    """List of countries with their latest known profile + AI cluster."""
    return insights.list_countries()


@app.get("/cluster")
def get_clusters():
    """K-Means cluster summaries (id, description, averages, member countries)."""
    clusters, _ = insights.list_clusters()
    return clusters


@app.post("/forecast")
def post_forecast(req: ForecastRequest):
    """Full historical + predicted time series for a country up to targetYear."""
    try:
        return insights.forecast_country(req.countryCode, req.targetYear)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/predict")
def post_predict(req: PredictRequest):
    """Single-point prediction for the next available year (kept for parity
    with the endpoint name referenced in the original frontend mock)."""
    state = get_trained_state()
    year = req.year or 2030
    try:
        result = insights.forecast_country(req.countryCode, year)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {
        "countryCode": req.countryCode.upper(),
        "year": year,
        "predictedRenewables": result["stats"]["predictedGeneration"],
        "predictedDemand": result["stats"]["predictedDemand"],
        "coverage": result["stats"]["coverage"],
        "modelMetrics": state.metrics,
    }


@app.get("/metrics")
def get_metrics():
    """Exposes the same MAE / RMSE / R² printed in the notebook's Evaluate
    Model cell, for anyone building an admin/about page around it."""
    state = get_trained_state()
    return state.metrics
