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

def test_phase7():
    print("=" * 65)
    print("BHARAT QUEST - PHASE 7 ARTIFACTS & VIRTUAL MUSEUM VERIFICATION")
    print("=" * 65)
    
    client = TestClient(app)
    
    # 1. Test /api/museum/artifacts endpoint
    print("\n[1/6] Testing /api/museum/artifacts catalog endpoint...")
    resp = client.get("/api/museum/artifacts")
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
    artifacts = resp.json()
    assert len(artifacts) >= 7, f"Expected >= 7 artifacts, got {len(artifacts)}"
    print(f"  [PASS] /api/museum/artifacts delivered {len(artifacts)} museum vitrine exhibits")

    # 2. Verify all 7 Required Categories and Mandated Curatorial Fields
    print("\n[2/6] Verifying 7 mandatory artifact categories and curatorial fields...")
    required_categories = {
        "seal": "Indus Valley Seal",
        "pottery": "Pottery",
        "figurine": "Terracotta figure",
        "brick": "Ancient brick",
        "tool": "Tool",
        "ornament": "Ornament",
        "trade": "Trade-related artifact"
    }

    found_categories = set(a["category"] for a in artifacts)
    for cat_key, cat_name in required_categories.items():
        assert cat_key in found_categories, f"Missing required artifact category: {cat_key} ({cat_name})"

    # Verify each artifact has all required fields
    mandatory_fields = [
        "artifact_id", "name", "category", "period", "region", "site",
        "material", "dimensions", "possible_purpose", "historical_significance",
        "interesting_fact", "discovered", "svg_type", "xp_reward"
    ]
    for a in artifacts:
        for f in mandatory_fields:
            assert f in a and a[f] is not None, f"Missing or null field '{f}' in artifact {a.get('artifact_id')}"
        print(f"  [PASS] [{a['category_label']}] '{a['name']}' ({a['site']} • {a['period']}) verified")

    # 3. Test /api/museum/artifacts/{artifact_id} detail endpoint
    print("\n[3/6] Testing /api/museum/artifacts/{artifact_id} detail endpoints...")
    test_art_id = "art_unicorn_seal"
    d_resp = client.get(f"/api/museum/artifacts/{test_art_id}")
    assert d_resp.status_code == 200
    detail = d_resp.json()
    assert detail["artifact_id"] == test_art_id
    assert "steatite" in detail["material"].lower()
    assert len(detail["possible_purpose"]) > 20
    assert len(detail["historical_significance"]) > 20
    assert len(detail["interesting_fact"]) > 20
    print(f"  [PASS] Curatorial file for '{detail['name']}' retrieved successfully")

    # 4. Test Discovery Mechanics, XP Award, and Duplicate Prevention in MongoDB
    print("\n[4/6] Testing relic excavation, XP awards & duplicate prevention in MongoDB...")
    test_player = "MeeraMuseumCurator"
    # Register test player
    client.post("/api/auth/register", json={
        "username": test_player,
        "age": 15,
        "avatar": "🏛️",
        "archetype": "Town Architect",
        "password": "pass"
    })

    # First discovery of pottery urn
    disc_resp = client.post("/api/museum/discover/art_painted_pottery", json={"username": test_player})
    assert disc_resp.status_code == 200
    d_data = disc_resp.json()
    assert d_data["success"] is True
    assert d_data["is_new"] is True
    assert d_data["xp_awarded"] == 75
    print(f"  [PASS] First excavation awarded +{d_data['xp_awarded']} XP for '{d_data['artifact']['name']}'")

    # Test DUPLICATE discovery attempt for same artifact
    dup_resp = client.post("/api/museum/discover/art_painted_pottery", json={"username": test_player})
    assert dup_resp.status_code == 200
    dup_data = dup_resp.json()
    assert dup_data["success"] is True
    assert dup_data["is_new"] is False
    assert dup_data["xp_awarded"] == 0, "Duplicate discovery must NOT award duplicate XP!"
    assert "already documented" in dup_data["message"].lower() or "already" in dup_data["message"].lower()
    print("  [PASS] Duplicate discovery safely blocked (0 XP awarded, collection state preserved)")

    # Verify MongoDB state
    prof_resp = client.get(f"/api/user/profile/{test_player}")
    assert prof_resp.status_code == 200
    p_data = prof_resp.json()
    assert "art_painted_pottery" in p_data["stats"]["discovered_artifacts"]
    assert p_data["stats"]["discovered_artifacts"].count("art_painted_pottery") == 1
    print("  [PASS] MongoDB profile verified: artifact saved without duplicate entries")

    # 5. Test Frontend HTML Markup
    print("\n[5/6] Testing frontend/index.html for Museum Hub, Vitrines & Modal markup...")
    index_path = workspace_root / "frontend" / "index.html"
    assert index_path.exists()
    html = index_path.read_text(encoding="utf-8")

    museum_html_elements = [
        "museumHubContainer",
        "museumArtifactModal",
        "museumModalTitle",
        "museumModalIcon",
        "museumModalSvgStage",
        "curatorialPurposeText",
        "curatorialSignificanceText",
        "curatorialFactText",
        "propPeriod",
        "propSite",
        "propMaterial",
        "propDimensions",
        "museumDiscoverActionBtn",
        "/static/css/museum.css",
        "/static/js/museum.js"
    ]
    for el in museum_html_elements:
        assert el in html, f"Missing museum element in index.html: {el}"
    print("  [PASS] Museum Gallery Hub, Vitrine Modal, and script links verified in index.html")

    # 6. Test Frontend Controller, CSS & Static Asset Delivery
    print("\n[6/6] Testing museum.js, museum.css & static asset delivery...")
    museum_js = (workspace_root / "frontend" / "js" / "museum.js").read_text(encoding="utf-8")
    museum_css = (workspace_root / "frontend" / "css" / "museum.css").read_text(encoding="utf-8")

    assert "class BharatMuseumController" in museum_js
    assert "generateArtifactSvg" in museum_js
    assert "openArtifactModal" in museum_js
    assert "discoverArtifact" in museum_js
    assert "playAudioGuide" in museum_js
    assert "window.museumController" in museum_js
    print("  [PASS] BharatMuseumController verified with SVG generator & curatorial modal")

    assert ".museum-hub-container" in museum_css
    assert ".museum-vitrine-card" in museum_css
    assert ".vitrine-pedestal" in museum_css
    assert ".vitrine-brass-plaque" in museum_css
    assert ".museum-modal-overlay" in museum_css
    assert ".curatorial-props-grid" in museum_css
    print("  [PASS] museum.css verified with glass vitrines, pedestals & spotlights")

    css_res = client.get("/static/css/museum.css")
    assert css_res.status_code == 200
    js_res = client.get("/static/js/museum.js")
    assert js_res.status_code == 200
    print("  [PASS] /static/css/museum.css and /static/js/museum.js delivered successfully")

    print("\n" + "=" * 65)
    print("ALL PHASE 7 VIRTUAL MUSEUM VERIFICATIONS PASSED!")
    print("=" * 65)

if __name__ == "__main__":
    test_phase7()
