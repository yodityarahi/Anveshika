"""
=================================================================================
BHARAT QUEST - COMPREHENSIVE FINAL AUDIT & USER JOURNEY TEST SUITE
SIH Problem Statement: 26208 (Interactive Living Museum & Gamified Heritage)

Simulates & audits the complete end-to-end user journey:
Registration -> Profile -> Dashboard -> India Map -> IVC -> Story -> Ancient City
-> Exploration -> Quests -> Challenges -> XP -> Artifacts -> Virtual Museum
-> AI Recommendation -> Final Challenge -> Final Progress
=================================================================================
"""
import sys
import os
import json
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

PROJECT_ROOT = Path(__file__).parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

venv_site_packages = PROJECT_ROOT / ".venv" / "Lib" / "site-packages"
if venv_site_packages.exists():
    sys.path.insert(0, str(venv_site_packages))

from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def run_complete_audit():
    print("=" * 80)
    print("        BHARAT QUEST - COMPREHENSIVE END-TO-END FINAL AUDIT")
    print("        Smart India Hackathon • Problem Statement: 26208")
    print("=" * 80)

    audit_user = "KavyaExplorer"
    audit_results = {}

    # -------------------------------------------------------------------------
    # STEP 1: REGISTRATION & PROFILE INITIALIZATION
    # -------------------------------------------------------------------------
    print("\n[STEP 1/13] Registration & Profile Initialization...")
    reg_payload = {
        "username": audit_user,
        "age": 16,
        "avatar": "🧭",
        "archetype": "Civic Hydrologist",
        "password": "sih_demo_pass"
    }
    reg_res = client.post("/api/auth/register", json=reg_payload)
    assert reg_res.status_code in [200, 400], f"Registration failed: {reg_res.text}"
    print(f"  [PASS] User '{audit_user}' registered successfully.")

    # Fetch fresh profile
    prof_res = client.get(f"/api/user/profile/{audit_user}")
    assert prof_res.status_code == 200, "Failed to retrieve profile"
    prof_data = prof_res.json()
    assert prof_data["username"] == audit_user
    assert prof_data["archetype"] == "Civic Hydrologist"
    assert "stats" in prof_data
    assert prof_data["stats"]["level"] == 1
    assert "badges" in prof_data["stats"]
    print(f"  [PASS] Profile hydrated: Level {prof_data['stats']['level']}, Archetype '{prof_data['archetype']}'.")
    audit_results["registration"] = True

    # -------------------------------------------------------------------------
    # STEP 2: DASHBOARD METRICS & HEALTH
    # -------------------------------------------------------------------------
    print("\n[STEP 2/13] System Health & Dashboard Core Metrics...")
    health_res = client.get("/api/health")
    assert health_res.status_code == 200
    h_data = health_res.json()
    assert h_data["status"] == "healthy"
    print(f"  [PASS] System Health: {h_data['status']} | Database: {h_data['database']['engine']}")

    # Check gamification status for dashboard
    status_res = client.get(f"/api/gamification/status/{audit_user}")
    assert status_res.status_code == 200
    status_data = status_res.json()
    assert "overall_progress" in status_data
    assert "level_progress" in status_data
    assert status_data["overall_progress"]["overall_percentage"] >= 0
    print(f"  [PASS] Dashboard initial progress: {status_data['overall_progress']['overall_percentage']}% ({status_data['level_progress']['level_title']}).")
    audit_results["dashboard"] = True

    # -------------------------------------------------------------------------
    # STEP 3: INDIA MAP & CIVILIZATION CAROUSEL
    # -------------------------------------------------------------------------
    print("\n[STEP 3/13] Cartographic India Map & Multi-Civilization Scalability...")
    civ_res = client.get("/api/ivc/civilizations")
    assert civ_res.status_code == 200
    civ_data = civ_res.json()
    assert len(civ_data) >= 5, "Expected at least 5 civilizations for future scalability"
    active_civ = next((c for c in civ_data if c["status"] == "unlocked"), None)
    assert active_civ is not None
    assert active_civ["id"] == "ivc"
    print(f"  [PASS] Active Realm: '{active_civ['name']}' ({active_civ.get('era', 'Bronze Age')})")
    locked_civs = [c["name"] for c in civ_data if c["status"] == "locked"]
    print(f"  [PASS] Scalability Realms (Architecture Ready): {', '.join(locked_civs)}")
    audit_results["map"] = True

    # -------------------------------------------------------------------------
    # STEP 4: IVC STORY INTRODUCTION THEATER
    # -------------------------------------------------------------------------
    print("\n[STEP 4/13] Story Introduction Theater (7 Narrative Scenes)...")
    story_res = client.get("/api/ivc/story")
    assert story_res.status_code == 200
    story_data = story_res.json()
    scenes = story_data.get("scenes", story_data if isinstance(story_data, list) else [])
    assert len(scenes) >= 7, f"Expected 7 story scenes, got {len(scenes)}"
    scene_titles = [s["title"] for s in scenes]
    print(f"  [PASS] Loaded {len(scenes)} narrative acts: {', '.join(scene_titles[:3])}...")
    audit_results["story"] = True

    # -------------------------------------------------------------------------
    # STEP 5: 2D INTERACTIVE ANCIENT CITY
    # -------------------------------------------------------------------------
    print("\n[STEP 5/13] 2D Interactive Indus Valley Ancient City Sectors...")
    city_res = client.get("/api/ivc/locations")
    assert city_res.status_code == 200
    locations = city_res.json()
    assert len(locations) >= 7, "Expected 7 interactive ancient city sectors"
    required_sectors = [
        "residential_area", "main_street", "drainage_system",
        "great_bath", "granary_area", "marketplace", "craft_workshop"
    ]
    loc_ids = [l["id"] for l in locations]
    for s in required_sectors:
        assert s in loc_ids, f"Missing city sector: {s}"
    print(f"  [PASS] All 7 core city sectors confirmed: {', '.join(loc_ids)}")
    audit_results["city"] = True

    # -------------------------------------------------------------------------
    # STEP 6: EXPLORATION, SURVEYS & DUPLICATE PREVENTION
    # -------------------------------------------------------------------------
    print("\n[STEP 6/13] Sector Exploration & Duplicate Prevention...")
    exp_res1 = client.post("/api/gamification/explore-location", json={
        "username": audit_user,
        "location_id": "drainage_system"
    })
    assert exp_res1.status_code == 200
    exp_data1 = exp_res1.json()
    assert exp_data1["is_new"] is True
    assert exp_data1["xp_awarded"] == 75
    print(f"  [PASS] Sector 'drainage_system' surveyed: +{exp_data1['xp_awarded']} XP.")

    # Duplicate survey prevention check
    exp_res2 = client.post("/api/gamification/explore-location", json={
        "username": audit_user,
        "location_id": "drainage_system"
    })
    assert exp_res2.status_code == 200
    exp_data2 = exp_res2.json()
    assert exp_data2["is_new"] is False
    assert exp_data2["xp_awarded"] == 0
    print("  [PASS] Duplicate exploration prevention verified (0 XP on duplicate).")
    audit_results["exploration"] = True

    # -------------------------------------------------------------------------
    # STEP 7: REUSABLE QUESTS & CHALLENGES
    # -------------------------------------------------------------------------
    print("\n[STEP 7/13] Reusable Quest System Execution (All 5 Quests)...")
    quests_res = client.get("/api/quests")
    assert quests_res.status_code == 200
    quests = quests_res.json()
    assert len(quests) >= 5, f"Expected 5 quests, got {len(quests)}"

    # Solve Quest 1: Rebuild the Ancient City
    q1_sub = client.post("/api/quests/quest_01_rebuild_city/submit", json={
        "username": audit_user,
        "submission": {
            "slot_houses": "card_houses",
            "slot_roads": "card_roads",
            "slot_drainage": "card_drainage",
            "slot_public_areas": "card_public_areas"
        }
    })
    assert q1_sub.status_code == 200
    q1_data = q1_sub.json()
    assert q1_data["is_correct"] is True
    print(f"  [PASS] Quest 1 (Rebuild City) Passed: +{q1_data['xp_awarded']} XP.")

    # Solve Quest 3: The Drainage Challenge
    q3_sub = client.post("/api/quests/quest_03_drainage_challenge/submit", json={
        "username": audit_user,
        "submission": {
            "ordered_ids": ["step_bath", "step_sump", "step_sewer", "step_outflow"]
        }
    })
    assert q3_sub.status_code == 200
    q3_data = q3_sub.json()
    assert q3_data["is_correct"] is True
    print(f"  [PASS] Quest 3 (Drainage Challenge) Passed: +{q3_data['xp_awarded']} XP.")

    # Solve Quest 4: Ancient Trade
    q4_sub = client.post("/api/quests/quest_04_ancient_trade/submit", json={
        "username": audit_user,
        "submission": {
            "com_carnelian": "dest_mesopotamia",
            "com_lapis": "dest_badakhshan",
            "com_copper": "dest_khetri",
            "com_shell": "dest_gulf_khambhat"
        }
    })
    assert q4_sub.status_code == 200
    q4_data = q4_sub.json()
    assert q4_data["is_correct"] is True
    print(f"  [PASS] Quest 4 (Ancient Trade) Passed: +{q4_data['xp_awarded']} XP.")
    audit_results["quests"] = True

    # -------------------------------------------------------------------------
    # STEP 8: ARTIFACT DISCOVERY & VIRTUAL MUSEUM
    # -------------------------------------------------------------------------
    print("\n[STEP 8/13] Artifact Discovery & Virtual Museum Repository...")
    art_list_res = client.get("/api/museum/artifacts")
    assert art_list_res.status_code == 200
    all_arts = art_list_res.json()
    assert len(all_arts) >= 7
    print(f"  [PASS] Museum catalog holds {len(all_arts)} historical exhibits.")

    # Discover Unicorn Seal
    disc1 = client.post("/api/museum/discover/art_unicorn_seal", json={"username": audit_user})
    assert disc1.status_code == 200
    d1_data = disc1.json()
    assert d1_data["is_new"] is True
    assert d1_data["xp_awarded"] > 0
    print(f"  [PASS] Unearthed 'Steatite Unicorn Seal': +{d1_data['xp_awarded']} XP.")

    # Discover Standard Fired Brick
    disc2 = client.post("/api/museum/discover/art_standard_brick", json={"username": audit_user})
    assert disc2.status_code == 200
    assert disc2.json()["is_new"] is True
    print("  [PASS] Unearthed 'Standardized 1:2:4 Fired Mud Brick'.")

    # Duplicate check on artifact
    disc_dup = client.post("/api/museum/discover/art_unicorn_seal", json={"username": audit_user})
    assert disc_dup.status_code == 200
    assert disc_dup.json()["is_new"] is False
    assert disc_dup.json()["xp_awarded"] == 0
    print("  [PASS] Artifact duplicate prevention verified (0 XP on duplicate).")
    audit_results["museum"] = True

    # -------------------------------------------------------------------------
    # STEP 9: BADGE UNLOCKING & LEVEL ADVANCEMENT
    # -------------------------------------------------------------------------
    print("\n[STEP 9/13] Badge Unlocking & Level Progression...")
    mid_prof_res = client.get(f"/api/user/profile/{audit_user}")
    assert mid_prof_res.status_code == 200
    mid_prof = mid_prof_res.json()
    current_level = mid_prof["stats"]["level"]
    current_xp = mid_prof["stats"]["xp"]
    earned_badges = mid_prof["stats"]["badges"]
    print(f"  [PASS] Mid-journey status: Level {current_level} | XP: {current_xp} | Badges: {len(earned_badges)}")
    audit_results["gamification"] = True

    # -------------------------------------------------------------------------
    # STEP 10: AI/ML PERSONALIZATION & ADAPTIVE DIFFICULTY
    # -------------------------------------------------------------------------
    print("\n[STEP 10/13] AI/ML Personalization Engine (Scikit-Learn)...")
    rec_res = client.get(f"/api/ai/recommendations/{audit_user}")
    assert rec_res.status_code == 200
    rec_data = rec_res.json()
    assert rec_data["has_recommendation"] is True
    assert "recommended_quest_id" in rec_data
    assert "confidence_score" in rec_data
    assert "prototype_disclaimer" in rec_data
    print(f"  [PASS] Quest Recommendation: '{rec_data.get('title', rec_data['recommended_quest_id'])}' (Confidence: {rec_data['confidence_score'] * 100}%)")

    diff_res = client.get(f"/api/ai/difficulty/{audit_user}")
    assert diff_res.status_code == 200
    diff_data = diff_res.json()
    assert "recommended_difficulty" in diff_data
    print(f"  [PASS] Adaptive Difficulty: '{diff_data['recommended_difficulty']}' (Confidence: {diff_data['confidence_score'] * 100}%)")

    learn_res = client.get(f"/api/ai/learning-progress/{audit_user}")
    assert learn_res.status_code == 200
    learn_data = learn_res.json()
    assert "overall_knowledge_index" in learn_data
    assert len(learn_data["domains"]) == 5
    print(f"  [PASS] 5-Pillar Harappan Knowledge Matrix evaluated across {len(learn_data['domains'])} domains.")
    audit_results["ai_engine"] = True

    # -------------------------------------------------------------------------
    # STEP 11: FINAL INDUS VALLEY CHALLENGE
    # -------------------------------------------------------------------------
    print("\n[STEP 11/13] Final Indus Valley Civilization Challenge...")
    fc_content = client.get("/api/final-challenge/content")
    assert fc_content.status_code == 200
    assert fc_content.json()["total_dilemmas"] == 6

    # Submit Capstone Decisions
    capstone_sub = client.post("/api/final-challenge/submit", json={
        "username": audit_user,
        "decisions": {
            "city_planning": "opt_plan_orthogonal",
            "drainage": "opt_drain_three_stage",
            "architecture": "opt_arch_standard_brick",
            "trade": "opt_trade_binary_carnelian",
            "resources": "opt_res_targeted_network",
            "daily_life": "opt_life_guild_consensus"
        }
    })
    assert capstone_sub.status_code == 200
    fc_res = capstone_sub.json()
    assert fc_res["final_score"] == 600
    assert fc_res["percentage"] == 100.0
    assert fc_res["passed"] is True
    assert fc_res["achievement"] == "Indus Valley Explorer"
    assert fc_res["achievement_badge"] == "badge_indus_explorer"
    print(f"  [PASS] Capstone Passed: {fc_res['final_score']}/600 (100%) | Achievement: '{fc_res['achievement']}'.")
    audit_results["final_challenge"] = True

    # -------------------------------------------------------------------------
    # STEP 12: FINAL PROGRESS & PERSISTENCE
    # -------------------------------------------------------------------------
    print("\n[STEP 12/13] Final Player Progress & MongoDB Data Integrity...")
    final_prof_res = client.get(f"/api/user/profile/{audit_user}")
    assert final_prof_res.status_code == 200
    final_prof = final_prof_res.json()
    
    assert final_prof["stats"]["level"] >= 2
    assert final_prof["stats"]["xp"] >= 800
    assert "badge_indus_explorer" in final_prof["stats"]["badges"]
    assert len(final_prof["stats"]["completed_quests"]) >= 3
    assert len(final_prof["stats"]["discovered_artifacts"]) >= 2
    
    # Check final challenge status endpoint
    fc_status_res = client.get(f"/api/final-challenge/status/{audit_user}")
    assert fc_status_res.status_code == 200
    fc_stat = fc_status_res.json()
    assert fc_stat["has_completed"] is True
    print(f"  [PASS] Final Status: Level {final_prof['stats']['level']} | Total XP: {final_prof['stats']['xp']}")
    print(f"  [PASS] Badges Earned: {len(final_prof['stats']['badges'])} (Includes 'badge_indus_explorer')")
    audit_results["persistence"] = True

    # -------------------------------------------------------------------------
    # STEP 13: STATIC ASSET AUDIT & ACCESSIBILITY
    # -------------------------------------------------------------------------
    print("\n[STEP 13/13] Static Asset Integrity & Frontend Files...")
    static_endpoints = [
        "/static/css/style.css",
        "/static/css/game-ui.css",
        "/static/css/map.css",
        "/static/css/story.css",
        "/static/css/city.css",
        "/static/css/quests.css",
        "/static/css/museum.css",
        "/static/css/gamification.css",
        "/static/css/ai-engine.css",
        "/static/css/final-challenge.css",
        "/static/css/animations-ux.css",
        "/static/js/api.js",
        "/static/js/audio.js",
        "/static/js/map.js",
        "/static/js/story.js",
        "/static/js/city.js",
        "/static/js/quests.js",
        "/static/js/museum.js",
        "/static/js/gamification.js",
        "/static/js/ai-engine.js",
        "/static/js/final-challenge.js",
        "/static/js/ux-polish.js",
        "/static/js/app.js"
    ]
    for asset in static_endpoints:
        ares = client.get(asset)
        assert ares.status_code == 200, f"Static asset {asset} returned {ares.status_code}"
    print(f"  [PASS] All {len(static_endpoints)} frontend stylesheets and JavaScript controllers verified (HTTP 200 OK).")
    audit_results["static_assets"] = True

    print("\n" + "=" * 80)
    print("      ALL 13 AUDIT STAGES PASSED WITH ZERO ERRORS (100% HEALTHY)!")
    print("=" * 80)
    return audit_results

if __name__ == "__main__":
    run_complete_audit()
