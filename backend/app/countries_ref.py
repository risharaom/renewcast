"""
Single source of truth for country metadata: code, display name, region,
income group, and rough present-day baseline stats used to generate the
bundled starter dataset. Expand this table any time to add more countries.

Note: these baseline numbers are illustrative (this whole file backs the
placeholder dataset, not the real Kaggle data — see backend/README.md for
swapping in the real thing). If you load the real Kaggle CSV instead, the
backend no longer depends on this table for *which* countries exist — see
`build_code_maps()` in insights.py, which reads whatever countries are
actually in the dataset and only falls back to this table for region/
income/code lookups.
"""

# code, name, region, income group, population(M), gdp(T$),
# renewable share %, fossil share %, carbon intensity (gCO2/kWh) — all as
# of the most recent year (2025) in the bundled starter dataset.
COUNTRY_TABLE = [
    ("US", "United States", "North America", "High income", 335, 27.4, 22, 60, 368),
    ("DE", "Germany", "Europe", "High income", 84, 4.5, 46, 42, 311),
    ("CN", "China", "Asia", "Upper middle income", 1412, 17.7, 31, 62, 543),
    ("IN", "India", "Asia", "Lower middle income", 1428, 3.7, 23, 73, 632),
    ("BR", "Brazil", "South America", "Upper middle income", 216, 2.1, 82, 16, 96),
    ("NO", "Norway", "Europe", "High income", 5.5, 0.5, 98, 2, 26),
    ("FR", "France", "Europe", "High income", 68, 3.0, 27, 8, 55),
    ("GB", "United Kingdom", "Europe", "High income", 67, 3.3, 43, 40, 238),
    ("JP", "Japan", "Asia", "High income", 125, 4.2, 22, 71, 494),
    ("AU", "Australia", "Oceania", "High income", 26, 1.7, 32, 66, 549),
    ("CA", "Canada", "North America", "High income", 40, 2.1, 68, 19, 128),
    ("ES", "Spain", "Europe", "High income", 48, 1.6, 50, 30, 174),
    ("IT", "Italy", "Europe", "High income", 59, 2.2, 41, 55, 259),
    ("ZA", "South Africa", "Africa", "Upper middle income", 60, 0.4, 12, 86, 707),
    ("MX", "Mexico", "North America", "Upper middle income", 128, 1.8, 24, 71, 423),
    ("SE", "Sweden", "Europe", "High income", 10, 0.6, 71, 2, 42),
    ("AR", "Argentina", "South America", "Upper middle income", 46, 0.6, 34, 55, 380),
    ("CL", "Chile", "South America", "High income", 19.5, 0.35, 45, 40, 350),
    ("CO", "Colombia", "South America", "Upper middle income", 52, 0.36, 30, 50, 300),
    ("PE", "Peru", "South America", "Upper middle income", 34, 0.27, 55, 30, 250),
    ("NL", "Netherlands", "Europe", "High income", 18, 1.1, 40, 45, 320),
    ("PL", "Poland", "Europe", "Upper middle income", 38, 0.85, 20, 65, 620),
    ("DK", "Denmark", "Europe", "High income", 5.9, 0.4, 65, 20, 150),
    ("FI", "Finland", "Europe", "High income", 5.6, 0.3, 55, 25, 130),
    ("BE", "Belgium", "Europe", "High income", 11.7, 0.6, 25, 40, 180),
    ("AT", "Austria", "Europe", "High income", 9, 0.5, 78, 10, 100),
    ("CH", "Switzerland", "Europe", "High income", 8.8, 0.9, 68, 5, 30),
    ("PT", "Portugal", "Europe", "High income", 10.3, 0.28, 62, 20, 150),
    ("GR", "Greece", "Europe", "High income", 10.4, 0.24, 40, 40, 350),
    ("IE", "Ireland", "Europe", "High income", 5.2, 0.55, 40, 35, 300),
    ("CZ", "Czech Republic", "Europe", "High income", 10.9, 0.35, 18, 55, 400),
    ("RO", "Romania", "Europe", "Upper middle income", 19, 0.35, 40, 35, 280),
    ("UA", "Ukraine", "Europe", "Lower middle income", 36, 0.18, 12, 55, 450),
    ("KR", "South Korea", "Asia", "High income", 52, 1.8, 9, 60, 415),
    ("ID", "Indonesia", "Asia", "Lower middle income", 278, 1.4, 15, 80, 700),
    ("PK", "Pakistan", "Asia", "Lower middle income", 241, 0.34, 40, 55, 350),
    ("BD", "Bangladesh", "Asia", "Lower middle income", 173, 0.45, 3, 88, 500),
    ("VN", "Vietnam", "Asia", "Lower middle income", 99, 0.43, 40, 55, 460),
    ("TH", "Thailand", "Asia", "Upper middle income", 72, 0.51, 20, 65, 450),
    ("PH", "Philippines", "Asia", "Lower middle income", 117, 0.44, 25, 65, 480),
    ("MY", "Malaysia", "Asia", "Upper middle income", 34, 0.44, 20, 60, 500),
    ("SG", "Singapore", "Asia", "High income", 5.9, 0.5, 5, 90, 400),
    ("SA", "Saudi Arabia", "Middle East", "High income", 36, 1.1, 1, 99, 620),
    ("AE", "United Arab Emirates", "Middle East", "High income", 9.4, 0.5, 5, 90, 500),
    ("TR", "Turkey", "Middle East", "Upper middle income", 85, 1.1, 45, 40, 380),
    ("IR", "Iran", "Middle East", "Upper middle income", 89, 0.4, 5, 90, 550),
    ("IL", "Israel", "Middle East", "High income", 9.4, 0.53, 10, 75, 450),
    ("QA", "Qatar", "Middle East", "High income", 2.7, 0.24, 1, 99, 500),
    ("NG", "Nigeria", "Africa", "Lower middle income", 223, 0.48, 25, 60, 450),
    ("EG", "Egypt", "Africa", "Lower middle income", 112, 0.4, 12, 80, 500),
    ("KE", "Kenya", "Africa", "Lower middle income", 55, 0.11, 75, 15, 150),
    ("MA", "Morocco", "Africa", "Lower middle income", 37, 0.14, 35, 55, 550),
    ("ET", "Ethiopia", "Africa", "Low income", 126, 0.16, 90, 5, 50),
    ("GH", "Ghana", "Africa", "Lower middle income", 33, 0.075, 45, 40, 400),
    ("DZ", "Algeria", "Africa", "Upper middle income", 45, 0.2, 5, 90, 550),
    ("NZ", "New Zealand", "Oceania", "High income", 5.2, 0.25, 82, 10, 100),
]

CODE_TO_NAME = {row[0]: row[1] for row in COUNTRY_TABLE}
NAME_TO_CODE = {row[1]: row[0] for row in COUNTRY_TABLE}
REGION_INCOME = {row[1]: (row[2], row[3]) for row in COUNTRY_TABLE}