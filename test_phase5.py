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

def test_phase5():
    print("=" * 65)
    print("BHARAT QUEST - PHASE 5 INTERACTIVE ANCIENT CITY VERIFICATION")
    print("=" * 65)
    
    client = TestClient(app)
    
    # 1. Test /api/ivc/locations Endpoint
    print("\n[1/5] Testing /api/ivc/locations endpoint...")
    resp = client.get("/api/ivc/locations")
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
    locations = resp.json()
    
    assert len(locations) == 7, f"Expected 7 locations, got {len(locations)}"
    print(f"  [PASS] /api/ivc/locations delivered {len(locations)} authentic ancient city sectors")

    # 2. Verify all 7 required locations and metadata
    print("\n[2/5] Verifying 7 mandatory locations, inspectable relics, and quests...")
    required_locations = {
        "residential_area": "Residential Area",
        "main_street": "Main Street",
        "drainage_system": "Drainage System",
        "great_bath": "Great Bath",
        "granary_area": "Storage/Granary Area",
        "marketplace": "Marketplace",
        "craft_workshop": "Craft Workshop"
    }

    found_ids = {loc["id"]: loc for loc in locations}
    
    for loc_id, loc_name in required_locations.items():
        assert loc_id in found_ids, f"Missing required location: {loc_id} ({loc_name})"
        loc = found_ids[loc_id]
        
        # Verify historical explanation
        assert "historical_explanation" in loc and len(loc["historical_explanation"]) > 40, f"Missing or short explanation for {loc_id}"
        
        # Verify inspectable objects (minimum 3 objects per location)
        objects = loc.get("interactive_objects", [])
        assert len(objects) >= 3, f"Expected >= 3 inspectable objects in {loc_id}, got {len(objects)}"
        for obj in objects:
            assert all(k in obj for k in ["id", "name", "category", "description", "archaeological_fact", "xp_reward"]), f"Malformed object in {loc_id}: {obj}"
            assert obj["xp_reward"] >= 25, f"XP reward too low in {obj['id']}"

        # Verify quests
        quests = loc.get("quests", [])
        assert len(quests) >= 1, f"Expected >= 1 quest in {loc_id}"
        for q in quests:
            assert all(k in q for k in ["id", "title", "description", "reward_xp", "reward_tokens"]), f"Malformed quest in {loc_id}: {q}"

        # Verify discovery reward
        reward = loc.get("discovery_reward", {})
        assert reward.get("xp", 0) >= 50, f"Discovery XP too low in {loc_id}"
        assert reward.get("tokens", 0) >= 3, f"Discovery tokens too low in {loc_id}"
        
        # Verify coordinates and zone
        assert "coordinates" in loc and "x" in loc["coordinates"] and "y" in loc["coordinates"]
        assert loc.get("zone") in ["Citadel", "Lower Town"]
        
        print(f"  [PASS] Location '{loc['name']}' verified ({len(objects)} inspectable relics, {len(quests)} quests, {loc['zone']})")

    # 3. Test Frontend HTML Markup
    print("\n[3/5] Testing frontend/index.html for 2D City Stage, Inspector Modal & Discovery Toast...")
    index_path = workspace_root / "frontend" / "index.html"
    assert index_path.exists()
    html = index_path.read_text(encoding="utf-8")
    
    city_elements = [
        "cityStageContainer",        # City stage mount container
        "cityInspectorModal",        # Location inspector modal
        "inspectorIcon",             # Inspector header icon
        "inspectorTitle",            # Inspector header title
        "inspectorZone",             # Inspector header zone pill
        "inspectorHistoryText",      # Historical explanation container
        "inspectableObjectsGrid",    # Inspectable relics container
        "inspectorQuestsContainer",  # Quests container
        "cityDiscoveryToast",        # Discovery banner toast
        "/static/css/city.css",      # City stylesheet link
        "/static/js/city.js"         # City controller script
    ]
    for el in city_elements:
        assert el in html, f"Missing city element in index.html: {el}"
    print("  [PASS] City Stage Container, Inspector Modal, and Discovery Toast verified in index.html")

    # 4. Test City JavaScript Controller & CSS
    print("\n[4/5] Testing city.js controller and city.css...")
    city_js = (workspace_root / "frontend" / "js" / "city.js").read_text(encoding="utf-8")
    city_css = (workspace_root / "frontend" / "css" / "city.css").read_text(encoding="utf-8")
    
    # Check JS Controller
    assert "class AncientCityController" in city_js
    assert "renderCityStage" in city_js
    assert "generateCitySvg" in city_js
    assert "selectLocation" in city_js
    assert "inspectObject" in city_js
    assert "filterLocations" in city_js
    assert "showFloatingXp" in city_js
    assert "showDiscoveryToast" in city_js
    assert "registerLocation" in city_js
    assert "window.cityController" in city_js
    print("  [PASS] AncientCityController verified with SVG engine, object inspector & discovery rewards")
    
    # Check CSS
    assert ".city-exploration-container" in city_css
    assert ".city-viewport-card" in city_css
    assert ".city-svg-stage" in city_css
    assert ".city-location-zone" in city_css
    assert ".bath-water-ripple" in city_css
    assert ".kiln-smoke-particle" in city_css
    assert ".floating-xp-particle" in city_css
    assert ".discovery-toast-banner" in city_css
    assert ".city-inspector-modal" in city_css
    print("  [PASS] city.css verified with SVG styling, water ripples, smoke and particle animations")

    # 5. Test Static Delivery
    print("\n[5/5] Testing static asset delivery via FastAPI...")
    css_res = client.get("/static/css/city.css")
    assert css_res.status_code == 200
    js_res = client.get("/static/js/city.js")
    assert js_res.status_code == 200
    print("  [PASS] /static/css/city.css and /static/js/city.js delivered successfully")

    print("\n" + "=" * 65)
    print("ALL PHASE 5 ANCIENT CITY VERIFICATIONS PASSED!")
    print("=" * 65)

if __name__ == "__main__":
    test_phase5()
