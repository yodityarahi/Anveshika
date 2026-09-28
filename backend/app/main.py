import os
import logging
from datetime import datetime
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

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
from backend.app.models.user import UserRegisterRequest, UserProfileResponse
from backend.app.models.quest import QuestSubmitRequest, QuestSubmitResponse

logger = logging.getLogger("anveshika.main")
logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Anveshika: Interactive Living Museum of Indian Heritage - SIH Problem Statement 26208."
)

# Standard CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    try:
        db_manager.connect()
        logger.info("Anveshika database connection initialized.")
    except Exception as e:
        logger.warning(f"Startup database notice: {e}")

# Include all core API routers with /api prefix
app.include_router(auth.router, prefix="/api")
app.include_router(user.router, prefix="/api")
app.include_router(ivc.router, prefix="/api")
app.include_router(quests.router, prefix="/api")
app.include_router(puzzles.router, prefix="/api")
app.include_router(museum.router, prefix="/api")
app.include_router(gamification.router, prefix="/api")
app.include_router(ai_engine.router, prefix="/api")
app.include_router(final_challenge.router, prefix="/api")

# Static frontend assets mount for local execution
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend"))
if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# -------------------------------------------------------------
# ROOT & CONVENIENCE ALIAS ENDPOINTS FOR SERVERLESS RESILIENCE
# -------------------------------------------------------------

@app.get("/")
def serve_index():
    index_file = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {
        "status": "online",
        "app_name": settings.APP_NAME,
        "message": "Welcome to Anveshika: Interactive Living Museum of Indian Heritage."
    }

@app.get("/api")
@app.get("/api/")
def api_root():
    return {
        "status": "online",
        "app_name": settings.APP_NAME,
        "version": settings.VERSION,
        "civilization": settings.CIVILIZATION,
        "message": "Anveshika Serverless API is online."
    }

@app.get("/api/health")
@app.get("/health")
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

# Flexible Profile Request Model for /create-player-profile
class CreateProfilePayload(BaseModel):
    username: Optional[str] = "Arjun"
    name: Optional[str] = None
    age: Optional[int] = 14
    avatar: Optional[str] = "🧑‍🎓"
    archetype: Optional[str] = "Town Architect"
    password: Optional[str] = "1234"

@app.post("/create-player-profile", response_model=UserProfileResponse)
@app.post("/api/create-player-profile", response_model=UserProfileResponse)
def create_player_profile(payload: CreateProfilePayload):
    """
    Dedicated endpoint supporting /create-player-profile and /api/create-player-profile.
    Auto-registers new explorer profiles or loads existing profile gracefully without 500 error.
    """
    username = (payload.username or payload.name or "Arjun").strip()
    user_doc = db_manager.ensure_user(
        username=username,
        age=payload.age or 14,
        avatar=payload.avatar or "🧑‍🎓",
        archetype=payload.archetype or "Town Architect"
    )
    return auth.format_user_profile(user_doc)

# Flexible Quest Submission Model for /submit-quest
class DirectQuestSubmitPayload(BaseModel):
    quest_id: Optional[str] = "quest_01_rebuild_city"
    questId: Optional[str] = None
    username: Optional[str] = "Arjun"
    submission: Dict[str, Any] = Field(default_factory=dict)
    time_taken_seconds: Optional[float] = 30.0
    attempts_count: Optional[int] = 1
    hints_used: Optional[int] = 0

@app.post("/submit-quest", response_model=QuestSubmitResponse)
@app.post("/api/submit-quest", response_model=QuestSubmitResponse)
def direct_submit_quest(payload: DirectQuestSubmitPayload):
    """
    Direct alias endpoint for /submit-quest and /api/submit-quest.
    Submits quest solutions safely and guarantees user profile auto-provisioning if missing.
    """
    q_id = payload.quest_id or payload.questId or "quest_01_rebuild_city"
    user_name = (payload.username or "Arjun").strip()
    
    # Ensure player exists in state
    db_manager.ensure_user(user_name)
    
    req = QuestSubmitRequest(
        username=user_name,
        submission=payload.submission,
        time_taken_seconds=payload.time_taken_seconds or 30.0,
        attempts_count=payload.attempts_count or 1,
        hints_used=payload.hints_used or 0
    )
    return quests.submit_quest_solution(quest_id=q_id, payload=req)

# -------------------------------------------------------------
# GLOBAL STRUCTURED EXCEPTION HANDLERS WITH GUARANTEED CORS
# -------------------------------------------------------------

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Credentials": "true"
        },
        content={
            "error": "Request Error",
            "status_code": exc.status_code,
            "detail": exc.detail,
            "path": request.url.path
        }
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled exception on {request.method} {request.url.path}: {exc}")
    return JSONResponse(
        status_code=500,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Credentials": "true"
        },
        content={
            "error": "Internal Server Error",
            "detail": str(exc) if settings.DEBUG else "An unexpected error occurred in Anveshika backend.",
            "path": request.url.path
        }
    )
