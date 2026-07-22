// Talks to the FastAPI backend in /backend, which runs your actual
// notebook pipeline (pandas cleaning, RandomForestRegressor, KMeans).
// If the backend isn't running, every function here falls back to the
// local JS approximations (js/forecast.js, js/clusters.js) so the site
// still works — you'll just see a small "preview data" note instead of
// "live model" in that case.

// Locally (opening index.html directly, or serving it from your own
// machine) this points at localhost automatically. Once you deploy the
// backend somewhere public (see backend/README.md), put that URL here —
// it'll be used automatically for anyone visiting the published site.
const DEPLOYED_API_BASE = "https://renewcast-backend.onrender.com"; // e.g. "https://renewcast-backend.onrender.com"

const isLocal = ["localhost", "127.0.0.1", ""].includes(location.hostname);
const API_BASE = isLocal ? "http://localhost:8000" : DEPLOYED_API_BASE;

async function tryFetch(path, options) {
  if (!API_BASE) return null; // no deployed backend URL configured yet
  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 6000);
    const res = await fetch(`${API_BASE}${path}`, {
      ...options,
      signal: controller.signal,
      headers: { "Content-Type": "application/json" },
    });
    clearTimeout(timeout);
    if (!res.ok) return null;
    return await res.json();
  } catch {
    return null;
  }
}

async function isBackendLive() {
  const data = await tryFetch("/health");
  return data && data.status === "ok";
}

async function apiFetchCountries() {
  return tryFetch("/country");
}

async function apiFetchClusters() {
  return tryFetch("/cluster");
}

async function apiFetchForecast(countryCode, targetYear) {
  return tryFetch("/forecast", {
    method: "POST",
    body: JSON.stringify({ countryCode, targetYear }),
  });
}

// Small "Live model" / "Preview data" badge shown on each page so it's
// obvious which data source you're looking at.
function renderLiveBadge(elementId, live) {
  const node = document.getElementById(elementId);
  if (!node) return;
  node.innerHTML = live
    ? `<span class="badge" style="color:#16a34a;border-color:#16a34a55;">● Live Python model</span>`
    : `<span class="badge">○ Preview data — start the backend for live predictions</span>`;
}
