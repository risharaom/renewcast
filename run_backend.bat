@echo off
REM One-command backend startup: creates a virtual environment on first run,
REM installs dependencies, then starts the API on http://localhost:8000
cd /d "%~dp0backend"

if not exist ".venv" (
  echo Setting up (first run only)...
  python -m venv .venv
)

call .venv\Scripts\activate.bat
pip install -q -r requirements.txt

echo.
echo Starting backend at http://localhost:8000 — leave this window open.
echo Now open index.html (in the project folder) in your browser.
echo.
uvicorn app.main:app --host 0.0.0.0 --port 8000
