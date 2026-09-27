"""
=================================================================
BHARAT QUEST - PHASE 10 VERIFICATION SUITE
Final Indus Valley Civilization Challenge
(City Planning, Drainage, Architecture, Trade, Resources, Daily Life)
=================================================================
"""
import sys
import os

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

client = TestClient(app)

def test_final_challenge_content_delivery():
    print("\n--- [TEST 1] Final Challenge Content Delivery ---")
    res = client.get("/api/final-challenge/content")
    assert res.status_code == 200
    data = res.json()
    assert data["total_dilemmas"] == 6
    assert data["max_score"] == 600
    assert len(data["dilemmas"]) == 6

    pillars = [d["pillar"] for d in data["dilemmas"]]
    assert "City Planning" in pillars
    assert "Drainage" in pillars
    assert "Architecture" in pillars
    assert "Trade" in pillars
    assert "Resources" in pillars
    assert "Daily Life" in pillars
    print(f"  [PASS] All 6 Core Pillars verified: {', '.join(pillars)}")

    # Ensure answers are not leaked in the content payload
    for d in data["dilemmas"]:
        for opt in d["options"]:
            assert "is_correct" not in opt, f"Option {opt['id']} leaked is_correct!"
    print("  [PASS] Anti-cheat payload sanitization verified (is_correct hidden from client)")

def test_final_challenge_perfect_submission_and_persistence():
    print("\n--- [TEST 2] Authentic Decision Submission & Scoring ---")
    test_user = "MeeraArchon"
    
    # 1. Register test explorer
    reg = client.post("/api/auth/register", json={
        "username": test_user,
        "age": 16,
        "avatar": "🧑‍🎓",
        "archetype": "Town Architect",
        "password": "pass"
    })
    assert reg.status_code in [200, 400]

    # 2. Discover an artifact & explore a sector first to test summary aggregation
    client.post("/api/museum/discover/art_unicorn_seal", json={"username": test_user})
    client.post("/api/gamification/explore-location", json={"username": test_user, "location_id": "residential_area"})

    # 3. Submit perfect Harappan decisions
    sub_payload = {
        "username": test_user,
        "decisions": {
            "city_planning": "opt_plan_orthogonal",
            "drainage": "opt_drain_three_stage",
            "architecture": "opt_arch_standard_brick",
            "trade": "opt_trade_binary_carnelian",
            "resources": "opt_res_targeted_network",
            "daily_life": "opt_life_guild_consensus"
        }
    }
    sub_res = client.post("/api/final-challenge/submit", json=sub_payload)
    assert sub_res.status_code == 200
    res_data = sub_res.json()

    assert res_data["final_score"] == 600
    assert res_data["percentage"] == 100.0
    assert res_data["passed"] is True
    assert res_data["xp_earned"] == 500
    assert res_data["achievement"] == "Indus Valley Explorer"
    assert res_data["achievement_badge"] == "badge_indus_explorer"
    print(f"  [PASS] Perfect Score: {res_data['final_score']} / {res_data['max_score']} (100.0%)")
    print(f"  [PASS] XP Earned: +{res_data['xp_earned']} XP | New Level: {res_data['new_level']}")
    print(f"  [PASS] Capstone Achievement Awarded: '{res_data['achievement']}' ({res_data['honorary_title']})")

    # 4. Verify Comprehensive Summary Metrics
    assert res_data["artifacts_discovered_count"] >= 1
    assert "art_unicorn_seal" in res_data["artifacts_discovered"]
    assert res_data["areas_explored_count"] >= 1
    assert "residential_area" in res_data["areas_explored"]
    assert res_data["badges_earned_count"] >= 1
    
    badge_ids = {b["id"] for b in res_data["badges_earned"]}
    assert "badge_indus_explorer" in badge_ids
    print(f"  [PASS] Verified Summary Aggregation: {res_data['artifacts_discovered_count']} Relics, {res_data['areas_explored_count']} Sectors, {res_data['badges_earned_count']} Badges")

    # 5. Verify 6-Pillar Learning Summary
    ls = res_data["learning_summary"]
    assert len(ls) == 6
    assert "city_planning" in ls
    assert "drainage" in ls
    assert "architecture" in ls
    assert "trade" in ls
    assert "resources" in ls
    assert "daily_life" in ls
    print("  [PASS] Comprehensive 6-Pillar Learning Summary successfully hydrated")

def test_final_challenge_mongodb_persistence():
    print("\n--- [TEST 3] MongoDB Final Result Persistence ---")
    test_user = "MeeraArchon"
    
    # Verify via Profile API
    prof_res = client.get(f"/api/user/profile/{test_user}")
    assert prof_res.status_code == 200
    prof = prof_res.json()
    assert "badge_indus_explorer" in prof["stats"]["badges"]
    print("  [PASS] 'badge_indus_explorer' confirmed in MongoDB player profile stats")

    # Verify via Final Challenge Status API
    status_res = client.get(f"/api/final-challenge/status/{test_user}")
    assert status_res.status_code == 200
    st_data = status_res.json()
    assert st_data["has_completed"] is True
    assert st_data["final_challenge"]["score"] == 600
    assert st_data["final_challenge"]["achievement"] == "Indus Valley Explorer"
    print(f"  [PASS] Final Challenge persistence confirmed via /api/final-challenge/status/{test_user}")

def test_suboptimal_decision_scoring():
    print("\n--- [TEST 4] Partial / Anachronistic Decision Grading ---")
    novice_user = "NoviceSurveyor"
    client.post("/api/auth/register", json={
        "username": novice_user,
        "age": 12,
        "avatar": "🧑‍🎓",
        "archetype": "Curious Explorer",
        "password": "pass"
    })

    # Submit anachronistic / incorrect decisions
    sub_res = client.post("/api/final-challenge/submit", json={
        "username": novice_user,
        "decisions": {
            "city_planning": "opt_plan_radial",       # Radial royal palace
            "drainage": "opt_drain_open_gutter",       # Open gutters
            "architecture": "opt_arch_sun_dried",      # Sun-dried mud
            "trade": "opt_trade_iron_coins",           # Iron cutlery & coinage
            "resources": "opt_res_deep_south_iron",    # Bauxite in Deccan
            "daily_life": "opt_life_military_crackdown"# Royal chariots & dungeon
        }
    })
    assert sub_res.status_code == 200
    data = sub_res.json()
    assert data["final_score"] < 300
    assert data["percentage"] < 50.0
    assert data["passed"] is False
    print(f"  [PASS] Inaccurate decisions graded rigorously: {data['final_score']} / {data['max_score']} ({data['percentage']}%)")

def test_static_assets_and_html_elements():
    print("\n--- [TEST 5] Phase 10 Static Assets & HTML Delivery ---")
    css_res = client.get("/static/css/final-challenge.css")
    assert css_res.status_code == 200
    print("  [PASS] /static/css/final-challenge.css delivered (200 OK)")

    js_res = client.get("/static/js/final-challenge.js")
    assert js_res.status_code == 200
    print("  [PASS] /static/js/final-challenge.js delivered (200 OK)")

    idx_res = client.get("/")
    assert idx_res.status_code == 200
    html = idx_res.text

    phase10_elements = [
        "tab-final-challenge",
        "finalChallengeContainer",
        "/static/css/final-challenge.css",
        "/static/js/final-challenge.js"
    ]
    for el in phase10_elements:
        assert el in html, f"Missing Phase 10 element {el} in index.html"
    print("  [PASS] Phase 10 navigation tab, challenge stage, and script bundles integrated in index.html")

def run_phase10_suite():
    print("=" * 65)
    print("BHARAT QUEST - PHASE 10: FINAL CHALLENGE TEST SUITE")
    print("=" * 65)
    test_final_challenge_content_delivery()
    test_final_challenge_perfect_submission_and_persistence()
    test_final_challenge_mongodb_persistence()
    test_suboptimal_decision_scoring()
    test_static_assets_and_html_elements()
    print("\n" + "=" * 65)
    print("ALL PHASE 10 FINAL CHALLENGE TESTS PASSED SUCCESSFULLY! (100%)")
    print("=" * 65)

if __name__ == "__main__":
    run_phase10_suite()
