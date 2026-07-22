"""
Generates backend/data/energy.csv — a ready-to-use starter dataset so the
backend works immediately with zero setup (no Kaggle account needed).

This is a *placeholder* dataset: it's structured exactly like the real
"world-energy-transition-2000-2025" Kaggle dataset the notebook uses (same
columns, same 2000-2025 year range, same 16 countries), with historical
trends anchored to realistic present-day profiles for each country. It lets
you run the exact notebook pipeline (cleaning, feature engineering,
RandomForestRegressor, KMeans) end-to-end right away.

To use the REAL Kaggle dataset instead: delete backend/data/energy.csv,
set KAGGLE_USERNAME / KAGGLE_KEY env vars (see backend/README.md), and
restart the backend — it will download the real dataset in its place.
"""

import csv
import math
import os

COUNTRIES = [
    # code, name, region, income, population(M), gdp(T$), renewableShare%, fossilShare%, carbonIntensity
    ("US", "United States", 335, 27.4, 22, 60, 368),
    ("DE", "Germany", 84, 4.5, 46, 42, 311),
    ("CN", "China", 1412, 17.7, 31, 62, 543),
    ("IN", "India", 1428, 3.7, 23, 73, 632),
    ("BR", "Brazil", 216, 2.1, 82, 16, 96),
    ("NO", "Norway", 5.5, 0.5, 98, 2, 26),
    ("FR", "France", 68, 3.0, 27, 8, 55),
    ("GB", "United Kingdom", 67, 3.3, 43, 40, 238),
    ("JP", "Japan", 125, 4.2, 22, 71, 494),
    ("AU", "Australia", 26, 1.7, 32, 66, 549),
    ("CA", "Canada", 40, 2.1, 68, 19, 128),
    ("ES", "Spain", 48, 1.6, 50, 30, 174),
    ("IT", "Italy", 59, 2.2, 41, 55, 259),
    ("ZA", "South Africa", 60, 0.4, 12, 86, 707),
    ("MX", "Mexico", 128, 1.8, 24, 71, 423),
    ("SE", "Sweden", 10, 0.6, 71, 2, 42),
]

OUT_PATH = os.path.join(os.path.dirname(__file__), "backend", "data", "energy.csv")

rows = []
for code, name, pop_m, gdp_t, ren_share_2025, fossil_share_2025, carbon_2025 in COUNTRIES:
    pop = pop_m * 1_000_000
    gdp = gdp_t * 1_000_000_000_000
    base_demand_2025 = 50 + pop_m * 3.5 + gdp_t * 80

    for year in range(2000, 2026):
        t = year - 2015  # matches the growth model used across the project
        t25 = 2025 - 2015

        demand = base_demand_2025 * (1 + 0.022 * t) / (1 + 0.022 * t25)
        ren_share = max(1.0, ren_share_2025 - 0.35 * (2025 - year))
        fossil_share = min(97.0, fossil_share_2025 + 0.30 * (2025 - year))
        carbon = carbon_2025 + 4.0 * (2025 - year)

        renewables_gen = demand * (ren_share / 100)
        total_gen = demand * (1 + 0.02)  # generation slightly exceeds demand
        solar = renewables_gen * 0.30
        wind = renewables_gen * 0.30
        low_carbon_share = min(99.0, ren_share + 5)
        co2_saved = renewables_gen * 0.5
        pop_year = pop * (1 + 0.01 * (year - 2025))
        gdp_year = gdp * (1 + 0.03 * (year - 2025))

        rows.append(
            dict(
                country=name,
                year=year,
                population=round(pop_year),
                gdp_usd=round(gdp_year),
                total_electricity_generation_twh=round(total_gen, 2),
                electricity_demand_twh=round(demand, 2),
                renewables_electricity_twh=round(renewables_gen, 2),
                solar_electricity_twh=round(solar, 2),
                wind_electricity_twh=round(wind, 2),
                carbon_intensity_gco2_kwh=round(carbon, 1),
                renewables_share_pct=round(ren_share, 2),
                fossil_share_pct=round(fossil_share, 2),
                solar_share_pct=round(ren_share * 0.3, 2),
                wind_share_pct=round(ren_share * 0.3, 2),
                low_carbon_share_pct=round(low_carbon_share, 2),
                co2_saved_solar_wind_mt=round(co2_saved, 2),
            )
        )

os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
with open(OUT_PATH, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {len(rows)} rows to {OUT_PATH}")
