# RenewCast backend

A FastAPI service that reproduces your Colab notebook ("Global Renewable
Energy Forecasting") as a real API: same data cleaning, same lag-feature
engineering, same `RandomForestRegressor` models (n_estimators=100,
random_state=42), same `KMeans(n_clusters=4)` clustering. See
`app/data.py` and `app/model.py` — each function is commented with which
notebook cell it corresponds to.

On top of the notebook it adds:
- A recursive forecaster (`app/insights.py`) so you can ask for years past
  the dataset's last year (e.g. 2030) — it feeds each year's own prediction
  back in as next year's lag feature, the standard way to extend a
  lag-feature model beyond its training range.
- Four HTTP endpoints matching what the frontend already expects
  (see the frontend's `js/api.js`, which calls these and falls back to
  local JS if the backend isn't reachable).

## Endpoints

| Method | Path        | Purpose                                                        |
|--------|-------------|-----------------------------------------------------------------|
| GET    | `/country`  | List of countries with latest profile + AI cluster              |
| GET    | `/cluster`  | K-Means cluster summaries (averages + member countries)          |
| POST   | `/forecast` | `{countryCode, targetYear}` → full historical+predicted series  |
| POST   | `/predict`  | `{countryCode, year}` → single-point prediction                 |
| GET    | `/metrics`  | MAE / RMSE / R² for both models (same numbers the notebook prints)|
| GET    | `/health`   | Liveness check                                                   |

## Run it locally

The easiest way is the project-root `run_backend.sh` (Mac/Linux) or
`run_backend.bat` (Windows) script — it handles all of this for you.
Manual equivalent:

```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # optional but recommended
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

This project ships with `backend/data/energy.csv` already in place (a
stand-in dataset shaped exactly like the real Kaggle data), so it runs
immediately — no Kaggle account needed to get started. See the root
`README.md` for how to swap in the real Kaggle dataset later.

## Deploying it for free

The dataset download needs outbound internet access, so pick a host that
allows that (and isn't limited to an allowlist of domains — this rules out
PythonAnywhere's free tier, which only allows outbound requests to a small
allowlist that doesn't include Kaggle). The easiest free options as of 2026:

1. **Render (free web service)** — the most drop-in option: push this repo
   to GitHub, create a new "Web Service" on render.com, set the root
   directory to `backend`, build command `pip install -r requirements.txt`,
   start command `uvicorn app.main:app --host 0.0.0.0 --port $PORT`. Free
   tier spins the service down after ~15 minutes idle, so the first request
   after a while takes ~30–60s to wake up — fine for a portfolio/demo project.
2. **Fly.io** — also has a free allowance and doesn't spin all the way down
   the way Render's free tier does, at the cost of a slightly fiddlier setup
   (needs a `Dockerfile` + `fly.toml`; ask me and I can generate one).
3. **Hugging Face Spaces (Docker SDK)** — free, always-on for light traffic,
   good if you want a public demo and don't mind an `huggingface.co` URL.

Whichever you pick, once it's deployed, open `js/api.js` and change the
`API_BASE` constant near the top from `http://localhost:8000` to your
deployed URL (and set `ALLOWED_ORIGINS` on the backend to wherever you're
hosting the frontend instead of `*`).

### Can I skip a separate backend entirely?

Not cleanly with scikit-learn — a `RandomForestRegressor` and `KMeans`
need Python to run, and this project's frontend is plain HTML/CSS/JS with
no Python runtime. If you'd rather avoid hosting a second service, the
realistic options are:
- Pre-compute the forecasts/clusters offline and ship them as static JSON
  the frontend reads directly (loses "live" recomputation, but zero backend
  hosting needed).
- Keep using the built-in JS fallback (`js/forecast.js`, `js/clusters.js`)
  as the permanent source — that's exactly what the site does today
  whenever the backend isn't reachable.

Given you specifically wanted the notebook's real model driving the site,
a small free-tier backend (option 1 above) is the simplest path.
