from fastapi import APIRouter, HTTPException, Query, status
from typing import List, Optional, Dict, Any
from backend.app.database import db_manager
from backend.app.models.artifact import (
    ArtifactModel,
    ArtifactDiscoverRequest,
    ArtifactDiscoverResponse
)
from datetime import datetime

router = APIRouter(prefix="/museum", tags=["Living Virtual Museum"])

ARTIFACTS_CATALOG: Dict[str, Dict[str, Any]] = {
    "art_unicorn_seal": {
        "artifact_id": "art_unicorn_seal",
        "name": "Steatite Unicorn Stamp Seal",
        "category": "seal",
        "category_label": "Indus Valley Seal",
        "civilization_id": "ivc",
        "period": "c. 2600–1900 BCE (Mature Harappan Phase)",
        "region": "Lower Indus Basin (Sindh)",
        "site": "Mohenjo-daro (DK Area)",
        "material": "High-fired Steatite (Soapstone) with White Alkali Glaze",
        "dimensions": "2.9 × 2.9 × 0.8 cm",
        "possible_purpose": "Used by merchant guilds and civic administrators to impress wet clay tags (bullae) around wrapped trade bales destined for Mesopotamian ports.",
        "historical_significance": "The intaglio carving showcases world-class Bronze Age lapidary artistry and preserves 5 pictographic script symbols running from right to left.",
        "interesting_fact": "Over 65% of all recovered Indus stamp seals depict this mythical single-horned quadruped standing before a sacred ritual brazier.",
        "icon": "🦄",
        "svg_type": "seal_unicorn",
        "xp_reward": 80
    },
    "art_painted_pottery": {
        "artifact_id": "art_painted_pottery",
        "name": "Black-on-Red Painted Storage Urn",
        "category": "pottery",
        "category_label": "Ceramics & Pottery",
        "civilization_id": "ivc",
        "period": "c. 2500–1900 BCE",
        "region": "Punjab & Saraswati Basin",
        "site": "Harappa (Mound AB)",
        "material": "Fine levigated alluvial clay, red slip, manganese black pigment",
        "dimensions": "58 cm height, 38 cm diameter",
        "possible_purpose": "Storing grain reserves, sesame oils, and fermented beverages in domestic courtyards and municipal storehouses.",
        "historical_significance": "Demonstrates sophisticated mastery of the fast pottery wheel and high-temperature kiln firing exceeding 1,000°C.",
        "interesting_fact": "Painted with interlocking circular geometry, peacocks, pipal tree leaves, and fish scales, reflecting deep reverence for local ecology.",
        "icon": "🏺",
        "svg_type": "pottery_urn",
        "xp_reward": 75
    },
    "art_mother_goddess": {
        "artifact_id": "art_mother_goddess",
        "name": "Terracotta Mother Goddess Figurine",
        "category": "figurine",
        "category_label": "Terracotta Figurine",
        "civilization_id": "ivc",
        "period": "c. 2600–2000 BCE",
        "region": "Lower Indus Basin",
        "site": "Mohenjo-daro (HR Area)",
        "material": "Hand-modeled terracotta clay with pinched features and applique ornaments",
        "dimensions": "18.5 × 7.2 × 4.1 cm",
        "possible_purpose": "Domestic household shrine worship and fertility rituals invoking agricultural bounty and maternal protection.",
        "historical_significance": "Offers invaluable insights into Harappan personal spirituality, fan-shaped headdresses, disc earrings, and layered bead necklaces.",
        "interesting_fact": "Traces of carbon soot found in the pannier-shaped side cups suggest they were used as miniature oil lamps during twilight ceremonies.",
        "icon": "🗿",
        "svg_type": "terracotta_goddess",
        "xp_reward": 75
    },
    "art_standard_brick": {
        "artifact_id": "art_standard_brick",
        "name": "Standardized 1:2:4 Fired Mud Brick",
        "category": "brick",
        "category_label": "Civic Masonry & Architecture",
        "civilization_id": "ivc",
        "period": "c. 2600–1900 BCE",
        "region": "Alluvial Plains across Indus Basin",
        "site": "Harappa & Mohenjo-daro",
        "material": "Kiln-fired alluvial clay with straw binder",
        "dimensions": "7 × 14 × 28 cm (Strict 1:2:4 Ratio)",
        "possible_purpose": "Constructing multi-storey residential walls, fortified Citadel revetments, and waterproof sewer drains.",
        "historical_significance": "The universal 1:2:4 mathematical thickness-width-length ratio provided optimal tensile bonding against seismic tremors and floods.",
        "interesting_fact": "Identical brick dimensions have been unearthed at sites over 1,500 kilometers apart—from Shortugai in Afghanistan to Lothal in Gujarat.",
        "icon": "🧱",
        "svg_type": "ancient_brick",
        "xp_reward": 70
    },
    "art_chert_drill": {
        "artifact_id": "art_chert_drill",
        "name": "Constricted Micro-Chert Stone Drill & Bronze Axe",
        "category": "tool",
        "category_label": "Artisan Tools & Metallurgy",
        "civilization_id": "ivc",
        "period": "c. 2500–1800 BCE",
        "region": "Saraswati-Narmada Corridor",
        "site": "Chanhudaro & Lothal Workshops",
        "material": "Ernestite/chert cryptocrystalline quartz & copper-tin bronze",
        "dimensions": "Drill: 3.2 cm length, 1.2 mm tip; Axe: 14.5 cm length",
        "possible_purpose": "Microscopic axial drilling of extremely hard gemstone beads (carnelian, agate) and carpentry timber shaping.",
        "historical_significance": "Ernestite drills were a proprietary Harappan technological breakthrough that astonished the ancient world with drilling precision under 1 mm.",
        "interesting_fact": "A single 6 cm carnelian bead required nearly two full weeks of continuous rotary bow-drilling with these specialized stone micro-bits.",
        "icon": "⛏️",
        "svg_type": "artisan_tool",
        "xp_reward": 75
    },
    "art_carnelian_necklace": {
        "artifact_id": "art_carnelian_necklace",
        "name": "Etched Carnelian Bead Necklace & Bangles",
        "category": "ornament",
        "category_label": "Jewelry & Lapidary Ornaments",
        "civilization_id": "ivc",
        "period": "c. 2500–1900 BCE",
        "region": "Gulf of Khambhat & Sindh",
        "site": "Lothal & Mohenjo-daro",
        "material": "Red carnelian stone, white alkali chemical etching, marine conch shell",
        "dimensions": "Beads ranging from 1.5 to 7.8 cm in length",
        "possible_purpose": "Personal adornment worn by citizens of all genders as markers of civic pride, beauty, and protective talismanic amulets.",
        "historical_significance": "White geometric alkali bleaching on crimson carnelian was a technological trade secret that commanded immense wealth in Mesopotamia.",
        "interesting_fact": "Found buried inside intact terracotta urns beneath courtyard floors, serving as ancient household jewelry safes.",
        "icon": "📿",
        "svg_type": "carnelian_necklace",
        "xp_reward": 80
    },
    "art_chert_weights": {
        "artifact_id": "art_chert_weights",
        "name": "Standardized Cubical Chert Weights & Clay Bulla",
        "category": "trade",
        "category_label": "Trade, Currency & Metrology",
        "civilization_id": "ivc",
        "period": "c. 2600–1900 BCE",
        "region": "Major Commercial Trade Hubs",
        "site": "Lothal & Harappa",
        "material": "Polished banded chert stone & sun-dried clay sealing",
        "dimensions": "Base unit weight: 0.857 grams (binary series 1, 2, 4, 8, 16, 32, 64)",
        "possible_purpose": "Weighing precious metals (gold, copper), lapis lazuli, and agricultural commodities to calculate municipal exchange values.",
        "historical_significance": "Followed a binary metrological progression followed by decimal ratios, standardized with less than 1% variance across the civilization.",
        "interesting_fact": "The 16th unit ratio became the direct historical ancestor of the traditional Indian rupee currency division (1 Rupee = 16 Annas).",
        "icon": "⚖️",
        "svg_type": "trade_weights",
        "xp_reward": 85
    },
    "art_dancing_girl": {
        "artifact_id": "art_dancing_girl",
        "name": "The Bronze Dancing Girl",
        "category": "figurine",
        "category_label": "Bronze Metallurgy Masterpiece",
        "civilization_id": "ivc",
        "period": "c. 2300–1750 BCE",
        "region": "Lower Indus Basin",
        "site": "Mohenjo-daro (HR Area)",
        "material": "Copper-tin bronze alloy (Lost-wax casting technique)",
        "dimensions": "10.5 cm height, 5 cm width",
        "possible_purpose": "Artistic appreciation, cultural dance commemoration, or personal keepsake of an adolescent performing artist.",
        "historical_significance": "The world's earliest masterpiece of cire-perdue (lost-wax casting), capturing dynamic naturalism, confidence, and anatomical grace.",
        "interesting_fact": "Her left arm is heavily adorned with 24-25 bangles right up to the shoulder, while her right arm wears only four at the wrist and elbow.",
        "icon": "💃",
        "svg_type": "dancing_girl",
        "xp_reward": 90
    }
}

@router.get("/artifacts", response_model=List[ArtifactModel])
def get_museum_artifacts(
    username: Optional[str] = Query(None, description="Player username to check discovery status"),
    civilization_id: str = Query("ivc", description="Civilization ID")
):
    """
    List all cataloged museum artifacts, enriched with the user's discovery status from MongoDB.
    """
    db = db_manager.get_db()
    discovered_ids = set()

    if username:
        clean_user = username.strip()
        user = db["users"].find_one({"username": {"$regex": f"^{clean_user}$", "$options": "i"}})
        if user and "stats" in user:
            discovered_ids = set(user["stats"].get("discovered_artifacts", []))

    results = []
    for art_id, art_data in ARTIFACTS_CATALOG.items():
        if civilization_id and art_data.get("civilization_id") != civilization_id:
            continue
        
        is_discovered = art_id in discovered_ids
        item = ArtifactModel(
            artifact_id=art_data["artifact_id"],
            name=art_data["name"],
            category=art_data["category"],
            category_label=art_data["category_label"],
            civilization_id=art_data["civilization_id"],
            period=art_data["period"],
            region=art_data["region"],
            site=art_data["site"],
            material=art_data["material"],
            dimensions=art_data["dimensions"],
            possible_purpose=art_data["possible_purpose"],
            historical_significance=art_data["historical_significance"],
            interesting_fact=art_data["interesting_fact"],
            icon=art_data["icon"],
            svg_type=art_data["svg_type"],
            xp_reward=art_data["xp_reward"],
            discovered=is_discovered
        )
        results.append(item)

    return results

@router.get("/artifacts/{artifact_id}", response_model=ArtifactModel)
def get_artifact_detail(
    artifact_id: str,
    username: Optional[str] = Query(None)
):
    """
    Retrieve full curation details of a specific artifact.
    """
    if artifact_id not in ARTIFACTS_CATALOG:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Artifact '{artifact_id}' was not found in Anveshika catalog."
        )
    
    art_data = ARTIFACTS_CATALOG[artifact_id]
    db = db_manager.get_db()
    is_discovered = False

    if username:
        clean_user = username.strip()
        user = db["users"].find_one({"username": {"$regex": f"^{clean_user}$", "$options": "i"}})
        if user and "stats" in user:
            is_discovered = artifact_id in user["stats"].get("discovered_artifacts", [])

    return ArtifactModel(
        **art_data,
        discovered=is_discovered
    )

@router.post("/discover/{artifact_id}", response_model=ArtifactDiscoverResponse)
def discover_artifact(artifact_id: str, payload: ArtifactDiscoverRequest):
    """
    Discover an artifact:
    1. Check if already discovered (prevent duplicate rewards).
    2. If new: award XP, add to player profile, and unlock in museum.
    """
    if artifact_id not in ARTIFACTS_CATALOG:
        raise HTTPException(status_code=404, detail=f"Artifact '{artifact_id}' not found.")

    art_data = ARTIFACTS_CATALOG[artifact_id]
    db = db_manager.get_db()
    
    clean_user = (payload.username or "Arjun").strip()
    user = db["users"].find_one({"username": {"$regex": f"^{clean_user}$", "$options": "i"}})
    if not user:
        user = db_manager.ensure_user(clean_user)

    stats = user.get("stats", {})
    discovered_list = stats.get("discovered_artifacts", [])

    # Check for duplicate
    if artifact_id in discovered_list:
        art_model = ArtifactModel(**art_data, discovered=True)
        return ArtifactDiscoverResponse(
            success=True,
            is_new=False,
            message=f"'{art_data['name']}' is already documented in your Virtual Museum gallery.",
            xp_awarded=0,
            artifact=art_model,
            total_discovered=len(discovered_list),
            collection_size=len(ARTIFACTS_CATALOG)
        )

    # New Discovery: Award XP & Save to State
    xp_to_award = art_data.get("xp_reward", 75)
    tokens_to_award = 5
    stats["xp"] = stats.get("xp", 0) + xp_to_award
    stats["seal_tokens"] = stats.get("seal_tokens", 0) + tokens_to_award
    discovered_list.append(artifact_id)
    stats["discovered_artifacts"] = discovered_list

    db["users"].update_one({"_id": user["_id"]}, {"$set": {"stats": stats}})
    db_manager.save_state()

    art_model = ArtifactModel(**art_data, discovered=True)
    return ArtifactDiscoverResponse(
        success=True,
        is_new=True,
        message=f"🌟 New Relic Excavated: '{art_data['name']}' added to your Living Virtual Museum!",
        xp_awarded=xp_to_award,
        artifact=art_model,
        total_discovered=len(discovered_list),
        collection_size=len(ARTIFACTS_CATALOG)
    )
