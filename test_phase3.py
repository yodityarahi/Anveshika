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

def test_phase3():
    print("=" * 60)
    print("BHARAT QUEST - PHASE 3 VERIFICATION SUITE")
    print("=" * 60)
    
    client = TestClient(app)
    
    # 1. Test Civilizations API
    print("\n[1/5] Testing /api/ivc/civilizations endpoint...")
    resp = client.get("/api/ivc/civilizations")
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
    civs = resp.json()
    assert len(civs) == 5, f"Expected 5 civilizations, got {len(civs)}"
    
    ivc = next((c for c in civs if c["id"] == "ivc"), None)
    assert ivc is not None, "IVC not found in civilizations"
    assert ivc["status"] == "unlocked", "IVC should be unlocked"
    assert len(ivc["major_sites"]) >= 6, "IVC should feature at least 6 major sites"
    print(f"  [PASS] IVC Active: {ivc['name']} ({ivc['era']})")
    
    locked_civs = [c for c in civs if c["status"] == "locked"]
    assert len(locked_civs) == 4, f"Expected 4 locked civilizations for future scalability, got {len(locked_civs)}"
    for lc in locked_civs:
        print(f"  [PASS] Scalability Region Locked: {lc['name']} ({lc['era']})")

    # 2. Test Locations API
    print("\n[2/5] Testing /api/ivc/locations endpoint...")
    resp_loc = client.get("/api/ivc/locations")
    assert resp_loc.status_code == 200
    locations = resp_loc.json()
    assert len(locations) >= 5, "Locations list should contain ancient sites"
    print(f"  [PASS] {len(locations)} Ancient city locations available")

    # 3. Test Frontend HTML Markup
    print("\n[3/5] Testing frontend/index.html markup for Dashboard & Map...")
    index_path = workspace_root / "frontend" / "index.html"
    assert index_path.exists(), "frontend/index.html must exist"
    html_content = index_path.read_text(encoding="utf-8")
    
    # Check Dashboard elements (all 8 required items)
    required_dash_elements = [
        "dashPlayerName",        # Player name
        "dashAvatarRing",        # Avatar
        "dashLevelVal",          # Level
        "dashXpVal",             # XP progress
        "dashQuestsVal",         # Completed quests
        "dashArtifactsVal",      # Artifacts collected
        "dashBadgesVal",         # Badges
        "dashProgressPct",       # Progress percentage
        "dashOverallCircle",     # Overall progress radial
    ]
    for el in required_dash_elements:
        assert el in html_content, f"Dashboard element #{el} missing in index.html"
    print("  [PASS] All 8 required dashboard metrics present in index.html")
    
    # Check Interactive Map elements
    required_map_elements = [
        "bharatMapWrapper",      # Map wrapper
        "mapRegionIvc",          # Unlocked IVC region polygon
        "mapRegionVedic",        # Locked Vedic region
        "mapRegionMaurya",       # Locked Mauryan region
        "mapRegionGupta",        # Locked Gupta region
        "mapRegionChola",        # Locked Chola region
        "data-site=\"mohenjo-daro\"", # Mohenjo-daro pin
        "data-site=\"harappa\"",      # Harappa pin
        "data-site=\"lothal\"",       # Lothal pin
        "data-site=\"dholavira\"",    # Dholavira pin
        "data-site=\"kalibangan\"",   # Kalibangan pin
        "data-site=\"rakhigarhi\"",   # Rakhigarhi pin
        "mapHoverCard",          # Contextual hover card
        "ivcIntroModal",         # IVC introduction modal
        "enterIvcCity()",        # City transition trigger
        "/static/css/map.css",   # Map stylesheet
        "/static/js/audio.js",   # Audio engine
        "/static/js/map.js",     # Map controller
    ]
    for mel in required_map_elements:
        assert mel in html_content, f"Map element {mel} missing in index.html"
    print("  [PASS] Interactive India Map SVG, site pins, and IVC modal present in index.html")

    # 4. Test Frontend JavaScript Files
    print("\n[4/5] Testing frontend JS controllers...")
    map_js = (workspace_root / "frontend" / "js" / "map.js").read_text(encoding="utf-8")
    audio_js = (workspace_root / "frontend" / "js" / "audio.js").read_text(encoding="utf-8")
    app_js = (workspace_root / "frontend" / "js" / "app.js").read_text(encoding="utf-8")
    
    assert "class BharatMapController" in map_js
    assert "selectCivilization" in map_js
    assert "enterIvcCity" in map_js
    assert "window.mapController" in map_js
    print("  [PASS] BharatMapController verified")
    
    assert "class AncientAudioEngine" in audio_js
    assert "playGong" in audio_js
    assert "playChime" in audio_js
    assert "playLevelUp" in audio_js
    print("  [PASS] AncientAudioEngine verified")
    
    assert "calculateOverallProgress" in app_js
    assert "renderDashboard" in app_js
    assert "window.mapController.init()" in app_js
    print("  [PASS] BharatQuestApp Dashboard rendering & Map init verified")

    # 5. Test Static Route Mount
    print("\n[5/5] Testing static asset delivery via FastAPI...")
    map_css_resp = client.get("/static/css/map.css")
    assert map_css_resp.status_code == 200, "Failed to load /static/css/map.css"
    map_js_resp = client.get("/static/js/map.js")
    assert map_js_resp.status_code == 200, "Failed to load /static/js/map.js"
    audio_js_resp = client.get("/static/js/audio.js")
    assert audio_js_resp.status_code == 200, "Failed to load /static/js/audio.js"
    index_resp = client.get("/")
    assert index_resp.status_code == 200, "Failed to load root HTML"
    print("  [PASS] Static assets and root HTML served successfully")

    print("\n" + "=" * 60)
    print("ALL PHASE 3 VERIFICATIONS PASSED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    test_phase3()
