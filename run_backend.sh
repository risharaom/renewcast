#!/usr/bin/env bash
# One-command backend startup: creates a virtual environment on first run,
# installs dependencies, then starts the API on http://localhost:8000
set -e
cd "$(dirname "$0")/backend"

if [ ! -d ".venv" ]; then
  echo "Setting up (first run only)..."
  python3 -m venv .venv
fi

source .venv/bin/activate
pip install -q -r requirements.txt
echo ""
echo "Starting backend at http://localhost:8000 — leave this window open."
echo "Now open index.html (in the project folder) in your browser."
echo ""
uvicorn app.main:app --host 0.0.0.0 --port 8000
