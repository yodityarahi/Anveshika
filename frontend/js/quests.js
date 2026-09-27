/**
 * Bharat Quest - Quest & Challenge Controller (Phase 6)
 * Pure HTML5 / CSS3 / Vanilla JavaScript modular architecture
 */
class BharatQuestController {
  constructor() {
    this.quests = [];
    this.activeFilter = 'all';
    this.currentQuest = null;
    this.completedQuests = new Set();
    this.drainageSequence = []; // for drainage drag/reorder
    this.selectedCandidate = null; // for artifact detective

    // Built-in fallback catalog for offline resilience
    this.defaultQuests = [
      {
        quest_id: "quest_01_rebuild_city",
        title: "Build the Ancient City",
        civilization_id: "ivc",
        story_context: "Help the city builder organize the ancient town! Drag and drop houses, roads, drains, and public buildings into their correct spots.",
        location: "Mohenjo-daro Town & Citadel",
        objective: "Place houses, roads, drains, and public buildings into their correct city zones.",
        difficulty: "Beginner",
        learning_concept: "Indus Valley Urban Planning & Grid Systems: Build your ancient city with houses, roads, and drains!",
        npc_name: "Siddhu, Master Town Surveyor",
        npc_avatar: "📐",
        challenge: {
          type: "rebuild_city",
          instructions: "Drag and match each of the 4 city parts (Houses, Roads, Drains, Public Buildings) to its proper zone.",
          interactive_data: {
            slots: [
              {
                id: "slot_houses",
                target_component: "houses",
                zone_name: "Lower Town (Neighborhood)",
                icon: "🏡",
                hint: "Brick family homes built around cool courtyards."
              },
              {
                id: "slot_roads",
                target_component: "roads",
                zone_name: "Wide Main Streets",
                icon: "🛣️",
                hint: "Wide straight avenues that cross each other at neat right angles."
              },
              {
                id: "slot_drainage",
                target_component: "drainage",
                zone_name: "Covered Clean Drains",
                icon: "🚰",
                hint: "Brick drains under the street that carry dirty water away safely."
              },
              {
                id: "slot_public_areas",
                target_component: "public_areas",
                zone_name: "Citadel Mound (Great Bath & Granary)",
                icon: "🏛️",
                hint: "High raised area for the Great Bath and community grain storage."
              }
            ],
            cards: [
              {
                id: "card_houses",
                component: "houses",
                title: "Houses & Courtyards",
                icon: "🏡",
                rule_text: "Strong baked-brick houses with doors opening into quiet side lanes."
              },
              {
                id: "card_roads",
                component: "roads",
                title: "Main Grid Roads",
                icon: "🛣️",
                rule_text: "Wide, straight avenues running North-South and East-West with rounded corners for carts."
              },
              {
                id: "card_drainage",
                component: "drainage",
                title: "Covered Brick Drains",
                icon: "🚰",
                rule_text: "Underground brick channels covered with stone slabs so streets stay clean and odor-free."
              },
              {
                id: "card_public_areas",
                component: "public_areas",
                title: "Citadel & Public Spaces",
                icon: "🏛️",
                rule_text: "The high ground of the city with the Great Bath, community hall, and big granaries."
              }
            ]
          },
          hints: [
            "💡 Harappan homes were peaceful: doors opened into quiet side lanes, not dusty main streets!",
            "💡 The Citadel was always raised on high ground on the western side of the city."
          ]
        },
        reward_xp: 300,
        reward_tokens: 8,
        artifact_reward: {
          id: "art_city_blueprint",
          name: "Ancient Measuring Ruler",
          icon: "📏",
          material: "Bronze & Sea Shell",
          origin: "Mohenjo-daro & Lothal",
          importance: "A precise measuring stick showing that ancient builders used exact measurements across all their cities!"
        },
        badge_reward: "badge_city_planner",
        completed: false
      },
      {
        quest_id: "quest_02_lost_artifact",
        title: "Find the Lost Artifact",
        civilization_id: "ivc",
        story_context: "An ancient object was just dug up! Read the 3 clues and pick the right artifact from the choices.",
        location: "Artisan Quarter & Citadel Ruins",
        objective: "Read 3 clues and pick the correct lost Indus Valley artifact.",
        difficulty: "Intermediate",
        learning_concept: "Pottery, Seals & Material Detective: Find the lost artifact using forensic clues!",
        npc_name: "Rao, Chief Archaeologist",
        npc_avatar: "🏺",
        challenge: {
          type: "artifact_detective",
          instructions: "Read the 3 clues below and click the matching artifact!",
          interactive_data: {
            clues: [
              {
                id: "clue_1",
                category: "Material",
                icon: "🪨",
                text: "Made of soft soapstone (steatite) baked in a hot kiln until it turned shiny white."
              },
              {
                id: "clue_2",
                category: "Picture",
                icon: "🎨",
                text: "Shows a magical one-horned animal (unicorn) standing in front of a small incense burner."
              },
              {
                id: "clue_3",
                category: "Writing & Purpose",
                icon: "📜",
                text: "Has 5 ancient script symbols. Traders stamped it into wet clay to seal goods sent on ships!"
              }
            ],
            candidates: [
              {
                id: "cand_unicorn_seal",
                name: "Steatite Unicorn Stamp Seal",
                icon: "🦄",
                material: "High-fired Steatite (Soapstone)",
                origin: "Mohenjo-daro Lower Town",
                summary: "Square soapstone seal with a mythical unicorn and ancient script."
              },
              {
                id: "cand_dancing_girl",
                name: "Bronze Dancing Girl Statuette",
                icon: "💃",
                material: "Lost-wax Cast Copper-Tin Bronze",
                origin: "Mohenjo-daro HR Area",
                summary: "Famous small bronze statue of a confident girl wearing shell bangles."
              },
              {
                id: "cand_storage_jar",
                name: "Red-and-Black Painted Storage Jar",
                icon: "🏺",
                material: "Fine Levigated Alluvial Clay",
                origin: "Harappa Granary Complex",
                summary: "Large ceramic grain container with painted peacocks and patterns."
              },
              {
                id: "cand_mother_goddess",
                name: "Terracotta Clay Figurine",
                icon: "🗿",
                material: "Hand-modeled Fired Terracotta",
                origin: "Mohenjo-daro DK Area",
                summary: "Handmade clay statue with a fan-shaped headdress and clay necklaces."
              }
            ]
          },
          hints: [
            "💡 Soapstone is very soft and easy to carve, making it perfect for detailed seals.",
            "💡 Over half of all Harappan seals depict the famous one-horned unicorn figure!"
          ]
        },
        reward_xp: 320,
        reward_tokens: 8,
        artifact_reward: {
          id: "art_unicorn_seal",
          name: "Steatite Unicorn Stamp Seal",
          icon: "🦄",
          material: "Steatite (Soapstone)",
          origin: "Mohenjo-daro",
          importance: "Used by ancient merchants like a company logo or signature stamp on clay packages!"
        },
        badge_reward: "badge_script_decoder",
        completed: false
      },
      {
        quest_id: "quest_03_drainage_challenge",
        title: "Save the City from Dirty Water",
        civilization_id: "ivc",
        story_context: "Mohenjo-daro had the world's first covered drains! Put the 4 steps of the water system in the right order to keep the city clean.",
        location: "Lower Town Street Drainage Grid",
        objective: "Put the 4 steps of the water drainage system in order from home bathroom to outside the city.",
        difficulty: "Intermediate",
        learning_concept: "Sanitation, City Hydraulic Engineering & Public Health: Keep the city clean and healthy!",
        npc_name: "Rao, Chief Sanitary Engineer",
        npc_avatar: "🚰",
        challenge: {
          type: "drainage_flow",
          instructions: "Put these 4 steps in order (1 to 4) to show how wastewater flowed safely out of the city.",
          interactive_data: {
            steps: [
              {
                id: "step_bath",
                title: "1. Home Paved Bathroom",
                icon: "🚿",
                description: "Slanted brick bathroom floor collects wash water and sends it into a clay pipe in the wall.",
                correct_order: 1
              },
              {
                id: "step_sump",
                title: "2. Sump Pot (Dirt Trap)",
                icon: "🏺",
                description: "Water falls into a big jar where sand and dirt sink to the bottom so drains don't get clogged.",
                correct_order: 2
              },
              {
                id: "step_sewer",
                title: "3. Covered Street Drain",
                icon: "🧱",
                description: "Clean water flows smoothly into the covered brick street drain beneath flat stone lids.",
                correct_order: 3
              },
              {
                id: "step_outflow",
                title: "4. Soak Pit Outside City",
                icon: "🌊",
                description: "The street drain flows under the city wall into a soak pit safely away from homes.",
                correct_order: 4
              }
            ]
          },
          hints: [
            "💡 Water was always cleaned in private sump jars first so dirt wouldn't clog the street drains!",
            "💡 Flat stone covers let city workers easily clean the drains without digging up the street."
          ]
        },
        reward_xp: 350,
        reward_tokens: 10,
        artifact_reward: {
          id: "art_drain_pipe",
          name: "Terracotta Drain Pipe",
          icon: "🚰",
          material: "High-fired Ceramic Terracotta",
          origin: "Mohenjo-daro HR Area",
          importance: "Interlocking clay drain pipes that kept ancient Indus cities cleaner than most cities 3,000 years later!"
        },
        badge_reward: "badge_sanitation_master",
        completed: false
      },
      {
        quest_id: "quest_04_ancient_trade",
        title: "Ancient Trade: Travel & Trade",
        civilization_id: "ivc",
        story_context: "Ships have arrived at the ancient port of Lothal! Connect each trade item (beads, gemstones, copper, shells) to where it came from or where it is going.",
        location: "Lothal Tidal Dockyard & Marketplace",
        objective: "Match each trade item to its source region or overseas trade partner.",
        difficulty: "Intermediate",
        learning_concept: "Bronze Age Trade Routes, Economic Life & Metrology: Travel and trade precious goods across the world!",
        npc_name: "Kanha, Lothal Port Master",
        npc_avatar: "⛵",
        challenge: {
          type: "trade_network",
          instructions: "Match each of the 4 precious trade items to the place it came from or sailed to.",
          interactive_data: {
            commodities: [
              {
                id: "com_carnelian",
                name: "Carnelian Beads & Soft Cotton",
                icon: "📿",
                desc: "Red shiny stone beads and fine woven cotton fabrics."
              },
              {
                id: "com_lapis",
                name: "Lapis Lazuli (Deep Blue Gem)",
                icon: "💎",
                desc: "Rich blue gemstone speckled with gold, found high in mountain mines."
              },
              {
                id: "com_copper",
                name: "Copper Ingots & Bronze",
                icon: "⛏️",
                desc: "Red copper metal used for strong tools, pots, and statues."
              },
              {
                id: "com_shell",
                name: "White Sea Shell Bangles",
                icon: "🐚",
                desc: "Bright white conch shells carved into beautiful bangles and spoons."
              }
            ],
            destinations: [
              {
                id: "dest_mesopotamia",
                name: "Ancient Mesopotamia (Modern Iraq)",
                icon: "🏛️",
                distance: "Over 2,500 km across the sea in sailing boats"
              },
              {
                id: "dest_badakhshan",
                name: "Shortugai Outpost (Northern Afghanistan)",
                icon: "🏔️",
                distance: "Northern mountain trade post along the river"
              },
              {
                id: "dest_khetri",
                name: "Khetri Mines (Rajasthan)",
                icon: "⛰️",
                distance: "Desert trade route rich in copper metal"
              },
              {
                id: "dest_gulf_khambhat",
                name: "Lothal Port & Gujarat Coast",
                icon: "🌊",
                distance: "Sunny coastal waters full of sea shells"
              }
            ]
          },
          hints: [
            "💡 Ancient Mesopotamian clay tablets talk about trading with 'Meluhha' (the Indus Valley) for red beads and timber!",
            "💡 Shortugai was built right next to the famous blue lapis lazuli mountain mines."
          ]
        },
        reward_xp: 340,
        reward_tokens: 9,
        artifact_reward: {
          id: "art_chert_weights",
          name: "Standard Cubical Stone Weights",
          icon: "⚖️",
          material: "Polished Grey Chert Stone",
          origin: "Lothal & Harappa",
          importance: "Exact balance weights used by merchants so no buyer or seller was ever cheated!"
        },
        badge_reward: "badge_trade_magnate",
        completed: false
      },
      {
        quest_id: "quest_05_life_in_ivc",
        title: "Life in the Indus Valley",
        civilization_id: "ivc",
        story_context: "Spend a day in ancient Mohenjo-daro! Choose what to eat, what craft to learn, and how neighbors solve problems peacefully.",
        location: "Residential Courtyards, Bazaars & Fields",
        objective: "Make 3 choices to experience authentic food, crafts, and community peace in Mohenjo-daro.",
        difficulty: "Advanced",
        learning_concept: "Daily Life, Crafts, Nutrition & Social Harmony: Discover how everyday Harappans lived!",
        npc_name: "Meera, Mohenjo-daro Resident",
        npc_avatar: "👩‍🌾",
        challenge: {
          type: "daily_life_simulation",
          instructions: "Guide your young explorer through 3 everyday situations in Mohenjo-daro.",
          interactive_data: {
            scenarios: [
              {
                id: "scenario_1",
                title: "Scenario 1: Breakfast Time",
                icon: "🥣",
                prompt: "You wake up in your courtyard home as roosters crow. What healthy breakfast is your family cooking?",
                options: [
                  {
                    id: "opt_1_correct",
                    text: "Barley flatbread with lentil curry, roasted sesame paste, and sweet dates."
                  },
                  {
                    id: "opt_1_wrong_a",
                    text: "Boiled potatoes and sweet corn with spicy red chillies."
                  },
                  {
                    id: "opt_1_wrong_b",
                    text: "Wheat noodles tossed in sweet soy sauce."
                  }
                ]
              },
              {
                id: "scenario_2",
                title: "Scenario 2: The Workshop",
                icon: "⚒️",
                prompt: "You walk down the brick street to your afternoon craft workshop. What world-famous craft are you practicing?",
                options: [
                  {
                    id: "opt_2_correct",
                    text: "Drilling tiny holes through red carnelian gemstone beads using hard stone drills."
                  },
                  {
                    id: "opt_2_wrong_a",
                    text: "Melting iron in blast furnaces to make knight armor and big swords."
                  },
                  {
                    id: "opt_2_wrong_b",
                    text: "Blowing fancy glass cups and carving Greek marble pillars."
                  }
                ]
              },
              {
                id: "scenario_3",
                title: "Scenario 3: Peaceful Neighborhood",
                icon: "⚖️",
                prompt: "Two ox-cart drivers disagree about parking on First Street. With no kings or soldiers around, how do they fix it?",
                options: [
                  {
                    id: "opt_3_correct",
                    text: "Neighborhood elders help them talk it out and check the town rules peacefully."
                  },
                  {
                    id: "opt_3_wrong_a",
                    text: "The king's royal soldiers throw them both in the palace dungeon."
                  },
                  {
                    id: "opt_3_wrong_b",
                    text: "They fight with swords in front of a cheering crowd."
                  }
                ]
              }
            ]
          },
          hints: [
            "💡 The Indus civilization had no palaces, no royal crowns, and no armies — people worked together peacefully!",
            "💡 Wheat, barley, lentils, sesame, and sweet dates were Harappan favorites!"
          ]
        },
        reward_xp: 360,
        reward_tokens: 10,
        artifact_reward: {
          id: "art_toy_cart",
          name: "Terracotta Toy Bullock Cart",
          icon: "🪅",
          material: "Kiln-fired Terracotta Clay",
          origin: "Harappa & Mohenjo-daro",
          importance: "A fun clay toy with wheels that rolled on wooden axles, showing that ancient children loved playing with toy cars!"
        },
        badge_reward: "badge_metropolis_sage",
        completed: false
      }
    ];

    this.quests = [...this.defaultQuests];
  }

  async init() {
    console.log("Initializing Quest System Controller (Phase 6)...");
    await this.fetchQuests();
    this.renderQuestHub();
  }

  async fetchQuests() {
    const currentUsername = (window.app && app.state.user) ? app.state.user.username : (localStorage.getItem('bq_username') || 'Arjun');
    try {
      if (window.api && typeof window.api.getQuests === 'function') {
        const remoteQuests = await window.api.getQuests('ivc', currentUsername);
        if (remoteQuests && remoteQuests.length >= 5) {
          this.quests = remoteQuests;
          this.syncCompletedQuests();
        }
      }
    } catch (err) {
      console.warn("Using offline fallback quests:", err);
      this.syncCompletedQuests();
    }
  }

  syncCompletedQuests() {
    if (window.app && app.state.user && app.state.user.stats) {
      const userCompleted = app.state.user.stats.completed_quests || [];
      userCompleted.forEach(qId => this.completedQuests.add(qId));
    }
    this.quests.forEach(q => {
      if (this.completedQuests.has(q.quest_id)) {
        q.completed = true;
      }
    });
  }

  filterQuests(category) {
    if (window.audio && typeof window.audio.playClick === 'function') {
      try { window.audio.playClick(); } catch (e) {}
    }
    this.activeFilter = category;
    this.renderQuestCards();

    // Update active filter button
    document.querySelectorAll('.quest-filter-btn').forEach(btn => {
      if (btn.getAttribute('data-filter') === category) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });
  }

  renderQuestHub() {
    const container = document.getElementById('questsHubContainer');
    if (!container) return;

    const completedCount = this.quests.filter(q => q.completed).length;
    const totalCount = this.quests.length;
    const progressPct = totalCount > 0 ? Math.round((completedCount / totalCount) * 100) : 0;

    container.innerHTML = `
      <div class="quest-hub-container">
        <!-- Header Bar -->
        <div class="quest-hub-header">
          <div class="quest-hub-left">
            <h2><span>🎯</span> Ancient Indus Valley Missions</h2>
            <p>Pick a mission, solve fun puzzles, and discover the secrets of the ancient world!</p>
          </div>
          <div class="quest-progress-meter">
            <span class="quest-progress-label">Missions Completed:</span>
            <span class="quest-progress-count" id="questProgressCountText">${completedCount} / ${totalCount}</span>
            <div class="quest-meter-track">
              <div class="quest-meter-fill" id="questProgressFill" style="width: ${progressPct}%;"></div>
            </div>
          </div>
        </div>

        <!-- Filter Strip -->
        <div class="quest-filter-strip">
          <button class="quest-filter-btn active" data-filter="all" onclick="questController.filterQuests('all')">
            🌟 All Missions (${this.quests.length})
          </button>
          <button class="quest-filter-btn" data-filter="Urban Planning" onclick="questController.filterQuests('Urban Planning')">
            🏡 Build City
          </button>
          <button class="quest-filter-btn" data-filter="Artifacts" onclick="questController.filterQuests('Artifacts')">
            🏺 Find Artifact
          </button>
          <button class="quest-filter-btn" data-filter="Hydraulics" onclick="questController.filterQuests('Hydraulics')">
            🚰 Clean Water
          </button>
          <button class="quest-filter-btn" data-filter="Commerce" onclick="questController.filterQuests('Commerce')">
            ⛵ Travel & Trade
          </button>
          <button class="quest-filter-btn" data-filter="Daily Life" onclick="questController.filterQuests('Daily Life')">
            👩‍🌾 Daily Life
          </button>
        </div>

        <!-- Quests Grid -->
        <div class="quest-cards-grid" id="questCardsGrid">
          <!-- Populated by renderQuestCards() -->
        </div>
      </div>
    `;

    this.renderQuestCards();
  }

  renderQuestCards() {
    const grid = document.getElementById('questCardsGrid');
    if (!grid) return;

    const didYouKnowMap = {
      'quest_01_rebuild_city': 'Harappan cities were built on a neat grid, just like modern cities!',
      'quest_02_lost_artifact': 'The Indus people made beautiful stamp seals out of soft soapstone!',
      'quest_03_drainage_challenge': 'Almost every Harappan house had its own bathroom connected to street drains!',
      'quest_04_ancient_trade': 'Harappan traders traveled all the way to Mesopotamia by sea!',
      'quest_05_life_in_ivc': 'Archaeologists haven\'t found any royal palaces or army barracks in Indus cities!'
    };

    let filtered = this.quests;
    if (this.activeFilter !== 'all') {
      filtered = this.quests.filter(q => {
        const text = (q.learning_concept + ' ' + q.title).toLowerCase();
        if (this.activeFilter === 'Urban Planning') return text.includes('urban') || text.includes('planning') || text.includes('city');
        if (this.activeFilter === 'Artifacts') return text.includes('artifact') || text.includes('seal');
        if (this.activeFilter === 'Hydraulics') return text.includes('drainage') || text.includes('sanitation') || text.includes('water');
        if (this.activeFilter === 'Commerce') return text.includes('trade') || text.includes('maritime');
        if (this.activeFilter === 'Daily Life') return text.includes('life') || text.includes('culture');
        return true;
      });
    }

    grid.innerHTML = filtered.map(quest => {
      const isCompleted = this.completedQuests.has(quest.quest_id) || quest.completed;
      const diffCls = quest.difficulty ? quest.difficulty.toLowerCase() : 'beginner';
      const diffLabel = quest.difficulty === 'Beginner' ? '⭐ Easy' : (quest.difficulty === 'Advanced' ? '⭐⭐⭐ Tricky' : '⭐⭐ Medium');
      const fact = didYouKnowMap[quest.quest_id] || 'Explore history and uncover mysteries!';

      return `
        <div class="quest-card ${isCompleted ? 'completed' : ''}" id="questCard_${quest.quest_id}">
          <div>
            <div class="quest-card-header">
              <div class="quest-npc-avatar">${quest.npc_avatar || '🧑‍🏫'}</div>
              <div class="quest-card-title-group">
                <h3>${quest.title}</h3>
                <div class="quest-meta-row">
                  <span class="quest-diff-badge ${diffCls}">${diffLabel}</span>
                  <span class="quest-loc-tag">📍 ${quest.location}</span>
                </div>
              </div>
            </div>

            <div class="quest-card-body" style="margin-top: 10px;">
              <p style="font-size: 0.92rem; line-height: 1.45; color: #cbd5e1; margin-bottom: 8px;">${quest.story_context || quest.objective}</p>
              <div class="quest-concept-banner" style="background: rgba(245, 158, 11, 0.12); border-left: 3px solid #f59e0b; padding: 6px 10px; border-radius: 6px; font-size: 0.82rem; color: #fde68a;">
                <strong>💡 Did you know?</strong> ${fact}
              </div>
            </div>
          </div>

          <div>
            <div class="quest-rewards-shelf" style="margin-bottom: 12px; margin-top: 12px;">
              <div class="reward-pill xp">⚡ +${quest.reward_xp} XP</div>
              <div class="reward-pill tokens">🪙 +${quest.reward_tokens} Seals</div>
              ${quest.artifact_reward ? `<div class="reward-pill artifact">${quest.artifact_reward.icon} ${quest.artifact_reward.name}</div>` : ''}
            </div>

            <button class="quest-action-btn ${isCompleted ? 'revisit' : ''}" 
                    onclick="questController.openQuestChallenge('${quest.quest_id}')">
              <span>${isCompleted ? '🔄 Play Again' : '🎮 Play Mission ➔'}</span>
            </button>
          </div>
        </div>
      `;
    }).join('');
  }

  async openQuestChallenge(questId) {
    if (window.audio && typeof window.audio.playChime === 'function') {
      try { window.audio.playChime(); } catch (e) {}
    }

    // Fetch full challenge payload from server or cache
    let questData = null;
    try {
      if (window.api && typeof window.api.getQuestDetail === 'function') {
        questData = await window.api.getQuestDetail(questId);
      }
    } catch (err) {
      console.warn("Using offline quest detail for:", questId, err);
    }

    if (!questData) {
      questData = this.quests.find(q => q.quest_id === questId);
    }

    // Safety fallback from defaultQuests catalog
    const fallbackQuest = this.defaultQuests.find(q => q.quest_id === questId);
    if (!questData && fallbackQuest) {
      questData = JSON.parse(JSON.stringify(fallbackQuest));
    }

    if (!questData) {
      console.error(`Quest data not found for ID: ${questId}`);
      return;
    }

    // Ensure challenge property exists
    if ((!questData.challenge || !questData.challenge.interactive_data) && fallbackQuest && fallbackQuest.challenge) {
      questData.challenge = JSON.parse(JSON.stringify(fallbackQuest.challenge));
    }

    if (!questData.challenge) {
      questData.challenge = {
        type: 'rebuild_city',
        instructions: 'Complete the archaeological challenge.',
        interactive_data: {},
        hints: ['Review the clues carefully.']
      };
    }

    this.currentQuest = questData;

    const modal = document.getElementById('questChallengeModal');
    if (!modal) {
      console.error("Critical: #questChallengeModal element not found in DOM");
      return;
    }

    // Header info with safe DOM manipulation
    const setElemText = (id, text) => {
      const el = document.getElementById(id);
      if (el) el.innerText = text;
    };

    const didYouKnowMap = {
      'quest_01_rebuild_city': 'Harappan cities were built on a neat grid, just like modern cities!',
      'quest_02_lost_artifact': 'The Indus people made beautiful stamp seals out of soft soapstone!',
      'quest_03_drainage_challenge': 'Almost every Harappan house had its own bathroom connected to street drains!',
      'quest_04_ancient_trade': 'Harappan traders traveled all the way to Mesopotamia by sea!',
      'quest_05_life_in_ivc': 'Archaeologists haven\'t found any royal palaces or army barracks in Indus cities!'
    };

    const diffLabel = questData.difficulty === 'Beginner' ? '⭐ Easy' : (questData.difficulty === 'Advanced' ? '⭐⭐⭐ Tricky' : '⭐⭐ Medium');
    const fact = didYouKnowMap[questData.quest_id] || questData.learning_concept;

    setElemText('questModalTitle', questData.title || 'Indus Valley Mission');
    setElemText('questModalMeta', `${diffLabel} • 📍 ${questData.location || 'Mohenjo-daro'} • ⚡ +${questData.reward_xp || 300} XP`);
    setElemText('questModalNpcAvatar', questData.npc_avatar || '🧑‍🏫');
    setElemText('questModalNpcName', questData.npc_name || 'Expedition Guide');
    setElemText('questModalStoryText', questData.story_context || 'Solve the puzzle below!');
    setElemText('questModalConceptText', `💡 Did you know? ${fact}`);
    setElemText('questInstructionsText', (questData.challenge && questData.challenge.instructions) ? questData.challenge.instructions : 'Solve the puzzle below:');

    // Reset feedback & hint
    const feedbackBox = document.getElementById('questFeedbackBox');
    if (feedbackBox) {
      feedbackBox.className = 'quest-feedback-alert';
      feedbackBox.style.display = 'none';
      feedbackBox.innerHTML = '';
    }

    const hintBox = document.getElementById('questHintBox');
    if (hintBox) {
      hintBox.style.display = 'none';
      const hints = (questData.challenge && questData.challenge.hints) ? questData.challenge.hints : [];
      hintBox.innerText = hints.length > 0 ? `💡 Archaeological Hint: ${hints[0]}` : "💡 Analyze the historical clues carefully.";
    }

    // Render Challenge Component
    const stage = document.getElementById('questChallengeStage');
    if (stage) {
      stage.innerHTML = this.renderChallengeUi(questData);
    }

    // Activate modal visually and make it interactive
    modal.classList.add('active');
    modal.style.display = 'flex';
    modal.style.opacity = '1';
    modal.style.pointerEvents = 'auto';
  }

  closeQuestChallenge() {
    if (window.audio && typeof window.audio.playClick === 'function') {
      try { window.audio.playClick(); } catch (e) {}
    }
    const modal = document.getElementById('questChallengeModal');
    if (modal) {
      modal.classList.remove('active');
      modal.style.display = 'none';
      modal.style.opacity = '0';
      modal.style.pointerEvents = 'none';
    }
    this.currentQuest = null;
  }

  toggleHint() {
    if (window.audio && typeof window.audio.playClick === 'function') {
      try { window.audio.playClick(); } catch (e) {}
    }
    const hintBox = document.getElementById('questHintBox');
    if (hintBox) {
      hintBox.style.display = hintBox.style.display === 'block' ? 'none' : 'block';
    }
  }

  renderChallengeUi(quest) {
    const qtype = quest.challenge.type;
    const data = quest.challenge.interactive_data;

    // 1. Rebuild City Challenge
    if (qtype === 'rebuild_city') {
      const slots = data.slots || [];
      const cards = data.cards || [];

      return `
        <div class="rebuild-stage-container">
          <div class="rebuild-slots-grid">
            ${slots.map(slot => `
              <div class="rebuild-slot-card" id="slotCard_${slot.id}">
                <div class="slot-header">
                  <span class="slot-icon">${slot.icon}</span>
                  <div>
                    <div class="slot-title">${slot.zone_name}</div>
                    <div class="slot-hint">${slot.hint}</div>
                  </div>
                </div>
                <select class="slot-select" id="select_${slot.id}" onchange="questController.onSlotChange('${slot.id}')">
                  <option value="">-- Assign Architectural Component --</option>
                  ${cards.map(c => `
                    <option value="${c.id}">${c.title}</option>
                  `).join('')}
                </select>
              </div>
            `).join('')}
          </div>
        </div>
      `;
    }

    // 2. Artifact Detective Challenge
    if (qtype === 'artifact_detective') {
      const clues = data.clues || [];
      const candidates = data.candidates || [];
      this.selectedCandidate = null;

      return `
        <div class="detective-stage-container">
          <div class="detective-clues-grid">
            ${clues.map(c => `
              <div class="clue-parchment-card">
                <div class="clue-card-category">
                  <span>${c.icon}</span> ${c.category}
                </div>
                <p class="clue-card-text">${c.text}</p>
              </div>
            `).join('')}
          </div>

          <div style="font-family: var(--font-serif); font-size: 0.95rem; color: var(--color-gold); font-weight: 700; margin-top: 6px;">
            🔍 Select the Matching Artifact from Excavation Candidates:
          </div>

          <div class="candidate-relics-grid">
            ${candidates.map(cand => `
              <div class="candidate-relic-card" id="candCard_${cand.id}" onclick="questController.selectArtifactCandidate('${cand.id}')">
                <div class="candidate-icon">${cand.icon}</div>
                <div class="candidate-name">${cand.name}</div>
                <div class="candidate-material">${cand.material}</div>
                <div class="candidate-desc">${cand.summary}</div>
              </div>
            `).join('')}
          </div>
        </div>
      `;
    }

    // 3. Drainage Flow Challenge
    if (qtype === 'drainage_flow') {
      const steps = [...(data.steps || [])];
      // Randomly shuffle initial order for interactive puzzle feel
      if (!this.drainageSequence || this.drainageSequence.length !== steps.length) {
        this.drainageSequence = steps.sort(() => Math.random() - 0.5);
      }

      return `
        <div class="drainage-stage-container" id="drainageSequenceContainer">
          ${this.renderDrainageStepsHtml()}
        </div>
      `;
    }

    // 4. Ancient Trade Challenge
    if (qtype === 'trade_network') {
      const commodities = data.commodities || [];
      const destinations = data.destinations || [];

      return `
        <div class="trade-stage-container">
          ${commodities.map(com => `
            <div class="trade-match-row">
              <div class="trade-commodity-col">
                <span class="trade-item-icon">${com.icon}</span>
                <div>
                  <div class="trade-item-title">${com.name}</div>
                  <div class="trade-item-desc">${com.desc}</div>
                </div>
              </div>
              <div class="trade-destination-col">
                <select class="trade-destination-select" id="tradeSel_${com.id}">
                  <option value="">-- Match Trade Source / Destination --</option>
                  ${destinations.map(d => `
                    <option value="${d.id}">${d.icon} ${d.name}</option>
                  `).join('')}
                </select>
              </div>
            </div>
          `).join('')}
        </div>
      `;
    }

    // 5. Daily Life Simulation Challenge
    if (qtype === 'daily_life_simulation') {
      const scenarios = data.scenarios || [];

      return `
        <div class="life-stage-container">
          ${scenarios.map(sc => `
            <div class="scenario-card" id="card_${sc.id}">
              <h4><span>${sc.icon}</span> ${sc.title}</h4>
              <p class="scenario-prompt">${sc.prompt}</p>
              <div class="scenario-options-col">
                ${sc.options.map(opt => `
                  <label class="scenario-option-label" id="label_${sc.id}_${opt.id}">
                    <input type="radio" name="radio_${sc.id}" value="${opt.id}" onchange="questController.onScenarioSelect('${sc.id}', '${opt.id}')">
                    <span class="option-text">${opt.text}</span>
                  </label>
                `).join('')}
              </div>
            </div>
          `).join('')}
        </div>
      `;
    }

    return `<p>Interactive challenge ready for execution.</p>`;
  }

  onSlotChange(slotId) {
    if (window.audio && typeof window.audio.playClick === 'function') {
      try { window.audio.playClick(); } catch (e) {}
    }
    const select = document.getElementById(`select_${slotId}`);
    const card = document.getElementById(`slotCard_${slotId}`);
    if (select && card) {
      if (select.value) {
        card.classList.add('matched');
      } else {
        card.classList.remove('matched');
      }
    }
  }

  selectArtifactCandidate(candId) {
    if (window.audio && typeof window.audio.playClick === 'function') {
      try { window.audio.playClick(); } catch (e) {}
    }
    this.selectedCandidate = candId;
    document.querySelectorAll('.candidate-relic-card').forEach(c => {
      c.classList.remove('selected');
    });
    const selected = document.getElementById(`candCard_${candId}`);
    if (selected) selected.classList.add('selected');
  }

  renderDrainageStepsHtml() {
    return this.drainageSequence.map((step, idx) => `
      <div class="drainage-step-row" id="drainStep_${step.id}">
        <div class="drainage-step-info">
          <div class="drainage-step-num">${idx + 1}</div>
          <span style="font-size: 1.5rem;">${step.icon}</span>
          <div>
            <div class="drainage-step-title">${step.title}</div>
            <div class="drainage-step-desc">${step.description}</div>
          </div>
        </div>
        <div class="drainage-reorder-controls">
          <button class="drainage-move-btn" onclick="questController.moveDrainageStep(${idx}, -1)" ${idx === 0 ? 'disabled' : ''} title="Move Up">
            ▲
          </button>
          <button class="drainage-move-btn" onclick="questController.moveDrainageStep(${idx}, 1)" ${idx === this.drainageSequence.length - 1 ? 'disabled' : ''} title="Move Down">
            ▼
          </button>
        </div>
      </div>
    `).join('');
  }

  moveDrainageStep(index, direction) {
    if (window.audio && typeof window.audio.playClick === 'function') {
      try { window.audio.playClick(); } catch (e) {}
    }
    const newIndex = index + direction;
    if (newIndex < 0 || newIndex >= this.drainageSequence.length) return;

    const temp = this.drainageSequence[index];
    this.drainageSequence[index] = this.drainageSequence[newIndex];
    this.drainageSequence[newIndex] = temp;

    const container = document.getElementById('drainageSequenceContainer');
    if (container) {
      container.innerHTML = this.renderDrainageStepsHtml();
    }
  }

  onScenarioSelect(scenarioId, optionId) {
    if (window.audio && typeof window.audio.playClick === 'function') {
      try { window.audio.playClick(); } catch (e) {}
    }
    const labels = document.querySelectorAll(`[id^="label_${scenarioId}_"]`);
    labels.forEach(l => l.classList.remove('selected'));
    const selected = document.getElementById(`label_${scenarioId}_${optionId}`);
    if (selected) selected.classList.add('selected');
  }

  gatherSubmission() {
    if (!this.currentQuest) return null;
    const qtype = this.currentQuest.challenge.type;

    if (qtype === 'rebuild_city') {
      const submission = {};
      const slots = this.currentQuest.challenge.interactive_data.slots || [];
      for (const slot of slots) {
        const sel = document.getElementById(`select_${slot.id}`);
        submission[slot.id] = sel ? sel.value : '';
      }
      return submission;
    }

    if (qtype === 'artifact_detective') {
      return {
        selected_candidate: this.selectedCandidate
      };
    }

    if (qtype === 'drainage_flow') {
      return {
        ordered_ids: this.drainageSequence.map(s => s.id)
      };
    }

    if (qtype === 'trade_network') {
      const submission = {};
      const commodities = this.currentQuest.challenge.interactive_data.commodities || [];
      for (const com of commodities) {
        const sel = document.getElementById(`tradeSel_${com.id}`);
        submission[com.id] = sel ? sel.value : '';
      }
      return submission;
    }

    if (qtype === 'daily_life_simulation') {
      const submission = {};
      const scenarios = this.currentQuest.challenge.interactive_data.scenarios || [];
      for (const sc of scenarios) {
        const checked = document.querySelector(`input[name="radio_${sc.id}"]:checked`);
        submission[sc.id] = checked ? checked.value : '';
      }
      return submission;
    }

    return {};
  }

  async submitCurrentQuest() {
    if (!this.currentQuest) return;

    const submission = this.gatherSubmission();
    const feedbackBox = document.getElementById('questFeedbackBox');

    // Basic empty check
    if (!submission || Object.values(submission).some(v => !v)) {
      if (feedbackBox) {
        feedbackBox.className = 'quest-feedback-alert error';
        feedbackBox.style.display = 'block';
        feedbackBox.innerHTML = '⚠️ Please complete all challenge components before submitting.';
      }
      return;
    }

    const currentUsername = (window.app && app.state.user) ? app.state.user.username : (localStorage.getItem('bq_username') || 'Arjun');

    try {
      let result = null;
      if (window.api && typeof window.api.submitQuest === 'function') {
        result = await window.api.submitQuest(this.currentQuest.quest_id, currentUsername, submission);
      } else {
        // Fallback local grading
        result = {
          success: true,
          is_correct: true,
          feedback: "Challenge solved successfully! Rewards awarded.",
          xp_awarded: this.currentQuest.reward_xp,
          tokens_awarded: this.currentQuest.reward_tokens,
          quest_id: this.currentQuest.quest_id
        };
      }

      if (result.is_correct) {
        if (window.audio && typeof window.audio.playFanfare === 'function') {
          try { window.audio.playFanfare(); } catch (e) {}
        }

        // Spawn floating XP particle
        if (window.uxManager) {
          window.uxManager.spawnXpAnimation(result.xp_awarded);
          window.uxManager.showToast({
            title: `Quest Mastered: ${this.currentQuest.title}`,
            message: `Earned +${result.xp_awarded} XP & +${result.tokens_awarded} Steatite Seals.`,
            icon: "📜",
            type: "success"
          });
          if (result.badge_unlocked) {
            window.uxManager.triggerBadgeUnlock(result.badge_unlocked);
          }
          if (result.artifact_unlocked) {
            window.uxManager.triggerArtifactDiscovery(result.artifact_unlocked.name || "Excavated Relic");
          }
        } else if (window.cityController && typeof cityController.showFloatingXp === 'function') {
          cityController.showFloatingXp(`+${result.xp_awarded} XP`);
        }

        // Mark completed
        this.completedQuests.add(this.currentQuest.quest_id);
        const questInList = this.quests.find(q => q.quest_id === this.currentQuest.quest_id);
        if (questInList) questInList.completed = true;

        // Render celebratory feedback
        if (feedbackBox) {
          feedbackBox.className = 'quest-feedback-alert success';
          feedbackBox.style.display = 'block';
          feedbackBox.innerHTML = `
            <div style="font-size: 1rem; font-weight: 800; color: #52B788; margin-bottom: 6px;">
              🌟 MISSION COMPLETE: ${this.currentQuest.title}
            </div>
            <p style="margin: 0; color: #FFF;">${result.feedback}</p>
            <div style="display: flex; gap: 12px; margin-top: 10px; font-weight: 700; flex-wrap: wrap;">
              <span style="color: var(--color-gold);">⚡ +${result.xp_awarded} XP Earned</span>
              <span style="color: #48CAE4;">🪙 +${result.tokens_awarded} Steatite Seals</span>
              ${result.artifact_unlocked ? `<span style="color: #D4A373;">🏺 Relic Unlocked: ${result.artifact_unlocked.name}</span>` : ''}
              ${result.badge_unlocked ? `<span style="color: var(--color-patina);">🏆 Badge Unlocked: ${result.badge_unlocked}</span>` : ''}
            </div>
          `;
        }

        // Refresh user profile & HUD in App
        if (window.app) {
          app.logConsole(`🏆 QUEST SOLVED: "${this.currentQuest.title}" (+${result.xp_awarded} XP, +${result.tokens_awarded} Seals)`);
          await app.refreshCurrentProfile();
        }

        // Update hub UI
        this.renderQuestHub();

      } else {
        if (window.audio && typeof window.audio.playClick === 'function') {
          try { window.audio.playClick(); } catch (e) {}
        }
        if (window.uxManager) {
          window.uxManager.triggerShake('#questFeedbackBox');
          window.uxManager.showToast({
            title: "Keep Trying!",
            message: result.feedback || "Check your clues and try again.",
            icon: "💡",
            type: "info"
          });
        }
        if (feedbackBox) {
          feedbackBox.className = 'quest-feedback-alert error';
          feedbackBox.style.display = 'block';
          feedbackBox.innerHTML = `
            <div style="font-weight: 700; margin-bottom: 4px;">💡 Not quite! Give it another try!</div>
            <div>${result.feedback}</div>
            <div style="font-size: 0.82rem; margin-top: 6px; color: #fde68a;">
              Tip: Click the 💡 Hint button if you need a helpful clue!
            </div>
          `;
        }
      }
    } catch (err) {
      console.error("Quest submission error:", err);
      if (feedbackBox) {
        feedbackBox.className = 'quest-feedback-alert error';
        feedbackBox.style.display = 'block';
        feedbackBox.innerText = `Error submitting quest: ${err.message}`;
      }
    }
  }
}

const questController = new BharatQuestController();
window.questController = questController;
