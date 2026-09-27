import os
import sys

# Ensure project root is in sys.path for backend imports
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.app.main import app

# Vercel automatically exposes 'app' as the ASGI application entry point
