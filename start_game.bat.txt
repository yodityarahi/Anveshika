@echo off
title Bharat Quest - SIH Living Museum Launcher
color 0E

echo =====================================================================
echo             BHARAT QUEST: AN INTERACTIVE LIVING MUSEUM
echo                Smart India Hackathon Prototype (SIH)
echo =====================================================================
echo.

:: Check for Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.10+ from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

:: Create Virtual Environment if not present
if not exist ".venv" (
    echo [1/3] Creating virtual environment (.venv)...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo [2/3] Installing dependencies from backend/requirements.txt...
    .\.venv\Scripts\pip install -r backend/requirements.txt
) else (
    echo [1/2] Virtual environment (.venv) detected.
)

:: Verify dependencies are installed
if not exist ".\.venv\Lib\site-packages\fastapi" (
    echo Installing dependencies...
    .\.venv\Scripts\pip install -r backend/requirements.txt
)

echo.
echo [LAUNCH] Starting FastAPI server at http://127.0.0.1:8000...
echo [INFO] Press Ctrl+C in this terminal window to stop the server anytime.
echo.

:: Wait 2 seconds and launch default browser
start "" cmd /c "timeout /t 2 /nobreak >nul && start http://127.0.0.1:8000"

:: Start backend
.\.venv\Scripts\python.exe backend/run.py

pause
