/**
 * Bharat Quest - App Controller & Tab Coordinator
 * Phase 2: Player Profile & Authentication System
 */
class BharatQuestApp {
  constructor() {
    this.state = {
      serverConnected: false,
      user: null
    };
  }

  async init() {
    console.log("Initializing Anveshika: Interactive Living Museum of Indian Heritage...");
    this.setupTabs();
    if (window.mapController) {
      window.mapController.init();
    }
    if (window.storyController) {
      window.storyController.init();
    }
    if (window.cityController) {
      window.cityController.init();
    }
    if (window.questController) {
      window.questController.init();
    }
    if (window.museumController) {
      window.museumController.init();
    }
    if (window.gamificationController) {
      await window.gamificationController.init();
    }
    if (window.aiController) {
      await window.aiController.init();
    }
    if (window.finalChallengeController) {
      await window.finalChallengeController.init();
    }
    await this.checkSystemHealth();
    await this.initUserSession();
  }

  setupTabs() {
    const tabs = document.querySelectorAll('.nav-tab');
    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        const targetId = tab.getAttribute('data-tab');
        this.switchTab(targetId);
      });
    });
  }

  switchTab(targetId) {
    const tabs = document.querySelectorAll('.nav-tab');
    tabs.forEach(t => {
      if (t.getAttribute('data-tab') === targetId) {
        t.classList.add('active');
      } else {
        t.classList.remove('active');
      }
    });

    document.querySelectorAll('.tab-pane').forEach(p => {
      if (p.id === targetId) {
        p.classList.add('active');
      } else {
        p.classList.remove('active');
      }
    });

    // Lazy load data when tab opens
    if (targetId === 'tab-profile') this.refreshCurrentProfile();
    if (targetId === 'tab-city') {
      if (window.cityController) {
        window.cityController.renderCityStage();
        window.cityController.updateDiscoveryCounters();
      }
    }
    if (targetId === 'tab-quests') {
      if (window.questController) {
        window.questController.renderQuestHub();
      } else {
        this.loadQuests();
      }
    }
    if (targetId === 'tab-museum') {
      if (window.museumController) {
        window.museumController.renderMuseumHub();
      } else {
        this.loadMuseum();
      }
    }
    if (targetId === 'tab-ai') {
      if (window.aiController) {
        window.aiController.renderHeritageGuide();
      }
    }
    if (targetId === 'tab-final-challenge') {
      if (window.finalChallengeController) {
        window.finalChallengeController.loadChallenge();
      }
    }
  }

  async initUserSession() {
    // Check if user is stored in localStorage
    const savedUsername = localStorage.getItem('anveshika_username') || localStorage.getItem('bq_username') || 'Arjun';
    try {
      this.logConsole(`Loading player profile: "${savedUsername}" from MongoDB...`);
      const profile = await api.getProfile(savedUsername);
      this.setUser(profile);
      this.logConsole(`[200 OK] Player profile "${profile.username}" (Level ${profile.stats.level}) loaded successfully.`);
    } catch (err) {
      // If profile does not exist yet, register a default explorer profile
      try {
        this.logConsole(`Creating initial explorer profile "${savedUsername}"...`);
        const newProfile = await api.register({
          username: savedUsername,
          age: 14,
          avatar: "🧑‍🎓",
          archetype: "Town Architect",
          password: "1234"
        });
        this.setUser(newProfile);
        this.logConsole(`[200 OK] Initial explorer profile created and persisted in MongoDB.`);
      } catch (regErr) {
        console.error("Initial profile setup failed:", regErr);
      }
    }
  }

  calculateOverallProgress(user) {
    if (!user || !user.stats) return 15;
    // Level progress contribution (max level 5 = 25%)
    const lvlScore = Math.min((user.stats.level || 1) / 5, 1) * 25;
    // Completed quests contribution (8 quests total = 25%)
    const questCount = (user.stats.completed_quests || []).length;
    const questScore = Math.min(questCount / 8, 1) * 25;
    // Discovered artifacts contribution (10 artifacts total = 25%)
    const artCount = (user.stats.discovered_artifacts || []).length;
    const artScore = Math.min(artCount / 10, 1) * 25;
    // Badges of honor contribution (8 badges total = 25%)
    const badgeCount = (user.stats.badges || []).length;
    const badgeScore = Math.min(badgeCount / 8, 1) * 25;
    
    return Math.min(Math.max(Math.round(lvlScore + questScore + artScore + badgeScore), 5), 100);
  }

  setUser(userData) {
    const oldLevel = this.state.previousLevel;
    const newLevel = userData.stats ? userData.stats.level : 1;
    
    // Trigger Level Up Celebration if level increased!
    if (oldLevel && newLevel > oldLevel) {
      if (window.gamificationController) {
        setTimeout(() => {
          gamificationController.showLevelUpModal({
            new_level: newLevel,
            level_title: (userData.level_progress && userData.level_progress.level_title) || `Level ${newLevel}`,
            unlocked_perks: (userData.level_progress && userData.level_progress.unlocked_perks) || []
          });
        }, 500);
      }
    }
    
    this.state.previousLevel = newLevel;
    this.state.user = userData;
    localStorage.setItem('anveshika_username', userData.username);
    localStorage.setItem('bq_username', userData.username);
    this.renderHUD(userData);
    this.renderDashboard(userData);
    this.renderProfile(userData);
    if (window.aiController && userData.username) {
      window.aiController.loadDashboardAi(userData.username);
    }
  }

  renderDashboard(user) {
    if (!user) return;
    const overallPct = user.overall_progress ? user.overall_progress.overall_percentage : (user.stats.progress_percentage || this.calculateOverallProgress(user));

    // Hero Profile Card
    const dashAvatar = document.getElementById('dashAvatarRing');
    const dashRank = document.getElementById('dashRankBadge');
    const dashName = document.getElementById('dashPlayerName');
    const dashArch = document.getElementById('dashArchetype');
    const dashOverallCirc = document.getElementById('dashOverallCircle');
    const dashOverallTxt = document.getElementById('dashOverallProgressText');

    if (dashAvatar) dashAvatar.innerText = user.avatar || "🧑‍🎓";
    if (dashRank) dashRank.innerText = `LVL ${user.stats.level}`;
    if (dashName) dashName.innerText = user.username;
    if (dashArch) dashArch.innerText = user.archetype || "Town Architect";
    if (dashOverallCirc) dashOverallCirc.innerText = `${overallPct}%`;

    const levelTitle = (user.level_progress && user.level_progress.level_title) || "Apprentice Explorer";
    if (dashOverallTxt) dashOverallTxt.innerText = levelTitle;

    // Metrics Grid
    const dashLvl = document.getElementById('dashLevelVal');
    const dashRankSub = document.getElementById('dashRankSub');
    const dashXp = document.getElementById('dashXpVal');
    const dashXpFill = document.getElementById('dashXpFill');
    const dashQuests = document.getElementById('dashQuestsVal');
    const dashArts = document.getElementById('dashArtifactsVal');
    const dashBadges = document.getElementById('dashBadgesVal');
    const dashPct = document.getElementById('dashProgressPct');

    if (dashLvl) dashLvl.innerText = `Level ${user.stats.level}`;
    if (dashRankSub) dashRankSub.innerText = levelTitle;

    const prog = user.level_progress;
    if (prog) {
      if (dashXp) dashXp.innerText = `${prog.current_xp} / ${prog.level_max_xp} XP`;
      if (dashXpFill) dashXpFill.style.width = `${prog.progress_percentage}%`;
    }

    const questCount = user.stats.completed_quests ? user.stats.completed_quests.length : 0;
    const artCount = user.stats.discovered_artifacts ? user.stats.discovered_artifacts.length : 0;
    const badgeCount = user.stats.badges ? user.stats.badges.length : 0;

    if (dashQuests) dashQuests.innerText = `${questCount} / 5`;
    if (dashArts) dashArts.innerText = `${artCount} / 8`;
    if (dashBadges) dashBadges.innerText = `${badgeCount} / 12`;
    if (dashPct) dashPct.innerText = `${overallPct}%`;

    // Hydrate Young Learner Kid-Home Elements
    const kidLevelLbl = document.getElementById('kidLevelLabel');
    const kidXpFrac = document.getElementById('kidXpFraction');
    if (kidLevelLbl) kidLevelLbl.innerText = `Level ${user.stats.level} • ${levelTitle}`;
    if (kidXpFrac && prog) kidXpFrac.innerText = `${prog.current_xp} / ${prog.level_max_xp} XP`;

    const pillXp = document.getElementById('pillXpVal');
    const pillLvl = document.getElementById('pillLevelVal');
    const pillArts = document.getElementById('pillArtifactsVal');
    const pillMissions = document.getElementById('pillMissionsVal');

    if (pillXp) pillXp.innerText = user.stats.xp;
    if (pillLvl) pillLvl.innerText = user.stats.level;
    if (pillArts) pillArts.innerText = `${artCount} / 8`;
    if (pillMissions) pillMissions.innerText = `${questCount} / 5`;

    const museumDesc = document.getElementById('kidMuseumCardDesc');
    if (museumDesc) {
      museumDesc.innerText = `${artCount} of 8 ancient artifacts discovered. Uncover seals, statues, and toys!`;
    }

    const recentBadgesContainer = document.getElementById('kidRecentBadgesContainer');
    if (recentBadgesContainer) {
      if (user.badges_details && user.badges_details.length > 0) {
        const unlocked = user.badges_details.filter(b => b.unlocked);
        if (unlocked.length > 0) {
          recentBadgesContainer.innerHTML = unlocked.slice(0, 4).map(b => `
            <div class="kid-badge-mini" title="${b.name}: ${b.description}" style="display: inline-flex; align-items: center; gap: 6px; background: rgba(233,196,106,0.12); border: 1px solid rgba(233,196,106,0.3); padding: 4px 10px; border-radius: 20px; font-size: 0.82rem; margin: 3px;">
              <span>${b.icon || '🏅'}</span>
              <strong style="color: #E9C46A;">${b.name}</strong>
            </div>
          `).join('');
        } else {
          recentBadgesContainer.innerHTML = `
            <div class="empty-badge-prompt" style="color: #A99B90; font-size: 0.85rem; padding: 6px 0;">
              <span>🎯</span> Complete your first mission to earn a shiny badge!
            </div>
          `;
        }
      }
    }

    // Phase 8: Render IVC Mastery 3-Pillar Breakdown Widget
    if (window.gamificationController && user.overall_progress) {
      gamificationController.renderMasteryOverview('dashMasteryContainer', user.overall_progress);
    }

    // Phase 9: Render AI/ML Personalization on Dashboard
    if (window.aiController && user.username) {
      aiController.loadDashboardAi(user.username);
    }
  }

  refreshFunFact() {
    const facts = [
      "Harappan cities were built on a neat grid with covered underground drains—cleaner than cities built 3,000 years later!",
      "The Great Bath at Mohenjo-daro was made 100% waterproof using natural tar called bitumen!",
      "Every merchant across 1,000 kilometers used identical balance weights—nobody could cheat in trade!",
      "Harappan kids played with whistle birds, pull-along clay toy carts, and real dice!",
      "Ancient Indus craftspeople drilled tiny gemstone beads using special stone drills that took two weeks per bead!",
      "Every single Harappan brick followed the exact same 1:2:4 ratio, fitting together like Lego blocks!",
      "The Indus Valley Civilization was larger than ancient Egypt and Mesopotamia combined!"
    ];
    this.currentFactIndex = ((this.currentFactIndex || 0) + 1) % facts.length;
    const el = document.getElementById('kidDailyFactContent');
    if (el) {
      el.innerHTML = `<p>${facts[this.currentFactIndex]}</p>`;
    }
    if (window.audio) audio.playClick();
  }

  renderHUD(user) {
    if (!user) return;
    document.getElementById('hudPlayerName').innerText = user.username;
    document.getElementById('hudPlayerLevel').innerText = `LVL ${user.stats.level}`;
    document.getElementById('hudAvatarIcon').innerText = user.avatar || "🧑‍🎓";
    document.getElementById('hudTokenCount').innerText = `${user.stats.seal_tokens} Seals`;

    const prog = user.level_progress;
    if (prog) {
      document.getElementById('hudXpFill').style.width = `${prog.progress_percentage}%`;
      document.getElementById('hudXpText').innerText = `${prog.current_xp} / ${prog.level_max_xp} XP`;
    }

    const authBtnText = document.getElementById('hudAuthBtnText');
    if (authBtnText) {
      authBtnText.innerText = `👤 ${user.username}`;
    }

    // Telemetry cards on Home screen
    const telName = document.getElementById('telPlayerName');
    const telArch = document.getElementById('telPlayerArchetype');
    const telBadges = document.getElementById('telBadgesCount');
    if (telName) telName.innerText = user.username;
    if (telArch) telArch.innerText = user.archetype || "Town Architect";
    if (telBadges) telBadges.innerText = `${user.stats.badges ? user.stats.badges.length : 1} Unlocked`;
  }

  renderProfile(user) {
    if (!user) return;

    // Profile Hero
    const largeAvatar = document.getElementById('profileLargeAvatar');
    const nameDisp = document.getElementById('profileNameDisplay');
    const levelPill = document.getElementById('profileLevelPill');
    const archDisp = document.getElementById('profileArchetypeDisplay');
    const ageDisp = document.getElementById('profileAgeDisplay');

    if (largeAvatar) largeAvatar.innerText = user.avatar || "🧑‍🎓";
    if (nameDisp) nameDisp.innerText = user.username;
    if (levelPill) levelPill.innerText = `LVL ${user.stats.level}`;
    if (archDisp) archDisp.innerText = user.archetype || "Town Architect";
    if (ageDisp) ageDisp.innerText = `Age: ${user.age || 14}`;

    // Counters
    const xpVal = document.getElementById('profileXpVal');
    const lvlVal = document.getElementById('profileLevelVal');
    const tokVal = document.getElementById('profileTokensVal');
    const questCount = document.getElementById('profileQuestsCount');

    if (xpVal) xpVal.innerText = user.stats.xp;
    if (lvlVal) lvlVal.innerText = user.stats.level;
    if (tokVal) tokVal.innerText = user.stats.seal_tokens;
    if (questCount) questCount.innerText = `${user.stats.completed_quests ? user.stats.completed_quests.length : 0} / 5`;

    // Level Progress Big Bar
    const prog = user.level_progress;
    if (prog) {
      const progTitle = document.getElementById('profileProgressTitle');
      const progRatio = document.getElementById('profileProgressRatio');
      const bigBar = document.getElementById('profileBigXpFill');

      const levelTitle = prog.level_title || "Apprentice Explorer";

      if (progTitle) progTitle.innerText = `Level ${user.stats.level}: ${levelTitle}`;
      if (progRatio) progRatio.innerText = `${prog.current_xp} / ${prog.level_max_xp} XP (${prog.progress_percentage}%)`;
      if (bigBar) bigBar.style.width = `${prog.progress_percentage}%`;
    }

    // Phase 8: Render Badges Showcase Shelf with Categories & Progress Bars
    if (window.gamificationController && user.badges_details) {
      gamificationController.renderBadgesShowcase('profileBadgesShowcaseContainer', user.badges_details);
      gamificationController.renderMilestoneRoadmap('profileMilestonesContainer', user.stats.level);
    } else {
      this.renderBadgesShelf(user.badges_details);
    }
  }

  renderBadgesShelf(badges) {
    const grid = document.getElementById('profileBadgesGrid');
    const countBadge = document.getElementById('badgesShelfCount');
    if (!grid) return;

    if (!badges || badges.length === 0) {
      grid.innerHTML = '<div class="ancient-card">No badge data available.</div>';
      return;
    }

    const unlockedCount = badges.filter(b => b.unlocked).length;
    if (countBadge) countBadge.innerText = `${unlockedCount} / ${badges.length} Unlocked`;

    grid.innerHTML = badges.map(badge => `
      <div class="badge-tile ${badge.unlocked ? 'unlocked' : 'locked'}">
        <span class="badge-status-pill">${badge.unlocked ? 'UNLOCKED' : 'LOCKED'}</span>
        <div class="badge-tile-icon">${badge.icon}</div>
        <div class="badge-tile-name">${badge.name}</div>
        <div class="badge-tile-desc">${badge.description}</div>
      </div>
    `).join('');
  }

  async refreshCurrentProfile() {
    if (!this.state.user) return;
    try {
      const updated = await api.getProfile(this.state.user.username);
      this.setUser(updated);
    } catch (err) {
      console.error("Failed to refresh profile:", err);
    }
  }

  // Auth Modals & Flow
  openAuthModal(mode = 'register') {
    const modal = document.getElementById('authModal');
    if (modal) {
      modal.classList.add('active');
      this.switchAuthMode(mode);
    }
  }

  closeAuthModal() {
    const modal = document.getElementById('authModal');
    if (modal) modal.classList.remove('active');
    this.hideAlert();
  }

  switchAuthMode(mode) {
    const regForm = document.getElementById('registerForm');
    const loginForm = document.getElementById('loginForm');
    const tabReg = document.getElementById('tabBtnRegister');
    const tabLogin = document.getElementById('tabBtnLogin');
    const title = document.getElementById('authModalTitle');

    this.hideAlert();

    if (mode === 'register') {
      regForm.style.display = 'block';
      loginForm.style.display = 'none';
      tabReg.classList.add('active');
      tabLogin.classList.remove('active');
      title.innerText = 'Create Player Profile';
    } else {
      regForm.style.display = 'none';
      loginForm.style.display = 'block';
      tabReg.classList.remove('active');
      tabLogin.classList.add('active');
      title.innerText = 'Sign In to Profile';
    }
  }

  selectAge(age) {
    document.getElementById('regAge').value = age;
    document.querySelectorAll('.age-chip').forEach(chip => {
      chip.classList.toggle('active', chip.innerText.includes(`${age} yrs`));
    });
  }

  selectAvatar(emoji, element) {
    document.getElementById('selectedAvatar').value = emoji;
    document.querySelectorAll('.avatar-picker-grid .avatar-option').forEach(opt => {
      opt.classList.remove('selected');
    });
    element.classList.add('selected');
  }

  async handleRegister(event) {
    event.preventDefault();
    const username = document.getElementById('regUsername').value.trim();
    const age = parseInt(document.getElementById('regAge').value, 10);
    const avatar = document.getElementById('selectedAvatar').value || "🧑‍🎓";
    const archetype = document.getElementById('regArchetype').value;
    const password = document.getElementById('regPassword').value || "1234";

    this.showAlert("Registering your archaeological identity...", "info");

    try {
      const userProfile = await api.register({
        username,
        age,
        avatar,
        archetype,
        password
      });

      this.setUser(userProfile);
      this.logConsole(`[200 OK] Explorer "${username}" created and saved to MongoDB.`);
      this.closeAuthModal();
      if (window.uxManager) {
        window.uxManager.showToast({
          title: "Expedition Begun!",
          message: `Welcome, ${username}! Your archaeological profile is saved in MongoDB.`,
          icon: "🏺",
          type: "success"
        });
      }
      this.switchTab('tab-profile');
    } catch (err) {
      this.showAlert(err.message, "error");
      if (window.uxManager) {
        window.uxManager.triggerShake('#registerForm');
      }
    }
  }

  async handleLogin(event) {
    event.preventDefault();
    const username = document.getElementById('loginUsername').value.trim();
    const password = document.getElementById('loginPassword').value || "1234";

    this.showAlert("Validating credentials...", "info");

    try {
      const userProfile = await api.login({ username, password });
      this.setUser(userProfile);
      this.logConsole(`[200 OK] Explorer "${username}" logged in successfully.`);
      this.closeAuthModal();
      if (window.uxManager) {
        window.uxManager.showToast({
          title: "Welcome Back!",
          message: `Resuming Indus expedition for ${username}.`,
          icon: "🏛️",
          type: "success"
        });
      }
      this.switchTab('tab-profile');
    } catch (err) {
      this.showAlert(err.message, "error");
      if (window.uxManager) {
        window.uxManager.triggerShake('#loginForm');
      }
    }
  }

  quickFillLogin(username) {
    const input = document.getElementById('loginUsername');
    if (input) {
      input.value = username;
      input.focus();
    }
  }

  // Edit Profile Modal
  openEditProfileModal() {
    if (!this.state.user) return;
    const modal = document.getElementById('editProfileModal');
    const ageInput = document.getElementById('editAge');
    const archSelect = document.getElementById('editArchetype');
    const hiddenAvatar = document.getElementById('editSelectedAvatar');

    if (ageInput) ageInput.value = this.state.user.age || 14;
    if (archSelect) archSelect.value = this.state.user.archetype || "Town Architect";
    if (hiddenAvatar) hiddenAvatar.value = this.state.user.avatar || "🧑‍🎓";

    // Highlight current avatar
    document.querySelectorAll('#editProfileModal .avatar-option').forEach(opt => {
      opt.classList.toggle('selected', opt.getAttribute('data-avatar') === (this.state.user.avatar || "🧑‍🎓"));
    });

    if (modal) modal.classList.add('active');
  }

  closeEditProfileModal() {
    const modal = document.getElementById('editProfileModal');
    if (modal) modal.classList.remove('active');
  }

  selectEditAvatar(emoji, el) {
    document.getElementById('editSelectedAvatar').value = emoji;
    document.querySelectorAll('#editProfileModal .avatar-option').forEach(opt => {
      opt.classList.remove('selected');
    });
    el.classList.add('selected');
  }

  async handleUpdateProfile(event) {
    event.preventDefault();
    if (!this.state.user) return;

    const age = parseInt(document.getElementById('editAge').value, 10);
    const archetype = document.getElementById('editArchetype').value;
    const avatar = document.getElementById('editSelectedAvatar').value || this.state.user.avatar;

    try {
      const updated = await api.updateProfile(this.state.user.username, {
        age,
        avatar,
        archetype
      });
      this.setUser(updated);
      this.logConsole(`[200 OK] Profile for "${updated.username}" updated in MongoDB.`);
      this.closeEditProfileModal();
      if (window.uxManager) {
        window.uxManager.showToast({
          title: "Profile Saved",
          message: "Explorer specialization & avatar updated in MongoDB.",
          icon: "✅",
          type: "success"
        });
      }
    } catch (err) {
      alert(`Update failed: ${err.message}`);
      if (window.uxManager) {
        window.uxManager.triggerShake('#editProfileModal .modal-card');
      }
    }
  }

  openProfileModal() {
    this.switchTab('tab-profile');
  }

  // Simulation Award Progress
  async simulateAward(xp, tokens, badgeId, questId) {
    if (!this.state.user) {
      this.openAuthModal('register');
      return;
    }

    this.logConsole(`Simulating achievement for "${this.state.user.username}": +${xp} XP, +${tokens} Seals...`);
    try {
      const updated = await api.awardProgress(this.state.user.username, {
        xp_to_add: xp,
        tokens_to_add: tokens,
        badge_to_unlock: badgeId,
        quest_to_complete: questId
      });

      const oldLevel = this.state.user.stats.level;
      this.setUser(updated);

      if (window.uxManager && xp > 0) {
        window.uxManager.spawnXpAnimation(xp);
      }

      if (updated.stats.level > oldLevel) {
        if (window.uxManager) {
          window.uxManager.triggerLevelUp(updated.stats.level, updated.level_progress?.level_title);
        } else if (window.audio) audio.playFanfare();
        this.logConsole(`🎉 LEVEL UP! ${updated.username} reached Level ${updated.stats.level}!`);
      } else if (badgeId) {
        if (window.uxManager) {
          window.uxManager.triggerBadgeUnlock(badgeId);
        } else if (window.audio) audio.playChime();
        this.logConsole(`🏆 BADGE UNLOCKED: ${badgeId}!`);
      } else {
        if (window.audio) audio.playClick();
      }
    } catch (err) {
      this.logConsole(`[ERROR] Progress award failed: ${err.message}`);
    }
  }

  showAlert(message, type = "error") {
    const banner = document.getElementById('authAlertBanner');
    if (!banner) return;
    banner.className = `alert-banner ${type}`;
    banner.innerText = message;
    banner.style.display = 'block';
  }

  hideAlert() {
    const banner = document.getElementById('authAlertBanner');
    if (banner) banner.style.display = 'none';
  }

  // Health & Verification
  async checkSystemHealth() {
    const statusPill = document.getElementById('systemStatusPill');
    const statusDot = statusPill.querySelector('.status-dot');
    const statusText = document.getElementById('statusPillText');
    const telDatabase = document.getElementById('telDatabase');
    const footerServerTime = document.getElementById('footerServerTime');

    try {
      const data = await api.getHealth();
      this.state.serverConnected = true;

      statusDot.className = 'status-dot healthy';
      statusText.innerText = 'Connected';
      statusPill.title = `FastAPI Active | ${data.database.engine}`;

      if (telDatabase) telDatabase.innerText = data.database.engine;
      if (footerServerTime) footerServerTime.innerText = `Server Time: ${new Date(data.timestamp).toLocaleTimeString()}`;
    } catch (err) {
      statusDot.className = 'status-dot';
      statusText.innerText = 'Offline';
      if (telDatabase) telDatabase.innerText = 'Unavailable';
      this.logConsole(`System Health Check Failed: ${err.message}\nMake sure FastAPI backend is running!`);
    }
  }

  async testPing() {
    this.logConsole("Pinging backend /api/health endpoint...");
    try {
      const res = await api.getHealth();
      this.logConsole(`[200 OK] Backend Response:\n` + JSON.stringify(res, null, 2));
    } catch (err) {
      this.logConsole(`[ERROR] Ping failed: ${err.message}`);
    }
  }

  async fetchIvcOverview() {
    this.logConsole("Fetching Indus Valley Civilization hallmarks from /api/ivc/overview...");
    try {
      const overview = await api.getIvcOverview();
      this.logConsole(`[200 OK] Historical Overview Retrieved:\n` + JSON.stringify(overview, null, 2));
    } catch (err) {
      this.logConsole(`[ERROR] Fetch overview failed: ${err.message}`);
    }
  }

  async loadCityLocations() {
    if (window.cityController) {
      window.cityController.renderCityStage();
      window.cityController.updateDiscoveryCounters();
      return;
    }
    const container = document.getElementById('cityStageContainer');
    if (!container) return;
    try {
      const locations = await api.getLocations();
      container.innerHTML = `<div class="ancient-card-grid" style="padding: 20px;">` + locations.map(loc => `
        <div class="ancient-card">
          <div style="font-size: 0.72rem; color: var(--color-sandstone); text-transform: uppercase; font-weight: 700;">
            ${loc.site} • ${loc.zone}
          </div>
          <h3>${loc.name}</h3>
          <p>Status: <strong style="color: ${loc.status === 'unlocked' ? 'var(--color-patina)' : '#999'}">
            ${loc.status.toUpperCase()} (Req LVL ${loc.level_required})
          </strong></p>
        </div>
      `).join('') + `</div>`;
    } catch (err) {
      container.innerHTML = `<div class="ancient-card">Error loading locations: ${err.message}</div>`;
    }
  }

  async loadQuests() {
    if (window.questController) {
      window.questController.renderQuestHub();
      return;
    }
    const container = document.getElementById('questsHubContainer');
    if (!container) return;
    try {
      const quests = await api.getQuests();
      container.innerHTML = `<div class="ancient-card-grid" style="padding: 20px;">` + quests.map(q => `
        <div class="ancient-card">
          <div style="font-size: 0.72rem; color: var(--color-gold); font-weight: 700;">TOPIC: ${q.learning_concept || q.topic}</div>
          <h3>${q.title}</h3>
          <p>NPC Guide: <strong>${q.npc_name}</strong></p>
          <p style="margin-top: 8px;">Reward: <span style="color: var(--color-patina); font-weight: 700;">+${q.reward_xp} XP</span> • ${q.reward_tokens} Seals</p>
        </div>
      `).join('') + `</div>`;
    } catch (err) {
      container.innerHTML = `<div class="ancient-card">Error loading quests: ${err.message}</div>`;
    }
  }

  async loadMuseum() {
    if (window.museumController) {
      window.museumController.renderMuseumHub();
      return;
    }
    const container = document.getElementById('museumHubContainer');
    if (!container) return;
    try {
      const artifacts = await api.getMuseumArtifacts();
      container.innerHTML = `<div class="ancient-card-grid" style="padding: 20px;">` + artifacts.map(art => `
        <div class="ancient-card">
          <div style="font-size: 0.72rem; color: var(--color-sandstone); font-weight: 700;">
            ${art.site || art.origin} • ${art.material}
          </div>
          <h3>${art.name}</h3>
          <p style="font-size: 0.8rem; margin: 8px 0;">${art.historical_significance || art.importance}</p>
          <span style="font-size: 0.75rem; color: ${art.discovered ? 'var(--color-patina)' : '#888'}; font-weight: 700;">
            ${art.discovered ? '✨ UNLOCKED IN MUSEUM' : '🔒 SILHOUETTE (DISCOVERY REQUIRED)'}
          </span>
        </div>
      `).join('') + `</div>`;
    } catch (err) {
      container.innerHTML = `<div class="ancient-card">Error loading artifacts: ${err.message}</div>`;
    }
  }

  async fetchAiRecommendations() {
    const box = document.getElementById('aiRecommendationBox');
    box.innerText = "Querying Scikit-Learn Recommender...";
    try {
      const data = await api.getAiRecommendations(1);
      box.innerHTML = `
        <div style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; border-left: 3px solid var(--color-gold);">
          <strong>Algorithm:</strong> ${data.algorithm}<br>
          <strong>Recommended:</strong> "${data.recommendations[0].title}"<br>
          <strong>Pedagogical Reason:</strong> ${data.recommendations[0].reason}<br>
          <strong>Match Confidence:</strong> ${(data.recommendations[0].confidence_score * 100).toFixed(0)}%
        </div>
      `;
    } catch (err) {
      box.innerText = `Error: ${err.message}`;
    }
  }

  async testDdaSimulation() {
    const box = document.getElementById('aiDdaBox');
    box.innerText = "Running DDA evaluation model...";
    try {
      const simulation = await api.calculateDynamicDifficulty({
        user_xp: 350,
        prior_solve_time: 18.5,
        attempts: 1,
        hints_used: 0
      });
      box.innerHTML = `
        <div style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; border-left: 3px solid var(--color-patina);">
          <strong>Classified Difficulty:</strong> ${simulation.difficulty_tier}<br>
          <strong>Allocated Time Limit:</strong> ${simulation.time_limit_seconds} seconds<br>
          <strong>Max Hints Allowed:</strong> ${simulation.max_hints_available}<br>
          <strong>XP Multiplier:</strong> ${simulation.xp_multiplier}x
        </div>
      `;
    } catch (err) {
      box.innerText = `Error: ${err.message}`;
    }
  }

  logConsole(message) {
    const consoleEl = document.getElementById('consoleOutput');
    if (!consoleEl) return;
    const timestamp = new Date().toLocaleTimeString();
    consoleEl.textContent = `[${timestamp}] ${message}\n\n` + consoleEl.textContent;
  }

  clearConsole() {
    const consoleEl = document.getElementById('consoleOutput');
    if (consoleEl) consoleEl.textContent = '// Console cleared.';
  }
}

const app = new BharatQuestApp();
window.addEventListener('DOMContentLoaded', () => app.init());