from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from uuid import uuid4
from backend.app.database import db_manager
from backend.app.models.user import (
    UserRegisterRequest,
    UserLoginRequest,
    UserProfileResponse,
    UserStats,
    LevelProgress,
    BadgeInfo
)
from backend.app.models.gamification import (
    compute_level_progress,
    hydrate_badges,
    compute_overall_progress,
    evaluate_user_badges,
    compute_unlocked_content
)

router = APIRouter(prefix="/auth", tags=["Authentication & Profile"])

def format_user_profile(user_doc: dict, token: str = None) -> UserProfileResponse:
    stats_data = user_doc.get("stats", {})
    
    # Evaluate badges dynamically based on achievements
    evaluated_badges = evaluate_user_badges(stats_data)
    stats_data["badges"] = evaluated_badges
    
    # Calculate level progress
    xp = stats_data.get("xp", 150)
    level_prog = compute_level_progress(xp)
    stats_data["level"] = level_prog["current_level"]
    
    # Calculate overall progress percentage
    overall_prog = compute_overall_progress(stats_data)
    stats_data["progress_percentage"] = overall_prog["overall_percentage"]
    
    # Calculate unlocked content perks
    unlocked_content = compute_unlocked_content(stats_data)
    stats_data["unlocked_content"] = [c["id"] for c in unlocked_content if c["unlocked"]]
    
    # Save any newly synchronized stats back to DB if user has an _id
    if "_id" in user_doc:
        db = db_manager.get_db()
        db["users"].update_one(
            {"_id": user_doc["_id"]},
            {"$set": {"stats": stats_data}}
        )
        
    stats = UserStats(**stats_data)
    badges_details = [BadgeInfo(**b) for b in hydrate_badges(stats.badges, stats=stats_data)]
    
    return UserProfileResponse(
        username=user_doc["username"],
        age=user_doc.get("age", 14),
        avatar=user_doc.get("avatar", "🧑‍🎓"),
        archetype=user_doc.get("archetype", "Town Architect"),
        token=token or user_doc.get("session_token"),
        stats=stats,
        level_progress=LevelProgress(**level_prog),
        badges_details=badges_details,
        overall_progress=overall_prog,
        unlocked_content=unlocked_content,
        created_at=user_doc.get("created_at", datetime.utcnow().isoformat() + "Z"),
        last_login_at=user_doc.get("last_login_at")
    )

@router.post("/register", response_model=UserProfileResponse)
def register_user(payload: UserRegisterRequest):
    db = db_manager.get_db()
    users_col = db["users"]
    
    # Check for duplicate username
    clean_username = payload.username.strip()
    existing = users_col.find_one({"username": {"$regex": f"^{clean_username}$", "$options": "i"}})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Player name '{clean_username}' is already registered. Please choose another name or login."
        )
    
    now_str = datetime.utcnow().isoformat() + "Z"
    session_token = f"bq_{uuid4().hex[:16]}"
    
    initial_stats = {
        "xp": 150,
        "level": 1,
        "seal_tokens": 15,
        "unlocked_zones": ["citadel_gateway", "citadel_great_bath"],
        "completed_quests": [],
        "badges": ["badge_apprentice_excavator"],
        "discovered_artifacts": [],
        "explored_locations": [],
        "unlocked_content": ["unlock_lower_town", "unlock_common_vitrines"],
        "progress_percentage": 0.0
    }
    
    new_user = {
        "username": clean_username,
        "age": payload.age,
        "avatar": payload.avatar,
        "archetype": payload.archetype,
        "password": payload.password or "1234",
        "session_token": session_token,
        "created_at": now_str,
        "last_login_at": now_str,
        "stats": initial_stats
    }
    
    users_col.insert_one(new_user)
    return format_user_profile(new_user, token=session_token)

@router.post("/login", response_model=UserProfileResponse)
def login_user(payload: UserLoginRequest):
    db = db_manager.get_db()
    users_col = db["users"]
    
    clean_username = payload.username.strip()
    user = users_col.find_one({"username": {"$regex": f"^{clean_username}$", "$options": "i"}})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Player profile '{clean_username}' not found. Please register first."
        )
    
    # Simple password check for prototype
    expected_pw = user.get("password", "1234")
    if payload.password and payload.password != expected_pw:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password / PIN. Default PIN is '1234'."
        )
    
    # Update last login & refresh token
    now_str = datetime.utcnow().isoformat() + "Z"
    token = user.get("session_token") or f"bq_{uuid4().hex[:16]}"
    users_col.update_one(
        {"_id": user["_id"]},
        {"$set": {"last_login_at": now_str, "session_token": token}}
    )
    user["last_login_at"] = now_str
    user["session_token"] = token
    
    return format_user_profile(user, token=token)

@router.get("/status")
def auth_status():
    return {"status": "ok", "service": "Authentication & Profile System"}