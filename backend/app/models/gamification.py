from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class BadgeModel(BaseModel):
    id: str
    name: str
    description: str
    icon: str
    category: str
    criteria: str
    unlocked: bool = False
    progress_current: Optional[int] = None
    progress_target: Optional[int] = None

class LevelTier(BaseModel):
    level: int
    title: str
    min_xp: int
    max_xp: int
    unlocked_perks: List[str]
    description: str

ALL_BADGES: List[Dict[str, Any]] = [
    {
        "id": "badge_apprentice_excavator",
        "name": "Apprentice of Mohenjo-daro",
        "description": "Entered the Indus Valley and earned initial excavation clearance.",
        "icon": "⛏️",
        "category": "Exploration",
        "criteria": "Register player profile & enter Indus Valley"
    },
    {
        "id": "badge_artifact_hunter",
        "name": "Artifact Hunter",
        "description": "Excavated and cataloged at least 4 unique Indus Valley relics in the Virtual Museum.",
        "icon": "🏺",
        "category": "Archaeology",
        "criteria": "Discover 4 or more unique artifacts"
    },
    {
        "id": "badge_master_planner",
        "name": "Master Planner",
        "description": "Mastered the orthogonal grid planning, cardinal alignment, and 1:2:4 brick ratios.",
        "icon": "📐",
        "category": "Urban Planning",
        "criteria": "Solve Quest 1 (Rebuild Ancient City) or survey main avenues"
    },
    {
        "id": "badge_heritage_explorer",
        "name": "Heritage Explorer",
        "description": "Surveyed all 7 core excavated archaeological sectors of the Harappan Metropolis.",
        "icon": "🧭",
        "category": "Exploration",
        "criteria": "Explore all 7 ancient city sectors"
    },
    {
        "id": "badge_indus_expert",
        "name": "Indus Valley Expert",
        "description": "Attained Level 3+, solved 3+ quests, collected 5+ relics, and explored all sectors.",
        "icon": "👑",
        "category": "Mastery",
        "criteria": "Level 3+, 3+ quests, 5+ relics, all 7 sectors explored"
    },
    {
        "id": "badge_sanitation_master",
        "name": "Harappan Hydraulic Engineer",
        "description": "Mastered the corbelled sewer networks, soak pits, and municipal drains.",
        "icon": "🚰",
        "category": "Engineering",
        "criteria": "Complete Quest 3 (The Drainage Challenge)"
    },
    {
        "id": "badge_seal_master",
        "name": "Indus Epigraphist & Scribe",
        "description": "Forensically identified steatite unicorn stamp seals and maritime bullae.",
        "icon": "🦏",
        "category": "Language & Epigraphy",
        "criteria": "Complete Quest 2 (The Lost Artifact)"
    },
    {
        "id": "badge_dockyard_trader",
        "name": "Lothal Maritime Merchant",
        "description": "Balanced standardized binary chert weights and maritime trade routes.",
        "icon": "⛵",
        "category": "Trade & Commerce",
        "criteria": "Complete Quest 4 (Ancient Trade)"
    },
    {
        "id": "badge_bronze_founder",
        "name": "Lost-Wax Metallurgist",
        "description": "Discovered the metallurgy secrets behind the Dancing Girl bronze sculpture.",
        "icon": "🔥",
        "category": "Crafts & Metallurgy",
        "criteria": "Discover Dancing Girl relic or inspect Craft Workshop"
    },
    {
        "id": "badge_great_bath_priest",
        "name": "Citadel Guardian",
        "description": "Inspected the natural bitumen waterproofing and sacred steps of the Great Bath.",
        "icon": "🌊",
        "category": "Architecture",
        "criteria": "Explore the Great Bath sector"
    },
    {
        "id": "badge_granary_curator",
        "name": "Harappan Agronomist",
        "description": "Analyzed granary ventilation ducts and civic food security systems.",
        "icon": "🌾",
        "category": "Agriculture",
        "criteria": "Explore the Great Granary sector"
    },
    {
        "id": "badge_heritage_sage",
        "name": "Living Heritage Sage",
        "description": "Mastered ancient daily nutrition, peaceful consensus governance, and reached Level 5.",
        "icon": "🪷",
        "category": "Living History",
        "criteria": "Complete Quest 5 (Life in Indus Valley) and reach Level 5"
    },
    {
        "id": "badge_indus_explorer",
        "name": "Indus Valley Explorer",
        "description": "Grand capstone achievement: Mastered city planning, drainage, architecture, trade, resources, and daily life in the Final Indus Valley Challenge.",
        "icon": "🎖️",
        "category": "Capstone Mastery",
        "criteria": "Complete the Phase 10 Final Indus Valley Civilization Challenge"
    }
]

LEVEL_TIERS: List[Dict[str, Any]] = [
    {
        "level": 1,
        "title": "Apprentice Explorer",
        "min_xp": 0,
        "max_xp": 500,
        "unlocked_perks": [
            "Lower Town Grid & Residential Alleys",
            "Public Museum Vitrines",
            "Introductory Quests (City Planning & Seal Identification)"
        ],
        "description": "Beginning your archaeological journey along the banks of the ancient Sindhu."
    },
    {
        "level": 2,
        "title": "Field Archaeologist",
        "min_xp": 500,
        "max_xp": 1200,
        "unlocked_perks": [
            "Citadel Mound Deep Access (Great Bath & Granary Vaults)",
            "Hydraulic Drainage Challenge (Quest 3)",
            "Lothal Maritime Trade Network (Quest 4)"
        ],
        "description": "Certified in stratigraphy and subterranean masonry excavation."
    },
    {
        "level": 3,
        "title": "Master Surveyor",
        "min_xp": 1200,
        "max_xp": 2200,
        "unlocked_perks": [
            "Life in Indus Valley Simulation Quest (Quest 5)",
            "Curatorial Audio Narration in Virtual Museum",
            "Crafts Quarter Master Artisan Workshops"
        ],
        "description": "Skilled in standard 1:2:4 masonry ratios and binary metrological standards."
    },
    {
        "level": 4,
        "title": "Senior Epigraphist",
        "min_xp": 2200,
        "max_xp": 3500,
        "unlocked_perks": [
            "The Harappan Secret Inscription Chamber",
            "Mohenjo-daro Epigraphic Vault & Dholavira Signboard",
            "Eligibility for Indus Valley Expert Honor"
        ],
        "description": "Distinguished scholar of undeciphered Indus pictographic logograms."
    },
    {
        "level": 5,
        "title": "Living Heritage Sage",
        "min_xp": 3500,
        "max_xp": 5000,
        "unlocked_perks": [
            "Vedic Realm & Saraswati Basin Expansion Sneak Peek",
            "Grand Living Heritage Sage Honor & Golden Halo",
            "Master Curator Hall of Fame Access"
        ],
        "description": "Supreme master of Bronze-Age Bharat urban planning, culture, and archaeology."
    }
]

def compute_level_progress(xp: int) -> Dict[str, Any]:
    level = 1
    for tier in LEVEL_TIERS:
        if xp >= tier["min_xp"]:
            level = tier["level"]
        else:
            break
            
    # Lookup current tier
    tier_idx = min(level - 1, len(LEVEL_TIERS) - 1)
    current_tier = LEVEL_TIERS[tier_idx]
    min_xp = current_tier["min_xp"]
    max_xp = current_tier["max_xp"]
    
    if level >= 5:
        # Cap or scaling top level
        xp_in_level = max(0, xp - min_xp)
        xp_needed_in_level = 1500
        progress_percentage = min(100.0, round((xp_in_level / xp_needed_in_level) * 100.0, 1))
    else:
        xp_in_level = max(0, xp - min_xp)
        xp_needed_in_level = max(1, max_xp - min_xp)
        progress_percentage = min(100.0, round((xp_in_level / xp_needed_in_level) * 100.0, 1))
        
    next_level = level + 1 if level < len(LEVEL_TIERS) else None
    next_title = LEVEL_TIERS[level]["title"] if next_level and level < len(LEVEL_TIERS) else "Maximum Level"
    xp_to_next = max(0, max_xp - xp) if level < 5 else 0

    return {
        "current_level": level,
        "level_title": current_tier["title"],
        "description": current_tier["description"],
        "current_xp": xp,
        "level_min_xp": min_xp,
        "level_max_xp": max_xp,
        "xp_in_level": xp_in_level,
        "xp_needed_in_level": xp_needed_in_level,
        "xp_to_next_level": xp_to_next,
        "next_level": next_level,
        "next_title": next_title,
        "progress_percentage": progress_percentage,
        "unlocked_perks": current_tier["unlocked_perks"]
    }

def compute_overall_progress(stats: dict) -> Dict[str, Any]:
    completed_quests = stats.get("completed_quests", [])
    discovered_artifacts = stats.get("discovered_artifacts", [])
    explored_locations = stats.get("explored_locations", [])
    
    quests_count = len(completed_quests)
    total_quests = 5
    quests_pct = min(1.0, quests_count / total_quests) * 35.0
    
    artifacts_count = len(discovered_artifacts)
    total_artifacts = 8
    artifacts_pct = min(1.0, artifacts_count / total_artifacts) * 35.0
    
    locations_count = len(explored_locations)
    total_locations = 7
    locations_pct = min(1.0, locations_count / total_locations) * 30.0
    
    overall = round(quests_pct + artifacts_pct + locations_pct, 1)
    
    return {
        "overall_percentage": min(100.0, overall),
        "quests": {
            "completed": quests_count,
            "total": total_quests,
            "weight_percentage": round(quests_pct, 1)
        },
        "artifacts": {
            "discovered": artifacts_count,
            "total": total_artifacts,
            "weight_percentage": round(artifacts_pct, 1)
        },
        "locations": {
            "explored": locations_count,
            "total": total_locations,
            "weight_percentage": round(locations_pct, 1)
        }
    }

def evaluate_user_badges(stats: dict) -> List[str]:
    """
    Evaluates player statistics and returns the comprehensive list of earned badge IDs.
    """
    earned = set(stats.get("badges", []))
    
    # Baseline welcome badge
    earned.add("badge_apprentice_excavator")
    
    discovered_artifacts = stats.get("discovered_artifacts", [])
    completed_quests = stats.get("completed_quests", [])
    explored_locations = stats.get("explored_locations", [])
    xp = stats.get("xp", 0)
    level = compute_level_progress(xp)["current_level"]
    
    # 1. Artifact Hunter: Discovered >= 4 unique artifacts
    if len(discovered_artifacts) >= 4:
        earned.add("badge_artifact_hunter")
        
    # 2. Master Planner: Completed quest_01_rebuild_city OR explored avenues & residential area
    if "quest_01_rebuild_city" in completed_quests or ("main_street" in explored_locations and "residential_area" in explored_locations):
        earned.add("badge_master_planner")
        earned.add("badge_city_planner")  # Backwards compatibility
        
    # 3. Heritage Explorer: Explored all 7 core excavated locations
    if len(explored_locations) >= 7:
        earned.add("badge_heritage_explorer")
        
    # 4. Indus Valley Expert: Level >= 3, >= 3 quests, >= 5 artifacts, 7 locations explored
    if level >= 3 and len(completed_quests) >= 3 and len(discovered_artifacts) >= 5 and len(explored_locations) >= 7:
        earned.add("badge_indus_expert")
        
    # Additional specific badges
    if "quest_03_drainage_flow" in completed_quests or "drainage_system" in explored_locations:
        earned.add("badge_sanitation_master")
    if "quest_02_lost_artifact" in completed_quests or "art_unicorn_seal" in discovered_artifacts:
        earned.add("badge_seal_master")
    if "quest_04_trade_network" in completed_quests or "marketplace" in explored_locations:
        earned.add("badge_dockyard_trader")
    if "art_dancing_girl" in discovered_artifacts or "craft_workshop" in explored_locations:
        earned.add("badge_bronze_founder")
    if "great_bath" in explored_locations:
        earned.add("badge_great_bath_priest")
    if "granary_area" in explored_locations:
        earned.add("badge_granary_curator")
    if level >= 5 and "quest_05_daily_life" in completed_quests:
        earned.add("badge_heritage_sage")
        
    return list(earned)

def hydrate_badges(user_badge_ids: List[str], stats: dict = None) -> List[Dict[str, Any]]:
    badges_out = []
    unlocked_set = set(user_badge_ids or [])
    stats = stats or {}
    
    discovered_artifacts = stats.get("discovered_artifacts", [])
    completed_quests = stats.get("completed_quests", [])
    explored_locations = stats.get("explored_locations", [])
    
    for b in ALL_BADGES:
        unlocked = b["id"] in unlocked_set
        progress_curr = None
        progress_target = None
        
        # Calculate specific progress bars for locked badges
        if b["id"] == "badge_artifact_hunter":
            progress_curr = min(4, len(discovered_artifacts))
            progress_target = 4
        elif b["id"] == "badge_heritage_explorer":
            progress_curr = min(7, len(explored_locations))
            progress_target = 7
        elif b["id"] == "badge_indus_expert":
            progress_curr = min(7, len(explored_locations))
            progress_target = 7
            
        badges_out.append({
            "id": b["id"],
            "name": b["name"],
            "description": b["description"],
            "icon": b["icon"],
            "category": b["category"],
            "criteria": b["criteria"],
            "unlocked": unlocked,
            "progress_current": progress_curr,
            "progress_target": progress_target
        })
    return badges_out

def compute_unlocked_content(stats: dict) -> List[Dict[str, Any]]:
    xp = stats.get("xp", 0)
    level = compute_level_progress(xp)["current_level"]
    completed_quests = stats.get("completed_quests", [])
    discovered_artifacts = stats.get("discovered_artifacts", [])
    explored_locations = stats.get("explored_locations", [])
    
    content_list = [
        {
            "id": "unlock_lower_town",
            "title": "Lower Town Grid & Residential Alleys",
            "category": "City Exploration",
            "level_required": 1,
            "unlocked": level >= 1,
            "badge_icon": "🏘️",
            "details": "Explore ancient residential courtyards, 90° avenues, and street niches."
        },
        {
            "id": "unlock_common_vitrines",
            "title": "Public Museum Vitrines",
            "category": "Virtual Museum",
            "level_required": 1,
            "unlocked": level >= 1,
            "badge_icon": "🏺",
            "details": "Access to view discovered Harappan relics in the Virtual Museum rotunda."
        },
        {
            "id": "unlock_citadel_depths",
            "title": "Citadel Mound & The Great Bath",
            "category": "City Exploration",
            "level_required": 2,
            "unlocked": level >= 2,
            "badge_icon": "🌊",
            "details": "Access to the elevated western Citadel, ceremonial bath, and state granary."
        },
        {
            "id": "unlock_advanced_quests",
            "title": "Advanced Engineering Quests",
            "category": "Quests",
            "level_required": 2,
            "unlocked": level >= 2,
            "badge_icon": "📜",
            "details": "Access to Quest 3 (The Drainage Challenge) and Quest 4 (Ancient Trade)."
        },
        {
            "id": "unlock_curatorial_audio",
            "title": "Curatorial Audio Guide Narration",
            "category": "Virtual Museum",
            "level_required": 3,
            "unlocked": level >= 3,
            "badge_icon": "🎙️",
            "details": "Hands-free archaeological voice narration for all discovered relics."
        },
        {
            "id": "unlock_daily_life_quest",
            "title": "Life in the Indus Valley Simulation",
            "category": "Quests",
            "level_required": 3,
            "unlocked": level >= 3,
            "badge_icon": "🌾",
            "details": "Immersion into Harappan daily nutrition, carnelian crafts, and civic peace."
        },
        {
            "id": "unlock_secret_archive",
            "title": "The Harappan Secret Inscription Chamber",
            "category": "Ancient Lore",
            "level_required": 4,
            "unlocked": level >= 4,
            "badge_icon": "📜",
            "details": "Epigraphic vault analyzing the Dholavira Signboard and undeciphered script."
        },
        {
            "id": "unlock_vedic_teaser",
            "title": "Vedic Realm & Saraswati Basin Expansion Sneak Peek",
            "category": "Expansion Realm",
            "level_required": 5,
            "unlocked": level >= 5,
            "badge_icon": "🌅",
            "details": "Exclusive preview of Chapter II: Painted Grey Ware, Vedic Hymns & Iron Metallurgy."
        },
        {
            "id": "unlock_grand_sage",
            "title": "Living Heritage Sage Honor & Golden Halo",
            "category": "Supreme Honor",
            "level_required": 5,
            "unlocked": level >= 5,
            "badge_icon": "🪷",
            "details": "Supreme recognition for mastering ancient Indian heritage and archaeology."
        }
    ]
    return content_list