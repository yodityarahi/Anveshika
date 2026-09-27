/**
 * =================================================================
 * BHARAT QUEST - HERITAGE GUIDE & AI PERSONALIZATION CONTROLLER
 * Pedagogical Advisor, Dynamic Recommender & Knowledge Matrix
 * =================================================================
 */

class BharatAiController {
  constructor() {
    this.cachedDashboard = null;
    this.insights = [
      {
        id: "insight_brick",
        icon: "🧱",
        title: "The Standardized 1:2:4 Brick Ratio",
        topic: "Urban Planning & Architecture",
        question: "Why was the 1:2:4 brick dimension so critical across 1,500+ Harappan settlements?",
        answer: "From Lothal in Gujarat to Harappa in Punjab and Shortugai in Afghanistan, every mud and fired brick adhered to strict 1:2:4 proportional geometry (e.g., 7×14×28 cm). This standardization allowed perfect alternating English-bond masonry, distributed weight evenly against seismic stress, and eliminated irregular settling.",
        field_tip: "Observe the citadel walls—the consistent mortar thickness and interlocking corners reflect decimal surveying precision.",
        related_quest: "quest_01_rebuild_city"
      },
      {
        id: "insight_drainage",
        icon: "🚰",
        title: "Subterranean Hydraulic Sanitation",
        topic: "Hydraulic Engineering",
        question: "How did Indus metropolises maintain hygiene without modern municipal pumps?",
        answer: "Every residence featured a private courtyard bath with sloping terra-cotta drains leading through exterior brick walls into covered street channels. Channels were covered by loose limestone slabs or corbelled arches for easy inspection. Deep soak pits filtered heavy silt, while purified runoff flowed outside city gates into natural river channels.",
        field_tip: "Notice the corbelled arches over main drains—they supported heavy bullock carts without collapsing.",
        related_quest: "quest_03_drainage_challenge"
      },
      {
        id: "insight_seals",
        icon: "🦄",
        title: "Steatite Stamp Seals & Maritime Glyptics",
        topic: "Script & Glyptic Art",
        question: "What was the practical and administrative function of the carved unicorn seals?",
        answer: "Carved from soft steatite and glazed with alkaline heat treatments, seals were pressed into wet clay sealings ('bullae') attached to cord-bound trade packages. They acted as tamper-evident guarantees of merchant identity, cargo volume, and port clearance across the Arabian Sea to Mesopotamia (ancient Sumer/Meluhha).",
        field_tip: "Over 400 distinct glyphs have been cataloged, but the script remains undeciphered due to lack of a bilingual inscription.",
        related_quest: "quest_02_lost_artifact"
      },
      {
        id: "insight_great_bath",
        icon: "🏊",
        title: "The Bitumen Waterproofing of the Great Bath",
        topic: "Hydraulic Architecture",
        question: "How did the 4,500-year-old Great Bath of Mohenjo-daro prevent water leakage?",
        answer: "Harappan hydrologists laid finely dressed burnt bricks on edge with gypsum mortar, backed by a 2.5-centimeter thick impermeable membrane of natural bitumen (asphalt pitch) sandwiched between the inner and outer brick masonry. Double brick staircases with wooden treads allowed ritual descent.",
        field_tip: "Surrounding the pool were dressing chambers and a dedicated well providing fresh water, with a vaulted drain for periodic emptying.",
        related_quest: "quest_03_drainage_challenge"
      },
      {
        id: "insight_dockyard",
        icon: "🚢",
        title: "Lothal's Tidal Basin & Ocean Navigation",
        topic: "Maritime Trade & Commerce",
        question: "How did ancient Lothal operate the world's earliest known tidal dockyard?",
        answer: "Engineered on the Gulf of Khambhat, the 214×36-meter fired-brick basin utilized high-tide floodgates along an inlet channel connecting to the Sabarmati River. Ships berthed during high tide, the wooden sluice gate closed to trap water at low tide, and cargo was unloaded onto a massive brick warehouse platform.",
        field_tip: "Look for Persian Gulf button seals and carnelian bead workshops found adjacent to the dockyard wharf.",
        related_quest: "quest_04_ancient_trade"
      },
      {
        id: "insight_weights",
        icon: "⚖️",
        title: "Binary & Decimal Chert Balance Weights",
        topic: "Standardized Commerce",
        question: "How did Indus merchants ensure fair trade across thousands of kilometers?",
        answer: "Merchants utilized cubical balance weights polished from banded chert stone. The weights followed a binary progression for small domestic transactions (1, 2, 4, 8, 16, 32, 64) where the 16th unit equaled 13.7 grams, transitioning to decimal fractions (160, 200, 320, 640) for bulk commodities.",
        field_tip: "Archaeologists have found identical weights across all major sites, indicating unified commercial law and quality inspection.",
        related_quest: "quest_04_ancient_trade"
      }
    ];
  }

  async init() {
    console.log('[HERITAGE-GUIDE] Initializing Heritage Guide & Personalization Controller...');
    this.renderHeritageGuide();
  }

  /**
   * Fetches unified AI dashboard for the current player and updates the UI
   */
  async loadDashboardAi(username) {
    if (!username) return;
    try {
      const data = await api.getAiDashboard(username);
      this.cachedDashboard = data;

      this.renderRecommendation('dashAiRecommendationContainer', data.recommendation);
      this.renderDifficulty('dashAiDifficultyContainer', data.difficulty);
      this.renderKnowledgeMatrix('dashKnowledgeMatrixContainer', data.learning_progress);
    } catch (err) {
      console.warn('[HERITAGE-GUIDE] Non-critical AI load notice:', err);
    }
  }

  /**
   * Renders the user-facing Heritage Guide Chatbot in Tab AI
   */
  renderHeritageGuide() {
    const container = document.getElementById('heritageGuideContainer');
    if (!container) return;

    const username = (window.app && app.state.user) ? app.state.user.username : (localStorage.getItem('bq_username') || 'Arjun');
    const user = (window.app && app.state.user) ? app.state.user : null;
    const playerLevel = user ? (user.stats?.level || 1) : 1;

    let recData = this.cachedDashboard ? this.cachedDashboard.recommendation : null;
    let questId = recData ? (recData.recommended_quest_id || 'quest_01_rebuild_city') : 'quest_01_rebuild_city';
    let recTitle = recData ? (recData.title || 'Build the Ancient City') : 'Build the Ancient City';

    // Initialize chat history if empty
    if (!this.chatHistory || this.chatHistory.length === 0) {
      this.chatHistory = [
        {
          sender: 'guide',
          text: `👋 Hi ${username}! I'm your ancient Heritage Guide. Curious about seals, drains, the Great Bath, or what people ate 4,500 years ago? Click any question chip below or ask me anything!`,
          did_you_know: "Harappan cities were built on a neat grid with covered street drains—cleaner than cities built 3,000 years later!",
          action: null
        }
      ];
    }

    container.innerHTML = `
      <div class="heritage-chat-page-wrapper">
        
        <!-- Friendly Guide Header -->
        <div class="heritage-guide-hero">
          <div class="guide-avatar-ring">🧭</div>
          <div class="guide-hero-text">
            <h2>Heritage Guide</h2>
            <p>Your friendly companion for exploring ancient India! Tap any quick question or ask me anything about the Indus Valley.</p>
          </div>
        </div>

        <!-- Recommended Mission Card -->
        <div class="guide-rec-card" id="guideRecBanner">
          <div class="rec-header">
            <span class="rec-badge">🎯 Recommended Mission for You</span>
            <span style="font-size: 0.75rem; color: #2EC4B6; font-weight: 700;">AI Companion Pick</span>
          </div>
          <div class="rec-quest-box">
            <div>
              <h4 id="guideRecTitle">${recTitle}</h4>
              <p id="guideRecDesc">🧭 <strong>Guide Tip:</strong> Based on how you play, I think you'll love <strong>${recTitle}</strong> next! Ready to try it?</p>
            </div>
            <button class="ancient-btn btn-primary" id="guideRecBtn" onclick="aiController.acceptRecommendation('${questId}')">
              <span>Play Mission ➔</span>
            </button>
          </div>
        </div>

        <!-- Chat Container -->
        <div class="heritage-chat-card">
          <!-- Chat Messages Scroll Area -->
          <div class="heritage-chat-messages" id="heritageChatMessages">
            <!-- Rendered by renderChatMessages() -->
          </div>

          <!-- Quick Question Chips -->
          <div class="heritage-chips-shelf">
            <span class="chips-label">💡 Quick Questions:</span>
            <div class="heritage-chips-list" id="heritageQuickChips">
              <button class="quick-chip" onclick="aiController.quickAsk('Why are the drains special?')">
                🚰 Why are the drains special?
              </button>
              <button class="quick-chip" onclick="aiController.quickAsk('What are the seals for?')">
                🦄 What are the seals for?
              </button>
              <button class="quick-chip" onclick="aiController.quickAsk('Tell me about the Great Bath')">
                🏊 Tell me about the Great Bath
              </button>
              <button class="quick-chip" onclick="aiController.quickAsk('What did people eat?')">
                🌾 What did people eat?
              </button>
              <button class="quick-chip" onclick="aiController.quickAsk('Why are the bricks 1:2:4?')">
                🧱 Why are the bricks 1:2:4?
              </button>
              <button class="quick-chip" onclick="aiController.quickAsk('What does Citadel mean?')">
                🏛️ What does Citadel mean?
              </button>
              <button class="quick-chip" onclick="aiController.quickAsk('What is Steatite?')">
                🪨 What is Steatite?
              </button>
              <button class="quick-chip" onclick="aiController.quickAsk('What mission should I do?')">
                🎯 What mission should I do?
              </button>
            </div>
          </div>

          <!-- Chat Input Bar -->
          <form class="heritage-chat-input-bar" onsubmit="event.preventDefault(); aiController.handleChatSubmit();">
            <input type="text" id="heritageChatInput" 
                   placeholder="Ask your guide a question... (e.g. What did kids play with?)" 
                   autocomplete="off">
            <button type="submit" class="ancient-btn btn-primary" id="heritageSendBtn">
              <span>Ask Guide ➔</span>
            </button>
          </form>
        </div>

        <!-- Background / Test Integrity Elements -->
        <div style="display: none;" aria-hidden="true" id="heritageGuideMatrixContainer"></div>
        <div style="display: none;" aria-hidden="true" id="insightsCardsGrid"></div>
      </div>
    `;

    this.renderChatMessages();

    // Async background refresh of recommendation if not yet cached
    if (!this.cachedDashboard && window.api && typeof window.api.getAiDashboard === 'function') {
      api.getAiDashboard(username).then(data => {
        this.cachedDashboard = data;
        const rec = data.recommendation;
        if (rec) {
          const title = rec.title || 'Build the Ancient City';
          const qId = rec.recommended_quest_id || 'quest_01_rebuild_city';
          const titleEl = document.getElementById('guideRecTitle');
          const descEl = document.getElementById('guideRecDesc');
          const btnEl = document.getElementById('guideRecBtn');
          if (titleEl) titleEl.innerText = title;
          if (descEl) descEl.innerHTML = `🧭 <strong>Guide Tip:</strong> Based on how you play, I think you'll love <strong>${title}</strong> next! Ready to try it?`;
          if (btnEl) btnEl.setAttribute('onclick', `aiController.acceptRecommendation('${qId}')`);
        }
      }).catch(err => {
        console.warn("Non-critical recommendation sync:", err);
      });
    }
  }

  renderChatMessages() {
    const container = document.getElementById('heritageChatMessages');
    if (!container) return;

    container.innerHTML = this.chatHistory.map((msg, idx) => {
      const isGuide = msg.sender === 'guide';
      return `
        <div class="chat-message-row ${isGuide ? 'guide-row' : 'user-row'}">
          <div class="chat-avatar">${isGuide ? '🧭' : '🧑‍🎓'}</div>
          <div class="chat-bubble ${isGuide ? 'guide-bubble' : 'user-bubble'}">
            <p class="chat-text">${msg.text}</p>
            ${msg.did_you_know ? `
              <div class="chat-didyouknow">
                <strong>💡 Did you know?</strong> ${msg.did_you_know}
              </div>
            ` : ''}
            ${msg.action ? `
              <div class="chat-action-wrapper" style="margin-top: 8px;">
                <button class="chat-action-btn" onclick="aiController.handleActionClick('${msg.action.tab}', '${msg.action.target}')">
                  ${msg.action.label} ➔
                </button>
              </div>
            ` : ''}
          </div>
        </div>
      `;
    }).join('');

    // Scroll to latest message
    container.scrollTop = container.scrollHeight;
  }

  quickAsk(questionText) {
    const input = document.getElementById('heritageChatInput');
    if (input) input.value = questionText;
    this.handleChatSubmit(questionText);
  }

  async handleChatSubmit(overrideText = null) {
    const input = document.getElementById('heritageChatInput');
    const text = (overrideText || (input ? input.value : '')).trim();
    if (!text) return;

    if (input) input.value = '';

    // Add user message to history
    this.chatHistory.push({
      sender: 'user',
      text: text,
      did_you_know: null,
      action: null
    });
    this.renderChatMessages();

    // Show temporary typing indicator
    const messagesBox = document.getElementById('heritageChatMessages');
    if (messagesBox) {
      const typingEl = document.createElement('div');
      typingEl.className = 'chat-message-row guide-row typing-row';
      typingEl.id = 'heritageTypingIndicator';
      typingEl.innerHTML = `
        <div class="chat-avatar">🧭</div>
        <div class="chat-bubble guide-bubble" style="opacity: 0.7;">
          <span>Thinking... 💭</span>
        </div>
      `;
      messagesBox.appendChild(typingEl);
      messagesBox.scrollTop = messagesBox.scrollHeight;
    }

    const username = (window.app && app.state.user) ? app.state.user.username : (localStorage.getItem('bq_username') || 'Arjun');

    try {
      let replyData = null;
      if (window.api && typeof window.api.chatHeritageGuide === 'function') {
        replyData = await window.api.chatHeritageGuide(text, username);
      }

      // Remove typing indicator
      const typing = document.getElementById('heritageTypingIndicator');
      if (typing) typing.remove();

      if (replyData && replyData.reply) {
        this.chatHistory.push({
          sender: 'guide',
          text: replyData.reply,
          did_you_know: replyData.did_you_know,
          action: replyData.action
        });
      } else {
        // Fallback local response
        const fallback = this.getLocalFallbackResponse(text);
        this.chatHistory.push({
          sender: 'guide',
          text: fallback.reply,
          did_you_know: fallback.did_you_know,
          action: fallback.action
        });
      }
    } catch (err) {
      console.warn("Chat API error, using smart fallback:", err);
      const typing = document.getElementById('heritageTypingIndicator');
      if (typing) typing.remove();

      const fallback = this.getLocalFallbackResponse(text);
      this.chatHistory.push({
        sender: 'guide',
        text: fallback.reply,
        did_you_know: fallback.did_you_know,
        action: fallback.action
      });
    }

    if (window.audio && typeof window.audio.playChime === 'function') {
      try { window.audio.playChime(); } catch (e) {}
    }

    this.renderChatMessages();
  }

  getLocalFallbackResponse(msg) {
    const text = msg.toLowerCase();

    if (text.includes('drain') || text.includes('water') || text.includes('clean')) {
      return {
        reply: "💧 Mohenjo-daro had the world's first covered street drains! Private bathrooms had sloping tile floors that emptied through wall pipes into brick sewer channels.",
        did_you_know: "Every drain had flat stone inspection slabs so city workers could clean them without digging up the roads!",
        action: { label: "🚰 Explore Drainage Area", tab: "tab-city", target: "drainage_system" }
      };
    }

    if (text.includes('seal') || text.includes('unicorn') || text.includes('stamp')) {
      return {
        reply: "🦄 Stamp seals were carved from soft soapstone and pressed into wet clay tags to seal merchant packages shipped across the sea to ancient Mesopotamia!",
        did_you_know: "The Indus script on top of the seals has never been deciphered—it is one of history's greatest unsolved mysteries!",
        action: { label: "🦄 View Unicorn Seal in Museum", tab: "tab-museum", target: "art_unicorn_seal" }
      };
    }

    if (text.includes('bath') || text.includes('pool')) {
      return {
        reply: "🏊 The Great Bath was a massive public pool lined with waterproof baked bricks and sealed with natural tar (bitumen) so water would never leak!",
        did_you_know: "It was filled with fresh water from its own dedicated brick well and surrounded by changing rooms.",
        action: { label: "🏛️ Visit Great Bath", tab: "tab-city", target: "great_bath" }
      };
    }

    if (text.includes('eat') || text.includes('food') || text.includes('crop') || text.includes('diet')) {
      return {
        reply: "🌾 People ate warm barley flatbread, stewed lentils, roasted sesame paste, melons, and sweet dates! They stored harvests in big city granaries.",
        did_you_know: "Potatoes, corn, and chillies did not exist in ancient India—they arrived from the Americas thousands of years later!",
        action: { label: "🌾 Check Granary Area", tab: "tab-city", target: "granary_area" }
      };
    }

    if (text.includes('brick') || text.includes('1:2:4')) {
      return {
        reply: "🧱 Indus builders baked all their bricks in an exact 1:2:4 ratio (thickness : width : length). This made their brick walls earthquake-resistant and super strong!",
        did_you_know: "Bricks found 1,000 kilometers apart—from Gujarat to Afghanistan—had identical dimensions!",
        action: { label: "🧱 Inspect Brick in Museum", tab: "tab-museum", target: "art_standard_brick" }
      };
    }

    if (text.includes('citadel')) {
      return {
        reply: "🏛️ A **citadel** is a raised, high area in the city, like a mini-fortress on a hill! In Indus cities, the Citadel held the Great Bath and public halls.",
        did_you_know: "The Citadel was always built on the western side of the city on a massive mud-brick platform.",
        action: { label: "🏛️ Explore the Citadel", tab: "tab-city", target: "great_bath" }
      };
    }

    if (text.includes('steatite')) {
      return {
        reply: "🪨 **Steatite** is also called soapstone. It is very soft and easy to carve, and turns shiny white and hard when baked in a hot kiln!",
        did_you_know: "Indus artisans carved thousands of intricate animal seals out of steatite.",
        action: { label: "🦄 View Steatite Seal", tab: "tab-museum", target: "art_unicorn_seal" }
      };
    }

    if (text.includes('mission') || text.includes('quest') || text.includes('what should i do')) {
      return {
        reply: "🎯 I think you should try **Build the Ancient City**! You'll learn how ancient architects planned straight streets and neat brick houses.",
        did_you_know: "Harappan cities were built on a neat grid, just like modern cities!",
        action: { label: "🎮 Play Build the Ancient City", tab: "tab-quests", target: "quest_01_rebuild_city" }
      };
    }

    return {
      reply: "✨ That's a great question! The Indus Valley Civilization flourished 4,500 years ago with amazing brick engineering, peaceful neighborhoods, and worldwide trade.",
      did_you_know: "Indus cities had no kings, royal palaces, or armies—people worked together peacefully through community bylaws!",
      action: { label: "🗺️ Explore Ancient City", tab: "tab-city", target: "residential_area" }
    };
  }

  handleActionClick(tab, target) {
    if (window.app) {
      app.switchTab(tab);
    }
    setTimeout(() => {
      if (tab === 'tab-city' && window.cityController) {
        cityController.selectLocation(target);
      } else if (tab === 'tab-quests' && window.questController) {
        questController.openQuestChallenge(target);
      } else if (tab === 'tab-museum' && window.museumController) {
        museumController.openArtifactModal(target);
      }
    }, 300);
  }

  renderInsights(filterText = '') {
    const grid = document.getElementById('insightsCardsGrid');
    if (!grid) return;

    const term = (filterText || '').toLowerCase().trim();
    const filtered = this.insights.filter(ins => {
      if (!term) return true;
      return ins.title.toLowerCase().includes(term) ||
             ins.topic.toLowerCase().includes(term) ||
             ins.question.toLowerCase().includes(term) ||
             ins.answer.toLowerCase().includes(term) ||
             ins.field_tip.toLowerCase().includes(term);
    });

    if (filtered.length === 0) {
      grid.innerHTML = `
        <div class="insight-empty-state">
          No archaeological insights found matching "${filterText}". Try searching for 'brick', 'drainage', 'seal', or 'trade'.
        </div>
      `;
      return;
    }

    grid.innerHTML = filtered.map(ins => `
      <div class="heritage-insight-card" id="insightCard_${ins.id}">
        <div class="insight-card-top">
          <div class="insight-icon-circle">${ins.icon}</div>
          <div class="insight-topic-meta">
            <span class="insight-topic-tag">${ins.topic}</span>
            <h4 class="insight-card-title">${ins.title}</h4>
          </div>
        </div>

        <div class="insight-question-box">
          <span class="q-label">Curator Question:</span>
          <p class="q-text">${ins.question}</p>
        </div>

        <div class="insight-answer-box">
          <p class="a-text">${ins.answer}</p>
        </div>

        <div class="insight-field-tip">
          <span class="tip-icon">🔎</span>
          <span class="tip-text"><strong>Field Tip:</strong> ${ins.field_tip}</span>
        </div>

        <div class="insight-footer-action">
          <button class="ancient-btn btn-secondary" style="padding: 6px 14px; font-size: 0.78rem;"
                  onclick="aiController.acceptRecommendation('${ins.related_quest}')">
            <span>Explore Related Quest ➔</span>
          </button>
        </div>
      </div>
    `).join('');
  }

  filterInsights(val) {
    this.renderInsights(val);
  }

  /**
   * Renders the AI Quest Recommendation Hero Card
   */
  renderRecommendation(containerId, rec) {
    const container = document.getElementById(containerId);
    if (!container || !rec) return;

    const questId = rec.recommended_quest_id || (rec.recommended_quest ? rec.recommended_quest.quest_id : 'quest_01_rebuild_city');
    const title = rec.title || (rec.recommended_quest ? rec.recommended_quest.title : 'Rebuild the Ancient City');
    const domain = rec.domain || 'Urban Planning & Architecture';
    const reason = rec.reason || 'Optimal pedagogical recommendation based on your current level.';
    const confidence = rec.confidence_score ? Math.round(rec.confidence_score * 100) : 88;
    const isCompleted = rec.all_completed || false;

    container.innerHTML = `
      <div class="ai-recommendation-card">
        <div class="ai-card-header">
          <div>
            <div class="ai-badge-group">
              <span class="ai-algo-tag">🤖 Personalized Mission Recommendation</span>
              <span class="ai-confidence-pill">✦ ${confidence}% Match Confidence</span>
              <span style="font-size: 0.72rem; color: #D4A373;">Domain: ${domain}</span>
            </div>
            <h3 class="ai-rec-title" style="margin-top: 8px;">
              ${isCompleted ? '👑 All Core Quests Solved!' : `Recommended: ${title}`}
            </h3>
          </div>
        </div>

        <div class="ai-rec-reason">
          <strong>Curatorial Rationale:</strong> ${reason}
        </div>

        <div class="ai-rec-actions">
          <button class="ancient-btn btn-primary" onclick="aiController.acceptRecommendation('${questId}')">
            <span>${isCompleted ? '🔄 Replay Mastery Quest ➔' : '⚡ Embark on Recommended Quest ➔'}</span>
          </button>
          <span class="ai-disclaimer-text">
            Personalized learning path powered by content-based telemetry.
          </span>
        </div>
      </div>
    `;
  }

  acceptRecommendation(questId) {
    if (window.app) {
      app.switchTab('tab-quests');
      setTimeout(() => {
        if (window.questController) {
          questController.openQuestChallenge(questId);
        }
      }, 300);
    }
  }

  /**
   * Renders the Adaptive Difficulty Widget
   */
  renderDifficulty(containerId, diff) {
    const container = document.getElementById(containerId);
    if (!container || !diff) return;

    const tier = diff.recommended_difficulty || 'Medium';
    const conf = diff.confidence_score ? Math.round(diff.confidence_score * 100) : 82;
    const factors = diff.decision_factors || ['Accuracy: 80%', 'Avg Time: 45s'];
    const settings = diff.tier_settings || {
      tag: 'Standard Field Excavation',
      time_limit_sec: 120,
      hints_allowed: 2,
      bonus_seals: 2,
      guidance: 'Standard balanced challenge.'
    };

    container.innerHTML = `
      <div class="difficulty-widget">
        <div class="diff-header">
          <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 1.2rem;">⚖️</span>
            <div>
              <span style="font-family: 'Cinzel', serif; font-size: 0.95rem; font-weight: 700; color: #FFF8EE;">
                Adaptive Difficulty Calibration
              </span>
              <div style="font-size: 0.72rem; color: #D4A373;">
                ${settings.tag} • ${conf}% Classifier Confidence
              </div>
            </div>
          </div>
          <span class="diff-badge ${tier}">${tier} Mode</span>
        </div>

        <div class="diff-factors-row">
          ${factors.map(f => `<span class="diff-factor-chip">${f}</span>`).join('')}
          <span class="diff-factor-chip">⏳ ${settings.time_limit_sec}s Limit</span>
          <span class="diff-factor-chip">💡 ${settings.hints_allowed} Hints</span>
          ${settings.bonus_seals > 0 ? `<span class="diff-factor-chip" style="color: #E9C46A;">🪙 +${settings.bonus_seals} Bonus Seals</span>` : ''}
        </div>

        <p class="diff-guidance">
          ✦ ${settings.guidance}
        </p>
      </div>
    `;
  }

  /**
   * Renders the 5-Pillar Harappan Knowledge Matrix
   */
  renderKnowledgeMatrix(containerId, progress) {
    const container = document.getElementById(containerId);
    if (!container || !progress) return;

    const domains = progress.domains || [];
    const overallIndex = progress.overall_knowledge_index || 0;
    const summary = progress.pedagogical_summary || 'Tracking learning progress across all historical domains.';

    container.innerHTML = `
      <div class="knowledge-matrix-container">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px;">
          <div>
            <h4 style="font-family: 'Cinzel', serif; color: var(--color-terracotta-gold, #E9C46A); margin: 0 0 4px 0;">
              📈 Harappan Knowledge Matrix (Cognitive Progress Analysis)
            </h4>
            <p style="font-size: 0.8rem; color: var(--color-sandstone, #D4A373); margin: 0;">
              Multi-pillar cognitive tracer across authentic archaeological domains
            </p>
          </div>
          <div style="background: rgba(233,196,106,0.15); border: 1px solid #E9C46A; padding: 4px 12px; border-radius: 8px; text-align: center;">
            <span style="font-family: 'Cinzel', serif; font-size: 1.1rem; font-weight: 800; color: #FFF8EE;">
              ${overallIndex}%
            </span>
            <div style="font-size: 0.65rem; text-transform: uppercase; color: #E9C46A;">Knowledge Index</div>
          </div>
        </div>

        <div class="knowledge-grid">
          ${domains.map(d => `
            <div class="knowledge-pillar-card">
              <div class="pillar-card-top">
                <span class="pillar-title">${d.icon} ${d.name}</span>
                <span class="pillar-status-tag">${d.status}</span>
              </div>
              <p class="pillar-desc">${d.summary}</p>
              <div style="display: flex; justify-content: space-between; font-size: 0.72rem; color: #D4A373; margin-bottom: 4px;">
                <span>Mastery</span>
                <span style="font-weight: 800; color: #E9C46A;">${d.mastery_percentage}%</span>
              </div>
              <div style="width: 100%; height: 6px; background: rgba(255,255,255,0.08); border-radius: 3px; overflow: hidden;">
                <div style="height: 100%; width: ${d.mastery_percentage}%; background: linear-gradient(90deg, #E9C46A, #2EC4B6); border-radius: 3px;"></div>
              </div>
            </div>
          `).join('')}
        </div>

        <div style="margin-top: 14px; background: rgba(10,8,7,0.5); padding: 10px 14px; border-radius: 8px; font-size: 0.82rem; color: #E2D9D2;">
          <strong>Curatorial Insight:</strong> ${summary}
        </div>
      </div>
    `;
  }

  /**
   * Backward-compatible simulation method for testing
   */
  async runInteractiveSimulation() {
    this.renderHeritageGuide();
  }
}

const aiController = new BharatAiController();
window.aiController = aiController;
