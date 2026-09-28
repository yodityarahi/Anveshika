from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from backend.app.database import db_manager
from backend.app.models.gamification import (
    ALL_BADGES,
    LEVEL_TIERS,
    compute_level_progress,
    compute_overall_progress,
    evaluate_user_badges,
    hydrate_badges,
    compute_unlocked_content
)

router = APIRouter(prefix="/gamification", tags=["Gamification & Progression"])

VALID_LOCATIONS = {
    "residential_area": "Residential Quarter & Courtyard Dwellings",
    "main_street": "The Grand Avenue & 90° Grid Intersection",
    "drainage_system": "Subterranean Corbelled Drainage & Sump Network",
    "great_bath": "The Great Bath of Mohenjo-daro",
    "granary_area": "The Great Granary & Agronomic Reserve",
    "marketplace": "Bustling Marketplace & Trade Caravanserai",
    "craft_workshop": "Artisan Bead & Bronze Metallurgy Workshop"
}

class ExploreLocationRequest(BaseModel):
    username: str
    location_id: str

class ExploreLocationResponse(BaseModel):
    success: bool
    is_new: bool
    message: str
    location_id: str
    location_name: str
    xp_awarded: int
    tokens_awarded: int
    explored_count: int
    total_locations: int = 7
    level_up: Dict[str, Any]
    newly_unlocked_badges: List[str]
    overall_progress: Dict[str, Any]

@router.get("/badges")
def get_all_badges():
    """
    Returns the comprehensive catalog of all 12 Harappan badges with unlock criteria.
    """
    return {
        "total_badges": len(ALL_BADGES),
        "badges": ALL_BADGES
    }

@router.get("/levels")
def get_all_levels():
    """
    Returns all 5 progression level tiers with required XP and unlockable perks.
    """
    return {
        "total_levels": len(LEVEL_TIERS),
        "tiers": LEVEL_TIERS
    }

@router.get("/status/{username}")
def get_player_gamification_status(username: str):
    """
    Returns the full gamification dashboard status for a given player:
    XP math, level tiers, badge unlock states with progress bars, and unlockable perks.
    """
    db = db_manager.get_db()
    clean_username = (username or "Arjun").strip()
    user = db["users"].find_one({"username": {"$regex": f"^{clean_username}$", "$options": "i"}})
    if not user:
        user = db_manager.ensure_user(clean_username)
    
    stats = user.get("stats", {})
    xp = stats.get("xp", 150)
    
    # Evaluate badges
    evaluated_badges = evaluate_user_badges(stats)
    stats["badges"] = evaluated_badges
    
    # Calculate level and progress
    level_prog = compute_level_progress(xp)
    stats["level"] = level_prog["current_level"]
    
    overall_prog = compute_overall_progress(stats)
    stats["progress_percentage"] = overall_prog["overall_percentage"]
    
    unlocked_content = compute_unlocked_content(stats)
    stats["unlocked_content"] = [c["id"] for c in unlocked_content if c["unlocked"]]
    
    # Persist synced stats
    db["users"].update_one({"_id": user["_id"]}, {"$set": {"stats": stats}})
    db_manager.save_state()
    
    hydrated = hydrate_badges(stats["badges"], stats=stats)
    
    return {
        "username": user["username"],
        "level_progress": level_prog,
        "overall_progress": overall_prog,
        "badges_unlocked_count": len([b for b in hydrated if b["unlocked"]]),
        "total_badges_count": len(hydrated),
        "badges": hydrated,
        "unlocked_content": unlocked_content,
        "raw_stats": {
            "xp": xp,
            "level": level_prog["current_level"],
            "seal_tokens": stats.get("seal_tokens", 15),
            "completed_quests_count": len(stats.get("completed_quests", [])),
            "discovered_artifacts_count": len(stats.get("discovered_artifacts", [])),
            "explored_locations_count": len(stats.get("explored_locations", []))
        }
    }

@router.post("/explore-location", response_model=ExploreLocationResponse)
def record_location_exploration(payload: ExploreLocationRequest):
    """
    Records an ancient city sector exploration.
    Strictly prevents duplicate XP rewards! Awards +75 XP on first visit,
    evaluates level progression, badge unlock triggers, and persists to MongoDB / state.
    """
    db = db_manager.get_db()
    clean_username = (payload.username or "Arjun").strip()
    user = db["users"].find_one({"username": {"$regex": f"^{clean_username}$", "$options": "i"}})
    if not user:
        user = db_manager.ensure_user(clean_username)
        
    loc_id = payload.location_id.strip()
    loc_name = VALID_LOCATIONS.get(loc_id, loc_id.replace("_", " ").title())
    
    stats = user.get("stats", {})
    explored = stats.setdefault("explored_locations", [])
    current_xp = stats.get("xp", 150)
    current_level = stats.get("level", 1)
    current_badges = set(stats.get("badges", []))
    
    is_new = loc_id not in explored
    
    if not is_new:
        level_prog = compute_level_progress(current_xp)
        overall_prog = compute_overall_progress(stats)
        return ExploreLocationResponse(
            success=True,
            is_new=False,
            message=f"You have already surveyed '{loc_name}'. Relic observations remain documented in your field notes.",
            location_id=loc_id,
            location_name=loc_name,
            xp_awarded=0,
            tokens_awarded=0,
            explored_count=len(explored),
            total_locations=len(VALID_LOCATIONS),
            level_up={
                "level_up_occurred": False,
                "current_level": current_level,
                "level_title": level_prog["level_title"],
                "unlocked_perks": []
            },
            newly_unlocked_badges=[],
            overall_progress=overall_prog
        )
        
    # First time discovery:
    explored.append(loc_id)
    xp_to_add = 75
    tokens_to_add = 5
    new_xp = current_xp + xp_to_add
    new_tokens = stats.get("seal_tokens", 15) + tokens_to_add
    
    stats["xp"] = new_xp
    stats["seal_tokens"] = new_tokens
    
    # Check level up
    old_prog = compute_level_progress(current_xp)
    new_prog = compute_level_progress(new_xp)
    level_up_occurred = new_prog["current_level"] > old_prog["current_level"]
    stats["level"] = new_prog["current_level"]
    
    # Evaluate badges
    evaluated_badges = set(evaluate_user_badges(stats))
    new_badges = list(evaluated_badges - current_badges)
    stats["badges"] = list(evaluated_badges)
    
    # Calculate updated overall progress
    overall_prog = compute_overall_progress(stats)
    stats["progress_percentage"] = overall_prog["overall_percentage"]
    
    # Save to MongoDB
    db["users"].update_one(
        {"_id": user["_id"]},
        {"$set": {"stats": stats}}
    )
    
    return ExploreLocationResponse(
        success=True,
        is_new=True,
        message=f"🎉 Sector surveyed! You discovered '{loc_name}' (+{xp_to_add} XP, +{tokens_to_add} Seals).",
        location_id=loc_id,
        location_name=loc_name,
        xp_awarded=xp_to_add,
        tokens_awarded=tokens_to_add,
        explored_count=len(explored),
        total_locations=len(VALID_LOCATIONS),
        level_up={
            "level_up_occurred": level_up_occurred,
            "old_level": old_prog["current_level"],
            "new_level": new_prog["current_level"],
            "level_title": new_prog["level_title"],
            "unlocked_perks": new_prog["unlocked_perks"] if level_up_occurred else []
        },
        newly_unlocked_badges=new_badges,
        overall_progress=overall_prog
    )

@router.post("/evaluate/{username}")
def evaluate_player_gamification(username: str):
    """
    Manually triggers badge and level progression evaluation, saving any newly unlocked achievements.
    """
    db = db_manager.get_db()
    clean_username = (username or "Arjun").strip()
    user = db["users"].find_one({"username": {"$regex": f"^{clean_username}$", "$options": "i"}})
    if not user:
        user = db_manager.ensure_user(clean_username)
        
    stats = user.get("stats", {})
    old_badges = set(stats.get("badges", []))
    new_badges_set = set(evaluate_user_badges(stats))
    newly_earned = list(new_badges_set - old_badges)
    
    stats["badges"] = list(new_badges_set)
    level_prog = compute_level_progress(stats.get("xp", 150))
    stats["level"] = level_prog["current_level"]
    
    overall_prog = compute_overall_progress(stats)
    stats["progress_percentage"] = overall_prog["overall_percentage"]
    
    db["users"].update_one({"_id": user["_id"]}, {"$set": {"stats": stats}})
    db_manager.save_state()
    
    return {
        "username": user["username"],
        "newly_earned_badges": newly_earned,
        "total_badges": len(stats["badges"]),
        "level": stats["level"],
        "level_title": level_prog["level_title"],
        "progress_percentage": overall_prog["overall_percentage"]
    }

@router.get("/lore/secret-archive")
def get_secret_archive():
    """
    Unlocks high-level archaeological lore: The Harappan Secret Inscription Chamber.
    """
    return {
        "title": "The Harappan Secret Inscription Chamber",
        "level_required": 4,
        "discovery_site": "Dholavira Northern Gateway & Mohenjo-daro Citadel HR Area",
        "archive_entries": [
            {
                "topic": "The Dholavira 10-Symbol Signboard",
                "finding": "In 1999, ASI excavators at Dholavira uncovered a massive wooden signboard embedded with 10 giant gypsum-inlaid symbols (each 37cm tall). It was mounted above the northern gateway of the castle citadel, likely naming the city or welcoming maritime delegations.",
                "archaeological_insight": "Indicates public literacy or standardized civic heraldry 4,500 years ago!"
            },
            {
                "topic": "The Undeciphered Indus Script",
                "finding": "Over 400 distinct logograms have been recorded across 4,000+ inscribed objects. The script is written from right to left (proven by cramping of signs on the left margin of seals).",
                "archaeological_insight": "Computers and epigraphists continue statistical concordance analysis to crack this sacred Bronze Age tongue."
            },
            {
                "topic": "The Sacred 1:2:4 Brick Metrology",
                "finding": "Kiln-baked bricks throughout Mohenjo-daro, Harappa, Lothal, and Kalibangan strictly adhere to 7 x 14 x 28 cm (thickness:width:length = 1:2:4).",
                "archaeological_insight": "This mathematical proportion provided perfect English bond interlocking, giving structures extraordinary resistance against tectonic tremors."
            }
        ]
    }
