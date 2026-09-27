"""
Bharat Quest - Universal Cross-Platform Launcher
Works on Windows, macOS, and Linux without any .bat or .sh dependencies.
This file is safe from WhatsApp / Antivirus security filters.
"""
import os
import sys
import subprocess
import threading
import time
import webbrowser

# Reconfigure stdout for UTF-8 on Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
VENV_DIR = os.path.join(PROJECT_ROOT, ".venv")
REQ_FILE = os.path.join(PROJECT_ROOT, "backend", "requirements.txt")
RUN_SCRIPT = os.path.join(PROJECT_ROOT, "backend", "run.py")

# Determine python executable inside virtual environment
if sys.platform == "win32":
    VENV_PYTHON = os.path.join(VENV_DIR, "Scripts", "python.exe")
    VENV_PIP = os.path.join(VENV_DIR, "Scripts", "pip.exe")
else:
    VENV_PYTHON = os.path.join(VENV_DIR, "bin", "python")
    VENV_PIP = os.path.join(VENV_DIR, "bin", "pip")

def print_banner():
    print("=" * 65)
    print("       BHARAT QUEST: AN INTERACTIVE LIVING MUSEUM")
    print("       Smart India Hackathon Prototype (SIH - Problem 26208)")
    print("=" * 65)
    print()

def ensure_venv():
    if not os.path.exists(VENV_PYTHON):
        print("[1/3] Creating isolated virtual environment (.venv)...")
        import venv
        venv.create(VENV_DIR, with_pip=True)
        print("      Virtual environment created.")
    else:
        print("[1/3] Virtual environment (.venv) detected.")

def ensure_dependencies():
    # Check if fastapi is already installed in venv
    check_code = "import fastapi, uvicorn, pymongo, sklearn"
    result = subprocess.run([VENV_PYTHON, "-c", check_code], capture_output=True)
    if result.returncode != 0:
        print("[2/3] Installing required packages from backend/requirements.txt...")
        print("      (This only happens once on first setup, takes ~30-60 seconds)")
        cmd = [VENV_PIP, "install", "-r", REQ_FILE]
        res = subprocess.run(cmd)
        if res.returncode != 0:
            print("[WARNING] Pip install had issues. Attempting to continue...")
    else:
        print("[2/3] All dependencies verified.")

def open_browser_delayed():
    time.sleep(2)
    url = "http://127.0.0.1:8000"
    print(f"\n[BROWSER] Opening {url} in your default web browser...")
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"[NOTE] Please open {url} manually in your browser.")

def run_server():
    print("[3/3] Starting Bharat Quest FastAPI server...")
    print("      Server URL: http://127.0.0.1:8000")
    print("      API Docs:   http://127.0.0.1:8000/docs")
    print("      Health:     http://127.0.0.1:8000/api/health")
    print("-" * 65)
    print(">> Press Ctrl+C in this terminal window to stop the server anytime <<\n")

    # Start browser opener in background thread
    threading.Thread(target=open_browser_delayed, daemon=True).start()

    # Execute backend/run.py using venv python
    try:
        subprocess.run([VENV_PYTHON, RUN_SCRIPT])
    except KeyboardInterrupt:
        print("\n[STOP] Bharat Quest server stopped successfully.")

if __name__ == "__main__":
    print_banner()
    ensure_venv()
    ensure_dependencies()
    run_server()
