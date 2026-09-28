import os
import sys
import logging
import traceback
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# 1. Serverless sys.path configuration so execution can resolve project modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root not in sys.path:
    sys.path.insert(0, _root)

logger = logging.getLogger("anveshika.serverless")
logging.basicConfig(level=logging.INFO)

# 2. Strict top-level FastAPI declaration for Vercel static AST detection
app = FastAPI(title="Anveshika Serverless Entrypoint")

try:
    from backend.app.main import app as backend_app
    app = backend_app
    logger.info("Successfully loaded Anveshika backend.app.main into serverless runtime.")
except Exception as exc:
    err_traceback = traceback.format_exc()
    logger.critical(f"FATAL: Failed to import backend.app.main into serverless runtime: {exc}\n{err_traceback}")
    print(f"FATAL: Failed to import backend.app.main into serverless runtime: {exc}\n{err_traceback}", file=sys.stderr)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"])
    async def fallback_route(path_name: str):
        return JSONResponse(
            status_code=500,
            content={
                "error": "ServerlessModuleImportError",
                "message": "Failed to initialize backend.app.main in serverless environment.",
                "detail": str(exc),
                "traceback": err_traceback.splitlines(),
                "path": f"/{path_name}"
            }
        )

# 3. Explicit top-level handler aliases for Vercel (@vercel/python)
application = app
handler = app
