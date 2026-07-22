"""
Model training (RandomForest) and clustering (KMeans).

Mirrors the notebook cells:
  [10] Train/Test Split
  [11] Train Random Forest
  [12] Evaluate Model
  [17]/[21] Clustering

Everything is trained once at process startup and cached in memory
(`get_trained_state`), exactly like running the notebook top-to-bottom once.
"""

from __future__ import annotations

import functools
from dataclasses import dataclass

import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

from .data import get_dataset, FEATURES

CLUSTER_FEATURES = [
    "renewables_share_pct",
    "fossil_share_pct",
    "carbon_intensity_gco2_kwh",
    "electricity_demand_twh",
    "renewables_electricity_twh",
    "solar_share_pct",
    "wind_share_pct",
]


@dataclass
class TrainedState:
    df: "pd.DataFrame"
    renew_model: RandomForestRegressor
    demand_model: RandomForestRegressor
    metrics: dict
    cluster_labels: "pd.Series"
    cluster_summary: "pd.DataFrame"
    kmeans: KMeans
    scaler: StandardScaler


@functools.lru_cache(maxsize=1)
def get_trained_state() -> TrainedState:
    df = get_dataset().copy()

    # [10] Train/Test Split — identical split rule (<=2020 train, >2020 test)
    train = df[df["year"] <= 2020]
    test = df[df["year"] > 2020]

    X_train = train[FEATURES]
    X_test = test[FEATURES]

    y_train_renew = train["renewables_electricity_twh"]
    y_test_renew = test["renewables_electricity_twh"]

    y_train_demand = train["electricity_demand_twh"]
    y_test_demand = test["electricity_demand_twh"]

    # [11] Train Random Forest — same hyperparameters as the notebook
    renew_model = RandomForestRegressor(n_estimators=100, random_state=42)
    renew_model.fit(X_train, y_train_renew)

    demand_model = RandomForestRegressor(n_estimators=100, random_state=42)
    demand_model.fit(X_train, y_train_demand)

    # [12] Evaluate Model
    renew_predictions = renew_model.predict(X_test)
    demand_predictions = demand_model.predict(X_test)

    metrics = {
        "renewables": {
            "mae": float(mean_absolute_error(y_test_renew, renew_predictions)),
            "rmse": float(np.sqrt(mean_squared_error(y_test_renew, renew_predictions))),
            "r2": float(r2_score(y_test_renew, renew_predictions)),
        },
        "demand": {
            "mae": float(mean_absolute_error(y_test_demand, demand_predictions)),
            "rmse": float(np.sqrt(mean_squared_error(y_test_demand, demand_predictions))),
            "r2": float(r2_score(y_test_demand, demand_predictions)),
        },
    }

    # [17]/[21] Clustering
    cluster_df = df[CLUSTER_FEATURES].dropna()
    scaler = StandardScaler()
    cluster_scaled = scaler.fit_transform(cluster_df)

    kmeans = KMeans(n_clusters=4, random_state=42)
    clusters = kmeans.fit_predict(cluster_scaled)

    df.loc[cluster_df.index, "Cluster"] = clusters

    cluster_summary = df.groupby("Cluster")[
        [
            "renewables_share_pct",
            "fossil_share_pct",
            "carbon_intensity_gco2_kwh",
            "electricity_demand_twh",
            "renewables_electricity_twh",
        ]
    ].mean()

    return TrainedState(
        df=df,
        renew_model=renew_model,
        demand_model=demand_model,
        metrics=metrics,
        cluster_labels=df["Cluster"],
        cluster_summary=cluster_summary,
        kmeans=kmeans,
        scaler=scaler,
    )
