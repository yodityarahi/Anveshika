import sys
import os
from pathlib import Path

# Add project root and virtual environment site-packages
workspace_root = Path(__file__).parent.resolve()
sys.path.insert(0, str(workspace_root))

venv_site_packages = workspace_root / ".venv" / "Lib" / "site-packages"
if venv_site_packages.exists():
    sys.path.insert(0, str(venv_site_packages))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from fastapi.testclient import TestClient
from backend.app.main import app

def test_phase6():
    print("=" * 65)
    print("BHARAT QUEST - PHASE 6 QUEST & CHALLENGE SYSTEM VERIFICATION")
    print("=" * 65)
    
    client = TestClient(app)
    
    # 1. Test /api/quests endpoint
    print("\n[1/6] Testing /api/quests catalog endpoint...")
    resp = client.get("/api/quests")
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
    quests = resp.json()
    assert len(quests) == 5, f"Expected 5 quests, got {len(quests)}"
    print(f"  [PASS] /api/quests delivered {len(quests)} core Harappan quests")

    # 2. Verify all 5 Required Quests and their Learning Concepts
    print("\n[2/6] Verifying 5 mandatory quests, learning concepts & metadata...")
    expected_quests = {
        "quest_01_rebuild_city": {
            "title": "Rebuild the Ancient City",
            "concept_keywords": ["urban", "planning", "grid"],
            "difficulty": "Beginner"
        },
        "quest_02_lost_artifact": {
            "title": "The Lost Artifact",
            "concept_keywords": ["pottery", "seal", "metallurgy", "classification"],
            "difficulty": "Intermediate"
        },
        "quest_03_drainage_challenge": {
            "title": "The Drainage Challenge",
            "concept_keywords": ["sanitation", "hydraulic", "engineering"],
            "difficulty": "Intermediate"
        },
        "quest_04_ancient_trade": {
            "title": "Ancient Trade & The Maritime Highway",
            "concept_keywords": ["trade", "route", "economic", "metrology"],
            "difficulty": "Intermediate"
        },
        "quest_05_life_in_ivc": {
            "title": "Life in the Indus Valley",
            "concept_keywords": ["daily life", "craft", "nutrition", "social"],
            "difficulty": "Advanced"
        }
    }

    found_ids = {q["quest_id"]: q for q in quests}

    for q_id, q_req in expected_quests.items():
        assert q_id in found_ids, f"Missing required quest: {q_id}"
        q = found_ids[q_id]
        
        # Verify required fields
        for field in ["quest_id", "title", "story_context", "location", "objective", "difficulty", "learning_concept", "reward_xp", "reward_tokens"]:
            assert field in q and q[field], f"Missing field '{field}' in quest {q_id}"
            
        assert q["reward_xp"] >= 250, f"XP reward too low in {q_id}"
        assert q["reward_tokens"] >= 5, f"Token reward too low in {q_id}"
        
        # Check concept keywords
        learning = q["learning_concept"].lower()
        matched_kw = [kw for kw in q_req["concept_keywords"] if kw in learning]
        assert len(matched_kw) > 0, f"Learning concept in {q_id} doesn't match requirement: {learning}"
        
        print(f"  [PASS] {q['title']} verified ({q['difficulty']}, {q['reward_xp']} XP, Concept: {q['learning_concept']})")

    # 3. Test /api/quests/{quest_id} detail endpoint
    print("\n[3/6] Testing /api/quests/{quest_id} detail endpoints...")
    for q_id in expected_quests.keys():
        d_resp = client.get(f"/api/quests/{q_id}")
        assert d_resp.status_code == 200
        detail = d_resp.json()
        assert "challenge" in detail
        assert "type" in detail["challenge"]
        assert "instructions" in detail["challenge"]
        assert "interactive_data" in detail["challenge"]
        print(f"  [PASS] Detailed challenge loaded: {q_id} (Type: {detail['challenge']['type']})")

    # 4. Test Interactive Quest Submission, Evaluation & MongoDB Persistence
    print("\n[4/6] Testing solution submission, automated grading & MongoDB award persistence...")
    test_player = "ArjunQuestMaster"
    # Ensure test player registered
    client.post("/api/auth/register", json={
        "username": test_player,
        "age": 14,
        "avatar": "🧑‍🎓",
        "archetype": "Town Architect",
        "password": "pass"
    })

    # Test wrong submission for Quest 1
    wrong_sub_resp = client.post("/api/quests/quest_01_rebuild_city/submit", json={
        "username": test_player,
        "submission": {
            "slot_houses": "card_public_areas",
            "slot_roads": "card_drainage",
            "slot_drainage": "card_houses",
            "slot_public_areas": "card_roads"
        }
    })
    assert wrong_sub_resp.status_code == 200
    wrong_data = wrong_sub_resp.json()
    assert wrong_data["is_correct"] is False
    assert "misplaced" in wrong_data["feedback"].lower() or "verify" in wrong_data["feedback"].lower()
    print("  [PASS] Incorrect solution properly rejected with pedagogical explanation")

    # Test correct solutions for all 5 quests
    correct_solutions = {
        "quest_01_rebuild_city": {
            "slot_houses": "card_houses",
            "slot_roads": "card_roads",
            "slot_drainage": "card_drainage",
            "slot_public_areas": "card_public_areas"
        },
        "quest_02_lost_artifact": {
            "selected_candidate": "cand_unicorn_seal"
        },
        "quest_03_drainage_challenge": {
            "ordered_ids": ["step_bath", "step_sump", "step_sewer", "step_outflow"]
        },
        "quest_04_ancient_trade": {
            "com_carnelian": "dest_mesopotamia",
            "com_lapis": "dest_badakhshan",
            "com_copper": "dest_khetri",
            "com_shell": "dest_gulf_khambhat"
        },
        "quest_05_life_in_ivc": {
            "scenario_1": "opt_1_correct",
            "scenario_2": "opt_2_correct",
            "scenario_3": "opt_3_correct"
        }
    }

    total_xp_awarded = 0
    for q_id, sol_payload in correct_solutions.items():
        s_resp = client.post(f"/api/quests/{q_id}/submit", json={
            "username": test_player,
            "submission": sol_payload
        })
        assert s_resp.status_code == 200, f"Error submitting {q_id}: {s_resp.text}"
        res_data = s_resp.json()
        assert res_data["is_correct"] is True, f"Failed solution for {q_id}: {res_data}"
        assert res_data["xp_awarded"] > 0
        total_xp_awarded += res_data["xp_awarded"]
        print(f"  [PASS] Solved '{q_id}': +{res_data['xp_awarded']} XP | {res_data['feedback'][:45]}...")

    # Verify MongoDB persistence
    prof_resp = client.get(f"/api/user/profile/{test_player}")
    assert prof_resp.status_code == 200
    p_data = prof_resp.json()
    user_stats = p_data["stats"]
    assert len(user_stats["completed_quests"]) == 5
    assert user_stats["xp"] >= total_xp_awarded
    assert len(user_stats["discovered_artifacts"]) >= 3
    assert len(user_stats["badges"]) >= 3
    print(f"  [PASS] MongoDB state verified: {len(user_stats['completed_quests'])}/5 quests completed, {user_stats['xp']} XP, Level {user_stats['level']}")

    # 5. Test Frontend HTML Markup
    print("\n[5/6] Testing frontend/index.html for Quest Hub & Modal markup...")
    index_path = workspace_root / "frontend" / "index.html"
    assert index_path.exists()
    html = index_path.read_text(encoding="utf-8")

    quest_html_elements = [
        "questsHubContainer",
        "questChallengeModal",
        "questModalTitle",
        "questModalNpcAvatar",
        "questModalStoryText",
        "questInstructionsText",
        "questChallengeStage",
        "questFeedbackBox",
        "questHintBox",
        "questController.submitCurrentQuest",
        "questController.toggleHint",
        "/static/css/quests.css",
        "/static/js/quests.js"
    ]
    for el in quest_html_elements:
        assert el in html, f"Missing quest element in index.html: {el}"
    print("  [PASS] Quest Hub, Interactive Modal, and script links verified in index.html")

    # 6. Test Frontend Controller, CSS & Static Asset Delivery
    print("\n[6/6] Testing quests.js, quests.css & static asset delivery...")
    quests_js = (workspace_root / "frontend" / "js" / "quests.js").read_text(encoding="utf-8")
    quests_css = (workspace_root / "frontend" / "css" / "quests.css").read_text(encoding="utf-8")

    assert "class BharatQuestController" in quests_js
    assert "openQuestChallenge" in quests_js
    assert "submitCurrentQuest" in quests_js
    assert "renderChallengeUi" in quests_js
    assert "rebuild_city" in quests_js
    assert "artifact_detective" in quests_js
    assert "drainage_flow" in quests_js
    assert "trade_network" in quests_js
    assert "daily_life_simulation" in quests_js
    assert "window.questController" in quests_js
    print("  [PASS] BharatQuestController verified with all 5 challenge renderers & grading hooks")

    assert ".quest-hub-container" in quests_css
    assert ".quest-card" in quests_css
    assert ".quest-modal-overlay" in quests_css
    assert ".rebuild-stage-container" in quests_css
    assert ".detective-stage-container" in quests_css
    assert ".drainage-stage-container" in quests_css
    assert ".trade-stage-container" in quests_css
    assert ".life-stage-container" in quests_css
    print("  [PASS] quests.css verified with complete responsive styling")

    css_res = client.get("/static/css/quests.css")
    assert css_res.status_code == 200
    js_res = client.get("/static/js/quests.js")
    assert js_res.status_code == 200
    print("  [PASS] /static/css/quests.css and /static/js/quests.js delivered successfully")

    print("\n" + "=" * 65)
    print("ALL PHASE 6 QUEST SYSTEM VERIFICATIONS PASSED!")
    print("=" * 65)

if __name__ == "__main__":
    test_phase6()
