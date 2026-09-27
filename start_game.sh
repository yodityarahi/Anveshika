#!/usr/bin/env bash

echo "====================================================================="
echo "            BHARAT QUEST: AN INTERACTIVE LIVING MUSEUM"
echo "               Smart India Hackathon Prototype (SIH)"
echo "====================================================================="
echo ""

# Find Python 3
PYTHON_BIN="python3"
if ! command -v "$PYTHON_BIN" &> /dev/null; then
    PYTHON_BIN="python"
fi

if ! command -v "$PYTHON_BIN" &> /dev/null; then
    echo "[ERROR] Python 3 is not installed or not in PATH!"
    echo "Please install Python 3.10+ from https://www.python.org/"
    exit 1
fi

# Create virtual environment if missing
if [ ! -d ".venv" ]; then
    echo "[1/3] Creating virtual environment (.venv)..."
    "$PYTHON_BIN" -m venv .venv
    echo "[2/3] Installing dependencies from backend/requirements.txt..."
    ./.venv/bin/pip install -r backend/requirements.txt
else
    echo "[1/2] Virtual environment (.venv) detected."
fi

# Ensure dependencies
if [ ! -d ".venv/lib" ] || ! ./.venv/bin/python -c "import fastapi" &> /dev/null; then
    echo "Installing missing dependencies..."
    ./.venv/bin/pip install -r backend/requirements.txt
fi

echo ""
echo "[LAUNCH] Starting FastAPI server at http://127.0.0.1:8000..."
echo "[INFO] Press Ctrl+C to stop the server."
echo ""

# Open browser
if command -v xdg-open &> /dev/null; then
    (sleep 2 && xdg-open "http://127.0.0.1:8000") &
elif command -v open &> /dev/null; then
    (sleep 2 && open "http://127.0.0.1:8000") &
fi

# Launch backend
./.venv/bin/python backend/run.py
