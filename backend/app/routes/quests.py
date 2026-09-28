from fastapi import APIRouter, HTTPException, Query, status
from typing import List, Optional, Dict, Any
from datetime import datetime
from backend.app.database import db_manager
from backend.app.models.quest import (
    QuestModel,
    QuestSummary,
    QuestSubmitRequest,
    QuestSubmitResponse,
    ArtifactReward,
    QuestChallenge
)
from backend.app.routes.auth import format_user_profile

router = APIRouter(prefix="/quests", tags=["Quests & Missions"])

# The 5 Core Quests for Indus Valley Civilization (Extensible for future civilizations)
QUESTS_CATALOG: Dict[str, Dict[str, Any]] = {
    "quest_01_rebuild_city": {
        "quest_id": "quest_01_rebuild_city",
        "title": "Build the Ancient City",
        "civilization_id": "ivc",
        "story_context": "Help the city builder organize the ancient town! Drag and drop houses, roads, drains, and public buildings into their correct spots.",
        "location": "Mohenjo-daro Town & Citadel",
        "objective": "Place houses, roads, drains, and public buildings into their correct city zones.",
        "difficulty": "Beginner",
        "learning_concept": "Indus Valley Urban Planning & Grid Systems: Build your ancient city with houses, roads, and drains!",
        "npc_name": "Siddhu, Master Town Surveyor",
        "npc_avatar": "📐",
        "challenge": {
            "type": "rebuild_city",
            "instructions": "Drag and match each of the 4 city parts (Houses, Roads, Drains, Public Buildings) to its proper zone.",
            "interactive_data": {
                "slots": [
                    {
                        "id": "slot_houses",
                        "target_component": "houses",
                        "zone_name": "Lower Town (Neighborhood)",
                        "icon": "🏡",
                        "hint": "Brick family homes built around cool courtyards."
                    },
                    {
                        "id": "slot_roads",
                        "target_component": "roads",
                        "zone_name": "Wide Main Streets",
                        "icon": "🛣️",
                        "hint": "Wide straight avenues that cross each other at neat right angles."
                    },
                    {
                        "id": "slot_drainage",
                        "target_component": "drainage",
                        "zone_name": "Covered Clean Drains",
                        "icon": "🚰",
                        "hint": "Brick drains under the street that carry dirty water away safely."
                    },
                    {
                        "id": "slot_public_areas",
                        "target_component": "public_areas",
                        "zone_name": "Citadel Mound (Great Bath & Granary)",
                        "icon": "🏛️",
                        "hint": "High raised area for the Great Bath and community grain storage."
                    }
                ],
                "cards": [
                    {
                        "id": "card_houses",
                        "component": "houses",
                        "title": "Houses & Courtyards",
                        "icon": "🏡",
                        "rule_text": "Strong baked-brick houses with doors opening into quiet side lanes."
                    },
                    {
                        "id": "card_roads",
                        "component": "roads",
                        "title": "Main Grid Roads",
                        "icon": "🛣️",
                        "rule_text": "Wide, straight avenues running North-South and East-West with rounded corners for carts."
                    },
                    {
                        "id": "card_drainage",
                        "component": "drainage",
                        "title": "Covered Brick Drains",
                        "icon": "🚰",
                        "rule_text": "Underground brick channels covered with stone slabs so streets stay clean and odor-free."
                    },
                    {
                        "id": "card_public_areas",
                        "component": "public_areas",
                        "title": "Citadel & Public Spaces",
                        "icon": "🏛️",
                        "rule_text": "The high ground of the city with the Great Bath, community hall, and big granaries."
                    }
                ]
            },
            "hints": [
                "💡 Harappan homes were peaceful: doors opened into quiet side lanes, not dusty main streets!",
                "💡 The Citadel was always raised on high ground on the western side of the city."
            ]
        },
        "solution": {
            "slot_houses": "card_houses",
            "slot_roads": "card_roads",
            "slot_drainage": "card_drainage",
            "slot_public_areas": "card_public_areas"
        },
        "reward_xp": 300,
        "reward_tokens": 8,
        "artifact_reward": {
            "id": "art_city_blueprint",
            "name": "Ancient Measuring Ruler",
            "icon": "📏",
            "material": "Bronze & Sea Shell",
            "origin": "Mohenjo-daro & Lothal",
            "importance": "A precise measuring stick showing that ancient builders used exact measurements across all their cities!"
        },
        "badge_reward": "badge_city_planner"
    },

    "quest_02_lost_artifact": {
        "quest_id": "quest_02_lost_artifact",
        "title": "Find the Lost Artifact",
        "civilization_id": "ivc",
        "story_context": "An ancient object was just dug up! Read the 3 clues and pick the right artifact from the choices.",
        "location": "Artisan Quarter & Citadel Ruins",
        "objective": "Read 3 clues and pick the correct lost Indus Valley artifact.",
        "difficulty": "Intermediate",
        "learning_concept": "Pottery, Seals & Material Detective: Find the lost artifact using forensic clues!",
        "npc_name": "Rao, Chief Archaeologist",
        "npc_avatar": "🏺",
        "challenge": {
            "type": "artifact_detective",
            "instructions": "Read the 3 clues below and click the matching artifact!",
            "interactive_data": {
                "clues": [
                    {
                        "id": "clue_1",
                        "category": "Material",
                        "icon": "🪨",
                        "text": "Made of soft soapstone (steatite) baked in a hot kiln until it turned shiny white."
                    },
                    {
                        "id": "clue_2",
                        "category": "Picture",
                        "icon": "🎨",
                        "text": "Shows a magical one-horned animal (unicorn) standing in front of a small incense burner."
                    },
                    {
                        "id": "clue_3",
                        "category": "Writing & Purpose",
                        "icon": "📜",
                        "text": "Has 5 ancient script symbols. Traders stamped it into wet clay to seal goods sent on ships!"
                    }
                ],
                "candidates": [
                    {
                        "id": "cand_unicorn_seal",
                        "name": "Steatite Unicorn Stamp Seal",
                        "icon": "🦄",
                        "material": "High-fired Steatite (Soapstone)",
                        "origin": "Mohenjo-daro Lower Town",
                        "summary": "Square soapstone seal with a mythical unicorn and ancient script.",
                        "is_correct": True
                    },
                    {
                        "id": "cand_dancing_girl",
                        "name": "Bronze Dancing Girl Statuette",
                        "icon": "💃",
                        "material": "Lost-wax Cast Copper-Tin Bronze",
                        "origin": "Mohenjo-daro HR Area",
                        "summary": "Famous small bronze statue of a confident girl wearing shell bangles.",
                        "is_correct": False
                    },
                    {
                        "id": "cand_storage_jar",
                        "name": "Red-and-Black Painted Storage Jar",
                        "icon": "🏺",
                        "material": "Fine Levigated Alluvial Clay",
                        "origin": "Harappa Granary Complex",
                        "summary": "Large ceramic grain container with painted peacocks and patterns.",
                        "is_correct": False
                    },
                    {
                        "id": "cand_mother_goddess",
                        "name": "Terracotta Clay Figurine",
                        "icon": "🗿",
                        "material": "Hand-modeled Fired Terracotta",
                        "origin": "Mohenjo-daro DK Area",
                        "summary": "Handmade clay statue with a fan-shaped headdress and clay necklaces.",
                        "is_correct": False
                    }
                ]
            },
            "hints": [
                "💡 Soapstone is very soft and easy to carve, making it perfect for detailed seals.",
                "💡 Over half of all Harappan seals depict the famous one-horned unicorn figure!"
            ]
        },
        "solution": {
            "selected_candidate": "cand_unicorn_seal"
        },
        "reward_xp": 320,
        "reward_tokens": 8,
        "artifact_reward": {
            "id": "art_unicorn_seal",
            "name": "Steatite Unicorn Stamp Seal",
            "icon": "🦄",
            "material": "Steatite (Soapstone)",
            "origin": "Mohenjo-daro",
            "importance": "Used by ancient merchants like a company logo or signature stamp on clay packages!"
        },
        "badge_reward": "badge_script_decoder"
    },

    "quest_03_drainage_challenge": {
        "quest_id": "quest_03_drainage_challenge",
        "title": "Save the City from Dirty Water",
        "civilization_id": "ivc",
        "story_context": "Mohenjo-daro had the world's first covered drains! Put the 4 steps of the water system in the right order to keep the city clean.",
        "location": "Lower Town Street Drainage Grid",
        "objective": "Put the 4 steps of the water drainage system in order from home bathroom to outside the city.",
        "difficulty": "Intermediate",
        "learning_concept": "Sanitation, City Hydraulic Engineering & Public Health: Keep the city clean and healthy!",
        "npc_name": "Rao, Chief Sanitary Engineer",
        "npc_avatar": "🚰",
        "challenge": {
            "type": "drainage_flow",
            "instructions": "Put these 4 steps in order (1 to 4) to show how wastewater flowed safely out of the city.",
            "interactive_data": {
                "steps": [
                    {
                        "id": "step_bath",
                        "title": "1. Home Paved Bathroom",
                        "icon": "🚿",
                        "description": "Slanted brick bathroom floor collects wash water and sends it into a clay pipe in the wall.",
                        "correct_order": 1
                    },
                    {
                        "id": "step_sump",
                        "title": "2. Sump Pot (Dirt Trap)",
                        "icon": "🏺",
                        "description": "Water falls into a big jar where sand and dirt sink to the bottom so drains don't get clogged.",
                        "correct_order": 2
                    },
                    {
                        "id": "step_sewer",
                        "title": "3. Covered Street Drain",
                        "icon": "🧱",
                        "description": "Clean water flows smoothly into the covered brick street drain beneath flat stone lids.",
                        "correct_order": 3
                    },
                    {
                        "id": "step_outflow",
                        "title": "4. Soak Pit Outside City",
                        "icon": "🌊",
                        "description": "The street drain flows under the city wall into a soak pit safely away from homes.",
                        "correct_order": 4
                    }
                ]
            },
            "hints": [
                "💡 Water was always cleaned in private sump jars first so dirt wouldn't clog the street drains!",
                "💡 Flat stone covers let city workers easily clean the drains without digging up the street."
            ]
        },
        "solution": {
            "ordered_ids": ["step_bath", "step_sump", "step_sewer", "step_outflow"]
        },
        "reward_xp": 350,
        "reward_tokens": 10,
        "artifact_reward": {
            "id": "art_drain_pipe",
            "name": "Terracotta Drain Pipe",
            "icon": "🚰",
            "material": "High-fired Ceramic Terracotta",
            "origin": "Mohenjo-daro HR Area",
            "importance": "Interlocking clay drain pipes that kept ancient Indus cities cleaner than most cities 3,000 years later!"
        },
        "badge_reward": "badge_sanitation_master"
    },

    "quest_04_ancient_trade": {
        "quest_id": "quest_04_ancient_trade",
        "title": "Ancient Trade: Travel & Trade",
        "civilization_id": "ivc",
        "story_context": "Ships have arrived at the ancient port of Lothal! Connect each trade item (beads, gemstones, copper, shells) to where it came from or where it is going.",
        "location": "Lothal Tidal Dockyard & Marketplace",
        "objective": "Match each trade item to its source region or overseas trade partner.",
        "difficulty": "Intermediate",
        "learning_concept": "Bronze Age Trade Routes, Economic Life & Metrology: Travel and trade precious goods across the world!",
        "npc_name": "Kanha, Lothal Port Master",
        "npc_avatar": "⛵",
        "challenge": {
            "type": "trade_network",
            "instructions": "Match each of the 4 precious trade items to the place it came from or sailed to.",
            "interactive_data": {
                "commodities": [
                    {
                        "id": "com_carnelian",
                        "name": "Carnelian Beads & Soft Cotton",
                        "icon": "📿",
                        "desc": "Red shiny stone beads and fine woven cotton fabrics."
                    },
                    {
                        "id": "com_lapis",
                        "name": "Lapis Lazuli (Deep Blue Gem)",
                        "icon": "💎",
                        "desc": "Rich blue gemstone speckled with gold, found high in mountain mines."
                    },
                    {
                        "id": "com_copper",
                        "name": "Copper Ingots & Bronze",
                        "icon": "⛏️",
                        "desc": "Red copper metal used for strong tools, pots, and statues."
                    },
                    {
                        "id": "com_shell",
                        "name": "White Sea Shell Bangles",
                        "icon": "🐚",
                        "desc": "Bright white conch shells carved into beautiful bangles and spoons."
                    }
                ],
                "destinations": [
                    {
                        "id": "dest_mesopotamia",
                        "name": "Ancient Mesopotamia (Modern Iraq)",
                        "icon": "🏛️",
                        "distance": "Over 2,500 km across the sea in sailing boats"
                    },
                    {
                        "id": "dest_badakhshan",
                        "name": "Shortugai Outpost (Northern Afghanistan)",
                        "icon": "🏔️",
                        "distance": "Northern mountain trade post along the river"
                    },
                    {
                        "id": "dest_khetri",
                        "name": "Khetri Mines (Rajasthan)",
                        "icon": "⛰️",
                        "distance": "Desert trade route rich in copper metal"
                    },
                    {
                        "id": "dest_gulf_khambhat",
                        "name": "Lothal Port & Gujarat Coast",
                        "icon": "🌊",
                        "distance": "Sunny coastal waters full of sea shells"
                    }
                ]
            },
            "hints": [
                "💡 Ancient Mesopotamian clay tablets talk about trading with 'Meluhha' (the Indus Valley) for red beads and timber!",
                "💡 Shortugai was built right next to the famous blue lapis lazuli mountain mines."
            ]
        },
        "solution": {
            "com_carnelian": "dest_mesopotamia",
            "com_lapis": "dest_badakhshan",
            "com_copper": "dest_khetri",
            "com_shell": "dest_gulf_khambhat"
        },
        "reward_xp": 340,
        "reward_tokens": 9,
        "artifact_reward": {
            "id": "art_chert_weights",
            "name": "Standard Cubical Stone Weights",
            "icon": "⚖️",
            "material": "Polished Grey Chert Stone",
            "origin": "Lothal & Harappa",
            "importance": "Exact balance weights used by merchants so no buyer or seller was ever cheated!"
        },
        "badge_reward": "badge_trade_magnate"
    },

    "quest_05_life_in_ivc": {
        "quest_id": "quest_05_life_in_ivc",
        "title": "Life in the Indus Valley",
        "civilization_id": "ivc",
        "story_context": "Spend a day in ancient Mohenjo-daro! Choose what to eat, what craft to learn, and how neighbors solve problems peacefully.",
        "location": "Residential Courtyards, Bazaars & Fields",
        "objective": "Make 3 choices to experience authentic food, crafts, and community peace in Mohenjo-daro.",
        "difficulty": "Advanced",
        "learning_concept": "Daily Life, Crafts, Nutrition & Social Harmony: Discover how everyday Harappans lived!",
        "npc_name": "Meera, Mohenjo-daro Resident",
        "npc_avatar": "👩‍🌾",
        "challenge": {
            "type": "daily_life_simulation",
            "instructions": "Guide your young explorer through 3 everyday situations in Mohenjo-daro.",
            "interactive_data": {
                "scenarios": [
                    {
                        "id": "scenario_1",
                        "title": "Scenario 1: Breakfast Time",
                        "icon": "🥣",
                        "prompt": "You wake up in your courtyard home as roosters crow. What healthy breakfast is your family cooking?",
                        "options": [
                            {
                                "id": "opt_1_correct",
                                "text": "Barley flatbread with lentil curry, roasted sesame paste, and sweet dates.",
                                "is_correct": True,
                                "explanation": "Great choice! Barley, wheat, lentils, sesame, and dates were real everyday foods in Harappa."
                            },
                            {
                                "id": "opt_1_wrong_a",
                                "text": "Boiled potatoes and sweet corn with spicy red chillies.",
                                "is_correct": False,
                                "explanation": "Not yet! Potatoes, corn, and chillies came from the Americas thousands of years later."
                            },
                            {
                                "id": "opt_1_wrong_b",
                                "text": "Wheat noodles tossed in sweet soy sauce.",
                                "is_correct": False,
                                "explanation": "Noodles and soy sauce were not eaten in the ancient Indus Valley!"
                            }
                        ]
                    },
                    {
                        "id": "scenario_2",
                        "title": "Scenario 2: The Workshop",
                        "icon": "⚒️",
                        "prompt": "You walk down the brick street to your afternoon craft workshop. What world-famous craft are you practicing?",
                        "options": [
                            {
                                "id": "opt_2_correct",
                                "text": "Drilling tiny holes through red carnelian gemstone beads using hard stone drills.",
                                "is_correct": True,
                                "explanation": "Spot on! Indus bead-makers were the finest in the world, exporting shiny beads everywhere."
                            },
                            {
                                "id": "opt_2_wrong_a",
                                "text": "Melting iron in blast furnaces to make knight armor and big swords.",
                                "is_correct": False,
                                "explanation": "The Indus Valley was in the Bronze Age — iron tools were invented over 1,000 years later!"
                            },
                            {
                                "id": "opt_2_wrong_b",
                                "text": "Blowing fancy glass cups and carving Greek marble pillars.",
                                "is_correct": False,
                                "explanation": "Blowing glass and marble pillars belong to ancient Rome and Greece, not Harappa."
                            }
                        ]
                    },
                    {
                        "id": "scenario_3",
                        "title": "Scenario 3: Peaceful Neighborhood",
                        "icon": "⚖️",
                        "prompt": "Two ox-cart drivers disagree about parking on First Street. With no kings or soldiers around, how do they fix it?",
                        "options": [
                            {
                                "id": "opt_3_correct",
                                "text": "Neighborhood elders help them talk it out and check the town rules peacefully.",
                                "is_correct": True,
                                "explanation": "Exactly right! Indus cities had no kings or armies — people cooperated peacefully through community rules."
                            },
                            {
                                "id": "opt_3_wrong_a",
                                "text": "The king's royal soldiers throw them both in the palace dungeon.",
                                "is_correct": False,
                                "explanation": "Indus cities had no kings, royal palaces, or armies!"
                            },
                            {
                                "id": "opt_3_wrong_b",
                                "text": "They fight with swords in front of a cheering crowd.",
                                "is_correct": False,
                                "explanation": "Indus people lived peacefully; gladiators were from ancient Rome!"
                            }
                        ]
                    }
                ]
            },
            "hints": [
                "💡 The Indus civilization had no palaces, no royal crowns, and no armies — people worked together peacefully!",
                "💡 Wheat, barley, lentils, sesame, and sweet dates were Harappan favorites!"
            ]
        },
        "solution": {
            "scenario_1": "opt_1_correct",
            "scenario_2": "opt_2_correct",
            "scenario_3": "opt_3_correct"
        },
        "reward_xp": 360,
        "reward_tokens": 10,
        "artifact_reward": {
            "id": "art_toy_cart",
            "name": "Terracotta Toy Bullock Cart",
            "icon": "🪅",
            "material": "Kiln-fired Terracotta Clay",
            "origin": "Harappa & Mohenjo-daro",
            "importance": "A fun clay toy with wheels that rolled on wooden axles, showing that ancient children loved playing with toy cars!"
        },
        "badge_reward": "badge_metropolis_sage"
    }
}

@router.get("", response_model=List[QuestSummary])
def list_quests(
    civilization_id: str = Query("ivc", description="Civilization ID (e.g. ivc, vedic, maurya)"),
    username: Optional[str] = Query(None, description="Optional player username to check completion status")
):
    """
    List all available quests for the selected civilization.
    Supports user completion status check from MongoDB.
    """
    db = db_manager.get_db()
    completed_quest_ids = set()
    
    if username:
        clean_user = username.strip()
        user = db["users"].find_one({"username": {"$regex": f"^{clean_user}$", "$options": "i"}})
        if user and "stats" in user:
            completed_quest_ids = set(user["stats"].get("completed_quests", []))

    results = []
    for q_id, q_data in QUESTS_CATALOG.items():
        if civilization_id and q_data.get("civilization_id") != civilization_id:
            continue
            
        summary = QuestSummary(
            quest_id=q_data["quest_id"],
            title=q_data["title"],
            civilization_id=q_data["civilization_id"],
            story_context=q_data["story_context"],
            location=q_data["location"],
            objective=q_data["objective"],
            difficulty=q_data["difficulty"],
            learning_concept=q_data["learning_concept"],
            npc_name=q_data["npc_name"],
            npc_avatar=q_data["npc_avatar"],
            reward_xp=q_data["reward_xp"],
            reward_tokens=q_data["reward_tokens"],
            artifact_reward=ArtifactReward(**q_data["artifact_reward"]) if q_data.get("artifact_reward") else None,
            badge_reward=q_data.get("badge_reward"),
            completed=(q_id in completed_quest_ids)
        )
        results.append(summary)

    return results

@router.get("/{quest_id}")
def get_quest_detail(quest_id: str):
    """
    Fetch complete quest details and interactive challenge payload for execution.
    """
    if quest_id not in QUESTS_CATALOG:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quest '{quest_id}' not found in Anveshika catalog."
        )
    
    quest = QUESTS_CATALOG[quest_id].copy()
    safe_quest = {k: v for k, v in quest.items() if k != "solution"}
    return safe_quest

@router.post("/{quest_id}/submit", response_model=QuestSubmitResponse)
def submit_quest_solution(quest_id: str, payload: QuestSubmitRequest):
    """
    Validate player's quest challenge solution, award XP/Seals,
    unlock artifacts & badges, and persist all progress directly into MongoDB / state.
    """
    if quest_id not in QUESTS_CATALOG:
        raise HTTPException(status_code=404, detail=f"Quest '{quest_id}' not found.")
        
    quest = QUESTS_CATALOG[quest_id]
    submission = payload.submission
    db = db_manager.get_db()
    
    clean_user = (payload.username or "Arjun").strip()
    user = db["users"].find_one({"username": {"$regex": f"^{clean_user}$", "$options": "i"}})
    if not user:
        user = db_manager.ensure_user(clean_user)

    stats = user.get("stats", {})
    already_completed = quest_id in stats.get("completed_quests", [])

    # Solution Validation
    expected_solution = quest["solution"]
    is_correct = False
    feedback = ""

    qtype = quest["challenge"]["type"]

    if qtype == "rebuild_city":
        # Check mapping of all 4 slots
        is_correct = True
        for slot_k, exp_card in expected_solution.items():
            if submission.get(slot_k) != exp_card:
                is_correct = False
                break
        if is_correct:
            feedback = "Masterful civic zoning! You correctly arranged Houses, Roads, Drainage, and Public Areas following the 1:2:4 Harappan grid plan."
        else:
            feedback = "Some urban components were misplaced. Verify that residential houses stay on side lanes and public areas remain on the elevated Citadel mound."

    elif qtype == "artifact_detective":
        selected = submission.get("selected_candidate")
        if selected == expected_solution.get("selected_candidate"):
            is_correct = True
            feedback = "Archaeological deduction verified! The steatite unicorn stamp seal matches all mineralogical and epigraphic clues."
        else:
            feedback = "The selected relic does not match the laboratory clues. Review the steatite talc stone analysis and unicorn intaglio description."

    elif qtype == "drainage_flow":
        submitted_order = submission.get("ordered_ids", [])
        if submitted_order == expected_solution.get("ordered_ids"):
            is_correct = True
            feedback = "Perfect hydraulic sequence! Wastewater flows seamlessly from domestic bathroom to soak jar, street sewer, and suburban culvert."
        else:
            feedback = "The drainage pipeline is interrupted. Water must be pre-filtered in courtyard soak jars before entering covered municipal sewers."

    elif qtype == "trade_network":
        is_correct = True
        for com_k, exp_dest in expected_solution.items():
            if submission.get(com_k) != exp_dest:
                is_correct = False
                break
        if is_correct:
            feedback = "Maritime trade routes confirmed! Carnelian reached Mesopotamia, lapis from Badakhshan, copper from Khetri, and shells from Gujarat."
        else:
            feedback = "Some trade routes were misaligned. Review the source of lapis lazuli in the northern colonies and carnelian exports to Sumer."

    elif qtype == "daily_life_simulation":
        is_correct = True
        for sc_k, exp_opt in expected_solution.items():
            if submission.get(sc_k) != exp_opt:
                is_correct = False
                break
        if is_correct:
            feedback = "Exceptional historical immersion! You chose the authentic barley diet, carnelian beadcraft, and peaceful consensus governance of the Indus Valley."
        else:
            feedback = "One or more daily life decisions did not reflect authentic Bronze Age Indus Valley realities. Remember that IVC lacked iron, monarchs, and New World crops."

    # Record attempt telemetry for Phase 9 ML Personalization
    history_entry = {
        "quest_id": quest_id,
        "is_correct": is_correct,
        "time_taken_seconds": getattr(payload, "time_taken_seconds", 30.0) or 30.0,
        "attempts_count": getattr(payload, "attempts_count", 1) or 1,
        "hints_used": getattr(payload, "hints_used", 0) or 0,
        "difficulty": quest.get("difficulty", "Intermediate"),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    stats.setdefault("quest_history", []).append(history_entry)

    if not is_correct:
        db["users"].update_one({"_id": user["_id"]}, {"$set": {"stats": stats}})
        db_manager.save_state()
        return QuestSubmitResponse(
            success=False,
            is_correct=False,
            feedback=feedback,
            quest_id=quest_id,
            completed_quests_count=len(stats.get("completed_quests", []))
        )

    # If correct: Award rewards and persist in MongoDB
    xp_to_award = 0 if already_completed else quest["reward_xp"]
    tokens_to_award = 0 if already_completed else quest["reward_tokens"]
    
    if not already_completed:
        stats["xp"] = stats.get("xp", 0) + xp_to_award
        stats["seal_tokens"] = stats.get("seal_tokens", 0) + tokens_to_award
        stats.setdefault("completed_quests", []).append(quest_id)
        
        badge_reward = quest.get("badge_reward")
        if badge_reward and badge_reward not in stats.get("badges", []):
            stats.setdefault("badges", []).append(badge_reward)
            
        art_reward = quest.get("artifact_reward")
        if art_reward and art_reward["id"] not in stats.get("discovered_artifacts", []):
            stats.setdefault("discovered_artifacts", []).append(art_reward["id"])
            
    db["users"].update_one({"_id": user["_id"]}, {"$set": {"stats": stats}})
    db_manager.save_state()
    user["stats"] = stats

    artifact_obj = ArtifactReward(**quest["artifact_reward"]) if quest.get("artifact_reward") else None

    return QuestSubmitResponse(
        success=True,
        is_correct=True,
        feedback=feedback + (" (Rewards already claimed previously)" if already_completed else " 🎉 Rewards granted and saved to MongoDB!"),
        xp_awarded=xp_to_award,
        tokens_awarded=tokens_to_award,
        quest_id=quest_id,
        artifact_unlocked=artifact_obj if not already_completed else None,
        badge_unlocked=quest.get("badge_reward") if not already_completed else None,
        completed_quests_count=len(stats.get("completed_quests", []))
    )
