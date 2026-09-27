"""
=================================================================
BHARAT QUEST - PHASE 9 VERIFICATION SUITE
AI/ML Personalization (Quest Recommender, Adaptive Difficulty & Knowledge Matrix)
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
from backend.app.ml.personalization import (
    quest_recommender,
    difficulty_classifier,
    progress_analyzer,
    PROTOTYPE_DISCLAIMER
)

client = TestClient(app)

def test_quest_recommender_logic():
    print("\n--- [TEST 1] Scikit-Learn Quest Recommender ---")
    uname = "AaravScholar"
    client.post("/api/auth/register", json={
        "username": uname,
        "age": 14,
        "avatar": "🧑‍🎓",
        "archetype": "Town Architect",
        "password": "1234"
    })

    # Test baseline recommendation
    res = client.get(f"/api/ai/recommendations/{uname}")
    assert res.status_code == 200
    data = res.json()
    assert data["has_recommendation"] is True
    assert "recommended_quest_id" in data
    assert "confidence_score" in data
    assert "reason" in data
    assert "prototype_disclaimer" in data
    print(f"  [PASS] Recommended Quest: {data['title']} ({data['confidence_score'] * 100}% confidence)")
    print(f"  [PASS] Explainable Reason: {data['reason']}")
    print(f"  [PASS] Model: {data['algorithm']}")

def test_adaptive_difficulty_classifier():
    print("\n--- [TEST 2] Adaptive Difficulty Classification ---")
    uname = "AaravScholar"
    res = client.get(f"/api/ai/difficulty/{uname}")
    assert res.status_code == 200
    data = res.json()
    assert data["recommended_difficulty"] in ["Easy", "Medium", "Hard"]
    assert "confidence_score" in data
    assert len(data["decision_factors"]) >= 3
    assert "tier_settings" in data
    print(f"  [PASS] Classified Tier: {data['recommended_difficulty']} Mode (Confidence: {data['confidence_score'] * 100}%)")
    print(f"  [PASS] Decision Factors: {', '.join(data['decision_factors'])}")
    print(f"  [PASS] Tier Guidance: {data['tier_settings']['guidance']}")

def test_learning_progress_analyzer():
    print("\n--- [TEST 3] Harappan Knowledge Matrix Analysis ---")
    uname = "AaravScholar"
    res = client.get(f"/api/ai/learning-progress/{uname}")
    assert res.status_code == 200
    data = res.json()
    assert "overall_knowledge_index" in data
    assert len(data["domains"]) == 5
    domain_names = [d["name"] for d in data["domains"]]
    assert "Urban Planning & Architecture" in domain_names
    assert "Epigraphy & Material Classification" in domain_names
    assert "Hydraulic Sanitation Engineering" in domain_names
    assert "Maritime Commerce & Metrology" in domain_names
    assert "Daily Life, Culture & Governance" in domain_names
    print(f"  [PASS] Verified 5 Domains: {', '.join(domain_names)}")
    print(f"  [PASS] Overall Knowledge Index: {data['overall_knowledge_index']}%")
    print(f"  [PASS] Top Strength: {data['top_strength']}")
    print(f"  [PASS] Growth Area: {data['growth_area']}")

def test_unified_ai_dashboard_endpoint():
    print("\n--- [TEST 4] Unified AI Dashboard API ---")
    uname = "AaravScholar"
    res = client.get(f"/api/ai/dashboard/{uname}")
    assert res.status_code == 200
    data = res.json()
    assert "recommendation" in data
    assert "difficulty" in data
    assert "learning_progress" in data
    assert "telemetry_summary" in data
    assert "prototype_disclaimer" in data
    print("  [PASS] Unified AI Dashboard returns recommendations, difficulty, and learning progress")
    print(f"  [PASS] Prototype Transparency Disclaimer present: '{data['prototype_disclaimer'][:65]}...'")

def test_interactive_ml_simulation():
    print("\n--- [TEST 5] Interactive ML Simulation (Accuracy & Speed Shift) ---")
    # Simulation 1: High Performer
    sim_high = client.post("/api/ai/simulate", json={
        "accuracy_rate": 0.95,
        "avg_solve_time": 20.0,
        "attempts_per_quest": 1.0,
        "player_level": 4,
        "hints_used": 0,
        "completed_quests": ["quest_01_rebuild_city"]
    })
    assert sim_high.status_code == 200
    d_high = sim_high.json()
    assert d_high["adaptive_difficulty"]["recommended_difficulty"] == "Hard"
    print("  [PASS] High performance (95% acc, 20s time) correctly classified as 'Hard' Mode")

    # Simulation 2: Struggling / Novice Performer
    sim_low = client.post("/api/ai/simulate", json={
        "accuracy_rate": 0.40,
        "avg_solve_time": 110.0,
        "attempts_per_quest": 3.0,
        "player_level": 1,
        "hints_used": 3,
        "completed_quests": []
    })
    assert sim_low.status_code == 200
    d_low = sim_low.json()
    assert d_low["adaptive_difficulty"]["recommended_difficulty"] == "Easy"
    print("  [PASS] Struggling performance (40% acc, 110s time) correctly classified as 'Easy' Mode (Assisted)")

def test_static_assets():
    print("\n--- [TEST 6] AI/ML Static Assets Delivery ---")
    r1 = client.get("/static/css/ai-engine.css")
    assert r1.status_code == 200
    r2 = client.get("/static/js/ai-engine.js")
    assert r2.status_code == 200
    print("  [PASS] /static/css/ai-engine.css delivered (200 OK)")
    print("  [PASS] /static/js/ai-engine.js delivered (200 OK)")

if __name__ == "__main__":
    print("=================================================================")
    print("BHARAT QUEST - PHASE 9: AI/ML PERSONALIZATION TEST SUITE")
    print("=================================================================")
    test_quest_recommender_logic()
    test_adaptive_difficulty_classifier()
    test_learning_progress_analyzer()
    test_unified_ai_dashboard_endpoint()
    test_interactive_ml_simulation()
    test_static_assets()
    print("\n=================================================================")
    print("ALL PHASE 9 AI/ML PERSONALIZATION TESTS PASSED SUCCESSFULLY! (100%)")
    print("=================================================================\n")
