/**
 * =================================================================
 * BHARAT QUEST - PHASE 11: UI/UX & ANIMATION POLISH CONTROLLER
 * Feedback, Particle Effects, Toasts & Motion Coordinator
 * =================================================================
 */

class UxPolishManager {
  constructor() {
    this.toastContainer = null;
    this.isInitialized = false;
  }

  init() {
    if (this.isInitialized) return;
    console.log("Initializing UxPolishManager (Phase 11)...");

    this.ensureToastContainer();
    this.attachButtonRipples();
    this.attachFormShakeHandlers();
    this.isInitialized = true;
  }

  ensureToastContainer() {
    let container = document.getElementById("ancientToastContainer");
    if (!container) {
      container = document.createElement("div");
      container.id = "ancientToastContainer";
      container.className = "ancient-toast-container";
      document.body.appendChild(container);
    }
    this.toastContainer = container;
  }

  /**
   * Attaches tactile ripple click effect to ancient buttons and tabs
   */
  attachButtonRipples() {
    document.addEventListener("click", (e) => {
      const btn = e.target.closest(".ancient-btn, .nav-tab, .quick-user-btn, .auth-hud-btn");
      if (!btn) return;

      const rect = btn.getBoundingClientRect();
      const circle = document.createElement("span");
      const diameter = Math.max(rect.width, rect.height);
      const radius = diameter / 2;

      circle.style.width = circle.style.height = `${diameter}px`;
      circle.style.left = `${e.clientX - rect.left - radius}px`;
      circle.style.top = `${e.clientY - rect.top - radius}px`;
      circle.classList.add("ripple-wave");

      // Clean existing ripples
      const existing = btn.querySelector(".ripple-wave");
      if (existing) existing.remove();

      btn.appendChild(circle);
      setTimeout(() => circle.remove(), 600);
    });
  }

  attachFormShakeHandlers() {
    // Intercept form submit attempts with empty required fields
    document.addEventListener("invalid", (e) => {
      if (e.target && e.target.classList) {
        this.triggerShake(e.target);
      }
    }, true);
  }

  /**
   * Displays an ancient sandstone toast notification
   */
  showToast({ title, message, icon = "🏺", type = "info", duration = 4200 }) {
    this.ensureToastContainer();

    const toast = document.createElement("div");
    toast.className = `ancient-toast toast-${type}`;
    toast.innerHTML = `
      <div class="toast-icon">${icon}</div>
      <div class="toast-content">
        <div class="toast-title">${title}</div>
        <div class="toast-message">${message}</div>
      </div>
      <div class="toast-progress-bar" style="animation-duration: ${duration}ms;"></div>
    `;

    // Click to dismiss
    toast.addEventListener("click", () => this.dismissToast(toast));

    this.toastContainer.appendChild(toast);

    // Audio cue
    if (typeof soundSynthesizer !== "undefined") {
      if (type === "success") soundSynthesizer.playSuccessTone();
      else soundSynthesizer.playClick();
    }

    setTimeout(() => {
      this.dismissToast(toast);
    }, duration);
  }

  dismissToast(toast) {
    if (!toast || toast.classList.contains("hiding")) return;
    toast.classList.add("hiding");
    setTimeout(() => toast.remove(), 320);
  }

  /**
   * Spawns a floating +XP particle that drifts up and pulses the HUD
   */
  spawnXpAnimation(amount, originEventOrElement) {
    let x = window.innerWidth / 2;
    let y = window.innerHeight / 2;

    if (originEventOrElement) {
      if (originEventOrElement.clientX) {
        x = originEventOrElement.clientX;
        y = originEventOrElement.clientY;
      } else if (originEventOrElement.getBoundingClientRect) {
        const rect = originEventOrElement.getBoundingClientRect();
        x = rect.left + rect.width / 2;
        y = rect.top + rect.height / 2;
      }
    }

    const pill = document.createElement("div");
    pill.className = "floating-xp-pill";
    pill.innerHTML = `<span>⚡</span> <span>+${amount} XP</span>`;
    pill.style.left = `${Math.min(window.innerWidth - 120, Math.max(20, x - 50))}px`;
    pill.style.top = `${Math.max(40, y - 20)}px`;

    document.body.appendChild(pill);
    setTimeout(() => pill.remove(), 1250);

    // Flash the HUD XP bar
    const hudBar = document.getElementById("hudXpFill");
    if (hudBar) {
      hudBar.classList.remove("xp-bar-surge");
      void hudBar.offsetWidth; // Force reflow
      hudBar.classList.add("xp-bar-surge");
    }

    // Audio chime
    if (typeof soundSynthesizer !== "undefined") {
      soundSynthesizer.playTokenCollect();
    }

    // Spawn tiny sparkles
    this.spawnSparkles(x, y, 12);
  }

  /**
   * Spawns an explosion of golden & terracotta sparkles
   */
  spawnSparkles(x, y, count = 16) {
    const colors = ["#E9C46A", "#F4A261", "#E76F51", "#2EC4B6", "#FFF"];
    for (let i = 0; i < count; i++) {
      const s = document.createElement("div");
      s.className = "ancient-sparkle";
      s.style.left = `${x}px`;
      s.style.top = `${y}px`;
      s.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];

      const angle = (Math.PI * 2 * i) / count + (Math.random() * 0.4 - 0.2);
      const distance = 40 + Math.random() * 80;
      const tx = Math.cos(angle) * distance;
      const ty = Math.sin(angle) * distance;

      s.style.setProperty("--tx", `${tx}px`);
      s.style.setProperty("--ty", `${ty}px`);

      document.body.appendChild(s);
      setTimeout(() => s.remove(), 1100);
    }
  }

  /**
   * Shakes an element on error
   */
  triggerShake(elementOrSelector) {
    const el = typeof elementOrSelector === "string" 
      ? document.querySelector(elementOrSelector) 
      : elementOrSelector;
    if (!el) return;

    el.classList.remove("shake-error");
    void el.offsetWidth; // Reflow
    el.classList.add("shake-error");
    setTimeout(() => el.classList.remove("shake-error"), 500);

    if (typeof soundSynthesizer !== "undefined") {
      soundSynthesizer.playErrorTone();
    }
  }

  /**
   * Triggers Level-Up celebration feedback
   */
  triggerLevelUp(newLevel, levelTitle) {
    this.showToast({
      title: `LEVEL UP! LEVEL ${newLevel}`,
      message: `Promoted to ${levelTitle || 'Senior Harappan Scholar'}! New perks unlocked in profile.`,
      icon: "🌟",
      type: "success",
      duration: 6000
    });

    if (typeof soundSynthesizer !== "undefined") {
      soundSynthesizer.playCelebrationFanfare();
    }
    this.spawnSparkles(window.innerWidth / 2, window.innerHeight / 3, 28);
  }

  /**
   * Triggers Badge Unlock celebration feedback
   */
  triggerBadgeUnlock(badgeName, icon = "🏆") {
    this.showToast({
      title: "NEW BADGE UNLOCKED!",
      message: `You earned the "${badgeName}" hallmark of archaeological honor.`,
      icon: icon,
      type: "success",
      duration: 5000
    });

    if (typeof soundSynthesizer !== "undefined") {
      soundSynthesizer.playSuccessTone();
    }
    this.spawnSparkles(window.innerWidth / 2, window.innerHeight / 2, 20);
  }

  /**
   * Triggers Artifact Discovery celebration feedback
   */
  triggerArtifactDiscovery(artifactName, icon = "🏺", xp = 200) {
    this.showToast({
      title: "ARTIFACT UNEARTHED!",
      message: `Discovered "${artifactName}". Cataloged in your Living Virtual Museum vitrine. (+${xp} XP)`,
      icon: icon,
      type: "success",
      duration: 5000
    });

    this.spawnXpAnimation(xp);
  }

  /**
   * Triggers Location Survey celebration feedback
   */
  triggerLocationDiscovery(locationName, icon = "🏛️", xp = 75) {
    this.showToast({
      title: "ANCIENT SECTOR SURVEYED!",
      message: `Surveyed ${locationName}. Recorded in Harappan archaeological register. (+${xp} XP)`,
      icon: icon,
      type: "info",
      duration: 4000
    });

    this.spawnXpAnimation(xp);
  }

  /**
   * Manages button loading state
   */
  setButtonLoading(button, isLoading, loadingText = "Consulting Archaeological Archives...") {
    if (!button) return;
    if (isLoading) {
      button.dataset.originalHtml = button.innerHTML;
      button.classList.add("btn-loading");
      button.disabled = true;
      button.innerHTML = `
        <span class="ancient-spinner"></span>
        <span style="margin-left: 8px;">${loadingText}</span>
      `;
    } else {
      if (button.dataset.originalHtml) {
        button.innerHTML = button.dataset.originalHtml;
      }
      button.classList.remove("btn-loading");
      button.disabled = false;
    }
  }
}

const uxManager = new UxPolishManager();
window.uxManager = uxManager;

// Auto-initialize when DOM is ready
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", () => uxManager.init());
} else {
  uxManager.init();
}
