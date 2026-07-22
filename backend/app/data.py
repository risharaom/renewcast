"""
Data loading, cleaning and feature engineering.

This module mirrors the exact logic from the original Colab notebook
("Global Renewable Energy Forecasting") cells:
  [3]  Loading the Dataset
  [8]  Data Cleaning
  [9]  Feature Engineering

The only thing added on top of the notebook is a small on-disk cache so the
Kaggle dataset isn't re-downloaded on every backend restart, plus an optional
local CSV fallback (backend/data/energy.csv) for hosts that can't reach
Kaggle (kagglehub needs outbound internet + a Kaggle account/API token).
"""

from __future__ import annotations

import os
import functools

import pandas as pd

from .countries_ref import REGION_INCOME

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
LOCAL_CSV_PATH = os.path.join(DATA_DIR, "energy.csv")

KAGGLE_DATASET = "alitaqishah/world-energy-transition-20002025"
KAGGLE_CSV_NAME = "global_renewable_energy_transition_2000_2025.csv"

# `REGION_INCOME` (imported above) maps country name -> (region, income
# group). Falls back to "Unclassified" for any country not listed in the
# shared reference table (e.g. if you swap in the real Kaggle CSV, which
# may include countries beyond the ones catalogued in countries_ref.py).


def _load_raw() -> pd.DataFrame:
    """[3] Loading the Dataset — identical to the notebook, with a local
    CSV cache/fallback layered on top so the backend can run without a
    live Kaggle connection once the file has been fetched once."""

    if os.path.exists(LOCAL_CSV_PATH):
        return pd.read_csv(LOCAL_CSV_PATH)

    import kagglehub  # imported lazily: only needed on first run

    path = kagglehub.dataset_download(KAGGLE_DATASET)
    df = pd.read_csv(os.path.join(path, KAGGLE_CSV_NAME))

    os.makedirs(DATA_DIR, exist_ok=True)
    df.to_csv(LOCAL_CSV_PATH, index=False)

    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """[8] Data Cleaning — exact same steps as the notebook."""
    df = df.sort_values(["country", "year"])
    df = df.ffill()  # notebook used df.fillna(method="ffill"), now deprecated
    df = df.drop_duplicates()
    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """[9] Feature Engineering — exact same lag/gap features as the notebook."""
    df = df.copy()

    df["renewables_lag1"] = df.groupby("country")["renewables_electricity_twh"].shift(1)
    df["solar_lag1"] = df.groupby("country")["solar_electricity_twh"].shift(1)
    df["wind_lag1"] = df.groupby("country")["wind_electricity_twh"].shift(1)
    df["demand_lag1"] = df.groupby("country")["electricity_demand_twh"].shift(1)
    df["renewables_lag2"] = df.groupby("country")["renewables_electricity_twh"].shift(2)
    df["renewables_lag3"] = df.groupby("country")["renewables_electricity_twh"].shift(3)
    df["demand_lag2"] = df.groupby("country")["electricity_demand_twh"].shift(2)

    df["demand_gap"] = df["electricity_demand_twh"] - df["total_electricity_generation_twh"]

    df = df.dropna()
    return df


FEATURES = [
    "population",
    "gdp_usd",
    "total_electricity_generation_twh",
    "carbon_intensity_gco2_kwh",
    "renewables_share_pct",
    "renewables_lag1",
    "solar_lag1",
    "wind_lag1",
    "demand_lag1",
    "demand_gap",
    "fossil_share_pct",
    "solar_share_pct",
    "wind_share_pct",
    "low_carbon_share_pct",
    "co2_saved_solar_wind_mt",
]


@functools.lru_cache(maxsize=1)
def get_dataset() -> pd.DataFrame:
    """Loads + cleans + feature-engineers the dataset once per process."""
    raw = _load_raw()
    cleaned = clean_data(raw)
    engineered = engineer_features(cleaned)
    return engineered


def region_income_for(country_name: str) -> tuple[str, str]:
    return REGION_INCOME.get(country_name, ("Unclassified", "Unclassified"))