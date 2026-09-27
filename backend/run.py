import os
import sys

# Ensure UTF-8 output encoding for Windows command line compatibility
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import uvicorn
from backend.app.config import settings

if __name__ == "__main__":
    print("=" * 60)
    print(f"[BHARAT QUEST] {settings.APP_NAME}")
    print(f"[CIVILIZATION] Focus: {settings.CIVILIZATION}")
    print(f"[SERVER URL]   http://{settings.HOST}:{settings.PORT}")
    print(f"[HEALTH CHECK] http://{settings.HOST}:{settings.PORT}/api/health")
    print("=" * 60)
    uvicorn.run(
        "backend.app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )