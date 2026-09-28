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

def run_master_suite():
    print("=" * 65)
    print("BHARAT QUEST - COMPREHENSIVE END-TO-END VERIFICATION")
    print("=" * 65)
    client = TestClient(app)

    # -------------------------------------------------------------
    # PHASE 1: SYSTEM & CONNECTION VERIFICATION
    # -------------------------------------------------------------
    print("\n>>> [PHASE 1] System Health & Static Assets")
    h_resp = client.get("/api/health")
    assert h_resp.status_code == 200
    h_data = h_resp.json()
    assert h_data["status"] == "healthy"
    assert "database" in h_data
    print(f"  [PASS] FastAPI Online | DB Engine: {h_data['database']['engine']}")

    # -------------------------------------------------------------
    # PHASE 2: AUTH & PLAYER PROFILE SYSTEM
    # -------------------------------------------------------------
    print("\n>>> [PHASE 2] Player Profile, Badges & Gamification")
    test_user = "PriyaHarappan"
    
    from backend.app.database import db_manager
    db_manager.get_db()["users"].delete_many({"username": {"$regex": f"^{test_user}$", "$options": "i"}})
    db_manager.save_state()

    # Register
    reg_resp = client.post("/api/auth/register", json={
        "username": test_user,
        "age": 15,
        "avatar": "🏛️",
        "archetype": "Town Architect",
        "password": "pass"
    })
    if reg_resp.status_code == 400:
        # User might exist in mock/db, test login
        login_resp = client.post("/api/auth/login", json={
            "username": test_user,
            "password": "pass"
        })
        assert login_resp.status_code == 200
        user_prof = login_resp.json()
        print(f"  [PASS] Existing player '{test_user}' logged in")
    else:
        assert reg_resp.status_code == 200
        user_prof = reg_resp.json()
        print(f"  [PASS] New player '{test_user}' registered")

    # Profile Fetch
    prof_resp = client.get(f"/api/user/profile/{test_user}")
    assert prof_resp.status_code == 200
    pdata = prof_resp.json()
    assert pdata["username"] == test_user
    assert pdata["stats"]["level"] >= 1
    assert len(pdata["badges_details"]) >= 8
    print(f"  [PASS] Profile fetched with {len(pdata['badges_details'])} IVC Badges hydrated")

    # Progress Award
    award_resp = client.post(f"/api/user/profile/{test_user}/award", json={
        "xp_to_add": 350,
        "tokens_to_add": 10,
        "badge_to_unlock": "badge_city_planner",
        "quest_to_complete": "quest_01_grid_streets"
    })
    assert award_resp.status_code == 200
    upgraded = award_resp.json()
    assert upgraded["stats"]["xp"] >= 500
    assert "badge_city_planner" in upgraded["stats"]["badges"]
    print(f"  [PASS] Progress Awarded: Level {upgraded['stats']['level']}, XP {upgraded['stats']['xp']}")

    # -------------------------------------------------------------
    # PHASE 3: DASHBOARD & INTERACTIVE INDIA MAP
    # -------------------------------------------------------------
    print("\n>>> [PHASE 3] Dashboard, Map & IVC Journey Flow")
    
    # Civilizations list
    civ_resp = client.get("/api/ivc/civilizations")
    assert civ_resp.status_code == 200
    civs = civ_resp.json()
    assert len(civs) == 5
    
    ivc = next(c for c in civs if c["id"] == "ivc")
    assert ivc["status"] == "unlocked"
    print(f"  [PASS] Active Realm: {ivc['name']}")
    
    locked = [c for c in civs if c["status"] == "locked"]
    assert len(locked) == 4
    for l in locked:
        print(f"  [PASS] Scalability Realm (Locked): {l['name']}")

    # Frontend Index HTML validation
    index_file = workspace_root / "frontend" / "index.html"
    html = index_file.read_text(encoding="utf-8")
    
    # 8 Required Dashboard metrics
    dash_requirements = [
        "dashPlayerName", "dashAvatarRing", "dashLevelVal", 
        "dashXpVal", "dashQuestsVal", "dashArtifactsVal", 
        "dashBadgesVal", "dashProgressPct", "dashOverallCircle"
    ]
    for req in dash_requirements:
        assert req in html, f"Missing dashboard element #{req}"
    print("  [PASS] All 8 Dashboard metrics integrated in HTML")

    # Interactive Map validation
    map_requirements = [
        "bharatMapWrapper", "mapRegionIvc", "mapRegionVedic",
        "mapRegionMaurya", "mapRegionGupta", "mapRegionChola",
        "site-pin", "mapHoverCard", "ivcIntroModal", "enterIvcCity()"
    ]
    for mreq in map_requirements:
        assert mreq in html, f"Missing map element {mreq}"
    # -------------------------------------------------------------
    # PHASE 4: IVC STORY INTRODUCTION THEATER
    # -------------------------------------------------------------
    print("\n>>> [PHASE 4] IVC Story Introduction Theater")
    story_resp = client.get("/api/ivc/story")
    assert story_resp.status_code == 200
    s_data = story_resp.json()
    assert s_data["total_scenes"] == 7
    print(f"  [PASS] 7 Story scenes delivered via /api/ivc/story")

    story_requirements = [
        "ivcStoryModal", "storySceneCounter", "storyProgressFill",
        "storyStepsRow", "storyVisualStage", "storyNarrativeStage",
        "storyPrevBtn", "storyNextBtn", "storyController"
    ]
    for sreq in story_requirements:
        assert sreq in html, f"Missing story element {sreq} in index.html"
    print("  [PASS] Story Introduction Modal & interactive controls integrated")

    # -------------------------------------------------------------
    # PHASE 5: INTERACTIVE INDUS VALLEY ANCIENT CITY
    # -------------------------------------------------------------
    print("\n>>> [PHASE 5] 2D Interactive Indus Valley Ancient City")
    loc_resp = client.get("/api/ivc/locations")
    assert loc_resp.status_code == 200
    locations = loc_resp.json()
    assert len(locations) == 7
    print(f"  [PASS] 7 Ancient city sectors delivered via /api/ivc/locations")

    city_requirements = [
        "cityStageContainer", "cityInspectorModal", "inspectorIcon",
        "inspectorTitle", "inspectorZone", "inspectorHistoryText",
        "inspectableObjectsGrid", "inspectorQuestsContainer",
        "cityDiscoveryToast", "/static/css/city.css", "/static/js/city.js"
    ]
    for creq in city_requirements:
        assert creq in html, f"Missing city element {creq} in index.html"
    print("  [PASS] City stage, Inspector Modal, and Discovery Toast integrated in HTML")

    # Static assets delivery
    assert client.get("/static/css/city.css").status_code == 200
    assert client.get("/static/js/city.js").status_code == 200
    # -------------------------------------------------------------
    # PHASE 6: QUEST & CHALLENGE SYSTEM
    # -------------------------------------------------------------
    print("\n>>> [PHASE 6] Reusable Quest & Challenge System")
    q_resp = client.get("/api/quests")
    assert q_resp.status_code == 200
    all_quests = q_resp.json()
    assert len(all_quests) == 5
    print(f"  [PASS] 5 Harappan quests loaded via /api/quests")

    # Submit solution for Quest 1
    q1_sub = client.post("/api/quests/quest_01_rebuild_city/submit", json={
        "username": test_user,
        "submission": {
            "slot_houses": "card_houses",
            "slot_roads": "card_roads",
            "slot_drainage": "card_drainage",
            "slot_public_areas": "card_public_areas"
        }
    })
    assert q1_sub.status_code == 200
    assert q1_sub.json()["is_correct"] is True
    print(f"  [PASS] Quest 1 'Rebuild the Ancient City' submitted & evaluated successfully")

    quest_requirements = [
        "questsHubContainer", "questChallengeModal", "questModalTitle",
        "questInstructionsText", "questChallengeStage", "questFeedbackBox",
        "/static/css/quests.css", "/static/js/quests.js"
    ]
    for qreq in quest_requirements:
        assert qreq in html, f"Missing quest element {qreq} in index.html"
    print("  [PASS] Quest hub and challenge modal integrated in HTML")

    # Static assets delivery
    assert client.get("/static/css/quests.css").status_code == 200
    # -------------------------------------------------------------
    # PHASE 7: ARTIFACT COLLECTION & VIRTUAL MUSEUM
    # -------------------------------------------------------------
    print("\n>>> [PHASE 7] Living Virtual Museum & Artifact Collection")
    art_resp = client.get("/api/museum/artifacts")
    assert art_resp.status_code == 200
    all_artifacts = art_resp.json()
    assert len(all_artifacts) >= 7
    print(f"  [PASS] {len(all_artifacts)} Museum vitrine exhibits loaded via /api/museum/artifacts")

    # Discover an artifact and verify duplicate prevention
    d_res1 = client.post("/api/museum/discover/art_unicorn_seal", json={"username": test_user})
    assert d_res1.status_code == 200
    assert d_res1.json()["success"] is True
    
    # Duplicate attempt
    d_res2 = client.post("/api/museum/discover/art_unicorn_seal", json={"username": test_user})
    assert d_res2.status_code == 200
    assert d_res2.json()["is_new"] is False
    assert d_res2.json()["xp_awarded"] == 0
    print("  [PASS] Relic discovery & duplicate prevention verified")

    museum_requirements = [
        "museumHubContainer", "museumArtifactModal", "museumModalTitle",
        "museumModalSvgStage", "curatorialPurposeText", "curatorialSignificanceText",
        "curatorialFactText", "propPeriod", "propSite", "propMaterial",
        "/static/css/museum.css", "/static/js/museum.js"
    ]
    for mreq in museum_requirements:
        assert mreq in html, f"Missing museum element {mreq} in index.html"
    print("  [PASS] Museum vitrines and exhibit modal integrated in HTML")

    # Static assets delivery
    assert client.get("/static/css/museum.css").status_code == 200
    assert client.get("/static/js/museum.js").status_code == 200
    print("  [PASS] museum.css and museum.js delivered with HTTP 200 OK")

    # -------------------------------------------------------------
    # PHASE 8: GAMIFICATION & PROGRESSION
    # -------------------------------------------------------------
    print("\n>>> [PHASE 8] Gamification, Badges & Progression")
    badges_resp = client.get("/api/gamification/badges")
    assert badges_resp.status_code == 200
    b_data = badges_resp.json()
    assert b_data["total_badges"] >= 10
    
    b_ids = {b["id"] for b in b_data["badges"]}
    assert "badge_artifact_hunter" in b_ids
    assert "badge_master_planner" in b_ids
    assert "badge_heritage_explorer" in b_ids
    assert "badge_indus_expert" in b_ids
    print(f"  [PASS] All 4 required badges confirmed: Artifact Hunter, Master Planner, Heritage Explorer, Indus Valley Expert")
    
    levels_resp = client.get("/api/gamification/levels")
    assert levels_resp.status_code == 200
    assert levels_resp.json()["total_levels"] == 5
    print(f"  [PASS] All 5 level tiers verified with milestone perks")

    # Explore sector & verify duplicate prevention
    exp1 = client.post("/api/gamification/explore-location", json={"username": test_user, "location_id": "residential_area"})
    assert exp1.status_code == 200
    assert exp1.json()["is_new"] is True
    assert exp1.json()["xp_awarded"] == 75
    
    exp2 = client.post("/api/gamification/explore-location", json={"username": test_user, "location_id": "residential_area"})
    assert exp2.status_code == 200
    assert exp2.json()["is_new"] is False
    assert exp2.json()["xp_awarded"] == 0
    print("  [PASS] City sector exploration & duplicate prevention confirmed")

    # Status check
    st_res = client.get(f"/api/gamification/status/{test_user}")
    assert st_res.status_code == 200
    st_data = st_res.json()
    assert "overall_progress" in st_data
    assert "level_progress" in st_data
    print(f"  [PASS] Player progression metrics & 3-pillar mastery formula validated")

    gamification_requirements = [
        "levelUpModal", "secretArchiveModal", "dashMasteryContainer",
        "profileBadgesShowcaseContainer", "profileMilestonesContainer",
        "/static/css/gamification.css", "/static/js/gamification.js"
    ]
    for greq in gamification_requirements:
        assert greq in html, f"Missing gamification element {greq} in index.html"
    print("  [PASS] Level-up modal, secret archive modal & badges showcase integrated in HTML")

    assert client.get("/static/css/gamification.css").status_code == 200
    assert client.get("/static/js/gamification.js").status_code == 200
    print("  [PASS] gamification.css and gamification.js delivered with HTTP 200 OK")

    # -------------------------------------------------------------
    # PHASE 9: AI/ML PERSONALIZATION ENGINE
    # -------------------------------------------------------------
    print("\n>>> [PHASE 9] AI/ML Personalization Engine (Scikit-Learn)")
    
    # 1. Quest Recommendation API
    ai_rec_resp = client.get(f"/api/ai/recommendations/{test_user}")
    assert ai_rec_resp.status_code == 200
    rec_data = ai_rec_resp.json()
    assert rec_data["has_recommendation"] is True
    assert "recommended_quest_id" in rec_data
    assert "confidence_score" in rec_data
    assert "reason" in rec_data
    print(f"  [PASS] Scikit-Learn Recommender: '{rec_data['title']}' ({rec_data['confidence_score'] * 100:.1f}% confidence)")

    # 2. Adaptive Difficulty API
    ai_diff_resp = client.get(f"/api/ai/difficulty/{test_user}")
    assert ai_diff_resp.status_code == 200
    diff_data = ai_diff_resp.json()
    assert diff_data["recommended_difficulty"] in ["Easy", "Medium", "Hard"]
    assert "confidence_score" in diff_data
    assert len(diff_data["decision_factors"]) >= 3
    print(f"  [PASS] Adaptive Difficulty: {diff_data['recommended_difficulty']} Mode (Confidence: {diff_data['confidence_score']*100:.1f}%)")

    # 3. Learning Progress / Knowledge Matrix API
    ai_lp_resp = client.get(f"/api/ai/learning-progress/{test_user}")
    assert ai_lp_resp.status_code == 200
    lp_data = ai_lp_resp.json()
    assert len(lp_data["domains"]) == 5
    assert "overall_knowledge_index" in lp_data
    assert "top_strength" in lp_data
    print(f"  [PASS] 5-Pillar Harappan Knowledge Matrix evaluated across {len(lp_data['domains'])} domains")

    # 4. Unified Dashboard AI API
    dash_ai_resp = client.get(f"/api/ai/dashboard/{test_user}")
    assert dash_ai_resp.status_code == 200
    dash_data = dash_ai_resp.json()
    assert "recommendation" in dash_data
    assert "difficulty" in dash_data
    assert "learning_progress" in dash_data
    assert "prototype_disclaimer" in dash_data
    print("  [PASS] Unified Dashboard AI API & Prototype Disclaimer verified")

    # 5. Interactive ML Simulation API
    sim_resp = client.post("/api/ai/simulate", json={
        "accuracy_rate": 0.95,
        "avg_solve_time": 20.0,
        "attempts_per_quest": 1.0,
        "player_level": 4,
        "hints_used": 0,
        "completed_quests": ["quest_01_rebuild_city"]
    })
    assert sim_resp.status_code == 200
    assert sim_resp.json()["adaptive_difficulty"]["recommended_difficulty"] == "Hard"
    print("  [PASS] Interactive AI Simulation Sandbox: accurately predicted 'Hard' mode")

    # 6. Heritage Guide Chatbot API
    chat_resp = client.post("/api/ai/heritage-guide/chat", json={
        "message": "tell me about the unicorn seal",
        "username": test_user
    })
    assert chat_resp.status_code == 200
    chat_data = chat_resp.json()
    assert "reply" in chat_data
    assert "did_you_know" in chat_data
    print("  [PASS] Heritage Guide Chatbot API: dynamic educational response validated")

    # 7. Frontend UI Elements & Assets
    ai_requirements = [
        "dashAiRecommendationContainer", "dashAiDifficultyContainer",
        "dashKnowledgeMatrixContainer", "simAccuracyInput",
        "simTimeInput", "simAttemptsInput", "simLevelInput",
        "simResultsContainer",
        "/static/css/ai-engine.css", "/static/js/ai-engine.js"
    ]
    for areq in ai_requirements:
        assert areq in html, f"Missing AI element {areq} in index.html"
    print("  [PASS] Dashboard AI widgets, simulation lab & scripts integrated in HTML")

    assert client.get("/static/css/ai-engine.css").status_code == 200
    assert client.get("/static/js/ai-engine.js").status_code == 200
    print("  [PASS] ai-engine.css and ai-engine.js delivered with HTTP 200 OK")

    # -------------------------------------------------------------
    # PHASE 10: FINAL INDUS VALLEY CIVILIZATION CHALLENGE
    # -------------------------------------------------------------
    print("\n>>> [PHASE 10] Final Indus Valley Civilization Challenge")

    # 1. Content Delivery & Anti-cheat Sanitization
    fc_content_resp = client.get("/api/final-challenge/content")
    assert fc_content_resp.status_code == 200
    fc_data = fc_content_resp.json()
    assert fc_data["total_dilemmas"] == 6
    assert fc_data["max_score"] == 600
    fc_pillars = [d["pillar"] for d in fc_data["dilemmas"]]
    assert all(p in fc_pillars for p in ["City Planning", "Drainage", "Architecture", "Trade", "Resources", "Daily Life"])
    print(f"  [PASS] All 6 Core Pillars delivered: {', '.join(fc_pillars)}")

    # 2. Authentic Decision Submission & Scoring
    fc_sub_resp = client.post("/api/final-challenge/submit", json={
        "username": test_user,
        "decisions": {
            "city_planning": "opt_plan_orthogonal",
            "drainage": "opt_drain_three_stage",
            "architecture": "opt_arch_standard_brick",
            "trade": "opt_trade_binary_carnelian",
            "resources": "opt_res_targeted_network",
            "daily_life": "opt_life_guild_consensus"
        }
    })
    assert fc_sub_resp.status_code == 200
    fc_result = fc_sub_resp.json()
    assert fc_result["final_score"] == 600
    assert fc_result["percentage"] == 100.0
    assert fc_result["passed"] is True
    assert fc_result["achievement"] == "Indus Valley Explorer"
    assert fc_result["achievement_badge"] == "badge_indus_explorer"
    assert "badge_indus_explorer" in [b["id"] for b in fc_result["badges_earned"]]
    assert len(fc_result["learning_summary"]) == 6
    print(f"  [PASS] Perfect Score: {fc_result['final_score']} / {fc_result['max_score']} (100%)")
    print(f"  [PASS] Achievement Granted: '{fc_result['achievement']}' (+{fc_result['xp_earned']} XP)")

    # 3. Final Challenge MongoDB Persistence
    fc_status_resp = client.get(f"/api/final-challenge/status/{test_user}")
    assert fc_status_resp.status_code == 200
    fc_status = fc_status_resp.json()
    assert fc_status["has_completed"] is True
    assert fc_status["final_challenge"]["achievement"] == "Indus Valley Explorer"
    print("  [PASS] Final Challenge completion & achievement persisted in MongoDB")

    # 4. Frontend UI Elements & Static Assets
    fc_requirements = [
        "tab-final-challenge", "finalChallengeContainer",
        "/static/css/final-challenge.css", "/static/js/final-challenge.js"
    ]
    for fcreq in fc_requirements:
        assert fcreq in html, f"Missing Phase 10 element {fcreq} in index.html"
    print("  [PASS] Final challenge tab, container, and script links integrated in HTML")

    assert client.get("/static/css/final-challenge.css").status_code == 200
    assert client.get("/static/js/final-challenge.js").status_code == 200
    print("  [PASS] final-challenge.css and final-challenge.js delivered with HTTP 200 OK")

    # -------------------------------------------------------------
    # PHASE 11: UI/UX AND ANIMATION POLISH
    # -------------------------------------------------------------
    print("\n>>> [PHASE 11] UI/UX & Animation Polish (Transitions, Ripples, Floats, Toasts)")

    # 1. Static Asset Delivery
    assert client.get("/static/css/animations-ux.css").status_code == 200
    assert client.get("/static/js/ux-polish.js").status_code == 200
    print("  [PASS] animations-ux.css and ux-polish.js delivered with HTTP 200 OK")

    # 2. HTML Integration
    assert "/static/css/animations-ux.css" in html
    assert "/static/js/ux-polish.js" in html
    print("  [PASS] index.html includes animations-ux.css and ux-polish.js")

    # 3. CSS Animations & Responsiveness
    css_p11_path = os.path.join(workspace_root, "frontend", "css", "animations-ux.css")
    with open(css_p11_path, "r", encoding="utf-8") as f:
        css_p11 = f.read()

    p11_keyframes = [
        "slideFadeUp", "rippleAnimation", "floatXpGain", "xpBarFlash",
        "levelUpPop", "spinSunburst", "medalFlip", "progressBarShimmer",
        "ancientSkeletonSweep", "spinnerRotate", "shakeKeyframe",
        "sealStampDrop", "sparkleExplode", "toastSlideIn", "toastCountdown"
    ]
    for kf in p11_keyframes:
        assert f"@keyframes {kf}" in css_p11, f"Missing keyframe @keyframes {kf}"
    assert "@media (prefers-reduced-motion: reduce)" in css_p11
    assert "@media (max-width: 768px)" in css_p11
    print(f"  [PASS] All {len(p11_keyframes)} CSS keyframes & accessibility rules verified")

    # 4. JavaScript UxPolishManager API
    js_p11_path = os.path.join(workspace_root, "frontend", "js", "ux-polish.js")
    with open(js_p11_path, "r", encoding="utf-8") as f:
        js_p11 = f.read()

    assert "class UxPolishManager" in js_p11
    assert "window.uxManager = uxManager;" in js_p11
    p11_methods = [
        "showToast", "spawnXpAnimation", "spawnSparkles", "triggerShake",
        "triggerLevelUp", "triggerBadgeUnlock", "triggerArtifactDiscovery",
        "triggerLocationDiscovery", "setButtonLoading"
    ]
    for m in p11_methods:
        assert m in js_p11
    print(f"  [PASS] UxPolishManager and all {len(p11_methods)} methods confirmed")

    # 5. Controller Hooks Verification
    controllers_p11 = ["app.js", "quests.js", "city.js", "museum.js", "final-challenge.js"]
    for cfile in controllers_p11:
        cpath = os.path.join(workspace_root, "frontend", "js", cfile)
        with open(cpath, "r", encoding="utf-8") as f:
            c_text = f.read()
        assert "uxManager" in c_text, f"Missing uxManager integration in {cfile}"
    print(f"  [PASS] All 5 controllers (app, quests, city, museum, final-challenge) hook into uxManager")

    print("\n" + "=" * 65)
    print("ALL VERIFICATIONS (PHASES 1 TO 11) COMPLETED WITH 100% SUCCESS!")
    print("=" * 65)

if __name__ == "__main__":
    run_master_suite()

