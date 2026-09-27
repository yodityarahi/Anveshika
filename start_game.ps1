# Bharat Quest - PowerShell Launcher for Windows
Write-Host "=====================================================================" -ForegroundColor Yellow
Write-Host "            BHARAT QUEST: AN INTERACTIVE LIVING MUSEUM" -ForegroundColor Cyan
Write-Host "               Smart India Hackathon Prototype (SIH)" -ForegroundColor Yellow
Write-Host "=====================================================================" -ForegroundColor Yellow
Write-Host ""

# Check Python
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Host "[ERROR] Python is not installed or not in PATH!" -ForegroundColor Red
    Write-Host "Please install Python 3.10+ from https://www.python.org/"
    pause
    exit 1
}

# Create venv if missing
if (-not (Test-Path ".venv")) {
    Write-Host "[1/3] Creating virtual environment (.venv)..." -ForegroundColor Green
    python -m venv .venv
    Write-Host "[2/3] Installing dependencies from backend/requirements.txt..." -ForegroundColor Green
    & .\.venv\Scripts\pip.exe install -r backend/requirements.txt
} else {
    Write-Host "[1/2] Virtual environment (.venv) detected." -ForegroundColor Green
}

# Ensure dependencies
if (-not (Test-Path ".\.venv\Lib\site-packages\fastapi")) {
    Write-Host "Installing missing dependencies..." -ForegroundColor Yellow
    & .\.venv\Scripts\pip.exe install -r backend/requirements.txt
}

Write-Host ""
Write-Host "[LAUNCH] Starting FastAPI server at http://127.0.0.1:8000..." -ForegroundColor Cyan
Write-Host "[INFO] Press Ctrl+C in this terminal to stop the server." -ForegroundColor Gray
Write-Host ""

# Open browser after 2 seconds
Start-Job -ScriptBlock { Start-Sleep -Seconds 2; Start-Process "http://127.0.0.1:8000" } | Out-Null

# Start server
& .\.venv\Scripts\python.exe backend/run.py
