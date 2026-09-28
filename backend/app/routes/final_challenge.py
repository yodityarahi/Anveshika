"""
=================================================================
BHARAT QUEST - PHASE 10: FINAL INDUS VALLEY CIVILIZATION CHALLENGE
FastAPI Router & MongoDB Persistence Engine
=================================================================
"""
from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any, List, Optional
from datetime import datetime
from backend.app.database import db_manager
from backend.app.models.final_challenge import (
    FINAL_CHALLENGE_DILEMMAS,
    LEARNING_SUMMARY_SYNTHESIS,
    FinalChallengeSubmitRequest
)
from backend.app.models.gamification import ALL_BADGES, LEVEL_TIERS

router = APIRouter(prefix="/final-challenge", tags=["Phase 10: Final Challenge"])

def _calculate_level_for_xp(xp: int) -> int:
    current_lvl = 1
    for tier in sorted(LEVEL_TIERS, key=lambda t: t["level"]):
        if xp >= tier["min_xp"]:
            current_lvl = tier["level"]
    return current_lvl

@router.get("/content")
def get_final_challenge_content():
    """
    Returns the 6 interactive decision dilemmas for the Final Indus Valley Civilization Challenge.
    Options are presented without revealing answers before player choice.
    """
    sanitized_dilemmas = []
    for d in FINAL_CHALLENGE_DILEMMAS:
        sanitized_options = []
        for opt in d["options"]:
            sanitized_options.append({
                "id": opt["id"],
                "title": opt["title"],
                "tagline": opt["tagline"],
                "description": opt["description"],
                "score_points": opt["score_points"]
            })
        sanitized_dilemmas.append({
            "id": d["id"],
            "pillar": d["pillar"],
            "title": d["title"],
            "subtitle": d["subtitle"],
            "icon": d["icon"],
            "historical_premise": d["historical_premise"],
            "archaeological_context": d["archaeological_context"],
            "interactive_instruction": d["interactive_instruction"],
            "options": sanitized_options
        })
    return {
        "title": "The Grand Harappan Metropolis Restoration Challenge",
        "description": "Apply your knowledge of city planning, drainage, architecture, trade, resources, and daily life to govern and restore the ancient metropolis.",
        "total_dilemmas": len(sanitized_dilemmas),
        "max_score": len(sanitized_dilemmas) * 100,
        "dilemmas": sanitized_dilemmas,
        "achievement_badge": "Indus Valley Explorer"
    }

@router.post("/submit")
def submit_final_challenge(req: FinalChallengeSubmitRequest):
    """
    Evaluates player decisions across all 6 core historical pillars, awards XP and the
    'Indus Valley Explorer' capstone achievement badge, and saves the final result in MongoDB.
    """
    clean_username = (req.username or "Arjun").strip()
    db = db_manager.get_db()
    user = db["users"].find_one({"username": {"$regex": f"^{clean_username}$", "$options": "i"}})
    if not user:
        user = db_manager.ensure_user(clean_username)

    user_stats = user.get("stats", {})
    total_score = 0
    max_score = len(FINAL_CHALLENGE_DILEMMAS) * 100
    evaluations = []

    # Map of all badges for hydration
    badge_catalog = {b["id"]: b for b in ALL_BADGES}

    # Evaluate each dilemma
    for dilemma in FINAL_CHALLENGE_DILEMMAS:
        d_id = dilemma["id"]
        chosen_opt_id = req.decisions.get(d_id)
        
        # Find matching option
        matched_option = next((opt for opt in dilemma["options"] if opt["id"] == chosen_opt_id), None)
        correct_option = next(opt for opt in dilemma["options"] if opt["is_correct"])

        if matched_option:
            pts = matched_option["score_points"] if matched_option["is_correct"] else matched_option.get("score_points", 0)
            is_correct = matched_option["is_correct"]
            feedback = matched_option["pedagogical_feedback"]
            chosen_title = matched_option["title"]
        else:
            pts = 0
            is_correct = False
            feedback = "No decision recorded for this municipal dilemma."
            chosen_title = "Unanswered"

        total_score += pts
        evaluations.append({
            "dilemma_id": d_id,
            "pillar": dilemma["pillar"],
            "title": dilemma["title"],
            "icon": dilemma["icon"],
            "chosen_option_id": chosen_opt_id,
            "chosen_title": chosen_title,
            "correct_option_id": correct_option["id"],
            "correct_title": correct_option["title"],
            "is_correct": is_correct,
            "points_earned": pts,
            "max_points": 100,
            "feedback": feedback
        })

    percentage = round((total_score / max_score) * 100, 1)
    passed = percentage >= 60.0

    # XP and Badge Rewards
    xp_to_award = 500 if passed else 200
    seals_to_award = 20 if passed else 5
    capstone_badge_id = "badge_indus_explorer"

    current_xp = user_stats.get("xp", 150)
    new_xp = current_xp + xp_to_award
    new_level = _calculate_level_for_xp(new_xp)
    current_badges = list(user_stats.get("badges", []))

    if passed and capstone_badge_id not in current_badges:
        current_badges.append(capstone_badge_id)

    # Save to MongoDB
    final_record = {
        "completed": True,
        "completed_at": datetime.utcnow().isoformat(),
        "score": total_score,
        "max_score": max_score,
        "percentage": percentage,
        "passed": passed,
        "xp_awarded": xp_to_award,
        "achievement": "Indus Valley Explorer" if passed else "Apprentice Surveyor",
        "decisions_summary": evaluations
    }

    db["users"].update_one(
        {"_id": user["_id"]},
        {
            "$set": {
                "stats.xp": new_xp,
                "stats.level": new_level,
                "stats.seal_tokens": user_stats.get("seal_tokens", 15) + seals_to_award,
                "stats.badges": current_badges,
                "final_challenge": final_record
            }
        }
    )
    db_manager.save_state()

    # Hydrate badges details
    hydrated_badges = []
    for b_id in current_badges:
        b_info = badge_catalog.get(b_id, {
            "id": b_id,
            "name": b_id.replace("badge_", "").replace("_", " ").title(),
            "description": "Harappan Archaeological Achievement.",
            "icon": "🏅",
            "category": "Excavation"
        })
        hydrated_badges.append(b_info)

    # Final Rank Designation
    if percentage >= 90.0:
        honorary_title = "Grand Archaeological Governor of the Indus Valley"
    elif percentage >= 75.0:
        honorary_title = "Chief Municipal Architect of Mohenjo-daro"
    elif percentage >= 60.0:
        honorary_title = "Indus Valley Master Surveyor"
    else:
        honorary_title = "Apprentice Field Excavator"

    return {
        "success": True,
        "username": clean_username,
        "final_score": total_score,
        "max_score": max_score,
        "percentage": percentage,
        "passed": passed,
        "xp_earned": xp_to_award,
        "seals_earned": seals_to_award,
        "new_total_xp": new_xp,
        "new_level": new_level,
        "honorary_title": honorary_title,
        "achievement": "Indus Valley Explorer",
        "achievement_badge": "badge_indus_explorer",
        "artifacts_discovered_count": len(user_stats.get("discovered_artifacts", [])),
        "artifacts_discovered": user_stats.get("discovered_artifacts", []),
        "quests_completed_count": len(user_stats.get("completed_quests", [])),
        "quests_completed": user_stats.get("completed_quests", []),
        "badges_earned_count": len(current_badges),
        "badges_earned": hydrated_badges,
        "areas_explored_count": len(user_stats.get("explored_locations", [])),
        "areas_explored": user_stats.get("explored_locations", []),
        "learning_summary": LEARNING_SUMMARY_SYNTHESIS,
        "evaluations": evaluations
    }

@router.get("/status/{username}")
def get_final_challenge_status(username: str):
    """
    Checks if a player has taken the Final Challenge and returns their completion profile and score.
    """
    clean_username = (username or "Arjun").strip()
    db = db_manager.get_db()
    user = db["users"].find_one({"username": {"$regex": f"^{clean_username}$", "$options": "i"}})
    if not user:
        user = db_manager.ensure_user(clean_username)

    final_challenge = user.get("final_challenge")
    user_stats = user.get("stats", {})
    badge_catalog = {b["id"]: b for b in ALL_BADGES}

    current_badges = user_stats.get("badges", [])
    hydrated_badges = [badge_catalog.get(b_id, {"id": b_id, "name": b_id, "icon": "🏅"}) for b_id in current_badges]

    return {
        "username": clean_username,
        "has_completed": final_challenge is not None and final_challenge.get("completed", False),
        "final_challenge": final_challenge,
        "stats_snapshot": {
            "total_xp": user_stats.get("xp", 150),
            "level": user_stats.get("level", 1),
            "artifacts_discovered_count": len(user_stats.get("discovered_artifacts", [])),
            "artifacts_discovered": user_stats.get("discovered_artifacts", []),
            "quests_completed_count": len(user_stats.get("completed_quests", [])),
            "quests_completed": user_stats.get("completed_quests", []),
            "badges_earned_count": len(current_badges),
            "badges_earned": hydrated_badges,
            "areas_explored_count": len(user_stats.get("explored_locations", [])),
            "areas_explored": user_stats.get("explored_locations", [])
        },
        "learning_summary": LEARNING_SUMMARY_SYNTHESIS
    }
