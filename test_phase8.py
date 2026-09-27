"""
=================================================================
BHARAT QUEST - PHASE 8 VERIFICATION SUITE
Gamification, XP Progression, Badges, Exploration Tracking & MongoDB
=================================================================
"""
import sys
import os

# Set UTF-8 encoding for Windows terminal
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.models.gamification import (
    compute_level_progress,
    compute_overall_progress,
    evaluate_user_badges,
    ALL_BADGES,
    LEVEL_TIERS
)

client = TestClient(app)

def test_xp_and_level_math():
    print("\n--- [TEST 1] XP Math & Level Progression Tiers ---")
    # Level 1
    prog1 = compute_level_progress(250)
    assert prog1["current_level"] == 1
    assert prog1["level_title"] == "Apprentice Explorer"
    assert prog1["progress_percentage"] == 50.0
    print("  [PASS] Level 1 (250 XP): Apprentice Explorer at 50%")

    # Level 2
    prog2 = compute_level_progress(850)
    assert prog2["current_level"] == 2
    assert prog2["level_title"] == "Field Archaeologist"
    assert prog2["xp_to_next_level"] == 350
    print("  [PASS] Level 2 (850 XP): Field Archaeologist at 50% (350 XP to Next)")

    # Level 3
    prog3 = compute_level_progress(1700)
    assert prog3["current_level"] == 3
    assert prog3["level_title"] == "Master Surveyor"
    print("  [PASS] Level 3 (1700 XP): Master Surveyor")

    # Level 4
    prog4 = compute_level_progress(2800)
    assert prog4["current_level"] == 4
    assert prog4["level_title"] == "Senior Epigraphist"
    print("  [PASS] Level 4 (2800 XP): Senior Epigraphist")

    # Level 5
    prog5 = compute_level_progress(4200)
    assert prog5["current_level"] == 5
    assert prog5["level_title"] == "Living Heritage Sage"
    print("  [PASS] Level 5 (4200 XP): Living Heritage Sage")

def test_required_badges_present():
    print("\n--- [TEST 2] Required Badges Catalog Verification ---")
    res = client.get("/api/gamification/badges")
    assert res.status_code == 200
    data = res.json()
    assert data["total_badges"] >= 10
    
    badge_ids = {b["id"]: b["name"] for b in data["badges"]}
    
    # 4 Explicit User-Required Badges
    assert "badge_artifact_hunter" in badge_ids, "Artifact Hunter badge missing!"
    assert "badge_master_planner" in badge_ids, "Master Planner badge missing!"
    assert "badge_heritage_explorer" in badge_ids, "Heritage Explorer badge missing!"
    assert "badge_indus_expert" in badge_ids, "Indus Valley Expert badge missing!"
    
    print(f"  [PASS] Verified 'Artifact Hunter': {badge_ids['badge_artifact_hunter']}")
    print(f"  [PASS] Verified 'Master Planner': {badge_ids['badge_master_planner']}")
    print(f"  [PASS] Verified 'Heritage Explorer': {badge_ids['badge_heritage_explorer']}")
    print(f"  [PASS] Verified 'Indus Valley Expert': {badge_ids['badge_indus_expert']}")
    print(f"  [PASS] Total Badges in Catalog: {data['total_badges']}")

def test_levels_and_milestones_api():
    print("\n--- [TEST 3] Levels & Milestones API ---")
    res = client.get("/api/gamification/levels")
    assert res.status_code == 200
    data = res.json()
    assert data["total_levels"] == 5
    for tier in data["tiers"]:
        assert len(tier["unlocked_perks"]) > 0
        print(f"  [PASS] Level {tier['level']}: {tier['title']} ({len(tier['unlocked_perks'])} Unlocked Perks)")

def test_area_exploration_and_duplicate_prevention():
    print("\n--- [TEST 4] Area Exploration & Duplicate Prevention ---")
    uname = "RaviSurveyor"
    reg_res = client.post("/api/auth/register", json={
        "username": uname,
        "age": 14,
        "avatar": "🧑‍🎓",
        "archetype": "Town Architect",
        "password": "1234"
    })
    assert reg_res.status_code == 200

    # 1. First exploration of Great Bath
    exp1 = client.post("/api/gamification/explore-location", json={
        "username": uname,
        "location_id": "great_bath"
    })
    assert exp1.status_code == 200
    d1 = exp1.json()
    assert d1["is_new"] is True
    assert d1["xp_awarded"] == 75
    assert d1["tokens_awarded"] == 5
    assert d1["explored_count"] == 1
    print(f"  [PASS] First survey of Great Bath: +{d1['xp_awarded']} XP, +{d1['tokens_awarded']} Seals awarded")

    # 2. Duplicate exploration of Great Bath
    exp2 = client.post("/api/gamification/explore-location", json={
        "username": uname,
        "location_id": "great_bath"
    })
    assert exp2.status_code == 200
    d2 = exp2.json()
    assert d2["is_new"] is False
    assert d2["xp_awarded"] == 0
    assert d2["tokens_awarded"] == 0
    print("  [PASS] Duplicate survey prevention: 0 XP awarded on repeat visit")

def test_badge_unlock_evaluation():
    print("\n--- [TEST 5] Dynamic Badge Unlock Evaluation ---")
    uname = "KavyaMaster"
    client.post("/api/auth/register", json={
        "username": uname,
        "age": 15,
        "avatar": "🏛️",
        "archetype": "Master Planner",
        "password": "1234"
    })

    # Explore all 7 sectors
    sectors = [
        "residential_area", "main_street", "drainage_system",
        "great_bath", "granary_area", "marketplace", "craft_workshop"
    ]
    for s in sectors:
        client.post("/api/gamification/explore-location", json={
            "username": uname,
            "location_id": s
        })

    # Check status
    st_res = client.get(f"/api/gamification/status/{uname}")
    assert st_res.status_code == 200
    st = st_res.json()
    
    unlocked_badge_ids = {b["id"] for b in st["badges"] if b["unlocked"]}
    assert "badge_heritage_explorer" in unlocked_badge_ids, "Heritage Explorer should unlock with all 7 sectors!"
    assert "badge_master_planner" in unlocked_badge_ids, "Master Planner should unlock with main_street & residential_area!"
    print("  [PASS] 'Heritage Explorer' badge unlocked after exploring all 7 sectors")
    print("  [PASS] 'Master Planner' badge unlocked after surveying avenues & residential grid")

    # Add 4 artifacts and verify Artifact Hunter badge
    for art_id in ["art_unicorn_seal", "art_painted_pottery", "art_mother_goddess", "art_standard_brick"]:
        client.post(f"/api/museum/discover/{art_id}", json={"username": uname})

    st2 = client.get(f"/api/gamification/status/{uname}").json()
    unlocked_badge_ids2 = {b["id"] for b in st2["badges"] if b["unlocked"]}
    assert "badge_artifact_hunter" in unlocked_badge_ids2, "Artifact Hunter should unlock with 4 artifacts!"
    print("  [PASS] 'Artifact Hunter' badge unlocked after discovering 4 relics")

def test_overall_progress_percentage():
    print("\n--- [TEST 6] Overall Mastery Percentage Formula ---")
    uname = "KavyaMaster"
    st = client.get(f"/api/gamification/status/{uname}").json()
    overall = st["overall_progress"]
    
    assert "overall_percentage" in overall
    assert "quests" in overall
    assert "artifacts" in overall
    assert "locations" in overall
    
    # 7 of 7 locations = 30% weight
    assert overall["locations"]["explored"] == 7
    assert overall["locations"]["weight_percentage"] == 30.0
    # 4 of 8 artifacts = 17.5% weight
    assert overall["artifacts"]["discovered"] == 4
    assert overall["artifacts"]["weight_percentage"] == 17.5
    
    print(f"  [PASS] Overall Mastery: {overall['overall_percentage']}% (Locations: {overall['locations']['weight_percentage']}%, Artifacts: {overall['artifacts']['weight_percentage']}%)")

def test_secret_archive_lore():
    print("\n--- [TEST 7] Secret Lore Archive API ---")
    res = client.get("/api/gamification/lore/secret-archive")
    assert res.status_code == 200
    data = res.json()
    assert len(data["archive_entries"]) >= 3
    print(f"  [PASS] Secret Lore Archive delivers {len(data['archive_entries'])} archaeological epigraphic entries")

def test_static_assets():
    print("\n--- [TEST 8] Gamification Static Assets ---")
    r1 = client.get("/static/css/gamification.css")
    assert r1.status_code == 200
    r2 = client.get("/static/js/gamification.js")
    assert r2.status_code == 200
    print("  [PASS] /static/css/gamification.css delivered (200 OK)")
    print("  [PASS] /static/js/gamification.js delivered (200 OK)")

if __name__ == "__main__":
    print("=================================================================")
    print("BHARAT QUEST - PHASE 8: GAMIFICATION & PROGRESSION TEST SUITE")
    print("=================================================================")
    test_xp_and_level_math()
    test_required_badges_present()
    test_levels_and_milestones_api()
    test_area_exploration_and_duplicate_prevention()
    test_badge_unlock_evaluation()
    test_overall_progress_percentage()
    test_secret_archive_lore()
    test_static_assets()
    print("\n=================================================================")
    print("ALL PHASE 8 GAMIFICATION TESTS PASSED SUCCESSFULLY! (100%)")
    print("=================================================================\n")
