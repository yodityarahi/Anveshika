import os
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from backend.app.config import settings
from backend.app.database import db_manager
from backend.app.routes import (
    auth,
    user,
    ivc,
    quests,
    puzzles,
    museum,
    gamification,
    ai_engine,
    final_challenge
)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Gamified interactive educational living museum prototype for SIH problem statement 26208."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    db_manager.connect()

app.include_router(auth.router, prefix="/api")
app.include_router(user.router, prefix="/api")
app.include_router(ivc.router, prefix="/api")
app.include_router(quests.router, prefix="/api")
app.include_router(puzzles.router, prefix="/api")
app.include_router(museum.router, prefix="/api")
app.include_router(gamification.router, prefix="/api")
app.include_router(ai_engine.router, prefix="/api")
app.include_router(final_challenge.router, prefix="/api")

FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend"))
if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/")
def serve_index():
    index_file = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "Welcome to Bharat Quest API. Frontend files not found at expected location."}

@app.get("/api")
@app.get("/api/")
def api_root():
    return {
        "status": "online",
        "app_name": settings.APP_NAME,
        "version": settings.VERSION,
        "civilization": settings.CIVILIZATION,
        "message": "Bharat Quest Serverless API is online."
    }

@app.get("/api/health")
def health_check():
    db_health = db_manager.health_check()
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.VERSION,
        "sih_problem": settings.SIH_PROBLEM_STATEMENT,
        "civilization": settings.CIVILIZATION,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "database": db_health
    }

@app.exception_handler(404)
def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Resource Not Found",
            "detail": f"Path '{request.url.path}' does not exist on Bharat Quest server."
        }
    )

@app.exception_handler(500)
def server_error_handler(request: Request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": "An unexpected error occurred in Bharat Quest backend."
        }
    )
