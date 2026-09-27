/**
 * =================================================================
 * BHARAT QUEST - PHASE 8: GAMIFICATION & PROGRESSION CONTROLLER
 * Level-Up Celebrations, Badges Showcase, and Mastery Tracking
 * =================================================================
 */

class BharatGamificationController {
  constructor() {
    this.activeBadgeFilter = 'all';
    this.cachedStatus = null;
    this.allBadges = [];
    this.allLevels = [];
  }

  async init() {
    console.log('[GAMIFICATION] Initializing Gamification & Progression Controller...');
    try {
      const [badgesRes, levelsRes] = await Promise.all([
        api.getAllBadges().catch(() => ({ badges: [] })),
        api.getAllLevels().catch(() => ({ tiers: [] }))
      ]);
      this.allBadges = badgesRes.badges || [];
      this.allLevels = levelsRes.tiers || [];
    } catch (err) {
      console.warn('[GAMIFICATION] Non-critical catalog pre-fetch notice:', err);
    }
  }

  /**
   * Triggers the Level-Up celebration modal with sound fanfare and particle rays.
   */
  showLevelUpModal(levelData) {
    if (window.audio) {
      try { audio.playFanfare(); } catch (e) {}
    }

    const modal = document.getElementById('levelUpModal');
    if (!modal) return;

    const levelNumEl = document.getElementById('levelUpNumber');
    const levelTitleEl = document.getElementById('levelUpTitle');
    const levelDescEl = document.getElementById('levelUpDesc');
    const perksContainer = document.getElementById('levelUpPerksList');

    const lvl = levelData.new_level || levelData.current_level || 2;
    const title = levelData.level_title || `Level ${lvl} Master`;
    const perks = levelData.unlocked_perks || [
      'New Ancient City Sectors Unlocked',
      'Advanced Archaeology Quests Available',
      'Virtual Museum Curatorial Access Expanded'
    ];

    if (levelNumEl) levelNumEl.innerText = lvl;
    if (levelTitleEl) levelTitleEl.innerText = `LEVEL ${lvl}: ${title.toUpperCase()}`;
    if (levelDescEl) {
      levelDescEl.innerText = `Outstanding archaeological deduction! Your excavation knowledge and historical mastery have ascended to Level ${lvl}.`;
    }

    if (perksContainer) {
      perksContainer.innerHTML = perks.map(p => `
        <div class="level-perk-item">
          <span class="level-perk-check">✦</span>
          <span>${p}</span>
        </div>
      `).join('');
    }

    modal.classList.add('active');
  }

  closeLevelUpModal() {
    const modal = document.getElementById('levelUpModal');
    if (modal) modal.classList.remove('active');
  }

  /**
   * Renders the 3-pillar IVC Mastery Overview Card
   */
  renderMasteryOverview(containerId, overallProg) {
    const container = document.getElementById(containerId);
    if (!container || !overallProg) return;

    const overallPct = overallProg.overall_percentage || 0;
    const q = overallProg.quests || { completed: 0, total: 5, weight_percentage: 0 };
    const a = overallProg.artifacts || { discovered: 0, total: 8, weight_percentage: 0 };
    const l = overallProg.locations || { explored: 0, total: 7, weight_percentage: 0 };

    const qPct = Math.min(100, Math.round((q.completed / q.total) * 100));
    const aPct = Math.min(100, Math.round((a.discovered / a.total) * 100));
    const lPct = Math.min(100, Math.round((l.explored / l.total) * 100));

    container.innerHTML = `
      <div class="mastery-overview-card">
        <div class="mastery-header">
          <div class="mastery-title-group">
            <h3>🏛️ Indus Valley Civilization Mastery</h3>
            <p>Overall Archaeological Exploration & Knowledge Synthesis</p>
          </div>
          <div class="mastery-badge-counter">
            <div class="mastery-badge-val">${overallPct}%</div>
            <div class="mastery-badge-lbl">Total Mastery</div>
          </div>
        </div>

        <div class="mastery-pillars-grid">
          <!-- Pillar 1: Quests -->
          <div class="mastery-pillar-box">
            <div class="pillar-top">
              <span class="pillar-name">📜 Quests Solved</span>
              <span class="pillar-ratio">${q.completed} / ${q.total}</span>
            </div>
            <div class="pillar-bar-bg">
              <div class="pillar-bar-fill pillar-bar-quests" style="width: ${qPct}%;"></div>
            </div>
            <div class="pillar-weight-text">${q.weight_percentage}% of total (35% weight)</div>
          </div>

          <!-- Pillar 2: Artifacts -->
          <div class="mastery-pillar-box">
            <div class="pillar-top">
              <span class="pillar-name">🏺 Relics Cataloged</span>
              <span class="pillar-ratio">${a.discovered} / ${a.total}</span>
            </div>
            <div class="pillar-bar-bg">
              <div class="pillar-bar-fill pillar-bar-artifacts" style="width: ${aPct}%;"></div>
            </div>
            <div class="pillar-weight-text">${a.weight_percentage}% of total (35% weight)</div>
          </div>

          <!-- Pillar 3: Sectors -->
          <div class="mastery-pillar-box">
            <div class="pillar-top">
              <span class="pillar-name">🧭 Sectors Surveyed</span>
              <span class="pillar-ratio">${l.explored} / ${l.total}</span>
            </div>
            <div class="pillar-bar-bg">
              <div class="pillar-bar-fill pillar-bar-locations" style="width: ${lPct}%;"></div>
            </div>
            <div class="pillar-weight-text">${l.weight_percentage}% of total (30% weight)</div>
          </div>
        </div>
      </div>
    `;
  }

  /**
   * Renders the interactive Badges Showcase with category filters & progress bars
   */
  renderBadgesShowcase(containerId, badgesList) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const badges = badgesList || [];
    const categories = ['all', ...new Set(badges.map(b => b.category))];

    const filtered = this.activeBadgeFilter === 'all'
      ? badges
      : badges.filter(b => b.category === this.activeBadgeFilter);

    const unlockedCount = badges.filter(b => b.unlocked).length;

    container.innerHTML = `
      <div class="badges-showcase-container">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
          <h4 style="font-family: 'Cinzel', serif; color: var(--color-terracotta-gold, #E9C46A); margin: 0;">
            🏅 Archaeological Medals & Badges (${unlockedCount} / ${badges.length} Unlocked)
          </h4>
        </div>

        <div class="badges-filter-bar">
          ${categories.map(cat => `
            <button class="badge-filter-btn ${this.activeBadgeFilter === cat ? 'active' : ''}"
                    onclick="gamificationController.filterBadges('${cat}', '${containerId}')">
              ${cat === 'all' ? 'All Medals' : cat}
            </button>
          `).join('')}
        </div>

        <div class="badges-grid">
          ${filtered.map(b => this.renderBadgeCardMarkup(b)).join('')}
        </div>
      </div>
    `;
  }

  filterBadges(category, containerId) {
    this.activeBadgeFilter = category;
    if (window.app && app.state.user) {
      this.renderBadgesShowcase(containerId, app.state.user.badges_details);
    }
  }

  renderBadgeCardMarkup(b) {
    const isUnlocked = b.unlocked;
    const progressMarkup = (!isUnlocked && b.progress_target)
      ? `
        <div style="margin-top: 6px;">
          <div style="display: flex; justify-content: space-between; font-size: 0.68rem; color: #D4A373; margin-bottom: 3px;">
            <span>Progress</span>
            <span>${b.progress_current || 0} / ${b.progress_target}</span>
          </div>
          <div style="width: 100%; height: 5px; background: rgba(255,255,255,0.08); border-radius: 3px; overflow: hidden;">
            <div style="height: 100%; background: #E9C46A; width: ${Math.round(((b.progress_current || 0) / b.progress_target) * 100)}%;"></div>
          </div>
        </div>
      `
      : '';

    return `
      <div class="badge-item-card ${isUnlocked ? 'unlocked' : 'locked'}">
        <div>
          <div class="badge-card-top">
            <div class="badge-icon-box">${isUnlocked ? b.icon : '🔒'}</div>
            <div class="badge-meta">
              <h5 class="badge-name">${b.name}</h5>
              <div class="badge-category">${b.category}</div>
            </div>
          </div>
          <p class="badge-desc">${b.description}</p>
        </div>

        <div>
          <div class="badge-criteria-box">
            <strong>Requirement:</strong> ${b.criteria || 'Complete game objectives'}
          </div>
          ${progressMarkup}
          <div style="margin-top: 8px;">
            <span class="badge-status-pill ${isUnlocked ? 'earned' : 'locked-pill'}">
              ${isUnlocked ? '✓ UNLOCKED & RECORDED' : '🔒 LOCKED'}
            </span>
          </div>
        </div>
      </div>
    `;
  }

  /**
   * Renders the Level Milestone Progression Roadmap
   */
  renderMilestoneRoadmap(containerId, currentLevel) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const tiers = this.allLevels.length > 0 ? this.allLevels : [
      { level: 1, title: 'Apprentice Explorer', min_xp: 0, unlocked_perks: ['Lower Town Grid Access', 'Public Museum Vitrines'] },
      { level: 2, title: 'Field Archaeologist', min_xp: 500, unlocked_perks: ['Citadel Mound & The Great Bath', 'Drainage Challenge Quest'] },
      { level: 3, title: 'Master Surveyor', min_xp: 1200, unlocked_perks: ['Life in Indus Valley Quest', 'Curatorial Audio Guide'] },
      { level: 4, title: 'Senior Epigraphist', min_xp: 2200, unlocked_perks: ['The Harappan Secret Inscription Chamber', 'Mohenjo-daro Epigraphic Vault'] },
      { level: 5, title: 'Living Heritage Sage', min_xp: 3500, unlocked_perks: ['Vedic Realm Expansion Sneak Peek', 'Golden Heritage Halo Honor'] }
    ];

    container.innerHTML = `
      <div class="milestones-roadmap">
        <h4 style="font-family: 'Cinzel', serif; color: var(--color-terracotta-gold, #E9C46A); margin: 0 0 10px 0;">
          🗺️ Level Progression & Archaeological Milestones
        </h4>
        ${tiers.map(t => {
          const isAchieved = currentLevel >= t.level;
          const isCurrent = currentLevel === t.level;
          return `
            <div class="milestone-step ${isAchieved ? 'achieved' : ''} ${isCurrent ? 'current' : ''}">
              <div class="milestone-lvl-circle">${t.level}</div>
              <div class="milestone-details">
                <div class="milestone-name">
                  ${t.title} ${isCurrent ? '⭐ (Current Level)' : ''}
                </div>
                <div class="milestone-xp">Requires: ${t.min_xp} XP</div>
                <div class="milestone-perks-list">
                  <strong>Unlocked Perks:</strong> ${(t.unlocked_perks || []).join(' • ')}
                </div>
              </div>
            </div>
          `;
        }).join('')}
      </div>
    `;
  }

  /**
   * Opens the Harappan Secret Inscription Chamber Modal (Level 4+ Secret Lore)
   */
  async openSecretArchiveModal() {
    try {
      const data = await api.getSecretArchive();
      const modal = document.getElementById('secretArchiveModal');
      const content = document.getElementById('secretArchiveContent');
      if (!modal || !content) return;

      content.innerHTML = (data.archive_entries || []).map(entry => `
        <div class="archive-entry-card">
          <div class="archive-entry-title">📜 ${entry.topic}</div>
          <div class="archive-entry-finding">${entry.finding}</div>
          <div class="archive-entry-insight">✦ ${entry.archaeological_insight}</div>
        </div>
      `).join('');

      modal.classList.add('active');
    } catch (err) {
      console.error('Error fetching secret archive:', err);
    }
  }

  closeSecretArchiveModal() {
    const modal = document.getElementById('secretArchiveModal');
    if (modal) modal.classList.remove('active');
  }
}

const gamificationController = new BharatGamificationController();
