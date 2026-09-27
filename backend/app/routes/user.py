from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from backend.app.database import db_manager
from backend.app.models.user import UserProfileResponse, UserUpdateRequest, UserStats
from backend.app.routes.auth import format_user_profile

router = APIRouter(prefix="/user", tags=["Player Profile & Stats"])

class AwardXpRequest(BaseModel):
    xp_to_add: int
    tokens_to_add: int = 0
    badge_to_unlock: Optional[str] = None
    quest_to_complete: Optional[str] = None
    artifact_to_add: Optional[str] = None

@router.get("/profile/{username}", response_model=UserProfileResponse)
def get_user_profile(username: str):
    db = db_manager.get_db()
    clean_username = username.strip()
    user = db["users"].find_one({"username": {"$regex": f"^{clean_username}$", "$options": "i"}})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player profile '{clean_username}' was not found in Bharat Quest."
        )
    return format_user_profile(user)

@router.put("/profile/{username}", response_model=UserProfileResponse)
def update_user_profile(username: str, payload: UserUpdateRequest):
    db = db_manager.get_db()
    clean_username = username.strip()
    user = db["users"].find_one({"username": {"$regex": f"^{clean_username}$", "$options": "i"}})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player profile '{clean_username}' not found."
        )
    
    update_fields = {}
    if payload.age is not None:
        update_fields["age"] = payload.age
    if payload.avatar is not None:
        update_fields["avatar"] = payload.avatar
    if payload.archetype is not None:
        update_fields["archetype"] = payload.archetype
        
    if update_fields:
        db["users"].update_one({"_id": user["_id"]}, {"$set": update_fields})
        user.update(update_fields)
        
    return format_user_profile(user)

@router.post("/profile/{username}/award", response_model=UserProfileResponse)
def award_player_progress(username: str, payload: AwardXpRequest):
    """
    Simulate or award game progress (XP, tokens, badges, quests, artifacts).
    """
    db = db_manager.get_db()
    clean_username = username.strip()
    user = db["users"].find_one({"username": {"$regex": f"^{clean_username}$", "$options": "i"}})
    if not user:
        raise HTTPException(status_code=404, detail="Player not found.")
    
    stats = user.get("stats", {})
    stats["xp"] = stats.get("xp", 0) + payload.xp_to_add
    stats["seal_tokens"] = stats.get("seal_tokens", 0) + payload.tokens_to_add
    
    if payload.badge_to_unlock and payload.badge_to_unlock not in stats.get("badges", []):
        stats.setdefault("badges", []).append(payload.badge_to_unlock)
        
    if payload.quest_to_complete and payload.quest_to_complete not in stats.get("completed_quests", []):
        stats.setdefault("completed_quests", []).append(payload.quest_to_complete)
        
    if payload.artifact_to_add and payload.artifact_to_add not in stats.get("discovered_artifacts", []):
        stats.setdefault("discovered_artifacts", []).append(payload.artifact_to_add)
        
    db["users"].update_one({"_id": user["_id"]}, {"$set": {"stats": stats}})
    user["stats"] = stats
    return format_user_profile(user)