"""
Turns the trained model + clustering output into the exact JSON shapes the
existing React frontend already expects (see src/lib/energy-data.ts):

    Country  { code, name, region, incomeGroup, population, gdp,
               renewableShare, fossilShare, carbonIntensity, cluster }
    Cluster  { id, name, description, avgRenewable, avgFossil,
               avgDemand, avgCarbon }
    Forecast { country, targetYear, series[], stats }
"""

from __future__ import annotations

import pandas as pd

from .data import region_income_for, FEATURES
from .model import get_trained_state

# The 16 countries surfaced in the UI (same set as the original mock data),
# mapped to how they appear in the Kaggle `country` column.
CODE_TO_NAME = {
    "US": "United States",
    "DE": "Germany",
    "CN": "China",
    "IN": "India",
    "BR": "Brazil",
    "NO": "Norway",
    "FR": "France",
    "GB": "United Kingdom",
    "JP": "Japan",
    "AU": "Australia",
    "CA": "Canada",
    "ES": "Spain",
    "IT": "Italy",
    "ZA": "South Africa",
    "MX": "Mexico",
    "SE": "Sweden",
}
NAME_TO_CODE = {v: k for k, v in CODE_TO_NAME.items()}


def list_countries() -> list[dict]:
    state = get_trained_state()
    df = state.df

    out = []
    for code, name in CODE_TO_NAME.items():
        rows = df[df["country"] == name]
        if rows.empty:
            continue
        latest = rows.sort_values("year").iloc[-1]
        region, income = region_income_for(name)
        cluster = latest.get("Cluster")
        out.append(
            {
                "code": code,
                "name": name,
                "region": region,
                "incomeGroup": income,
                "population": round(float(latest["population"]) / 1_000_000, 1),
                "gdp": round(float(latest["gdp_usd"]) / 1_000_000_000_000, 1),
                "renewableShare": round(float(latest["renewables_share_pct"]), 1),
                "fossilShare": round(float(latest["fossil_share_pct"]), 1),
                "carbonIntensity": round(float(latest["carbon_intensity_gco2_kwh"]), 1),
                "cluster": int(cluster) if cluster is not None and not pd.isna(cluster) else 0,
            }
        )
    return out


def list_clusters() -> list[dict]:
    state = get_trained_state()
    summary = state.cluster_summary
    df = state.df

    # Order clusters by renewable share so "Cluster 3" reads as the
    # cleanest group, matching the feel of the original mock data.
    ordered_ids = summary["renewables_share_pct"].sort_values().index.tolist()

    descriptions = [
        "Lower renewable share, higher fossil reliance and carbon intensity relative to the other discovered groups.",
        "Moderate renewable adoption with a still-significant fossil fuel base in the generation mix.",
        "Above-average renewable share with a generation mix actively shifting away from fossil fuels.",
        "Highest renewable share and lowest carbon intensity of the discovered groups — clean energy leaders.",
    ]

    clusters = []
    for new_id, old_id in enumerate(ordered_ids):
        row = summary.loc[old_id]
        members = df[df["Cluster"] == old_id]["country"].unique().tolist()
        member_codes = [NAME_TO_CODE[m] for m in members if m in NAME_TO_CODE]
        clusters.append(
            {
                "id": new_id,
                "name": f"Cluster {new_id}",
                "description": descriptions[min(new_id, len(descriptions) - 1)],
                "avgRenewable": round(float(row["renewables_share_pct"]), 1),
                "avgFossil": round(float(row["fossil_share_pct"]), 1),
                "avgDemand": round(float(row["electricity_demand_twh"]), 1),
                "avgCarbon": round(float(row["carbon_intensity_gco2_kwh"]), 1),
                "memberCodes": member_codes,
            }
        )
    # remap old cluster id -> new (renewable-share-ordered) id for lookups elsewhere
    remap = {old_id: new_id for new_id, old_id in enumerate(ordered_ids)}
    return clusters, remap


def _country_rows(name: str) -> pd.DataFrame:
    state = get_trained_state()
    return state.df[state.df["country"] == name].sort_values("year")


def forecast_country(code: str, target_year: int) -> dict:
    state = get_trained_state()
    name = CODE_TO_NAME.get(code.upper())
    if name is None:
        raise ValueError(f"Unknown country code: {code}")

    rows = _country_rows(name)
    if rows.empty:
        raise ValueError(f"No data for country: {name}")

    last_year_in_data = int(rows["year"].max())
    history = rows[rows["year"] >= max(2015, int(rows["year"].min()))]

    series = []
    for _, r in history.iterrows():
        series.append(
            {
                "year": int(r["year"]),
                "historicalGeneration": round(float(r["renewables_electricity_twh"]), 1),
                "predictedGeneration": None,
                "historicalDemand": round(float(r["electricity_demand_twh"]), 1),
                "predictedDemand": None,
                "coverage": round(
                    float(r["renewables_electricity_twh"]) / float(r["electricity_demand_twh"]) * 100, 1
                ),
            }
        )

    # Overlap point so the historical/predicted lines connect on the chart,
    # same trick the original mock data used.
    if series:
        series[-1]["predictedGeneration"] = series[-1]["historicalGeneration"]
        series[-1]["predictedDemand"] = series[-1]["historicalDemand"]

    # Recursive multi-step forecast for any year beyond the dataset.
    last_row = rows.iloc[-1].copy()
    renew_lags = [
        float(rows.iloc[-1]["renewables_electricity_twh"]),
        float(rows.iloc[-2]["renewables_electricity_twh"]) if len(rows) > 1 else float(rows.iloc[-1]["renewables_electricity_twh"]),
        float(rows.iloc[-3]["renewables_electricity_twh"]) if len(rows) > 2 else float(rows.iloc[-1]["renewables_electricity_twh"]),
    ]
    solar_lag1 = float(last_row["solar_electricity_twh"])
    wind_lag1 = float(last_row["wind_electricity_twh"])
    demand_lag1 = float(last_row["electricity_demand_twh"])

    predicted_gen = predicted_dem = None
    for year in range(last_year_in_data + 1, target_year + 1):
        feature_row = {
            "population": float(last_row["population"]),
            "gdp_usd": float(last_row["gdp_usd"]),
            "total_electricity_generation_twh": float(last_row["total_electricity_generation_twh"]),
            "carbon_intensity_gco2_kwh": float(last_row["carbon_intensity_gco2_kwh"]),
            "renewables_share_pct": float(last_row["renewables_share_pct"]),
            "renewables_lag1": renew_lags[0],
            "solar_lag1": solar_lag1,
            "wind_lag1": wind_lag1,
            "demand_lag1": demand_lag1,
            "demand_gap": float(last_row["demand_gap"]),
            "fossil_share_pct": float(last_row["fossil_share_pct"]),
            "solar_share_pct": float(last_row["solar_share_pct"]),
            "wind_share_pct": float(last_row["wind_share_pct"]),
            "low_carbon_share_pct": float(last_row["low_carbon_share_pct"]),
            "co2_saved_solar_wind_mt": float(last_row["co2_saved_solar_wind_mt"]),
        }
        X = pd.DataFrame([feature_row])[FEATURES]

        predicted_gen = float(state.renew_model.predict(X)[0])
        predicted_dem = float(state.demand_model.predict(X)[0])

        series.append(
            {
                "year": year,
                "historicalGeneration": None,
                "predictedGeneration": round(predicted_gen, 1),
                "historicalDemand": None,
                "predictedDemand": round(predicted_dem, 1),
                "coverage": round(predicted_gen / predicted_dem * 100, 1) if predicted_dem else 0,
            }
        )

        # roll the lag features forward using our own predictions
        renew_lags = [predicted_gen, renew_lags[0], renew_lags[1]]
        demand_lag1 = predicted_dem

    if predicted_gen is None:
        # target year already inside the historical range
        last = series[-1]
        predicted_gen = last["historicalGeneration"]
        predicted_dem = last["historicalDemand"]

    coverage = (predicted_gen / predicted_dem * 100) if predicted_dem else 0
    gap = predicted_dem - predicted_gen

    _, cluster_remap = list_clusters()
    raw_cluster = last_row.get("Cluster")
    cluster_id = cluster_remap.get(int(raw_cluster), 0) if raw_cluster is not None and not pd.isna(raw_cluster) else 0
    region, income = region_income_for(name)

    return {
        "country": {
            "code": code.upper(),
            "name": name,
            "region": region,
            "incomeGroup": income,
            "population": round(float(last_row["population"]) / 1_000_000, 1),
            "gdp": round(float(last_row["gdp_usd"]) / 1_000_000_000_000, 1),
            "renewableShare": round(float(last_row["renewables_share_pct"]), 1),
            "fossilShare": round(float(last_row["fossil_share_pct"]), 1),
            "carbonIntensity": round(float(last_row["carbon_intensity_gco2_kwh"]), 1),
            "cluster": cluster_id,
        },
        "targetYear": target_year,
        "series": series,
        "stats": {
            "predictedGeneration": round(predicted_gen, 1),
            "predictedDemand": round(predicted_dem, 1),
            "coverage": round(coverage, 1),
            "gap": round(gap, 1),
        },
    }
