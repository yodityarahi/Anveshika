"""
=================================================================
BHARAT QUEST - PHASE 11 VERIFICATION SUITE
UI/UX and Animation Polish Across the Entire Application
(Transitions, Ripples, XP Float, Level-Up, Badges, Modals, Toasts)
=================================================================
"""
import sys
import os
import re

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

def test_static_asset_delivery():
    print("\n--- [TEST 1] Static Asset Delivery & HTML Integration ---")
    
    # 1. Verify animations-ux.css
    res_css = client.get("/static/css/animations-ux.css")
    assert res_css.status_code == 200, f"animations-ux.css returned {res_css.status_code}"
    assert "text/css" in res_css.headers.get("content-type", "")
    assert len(res_css.text) > 1000
    print("  [PASS] /static/css/animations-ux.css delivered with HTTP 200 OK")

    # 2. Verify ux-polish.js
    res_js = client.get("/static/js/ux-polish.js")
    assert res_js.status_code == 200, f"ux-polish.js returned {res_js.status_code}"
    assert any(t in res_js.headers.get("content-type", "") for t in ["javascript", "text/plain"])
    assert len(res_js.text) > 1000
    print("  [PASS] /static/js/ux-polish.js delivered with HTTP 200 OK")

    # 3. Verify index.html loads both assets
    res_html = client.get("/")
    assert res_html.status_code == 200
    html_content = res_html.text
    assert "animations-ux.css" in html_content
    assert "ux-polish.js" in html_content
    print("  [PASS] index.html successfully links animations-ux.css and ux-polish.js")


def test_css_animation_keyframe_specifications():
    print("\n--- [TEST 2] CSS Keyframes & Design Token Integrity ---")
    
    css_path = os.path.join(PROJECT_ROOT, "frontend", "css", "animations-ux.css")
    assert os.path.exists(css_path), "animations-ux.css does not exist!"
    
    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()

    # Required animations check
    expected_keyframes = [
        ("slideFadeUp", "Smooth page & card entry transition"),
        ("rippleAnimation", "Tactile button click ripple wave"),
        ("floatXpGain", "XP gain floating particle animation"),
        ("xpBarFlash", "HUD progress bar surge illumination"),
        ("levelUpPop", "Level-up spring modal pop-in"),
        ("spinSunburst", "Level-up rotating celestial sunburst"),
        ("medalFlip", "3D Badge unlock medal rotation"),
        ("progressBarShimmer", "Fluid progress bar light sweep"),
        ("ancientSkeletonSweep", "Terracotta skeleton loading placeholder shimmer"),
        ("spinnerRotate", "Indus Harappan wheel loading spinner"),
        ("shakeKeyframe", "Error input validation tactile shake"),
        ("sealStampDrop", "Quest completion ancient seal stamp drop"),
        ("sparkleExplode", "Celebratory victory sparkle burst"),
        ("toastSlideIn", "Ancient toast notification entry slide"),
        ("toastCountdown", "Toast timer bar indicator")
    ]

    for keyframe, desc in expected_keyframes:
        assert f"@keyframes {keyframe}" in css, f"Missing keyframe @keyframes {keyframe} ({desc})"
        print(f"  [PASS] Keyframe verified: @keyframes {keyframe} ({desc})")

    # Accessibility and Mobile responsiveness check
    assert "@media (prefers-reduced-motion: reduce)" in css
    print("  [PASS] prefers-reduced-motion accessibility safeguard verified")

    assert "@media (max-width: 768px)" in css
    assert "@media (max-width: 480px)" in css
    print("  [PASS] Responsive layout rules for tablets & mobile viewports verified")

    assert "min-height: 44px" in css
    print("  [PASS] Accessible 44px touch targets enforced for mobile devices")


def test_ux_polish_javascript_architecture():
    print("\n--- [TEST 3] JavaScript UxPolishManager API Integrity ---")
    
    js_path = os.path.join(PROJECT_ROOT, "frontend", "js", "ux-polish.js")
    assert os.path.exists(js_path), "ux-polish.js does not exist!"
    
    with open(js_path, "r", encoding="utf-8") as f:
        js = f.read()

    # Core manager class and singleton check
    assert "class UxPolishManager" in js
    assert "window.uxManager = uxManager;" in js
    print("  [PASS] UxPolishManager and window.uxManager singleton initialized")

    # Required API methods check
    expected_methods = [
        "showToast",
        "spawnXpAnimation",
        "spawnSparkles",
        "triggerShake",
        "triggerLevelUp",
        "triggerBadgeUnlock",
        "triggerArtifactDiscovery",
        "triggerLocationDiscovery",
        "setButtonLoading",
        "attachButtonRipples",
        "attachFormShakeHandlers"
    ]

    for m in expected_methods:
        pattern = rf"{m}\s*\("
        assert re.search(pattern, js), f"Missing method {m} in ux-polish.js"
        print(f"  [PASS] UxManager method verified: {m}()")


def test_cross_controller_ux_hooks():
    print("\n--- [TEST 4] Cross-Controller UX Polish Hooks Verification ---")
    
    controllers = {
        "app.js": ["uxManager.showToast", "uxManager.triggerShake", "uxManager.spawnXpAnimation"],
        "quests.js": ["uxManager.spawnXpAnimation", "uxManager.showToast", "uxManager.triggerBadgeUnlock"],
        "city.js": ["uxManager.spawnXpAnimation", "uxManager.triggerLocationDiscovery", "uxManager.showToast"],
        "museum.js": ["uxManager.triggerArtifactDiscovery", "uxManager.showToast"],
        "final-challenge.js": ["uxManager.spawnXpAnimation", "uxManager.triggerBadgeUnlock", "uxManager.triggerShake"]
    }

    for fname, hooks in controllers.items():
        fpath = os.path.join(PROJECT_ROOT, "frontend", "js", fname)
        assert os.path.exists(fpath), f"{fname} not found!"
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        for hook in hooks:
            assert hook in content, f"Missing hook '{hook}' in {fname}"
        print(f"  [PASS] {fname} successfully integrates {len(hooks)} uxManager hook(s): {', '.join(hooks)}")


def run_all_phase11_tests():
    print("\n" + "=" * 65)
    print("   BHARAT QUEST - PHASE 11 COMPREHENSIVE TEST EXECUTION")
    print("=" * 65)
    
    test_static_asset_delivery()
    test_css_animation_keyframe_specifications()
    test_ux_polish_javascript_architecture()
    test_cross_controller_ux_hooks()

    print("\n" + "=" * 65)
    print("  ALL PHASE 11 UI/UX AND ANIMATION POLISH TESTS PASSED (4/4)")
    print("=" * 65)

if __name__ == "__main__":
    run_all_phase11_tests()
