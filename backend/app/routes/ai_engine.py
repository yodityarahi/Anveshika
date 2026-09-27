from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from backend.app.database import db_manager
from backend.app.ml.personalization import (
    quest_recommender,
    difficulty_classifier,
    progress_analyzer,
    PROTOTYPE_DISCLAIMER
)

router = APIRouter(prefix="/ai", tags=["AI / ML Personalization Engine"])

class SimulationRequest(BaseModel):
    accuracy_rate: float = Field(0.85, ge=0.0, le=1.0)
    avg_solve_time: float = Field(35.0, ge=5.0, le=300.0)
    attempts_per_quest: float = Field(1.2, ge=1.0, le=10.0)
    player_level: int = Field(2, ge=1, le=5)
    hints_used: int = Field(1, ge=0, le=5)
    completed_quests: List[str] = Field(default_factory=lambda: ["quest_01_rebuild_city"])

def _extract_player_telemetry(user_doc: dict) -> dict:
    stats = user_doc.get("stats", {})
    history = stats.get("quest_history", [])
    level = stats.get("level", 1)

    if history:
        correct_count = sum(1 for h in history if h.get("is_correct"))
        accuracy_rate = correct_count / len(history)
        avg_solve_time = sum(h.get("time_taken_seconds", 45.0) for h in history) / len(history)
        attempts_per_quest = sum(h.get("attempts_count", 1) for h in history) / len(history)
        hints_used = sum(h.get("hints_used", 0) for h in history)
    else:
        # Default baseline for new players
        accuracy_rate = 0.85 if level >= 2 else 0.75
        avg_solve_time = 40.0
        attempts_per_quest = 1.2
        hints_used = 0

    return {
        "accuracy_rate": accuracy_rate,
        "avg_solve_time": avg_solve_time,
        "attempts_per_quest": attempts_per_quest,
        "player_level": level,
        "hints_used": hints_used
    }

@router.get("/recommendations/{username}")
def get_quest_recommendations(username: str):
    """
    Recommends the next most suitable Indus Valley quest using Scikit-Learn NearestNeighbors.
    """
    db = db_manager.get_db()
    clean_username = username.strip()
    user = db["users"].find_one({"username": {"$regex": f"^{clean_username}$", "$options": "i"}})
    if not user:
        raise HTTPException(status_code=404, detail=f"Player '{clean_username}' not found.")

    stats = user.get("stats", {})
    return quest_recommender.recommend(stats)

@router.get("/difficulty/{username}")
def get_adaptive_difficulty(username: str):
    """
    Classifies player interaction telemetry and recommends dynamic difficulty: Easy, Medium, or Hard.
    """
    db = db_manager.get_db()
    clean_username = username.strip()
    user = db["users"].find_one({"username": {"$regex": f"^{clean_username}$", "$options": "i"}})
    if not user:
        raise HTTPException(status_code=404, detail=f"Player '{clean_username}' not found.")

    telemetry = _extract_player_telemetry(user)
    return difficulty_classifier.classify(telemetry)

@router.get("/learning-progress/{username}")
def get_learning_progress(username: str):
    """
    Generates an explainable 5-pillar Harappan Knowledge Matrix and learning progress analysis.
    """
    db = db_manager.get_db()
    clean_username = username.strip()
    user = db["users"].find_one({"username": {"$regex": f"^{clean_username}$", "$options": "i"}})
    if not user:
        raise HTTPException(status_code=404, detail=f"Player '{clean_username}' not found.")

    stats = user.get("stats", {})
    return progress_analyzer.analyze(stats)

@router.get("/dashboard/{username}")
def get_ai_dashboard(username: str):
    """
    Unified AI Personalization Dashboard endpoint for frontend display.
    """
    db = db_manager.get_db()
    clean_username = username.strip()
    user = db["users"].find_one({"username": {"$regex": f"^{clean_username}$", "$options": "i"}})
    if not user:
        raise HTTPException(status_code=404, detail=f"Player '{clean_username}' not found.")

    stats = user.get("stats", {})
    telemetry = _extract_player_telemetry(user)

    recommendation = quest_recommender.recommend(stats)
    difficulty = difficulty_classifier.classify(telemetry)
    progress = progress_analyzer.analyze(stats)

    return {
        "username": user["username"],
        "recommendation": recommendation,
        "difficulty": difficulty,
        "learning_progress": progress,
        "telemetry_summary": {
            "accuracy_rate": round(telemetry["accuracy_rate"] * 100, 1),
            "avg_solve_time_sec": round(telemetry["avg_solve_time"], 1),
            "attempts_per_quest": round(telemetry["attempts_per_quest"], 1),
            "completed_quests_count": len(stats.get("completed_quests", [])),
            "total_attempts_recorded": len(stats.get("quest_history", []))
        },
        "prototype_disclaimer": PROTOTYPE_DISCLAIMER
    }

@router.post("/simulate")
def simulate_ai(payload: SimulationRequest):
    """
    Simulation sandbox for testing adaptive difficulty and recommendations.
    """
    telemetry = {
        "accuracy_rate": payload.accuracy_rate,
        "avg_solve_time": payload.avg_solve_time,
        "attempts_per_quest": payload.attempts_per_quest,
        "player_level": payload.player_level,
        "hints_used": payload.hints_used
    }
    stats = {
        "level": payload.player_level,
        "completed_quests": payload.completed_quests
    }
    diff = difficulty_classifier.classify(telemetry)
    rec = quest_recommender.recommend(stats)
    return {
        "adaptive_difficulty": diff,
        "quest_recommendation": rec
    }

class HeritageGuideMessage(BaseModel):
    message: str
    username: Optional[str] = "Arjun"
    context: Optional[str] = None

@router.post("/heritage-guide/chat")
def heritage_guide_chat(payload: HeritageGuideMessage):
    """
    Friendly, educational conversational guide for young explorers (10-18 yo).
    Explains artifacts, locations, difficult words, and provides personalized next actions.
    """
    msg = payload.message.lower().strip()
    username = (payload.username or "Arjun").strip()

    # Query player stats if available for personalization
    stats = {}
    try:
        db = db_manager.get_db()
        user = db["users"].find_one({"username": {"$regex": f"^{username}$", "$options": "i"}})
        if user:
            stats = user.get("stats", {})
    except Exception:
        pass

    # Retrieve ML recommendation to offer contextual missions
    rec = quest_recommender.recommend(stats)
    rec_title = rec.get("recommended_quest_title", "Build the Ancient City")
    rec_id = rec.get("recommended_quest_id", "quest_01_rebuild_city")

    # Intent Matching for young learners
    if any(k in msg for k in ["drain", "water", "sewer", "dirty", "clean", "hygiene", "wash"]):
        return {
            "reply": "💧 The people of the Indus Valley built covered drains under their streets to carry away dirty water and keep their cities clean and healthy!",
            "did_you_know": "Indus Valley cities had the world's first covered street drainage system 4,500 years ago!",
            "action": {
                "label": "💧 Explore the Drainage Area",
                "tab": "tab-city",
                "target": "drainage_system"
            }
        }

    if any(k in msg for k in ["seal", "unicorn", "stamp", "animal", "writing", "script"]):
        return {
            "reply": "🏺 Indus Valley seals were small soapstone stamps carved with animals and mystery signs! Merchants pressed them into wet clay tags to seal trade packages.",
            "did_you_know": "Over 65% of all discovered seals feature the magical one-horned animal standing near a sacred brazier!",
            "action": {
                "label": "🦄 View the Unicorn Seal in Museum",
                "tab": "tab-museum",
                "target": "art_unicorn_seal"
            }
        }

    if any(k in msg for k in ["bath", "swimming", "pool", "tank"]):
        return {
            "reply": "🏊 The Great Bath of Mohenjo-daro was a massive public pool. Ancient builders lined it with fired bricks and sealed it with natural tar (bitumen) so water would never leak!",
            "did_you_know": "It was surrounded by changing rooms and filled with fresh water from its own dedicated brick well.",
            "action": {
                "label": "🏛️ Visit the Great Bath",
                "tab": "tab-city",
                "target": "great_bath"
            }
        }

    if any(k in msg for k in ["eat", "food", "breakfast", "crop", "grain", "diet", "wheat", "barley"]):
        return {
            "reply": "🌾 People ate warm barley flatbread, cooked lentils, roasted sesame paste, melons, and sweet dates! They farmed rich alluvial soil watered by the river floods.",
            "did_you_know": "Potatoes, tomatoes, and chillies did not exist in ancient India—they arrived from the Americas thousands of years later!",
            "action": {
                "label": "🌾 Check the Granary Area",
                "tab": "tab-city",
                "target": "granary_area"
            }
        }

    if any(k in msg for k in ["brick", "house", "building", "home", "wall", "ratio", "1:2:4"]):
        return {
            "reply": "🧱 Indus builders baked all their bricks in a strict 1:2:4 ratio (thickness : width : length). This made their brick walls earthquake-resistant and super strong!",
            "did_you_know": "Bricks found 1,000 kilometers apart—from Gujarat to Afghanistan—had identical dimensions!",
            "action": {
                "label": "🏠 Inspect the Ancient Houses",
                "tab": "tab-city",
                "target": "residential_area"
            }
        }

    if any(k in msg for k in ["trade", "boat", "ship", "sail", "money", "lothal", "mesopotamia"]):
        return {
            "reply": "⛵ Indus traders built the world's earliest tidal dockyard at Lothal! They sailed wooden boats across the Arabian Sea to trade carnelian beads and cotton with ancient Mesopotamia.",
            "did_you_know": "Cuneiform tablets in ancient Iraq talk about exotic merchant ships sailing from 'Meluhha' (the Indus Valley)!",
            "action": {
                "label": "🚚 Play Ancient Trade Mission",
                "tab": "tab-quests",
                "target": "quest_04_ancient_trade"
            }
        }

    if any(k in msg for k in ["what next", "next", "mission", "quest", "recommend", "should i do", "what to do", "play"]):
        return {
            "reply": f"🎯 Based on your journey so far, I recommend: **{rec_title}**! Test your skills and unearth a new ancient artifact.",
            "did_you_know": "Completing missions awards Steatite Seals and boosts your Explorer Level!",
            "action": {
                "label": f"🚀 Start {rec_title}",
                "tab": "tab-quests",
                "target": rec_id
            }
        }

    if any(k in msg for k in ["citadel", "what is a citadel"]):
        return {
            "reply": "🏛️ A **Citadel** was an artificial raised mud-brick hill where important public buildings (like the Great Bath and Assembly Halls) stood, safe above flood waters!",
            "did_you_know": "Citadels were always placed on the western side of Indus cities.",
            "action": {
                "label": "🏛️ Explore the Citadel",
                "tab": "tab-city",
                "target": "great_bath"
            }
        }

    if any(k in msg for k in ["steatite", "soapstone"]):
        return {
            "reply": "🪨 **Steatite** (also called soapstone) is a soft mineral that craftspeople carved into seals and beads, then baked in hot kilns until it turned shiny white and hard!",
            "did_you_know": "Harappan artisans could drill holes thinner than a needle through hard gemstone beads!",
            "action": {
                "label": "🏺 Visit the Craft Workshop",
                "tab": "tab-city",
                "target": "craft_workshop"
            }
        }

    if any(k in msg for k in ["terracotta", "clay"]):
        return {
            "reply": "🏺 **Terracotta** is clay baked in a kiln! Ancient children played with terracotta toy bullock carts with rolling wooden wheels, and clay animal whistles.",
            "did_you_know": "Indus toy carts look almost identical to traditional bullock carts still used in rural India today!",
            "action": {
                "label": "🪅 View Toy Bullock Cart",
                "tab": "tab-museum",
                "target": "art_toy_cart"
            }
        }

    if any(k in msg for k in ["disappear", "collapse", "die", "destroy", "end", "what happened"]):
        return {
            "reply": "🌧️ The civilization wasn't destroyed by war! Climate shifts caused the sacred Saraswati and Indus river branches to dry up or flood. People peacefully migrated to other fertile river valleys.",
            "did_you_know": "There are no signs of battles, weapons of war, or burned palaces in Indus cities.",
            "action": {
                "label": "🗺️ Explore Ancient City Map",
                "tab": "tab-city",
                "target": "main_street"
            }
        }

    # Friendly default reply
    return {
        "reply": "👋 Hi Explorer! I'm your Heritage Guide. You can ask me questions like: 'Why did they build drains?', 'What was the Great Bath for?', 'What did people eat?', or 'What mission should I do next?'",
        "did_you_know": "Indus cities had wide streets crossing in a neat grid pattern, just like modern planned cities!",
        "action": {
            "label": f"🎯 Play Recommended: {rec_title}",
            "tab": "tab-quests",
            "target": rec_id
        }
    }
