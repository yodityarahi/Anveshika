/**
 * =================================================================
 * BHARAT QUEST - PHASE 10: FINAL INDUS VALLEY CIVILIZATION CHALLENGE
 * Interactive Municipal Governor Simulation & Graduation Controller
 * =================================================================
 */

class BharatFinalChallengeController {
  constructor() {
    this.dilemmas = [];
    this.currentIndex = 0;
    this.userDecisions = {};
    this.resultData = null;
    this.isSubmitting = false;
  }

  async init() {
    console.log("Initializing BharatFinalChallengeController (Phase 10)...");
  }

  async loadChallenge() {
    const container = document.getElementById("finalChallengeContainer");
    if (!container) return;

    const user = app.getCurrentUser();
    if (!user) {
      container.innerHTML = `
        <div class="skeleton-card" style="text-align: center; padding: 40px;">
          <h3>Explorer Sign-In Required</h3>
          <p style="color: #D6C7BC; margin: 10px 0 20px 0;">
            Please sign in or register your archaeological profile to undertake the Final Indus Valley Civilization Challenge.
          </p>
          <button class="ancient-btn btn-primary" onclick="app.openAuthModal('login')">
            <span>👤 Sign In to Begin</span>
          </button>
        </div>
      `;
      return;
    }

    try {
      container.innerHTML = `<div class="skeleton-card">Unearthing the Grand Harappan Metropolis Challenge...</div>`;
      
      // Check if user already took the challenge
      const statusRes = await api.getFinalChallengeStatus(user.username);
      if (statusRes.has_completed && statusRes.final_challenge) {
        this.renderCompletionSummary(statusRes.final_challenge, statusRes.stats_snapshot, statusRes.learning_summary);
        return;
      }

      const res = await api.getFinalChallengeContent();
      this.dilemmas = res.dilemmas || [];
      this.currentIndex = 0;
      this.userDecisions = {};
      this.renderChallengeView();
    } catch (err) {
      console.error("Failed to load final challenge:", err);
      container.innerHTML = `
        <div class="alert-banner" style="display:block;">
          Failed to load the Final Challenge. Please verify backend connection. (${err.message})
        </div>
      `;
    }
  }

  renderChallengeView() {
    const container = document.getElementById("finalChallengeContainer");
    if (!container) return;

    if (!this.dilemmas || this.dilemmas.length === 0) {
      container.innerHTML = `<div class="alert-banner" style="display:block;">No challenge dilemmas found.</div>`;
      return;
    }

    container.innerHTML = `
      <div class="challenge-container">
        <!-- Challenge Header Hero -->
        <div class="challenge-hero-card">
          <div class="challenge-hero-header">
            <div class="challenge-title-group">
              <span class="challenge-badge-tag">👑 CAPSTONE ARCHAEOLOGICAL TRIAL</span>
              <h2>The Grand Harappan Metropolis Restoration</h2>
              <p>
                As Chief Municipal Overseer, resolve 6 critical municipal dilemmas facing the ancient metropolis. 
                Apply what you have mastered in urban planning, drainage, masonry architecture, maritime trade, georesources, and egalitarian daily life.
              </p>
            </div>
            <div style="text-align: right;">
              <span style="font-size: 0.8rem; color: #E9C46A; font-weight: 700;">CAPSTONE REWARD:</span>
              <div style="font-size: 1.1rem; color: #FFF; font-weight: 700; display: flex; align-items: center; gap: 6px; justify-content: flex-end; margin-top: 4px;">
                <span>🎖️ Indus Valley Explorer</span>
                <span style="color: #2EC4B6; font-size: 0.85rem;">(+500 XP)</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 6-Step Indicator Bar -->
        <div class="challenge-stepper" id="challengeStepper"></div>

        <!-- Active Dilemma Stage -->
        <div id="activeDilemmaStage"></div>

        <!-- Navigation Actions -->
        <div class="challenge-actions-bar" id="challengeActionsBar"></div>
      </div>
    `;

    this.renderStepper();
    this.renderCurrentDilemma();
  }

  renderStepper() {
    const stepper = document.getElementById("challengeStepper");
    if (!stepper) return;

    stepper.innerHTML = this.dilemmas.map((d, idx) => {
      let stateClass = "";
      if (idx === this.currentIndex) stateClass = "active";
      else if (this.userDecisions[d.id]) stateClass = "completed";

      return `
        <div class="step-item ${stateClass}" onclick="finalChallengeController.goToStep(${idx})" title="${d.title}">
          <div class="step-circle">${d.icon || (idx + 1)}</div>
          <span class="step-label">${d.pillar}</span>
        </div>
      `;
    }).join("");
  }

  renderCurrentDilemma() {
    const stage = document.getElementById("activeDilemmaStage");
    const actionsBar = document.getElementById("challengeActionsBar");
    if (!stage || !actionsBar) return;

    const dilemma = this.dilemmas[this.currentIndex];
    const selectedOptId = this.userDecisions[dilemma.id];

    // Generate responsive visual SVG stage
    const svgVisual = this.getSvgForDilemma(dilemma.id);

    stage.innerHTML = `
      <div class="dilemma-card">
        <div class="dilemma-header">
          <div class="dilemma-icon-box">${dilemma.icon}</div>
          <div class="dilemma-meta-title">
            <span>Dilemma ${this.currentIndex + 1} of ${this.dilemmas.length} • Pillar: ${dilemma.pillar}</span>
            <h3>${dilemma.title}</h3>
          </div>
        </div>

        <div class="dilemma-premise-box">
          <strong>📜 Municipal Dilemma:</strong> ${dilemma.historical_premise}
        </div>

        <div class="dilemma-context-box">
          <strong>🏛️ Archaeological Insight:</strong> ${dilemma.archaeological_context}
        </div>

        <!-- Interactive Visual Stage -->
        <div class="dilemma-visual-stage">
          ${svgVisual}
        </div>

        <div class="dilemma-instruction">
          👉 ${dilemma.interactive_instruction}
        </div>

        <!-- Options Grid -->
        <div class="options-grid">
          ${dilemma.options.map(opt => `
            <div class="decision-option-card ${selectedOptId === opt.id ? 'selected' : ''}"
                 onclick="finalChallengeController.selectOption('${dilemma.id}', '${opt.id}')">
              <div class="option-radio-ring">
                <div class="option-radio-dot"></div>
              </div>
              <div class="option-content">
                <div class="option-title">${opt.title}</div>
                <div class="option-tagline">${opt.tagline}</div>
                <div class="option-desc">${opt.description}</div>
              </div>
            </div>
          `).join("")}
        </div>
      </div>
    `;

    // Actions Bar
    const isFirst = this.currentIndex === 0;
    const isLast = this.currentIndex === this.dilemmas.length - 1;
    const allAnswered = this.dilemmas.every(d => !!this.userDecisions[d.id]);

    actionsBar.innerHTML = `
      <button class="ancient-btn btn-outline" onclick="finalChallengeController.prevDilemma()" ${isFirst ? 'disabled' : ''}>
        <span>⬅️ Previous Dilemma</span>
      </button>

      <div style="font-size: 0.85rem; color: #D4A373; font-weight: 600;">
        Decisions Made: ${Object.keys(this.userDecisions).length} / ${this.dilemmas.length}
      </div>

      ${isLast ? `
        <button class="ancient-btn btn-primary" onclick="finalChallengeController.submitChallenge()" ${!allAnswered ? 'disabled' : ''}>
          <span>👑 Finalize Decisions & Graduate</span>
        </button>
      ` : `
        <button class="ancient-btn btn-primary" onclick="finalChallengeController.nextDilemma()">
          <span>Next Dilemma ➔</span>
        </button>
      `}
    `;
  }

  selectOption(dilemmaId, optionId) {
    this.userDecisions[dilemmaId] = optionId;
    if (typeof soundSynthesizer !== 'undefined') {
      soundSynthesizer.playClick();
    }
    this.renderStepper();
    this.renderCurrentDilemma();
  }

  prevDilemma() {
    if (this.currentIndex > 0) {
      this.currentIndex--;
      this.renderStepper();
      this.renderCurrentDilemma();
    }
  }

  nextDilemma() {
    if (this.currentIndex < this.dilemmas.length - 1) {
      this.currentIndex++;
      this.renderStepper();
      this.renderCurrentDilemma();
    }
  }

  goToStep(index) {
    if (index >= 0 && index < this.dilemmas.length) {
      this.currentIndex = index;
      this.renderStepper();
      this.renderCurrentDilemma();
    }
  }

  async submitChallenge() {
    const user = app.getCurrentUser();
    if (!user) return;

    const unanswered = this.dilemmas.filter(d => !this.userDecisions[d.id]);
    if (unanswered.length > 0) {
      if (window.uxManager) {
        uxManager.triggerShake("#challengeActionsBar");
        uxManager.showToast({
          title: "Incomplete Municipal Survey",
          message: `Please resolve all 6 municipal dilemmas before submitting. Missing: ${unanswered.map(u => u.pillar).join(", ")}`,
          icon: "⚠️",
          type: "warning"
        });
      } else {
        alert(`Please resolve all 6 municipal dilemmas before submitting. Missing: ${unanswered.map(u => u.pillar).join(", ")}`);
      }
      return;
    }

    try {
      this.isSubmitting = true;
      const stage = document.getElementById("activeDilemmaStage");
      if (stage) {
        stage.innerHTML = `
          <div class="skeleton-card" style="text-align: center; padding: 40px;">
            <div class="ancient-spinner" style="margin: 0 auto 16px auto;"></div>
            <h4>Evaluating Harappan Municipal Governance...</h4>
            <p style="color: var(--color-sandstone); margin-top: 8px;">Synthesizing city planning, drainage, and trade records into your official archaeological dossier.</p>
          </div>
        `;
      }

      const res = await api.submitFinalChallenge(user.username, this.userDecisions);
      this.resultData = res;

      // Play fanfare
      if (typeof soundSynthesizer !== 'undefined') {
        soundSynthesizer.playCelebrationFanfare();
      }

      // Trigger Phase 11 Polish Animations
      if (window.uxManager) {
        uxManager.spawnXpAnimation(res.xp_earned);
        uxManager.triggerBadgeUnlock(res.achievement, "🎖️");
        if (res.level_up && res.level_up.level_up_occurred) {
          uxManager.triggerLevelUp(res.level_up.new_level, res.level_up.new_title);
        }
      }

      // Refresh HUD & user profile
      await app.fetchUserProfile(user.username);

      // Render Grand Graduation Summary
      this.renderGraduationModal(res);
    } catch (err) {
      console.error("Failed to submit final challenge:", err);
      if (window.uxManager) {
        uxManager.triggerShake("#activeDilemmaStage");
        uxManager.showToast({
          title: "Submission Error",
          message: err.message,
          icon: "❌",
          type: "error"
        });
      } else {
        alert("Submission error: " + err.message);
      }
      this.renderChallengeView();
    } finally {
      this.isSubmitting = false;
    }
  }

  renderGraduationModal(res) {
    const container = document.getElementById("finalChallengeContainer");
    if (!container) return;

    const scorePct = res.percentage;
    const passed = res.passed;

    container.innerHTML = `
      <div class="challenge-container">
        <div class="graduation-screen">
          <div class="grad-crest-banner">
            <span class="grad-laurel-badge">🎖️</span>
            <h2 class="grad-title">${passed ? 'Capstone Mastered: Indus Valley Explorer!' : 'Harappan Survey Completed'}</h2>
            <div class="grad-honorary-title">${res.honorary_title}</div>
            <p style="color: #D6C7BC; font-size: 0.95rem; margin-top: 10px; max-width: 680px; margin-left: auto; margin-right: auto;">
              By decree of the Harappan Civic Assembly, Explorer <strong>${res.username}</strong> has successfully resolved 
              the 6 foundational municipal dilemmas of the Indus-Saraswati Civilization.
            </p>
          </div>

          <!-- 4-Card Hero Metric Grid -->
          <div class="grad-metrics-grid">
            <div class="grad-metric-card">
              <div class="grad-metric-icon">🎯</div>
              <div class="grad-metric-value">${res.final_score} / ${res.max_score}</div>
              <div class="grad-metric-label">Final Score (${scorePct}%)</div>
            </div>

            <div class="grad-metric-card">
              <div class="grad-metric-icon">⚡</div>
              <div class="grad-metric-value">+${res.xp_earned} XP</div>
              <div class="grad-metric-label">XP Earned (Total: ${res.new_total_xp})</div>
            </div>

            <div class="grad-metric-card">
              <div class="grad-metric-icon">🏺</div>
              <div class="grad-metric-value">${res.artifacts_discovered_count} Relics</div>
              <div class="grad-metric-label">Museum Artifacts</div>
            </div>

            <div class="grad-metric-card">
              <div class="grad-metric-icon">📜</div>
              <div class="grad-metric-value">${res.quests_completed_count} Quests</div>
              <div class="grad-metric-label">Quests Mastered</div>
            </div>
          </div>

          <!-- Capstone Achievement Box -->
          <div style="background: rgba(233, 196, 106, 0.12); border: 2px solid #E9C46A; border-radius: 12px; padding: 18px 24px; margin: 20px 0; display: flex; align-items: center; gap: 16px;">
            <span style="font-size: 2.8rem;">👑</span>
            <div>
              <span style="font-size: 0.76rem; color: #2EC4B6; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;">FINAL CAPSTONE ACHIEVEMENT GRANTED</span>
              <h3 style="font-family: 'Cinzel', serif; color: #FFF; margin: 2px 0 4px 0; font-size: 1.3rem;">
                ${res.achievement} (Badge: #${res.achievement_badge})
              </h3>
              <p style="font-size: 0.84rem; color: #D6C7BC; margin: 0;">
                Awarded for synthesizing city planning, drainage engineering, brick standardization, Lothal maritime trade, georesource logistics, and egalitarian consensus.
              </p>
            </div>
          </div>

          <!-- Comprehensive Stats Strip: Badges & Explored Areas -->
          <div class="grad-stats-summary-strip">
            <div class="grad-stat-box">
              <div class="grad-stat-box-icon">🏆</div>
              <div class="grad-stat-box-text">
                <strong>${res.badges_earned_count} Badges Earned</strong>
                <span>${res.badges_earned.map(b => b.name).slice(0, 3).join(", ")}...</span>
              </div>
            </div>

            <div class="grad-stat-box">
              <div class="grad-stat-box-icon">🏛️</div>
              <div class="grad-stat-box-text">
                <strong>${res.areas_explored_count} / 7 Sectors Explored</strong>
                <span>All core Harappan excavated quarters surveyed</span>
              </div>
            </div>

            <div class="grad-stat-box">
              <div class="grad-stat-box-icon">🪙</div>
              <div class="grad-stat-box-text">
                <strong>+${res.seals_earned} Steatite Seals</strong>
                <span>Currency for Lothal maritime commerce</span>
              </div>
            </div>
          </div>

          <!-- Detailed 6-Pillar Learning Summary Dossier -->
          <div class="learning-summary-dossier">
            <div class="dossier-header">
              <span style="font-size: 1.4rem;">📚</span>
              <h4>Comprehensive Harappan Learning Summary</h4>
            </div>
            <div class="dossier-grid">
              ${Object.entries(res.learning_summary).map(([key, item]) => `
                <div class="dossier-item">
                  <h5>${item.title}</h5>
                  <p>${item.key_takeaway}</p>
                  <div class="dossier-evidence">📍 Evidence: ${item.archaeological_evidence}</div>
                </div>
              `).join("")}
            </div>
          </div>

          <!-- Decision Review List -->
          <div class="learning-summary-dossier" style="margin-top: 20px;">
            <div class="dossier-header">
              <span style="font-size: 1.4rem;">⚖️</span>
              <h4>Your Archaeological Decisions & Evaluations</h4>
            </div>
            <div class="evaluations-list">
              ${res.evaluations.map(ev => `
                <div class="eval-item ${ev.is_correct ? 'correct' : 'incorrect'}">
                  <div class="eval-item-top">
                    <span class="eval-item-pillar">${ev.icon} ${ev.pillar}: ${ev.title}</span>
                    <span class="eval-item-points">${ev.points_earned} / ${ev.max_points} pts</span>
                  </div>
                  <div style="font-size: 0.86rem; color: #FFF; font-weight: 600;">
                    Your Decision: "${ev.chosen_title}"
                  </div>
                  <div class="eval-feedback">
                    ${ev.feedback}
                  </div>
                </div>
              `).join("")}
            </div>
          </div>

          <!-- Actions: Print Certificate & Return to Hub -->
          <div class="certificate-actions">
            <button class="ancient-btn btn-primary" onclick="window.print()">
              <span>🖨️ Print / Save Official Certificate</span>
            </button>
            <button class="ancient-btn btn-secondary" onclick="app.switchTab('tab-profile')">
              <span>👤 View Updated Profile & Badges</span>
            </button>
            <button class="ancient-btn btn-outline" onclick="app.switchTab('tab-expedition')">
              <span>🧭 Return to Expedition Hub</span>
            </button>
          </div>
        </div>
      </div>
    `;
  }

  renderCompletionSummary(finalChallenge, stats, learningSummary) {
    const container = document.getElementById("finalChallengeContainer");
    if (!container) return;

    container.innerHTML = `
      <div class="challenge-container">
        <div class="graduation-screen">
          <div class="grad-crest-banner">
            <span class="grad-laurel-badge">🎖️</span>
            <h2 class="grad-title">Indus Valley Explorer</h2>
            <div class="grad-honorary-title">Challenge Completed (${finalChallenge.percentage}% Score)</div>
            <p style="color: #D6C7BC; font-size: 0.95rem; margin-top: 10px;">
              You have previously mastered the Final Indus Valley Civilization Challenge on 
              <strong>${new Date(finalChallenge.completed_at).toLocaleDateString()}</strong>.
            </p>
          </div>

          <!-- 4 Metrics -->
          <div class="grad-metrics-grid">
            <div class="grad-metric-card">
              <div class="grad-metric-icon">🎯</div>
              <div class="grad-metric-value">${finalChallenge.score} / ${finalChallenge.max_score}</div>
              <div class="grad-metric-label">Final Score (${finalChallenge.percentage}%)</div>
            </div>
            <div class="grad-metric-card">
              <div class="grad-metric-icon">⚡</div>
              <div class="grad-metric-value">${stats.total_xp} XP</div>
              <div class="grad-metric-label">Total Archaeology XP</div>
            </div>
            <div class="grad-metric-card">
              <div class="grad-metric-icon">🏺</div>
              <div class="grad-metric-value">${stats.artifacts_discovered_count} / 8 Relics</div>
              <div class="grad-metric-label">Artifacts Discovered</div>
            </div>
            <div class="grad-metric-card">
              <div class="grad-metric-icon">📜</div>
              <div class="grad-metric-value">${stats.quests_completed_count} / 5 Quests</div>
              <div class="grad-metric-label">Quests Completed</div>
            </div>
          </div>

          <!-- Learning Summary -->
          <div class="learning-summary-dossier">
            <div class="dossier-header">
              <span style="font-size: 1.4rem;">📚</span>
              <h4>Mastered Harappan Heritage Pillars</h4>
            </div>
            <div class="dossier-grid">
              ${Object.entries(learningSummary).map(([key, item]) => `
                <div class="dossier-item">
                  <h5>${item.title}</h5>
                  <p>${item.key_takeaway}</p>
                  <div class="dossier-evidence">📍 Evidence: ${item.archaeological_evidence}</div>
                </div>
              `).join("")}
            </div>
          </div>

          <div class="certificate-actions">
            <button class="ancient-btn btn-primary" onclick="window.print()">
              <span>🖨️ Print / Save Certificate</span>
            </button>
            <button class="ancient-btn btn-secondary" onclick="finalChallengeController.retakeChallenge()">
              <span>🔄 Retake Final Challenge</span>
            </button>
            <button class="ancient-btn btn-outline" onclick="app.switchTab('tab-expedition')">
              <span>🧭 Expedition Hub</span>
            </button>
          </div>
        </div>
      </div>
    `;
  }

  retakeChallenge() {
    this.userDecisions = {};
    this.currentIndex = 0;
    this.renderChallengeView();
  }

  getSvgForDilemma(dilemmaId) {
    switch (dilemmaId) {
      case "city_planning":
        return `
          <svg class="visual-blueprint-svg" viewBox="0 0 600 120">
            <!-- Grid avenues -->
            <rect width="600" height="120" fill="#140E0A" rx="8" />
            <!-- North-South Avenues -->
            <line x1="180" y1="10" x2="180" y2="110" stroke="#E9C46A" stroke-width="6" stroke-dasharray="4" />
            <line x1="380" y1="10" x2="380" y2="110" stroke="#E9C46A" stroke-width="6" stroke-dasharray="4" />
            <!-- East-West Street -->
            <line x1="20" y1="60" x2="580" y2="60" stroke="#E9C46A" stroke-width="6" />
            <!-- Western Elevated Citadel -->
            <rect x="30" y="20" width="120" height="80" fill="rgba(231,111,81,0.25)" stroke="#E76F51" stroke-width="2" rx="4" />
            <text x="90" y="55" fill="#E9C46A" font-size="11" font-weight="700" text-anchor="middle" font-family="'Cinzel', serif">CITADEL MOUND</text>
            <text x="90" y="72" fill="#D6C7BC" font-size="9" text-anchor="middle">(West Platform)</text>
            <!-- Lower Town Residential Blocks -->
            <rect x="210" y="20" width="140" height="35" fill="rgba(46,196,182,0.15)" stroke="#2EC4B6" stroke-width="1.5" rx="3" />
            <text x="280" y="42" fill="#B2DFDB" font-size="10" text-anchor="middle">Residential Block A</text>
            <rect x="210" y="65" width="140" height="45" fill="rgba(46,196,182,0.15)" stroke="#2EC4B6" stroke-width="1.5" rx="3" />
            <text x="280" y="92" fill="#B2DFDB" font-size="10" text-anchor="middle">Residential Block B</text>
            <!-- Artisan / Kiln Ward -->
            <rect x="410" y="20" width="160" height="80" fill="rgba(244,162,97,0.15)" stroke="#F4A261" stroke-width="1.5" rx="3" />
            <text x="490" y="55" fill="#F4A261" font-size="10" font-weight="700" text-anchor="middle">Artisan Kiln Ward</text>
            <text x="490" y="72" fill="#D6C7BC" font-size="9" text-anchor="middle">(Leeward Zone)</text>
            <!-- Wind Arrow -->
            <path d="M 520,10 L 570,10 L 560,5 M 570,10 L 560,15" stroke="#2EC4B6" stroke-width="2" fill="none" />
            <text x="470" y="13" fill="#2EC4B6" font-size="9" font-weight="700">Prevailing Wind</text>
          </svg>
        `;
      case "drainage":
        return `
          <svg class="visual-blueprint-svg" viewBox="0 0 600 120">
            <rect width="600" height="120" fill="#140E0A" rx="8" />
            <!-- House wall & chute -->
            <rect x="40" y="15" width="70" height="90" fill="rgba(231,111,81,0.2)" stroke="#E76F51" stroke-width="1.5" />
            <text x="75" y="45" fill="#E9C46A" font-size="9" text-anchor="middle">Bathroom</text>
            <path d="M 110,65 L 150,75" stroke="#F4A261" stroke-width="4" fill="none" />
            <!-- Settling Sump Jar -->
            <ellipse cx="170" cy="85" rx="18" ry="22" fill="rgba(233,196,106,0.25)" stroke="#E9C46A" stroke-width="2" />
            <text x="170" y="88" fill="#FFF" font-size="8" font-weight="700" text-anchor="middle">Sump Jar</text>
            <!-- Street Culvert -->
            <rect x="220" y="70" width="220" height="25" fill="#261812" stroke="#2EC4B6" stroke-width="2" />
            <!-- Removable Limestone Slabs -->
            <rect x="230" y="65" width="40" height="8" fill="#E9C46A" stroke="#140E0A" />
            <rect x="280" y="65" width="40" height="8" fill="#E9C46A" stroke="#140E0A" />
            <rect x="330" y="65" width="40" height="8" fill="#E9C46A" stroke="#140E0A" />
            <rect x="380" y="65" width="40" height="8" fill="#E9C46A" stroke="#140E0A" />
            <text x="330" y="86" fill="#2EC4B6" font-size="9" font-weight="700" text-anchor="middle">Covered Street Sewer Conduit</text>
            <!-- Outflow to Soakage Field -->
            <path d="M 440,82 L 490,82 L 530,95" stroke="#2EC4B6" stroke-width="3" stroke-dasharray="3" fill="none" />
            <circle cx="540" cy="95" r="14" fill="rgba(46,196,182,0.2)" stroke="#2EC4B6" stroke-width="1.5" />
            <text x="540" y="98" fill="#2EC4B6" font-size="8" text-anchor="middle">Soak Field</text>
          </svg>
        `;
      case "architecture":
        return `
          <svg class="visual-blueprint-svg" viewBox="0 0 600 120">
            <rect width="600" height="120" fill="#140E0A" rx="8" />
            <!-- Standard Brick 1:2:4 diagram -->
            <rect x="40" y="30" width="112" height="56" fill="#D4A373" stroke="#9A3412" stroke-width="2" rx="2" />
            <rect x="68" y="16" width="112" height="28" fill="#E9C46A" stroke="#9A3412" stroke-width="1.5" rx="2" />
            <text x="96" y="62" fill="#140E0A" font-size="11" font-weight="700" text-anchor="middle">1 : 2 : 4 RATIO</text>
            <text x="96" y="78" fill="#261812" font-size="8" text-anchor="middle">(7 x 14 x 28 cm)</text>
            <!-- Bitumen Seal Layer -->
            <rect x="220" y="25" width="140" height="70" fill="rgba(45,30,22,0.9)" stroke="#E9C46A" stroke-width="1.5" />
            <rect x="235" y="35" width="110" height="8" fill="#121212" stroke="#2EC4B6" stroke-width="1" />
            <text x="290" y="42" fill="#2EC4B6" font-size="7" font-weight="700" text-anchor="middle">Natural Bitumen Membrane</text>
            <rect x="235" y="48" width="110" height="40" fill="rgba(46,196,182,0.25)" stroke="#2EC4B6" />
            <text x="290" y="72" fill="#FFF" font-size="9" font-weight="700" text-anchor="middle">Great Bath Basin</text>
            <!-- Gypsum mortar tag -->
            <text x="480" y="55" fill="#E9C46A" font-size="10" font-weight="700" text-anchor="middle">English Interlocking Bond</text>
            <text x="480" y="75" fill="#D6C7BC" font-size="9" text-anchor="middle">Gypsum-Lime Mortar Joints</text>
          </svg>
        `;
      case "trade":
        return `
          <svg class="visual-blueprint-svg" viewBox="0 0 600 120">
            <rect width="600" height="120" fill="#140E0A" rx="8" />
            <!-- Lothal Ship -->
            <path d="M 50,85 C 90,85 130,95 160,75 C 140,55 90,55 60,65 Z" fill="#D4A373" stroke="#F4A261" stroke-width="2" />
            <line x1="105" y1="60" x2="105" y2="25" stroke="#E9C46A" stroke-width="3" />
            <path d="M 105,28 L 135,45 L 105,55 Z" fill="rgba(233,196,106,0.3)" stroke="#E9C46A" stroke-width="1" />
            <text x="105" y="105" fill="#F4A261" font-size="9" font-weight="700" text-anchor="middle">Lothal Merchant Galley</text>
            <!-- Chert binary balance scale -->
            <line x1="260" y1="65" x2="360" y2="65" stroke="#E9C46A" stroke-width="3" />
            <line x1="310" y1="35" x2="310" y2="90" stroke="#E9C46A" stroke-width="3" />
            <rect x="250" y="65" width="20" height="20" fill="#E9C46A" rx="2" />
            <text x="260" y="79" fill="#140E0A" font-size="8" font-weight="700" text-anchor="middle">16</text>
            <circle cx="350" cy="75" r="9" fill="#E76F51" />
            <text x="310" y="105" fill="#E9C46A" font-size="9" text-anchor="middle">Binary Chert Weights (1:2:4:8:16)</text>
            <!-- Steatite Unicorn Seal Bulla -->
            <rect x="440" y="35" width="50" height="50" fill="rgba(233,196,106,0.2)" stroke="#E9C46A" stroke-width="1.5" rx="4" />
            <text x="465" y="62" font-size="18" text-anchor="middle">🦏</text>
            <text x="535" y="55" fill="#FFF" font-size="10" font-weight="700">Ur & Dilmun</text>
            <text x="535" y="70" fill="#2EC4B6" font-size="8">Meluhha Seal Verified</text>
          </svg>
        `;
      case "resources":
        return `
          <svg class="visual-blueprint-svg" viewBox="0 0 600 120">
            <rect width="600" height="120" fill="#140E0A" rx="8" />
            <!-- Corridor Node 1: Shortugai -->
            <circle cx="100" cy="40" r="16" fill="rgba(46,196,182,0.25)" stroke="#2EC4B6" stroke-width="2" />
            <text x="100" y="44" font-size="12" text-anchor="middle">💎</text>
            <text x="100" y="70" fill="#2EC4B6" font-size="9" font-weight="700" text-anchor="middle">Shortugai (Oxus)</text>
            <text x="100" y="82" fill="#D6C7BC" font-size="8" text-anchor="middle">Azure Lapis Lazuli</text>
            <!-- Corridor Node 2: Khetri -->
            <circle cx="300" cy="60" r="16" fill="rgba(244,162,97,0.25)" stroke="#F4A261" stroke-width="2" />
            <text x="300" y="64" font-size="12" text-anchor="middle">🔥</text>
            <text x="300" y="90" fill="#F4A261" font-size="9" font-weight="700" text-anchor="middle">Khetri (Rajasthan)</text>
            <text x="300" y="102" fill="#D6C7BC" font-size="8" text-anchor="middle">Copper Smelting Ore</text>
            <!-- Corridor Node 3: Khambhat -->
            <circle cx="500" cy="50" r="16" fill="rgba(231,111,81,0.25)" stroke="#E76F51" stroke-width="2" />
            <text x="500" y="54" font-size="12" text-anchor="middle">🐚</text>
            <text x="500" y="80" fill="#E76F51" font-size="9" font-weight="700" text-anchor="middle">Khambhat (Gujarat)</text>
            <text x="500" y="92" fill="#D6C7BC" font-size="8" text-anchor="middle">Carnelian & Conch Shells</text>
            <!-- Connecting Trade Arrows -->
            <path d="M 120,45 Q 200,30 280,55" stroke="#E9C46A" stroke-width="2" stroke-dasharray="3" fill="none" />
            <path d="M 320,62 Q 410,75 480,55" stroke="#E9C46A" stroke-width="2" stroke-dasharray="3" fill="none" />
          </svg>
        `;
      case "daily_life":
        return `
          <svg class="visual-blueprint-svg" viewBox="0 0 600 120">
            <rect width="600" height="120" fill="#140E0A" rx="8" />
            <!-- Pillared Assembly Hall -->
            <rect x="60" y="25" width="160" height="70" fill="rgba(233,196,106,0.15)" stroke="#E9C46A" stroke-width="1.5" rx="4" />
            <circle cx="80" cy="45" r="4" fill="#E9C46A" />
            <circle cx="110" cy="45" r="4" fill="#E9C46A" />
            <circle cx="140" cy="45" r="4" fill="#E9C46A" />
            <circle cx="170" cy="45" r="4" fill="#E9C46A" />
            <circle cx="80" cy="75" r="4" fill="#E9C46A" />
            <circle cx="110" cy="75" r="4" fill="#E9C46A" />
            <circle cx="140" cy="75" r="4" fill="#E9C46A" />
            <circle cx="170" cy="75" r="4" fill="#E9C46A" />
            <text x="140" y="105" fill="#E9C46A" font-size="9" font-weight="700" text-anchor="middle">Pillared Civic Assembly Hall</text>
            <!-- Granary Ventilated Ducts -->
            <rect x="270" y="25" width="140" height="70" fill="rgba(244,162,97,0.15)" stroke="#F4A261" stroke-width="1.5" rx="4" />
            <rect x="280" y="40" width="120" height="8" fill="#140E0A" stroke="#F4A261" stroke-width="1" />
            <rect x="280" y="55" width="120" height="8" fill="#140E0A" stroke="#F4A261" stroke-width="1" />
            <text x="340" y="80" fill="#FFF" font-size="8" text-anchor="middle">Wheat & Barley Air Ducts</text>
            <text x="340" y="105" fill="#F4A261" font-size="9" font-weight="700" text-anchor="middle">Great Granary Reserve</text>
            <!-- Guild Balance Crest -->
            <circle cx="500" cy="60" r="28" fill="rgba(46,196,182,0.15)" stroke="#2EC4B6" stroke-width="2" />
            <text x="500" y="65" font-size="20" text-anchor="middle">⚖️</text>
            <text x="500" y="105" fill="#2EC4B6" font-size="9" font-weight="700" text-anchor="middle">Consensus Governance</text>
          </svg>
        `;
      default:
        return `<div style="text-align: center; color: #E9C46A;">Harappan Archaeological Survey Stage</div>`;
    }
  }
}

const finalChallengeController = new BharatFinalChallengeController();
