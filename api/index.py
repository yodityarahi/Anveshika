import os
import sys
import logging
import traceback

# 1. Serverless sys.path configuration so execution can resolve project modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root not in sys.path:
    sys.path.insert(0, _root)
_api = os.path.dirname(os.path.abspath(__file__))
if _api not in sys.path:
    sys.path.insert(0, _api)

logger = logging.getLogger("anveshika.serverless")
logging.basicConfig(level=logging.INFO)

# 2. Wrap top-level imports and app initialization in a robust try/except block
try:
    from backend.app.main import app
    logger.info("Successfully loaded Anveshika FastAPI app into serverless runtime.")
except Exception as exc:
    err_traceback = traceback.format_exc()
    logger.critical(f"FATAL: Failed to import backend.app.main into serverless runtime: {exc}\n{err_traceback}")
    print(f"FATAL: Failed to import backend.app.main into serverless runtime: {exc}\n{err_traceback}", file=sys.stderr)

    # Expose a resilient fallback ASGI FastAPI app so Vercel never crashes on module import
    try:
        from fastapi import FastAPI, Request
        from fastapi.responses import JSONResponse
        from fastapi.middleware.cors import CORSMiddleware

        app = FastAPI(title="Anveshika Serverless Recovery")
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        @app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"])
        async def fallback_route(path_name: str, request: Request):
            return JSONResponse(
                status_code=500,
                content={
                    "error": "ServerlessModuleImportError",
                    "message": "Failed to initialize backend.app.main in serverless environment.",
                    "detail": str(exc),
                    "traceback": err_traceback.splitlines(),
                    "requested_path": f"/{path_name}",
                    "method": request.method
                }
            )
    except Exception as fastapi_err:
        # Ultimate zero-dependency pure ASGI fallback
        async def app(scope, receive, send):
            if scope["type"] == "http":
                body = (
                    f'{{"error":"FatalServerlessBootstrapError","detail":"{str(exc)}",'
                    f'"fastapi_error":"{str(fastapi_err)}"}}'
                ).encode("utf-8")
                await send({
                    "type": "http.response.start",
                    "status": 500,
                    "headers": [
                        [b"content-type", b"application/json"],
                        [b"access-control-allow-origin", b"*"],
                        [b"content-length", str(len(body)).encode("ascii")]
                    ]
                })
                await send({
                    "type": "http.response.body",
                    "body": body,
                })

# Vercel automatically exposes 'app' as the ASGI application entry point
