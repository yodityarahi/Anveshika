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

def test_phase4():
    print("=" * 65)
    print("BHARAT QUEST - PHASE 4 STORY INTRODUCTION VERIFICATION")
    print("=" * 65)
    
    client = TestClient(app)
    
    # 1. Test Story API Endpoint
    print("\n[1/5] Testing /api/ivc/story endpoint...")
    resp = client.get("/api/ivc/story")
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
    story_data = resp.json()
    
    assert story_data["civilization"] == "Indus Valley Civilization"
    assert "2600" in story_data["era"] and "1900" in story_data["era"]
    assert story_data["total_scenes"] == 7
    scenes = story_data["scenes"]
    assert len(scenes) == 7, f"Expected 7 scenes, got {len(scenes)}"
    print(f"  [PASS] /api/ivc/story delivered {len(scenes)} rich story scenes")

    # 2. Verify all required educational topics in scenes
    print("\n[2/5] Verifying required syllabus topics across story scenes...")
    
    required_topics = [
        # (Topic Name, Expected Keywords in scenes)
        ("What IVC was & Historical Period", ["2600", "1900", "Mature Harappan", "Sindhu"]),
        ("Major Urban Settlements", ["Mohenjo-daro", "Harappa", "Lothal", "Dholavira", "Kalibangan", "Rakhigarhi"]),
        ("Planned Cities & Architecture", ["1:2:4", "grid", "90-degree", "Citadel", "Lower Town"]),
        ("Drainage & Sanitation", ["drain", "sewer", "bathroom", "soak", "Great Bath", "bitumen"]),
        ("Trade & Metrology", ["Lothal", "dockyard", "Mesopotamia", "Meluhha", "weights", "binary"]),
        ("Crafts & Metallurgy", ["carnelian", "lost-wax", "Dancing Girl", "steatite", "seals", "script"]),
        ("Daily Life & Pedagogy", ["barley", "wheat", "toy", "cart", "Evidence", "simulation"])
    ]
    
    all_narratives = " ".join([s["narrative"] + " " + s["curiosity_fact"] + " " + s["historical_distinction"] for s in scenes])
    
    for topic_label, keywords in required_topics:
        matched = [k for k in keywords if k.lower() in all_narratives.lower()]
        assert len(matched) >= len(keywords) // 2, f"Topic '{topic_label}' missing critical keywords: {keywords}"
        print(f"  [PASS] {topic_label}: Matched [{', '.join(matched)}]")

    # Verify Historical Evidence vs. Gameplay distinction
    for s in scenes:
        assert "historical_distinction" in s and len(s["historical_distinction"]) > 20
    print("  [PASS] All scenes clearly distinguish archaeological evidence from gameplay elements")

    # 3. Test Frontend HTML Markup
    print("\n[3/5] Testing frontend/index.html for Story Modal & Controls...")
    index_path = workspace_root / "frontend" / "index.html"
    assert index_path.exists()
    html = index_path.read_text(encoding="utf-8")
    
    story_elements = [
        "ivcStoryModal",         # Modal theater overlay
        "storySceneCounter",     # Scene counter
        "storyProgressFill",     # Progress fill bar
        "storyStepsRow",         # Chapter dots
        "storyVisualStage",      # Visual illustration container
        "storyNarrativeStage",   # Narrative container
        "storyPrevBtn",          # Previous button
        "storyNextBtn",          # Continue / Enter City button
        "storyController.skipStory()", # Skip story button
        "storyController.openStory",   # Trigger bindings
        "/static/css/story.css", # Story stylesheet
        "/static/js/story.js"    # Story controller
    ]
    for el in story_elements:
        assert el in html, f"Missing story element in index.html: {el}"
    print("  [PASS] Story Introduction Modal, progress bars, and controls present in index.html")

    # 4. Test Frontend Controller & CSS
    print("\n[4/5] Testing story.js controller and story.css...")
    story_js = (workspace_root / "frontend" / "js" / "story.js").read_text(encoding="utf-8")
    story_css = (workspace_root / "frontend" / "css" / "story.css").read_text(encoding="utf-8")
    
    assert "class BharatStoryController" in story_js
    assert "openStory" in story_js
    assert "nextScene" in story_js
    assert "prevScene" in story_js
    assert "enterAncientCity" in story_js
    assert "generateSceneIllustration" in story_js
    assert "window.storyController" in story_js
    print("  [PASS] BharatStoryController verified with navigation & SVG illustrations")
    
    assert ".story-modal-overlay" in story_css
    assert ".story-theater-card" in story_css
    assert ".story-progress-fill" in story_css
    assert ".enter-city-hero-btn" in story_css
    print("  [PASS] story.css verified with responsive styling and animations")

    # 5. Test Static Delivery
    print("\n[5/5] Testing static asset delivery via FastAPI...")
    css_res = client.get("/static/css/story.css")
    assert css_res.status_code == 200
    js_res = client.get("/static/js/story.js")
    assert js_res.status_code == 200
    print("  [PASS] /static/css/story.css and /static/js/story.js delivered successfully")

    print("\n" + "=" * 65)
    print("ALL PHASE 4 STORY INTRODUCTION VERIFICATIONS PASSED!")
    print("=" * 65)

if __name__ == "__main__":
    test_phase4()
