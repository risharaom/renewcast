# RenewCast

A minimalistic renewable energy dashboard, backed by a real Python
pipeline (pandas + scikit-learn) that runs your notebook's exact model:
`RandomForestRegressor(n_estimators=100, random_state=42)` for both the
renewables and demand predictions, and `KMeans(n_clusters=4)` for clustering.

**It ships with a ready-to-use dataset**, so it works the moment you run
one script — no Kaggle account needed to get started.

## Quick start (3 steps)

**1. Start the backend** (one command, one time per session):
- Mac/Linux: double-click `run_backend.sh`, or run it in a terminal:
  ```bash
  ./run_backend.sh
  ```
- Windows: double-click `run_backend.bat`

First run takes a little longer (installs Python packages). After that,
leave this window open — it's your live model server at
`http://localhost:8000`.

**2. Open the site** — double-click `index.html`. It opens in your browser
and talks to the backend automatically.

**3. Look for the badge** at the top of each page:
- 🟢 **"Live Python model"** — the backend is running, you're seeing real
  `RandomForestRegressor` / `KMeans` output.
- ⚪ **"Preview data"** — the backend isn't running (or hasn't finished
  starting up yet); the page is using a lightweight JS fallback instead so
  it never looks broken. Give the backend a few seconds and refresh.

That's it — steps 1 and 2 are all you need each time you want to use it.

## What's in the box

```
index.html, forecast.html, clustering.html, country.html, about.html
css/, js/                    the frontend (no build step, just files)
js/api.js                    calls the backend; falls back to local JS if it's not running
run_backend.sh / .bat        one-command backend startup
backend/                     the FastAPI service running your notebook's pipeline
backend/data/energy.csv      bundled starter dataset (see below)
generate_dataset.py          the script that made that starter CSV
```

## Using your real Kaggle dataset instead of the bundled one

The bundled `backend/data/energy.csv` is a stand-in shaped exactly like the
real dataset (same columns, same 2000-2025 range, same 16 countries) so
things work out of the box. To use the actual Kaggle data:

1. Get a free Kaggle API token: kaggle.com -> profile picture -> Settings
   -> API -> Create New Token (downloads a `kaggle.json` with your
   username + key).
2. Delete `backend/data/energy.csv`.
3. Set the credentials as environment variables before running the start
   script:
   ```bash
   export KAGGLE_USERNAME=your_username
   export KAGGLE_KEY=your_key
   ./run_backend.sh
   ```
   (Windows: `set KAGGLE_USERNAME=...` / `set KAGGLE_KEY=...` before
   running `run_backend.bat`.)
4. The backend will download the real dataset on first request and cache
   it as `backend/data/energy.csv` from then on.

## Publishing it as a real website

**1. Deploy the backend to Render** (free, gives you an `https://` URL):
push this project to GitHub, then on [render.com](https://render.com) click
**New +** → **Blueprint**, connect the repo — it'll pick up `render.yaml`
automatically. Full details, including how to handle the dataset, in
`backend/README.md`.

**2. Point the frontend at it** — open `js/api.js` and set:
```js
const DEPLOYED_API_BASE = "https://your-backend-name.onrender.com";
```
(Locally it keeps using `localhost:8000` automatically — you don't need to
touch anything for local use.)

**3. Publish the frontend as a static site** — any of these work, are
free, and need zero build step since it's already plain HTML/CSS/JS:
- **GitHub Pages**: repo → Settings → Pages → deploy from your main branch
- **Netlify** or **Vercel**: drag-and-drop the folder in their dashboard, or connect the GitHub repo
- **Cloudflare Pages**: connect the repo, no build command needed

**4. (Recommended) Tighten CORS** — in Render's dashboard, set the
backend's `ALLOWED_ORIGINS` environment variable to your published
frontend's URL instead of `*`.

One thing to expect: Render's free tier spins the backend down after ~15
minutes idle, so the first visitor after a quiet period waits ~30-60s for
it to wake up — everyone after that gets instant responses until it goes
idle again. The site still looks fine either way since it falls back to
"Preview data" while waiting.


