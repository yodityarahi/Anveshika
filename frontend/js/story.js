/**
 * Bharat Quest - Indus Valley Civilization Story Introduction Controller
 * Phase 4: Engaging, Story-Driven Multimodal Introduction Theater
 */
class BharatStoryController {
  constructor() {
    this.currentSceneIndex = 0;
    this.storyData = null;
    this.hasCompletedIntro = localStorage.getItem('bq_story_completed') === 'true';

    // Built-in fallback scenes to ensure 100% offline & instantaneous rendering
    this.defaultScenes = [
      {
        id: "scene_01_dawn",
        scene_number: 1,
        title: "The Dawn Along the Sindhu",
        subtitle: "A Colossal Bronze-Age Civilization Awakens",
        period: "c. 2600 BCE – 1900 BCE • Mature Harappan Phase",
        narrative: "Over 4,500 years ago, while the Egyptian Pyramids were young and Stonehenge was being erected, a breathtaking civilization flourished across the fertile river valleys of ancient Bharat. Spanning over 1 million square kilometers—larger than ancient Egypt and Mesopotamia combined—the Indus Valley Civilization was built along the mighty snow-fed Indus (Sindhu) and the ancient Saraswati (Ghaggar-Hakra) river basins.",
        curiosity_fact: "Archaeologists have identified over 1,000 Harappan settlements across modern-day India (Gujarat, Rajasthan, Haryana, Punjab) and Pakistan.",
        historical_distinction: "Historical Evidence: Radiocarbon dating and stratigraphy confirm thriving mature urban phases from 2600 to 1900 BCE without signs of monarchical palaces or standing imperial armies.",
        badge_icon: "🌅",
        highlight_topic: "Civilization & Era",
        svg_type: "river_dawn"
      },
      {
        id: "scene_02_metropolises",
        scene_number: 2,
        title: "The Great Metropolises",
        subtitle: "Twin Cities and Vast Trade Centers",
        period: "Major Urban Settlements Across the River Valleys",
        narrative: "Instead of isolated rural hamlets, Harappan society was anchored by massive, meticulously organized metropolises. Mohenjo-daro commanded the southern Indus in Sindh, while Harappa dominated the northern river routes of the Ravi. In Gujarat, Lothal served as a bustling maritime gateway, while Dholavira stood as an island fortress in the Rann of Kutch with monumental stone architecture. Farther east, Kalibangan and Rakhigarhi guarded the fertile plains.",
        curiosity_fact: "Rakhigarhi in Haryana is now confirmed to be the largest Harappan site, sprawling across more than 350 hectares!",
        historical_distinction: "Historical Evidence: Consistent city layouts, brick dimensions, and weights across thousands of miles point to shared standards and civic governance.",
        badge_icon: "🏛️",
        highlight_topic: "Major Settlements",
        svg_type: "twin_cities"
      },
      {
        id: "scene_03_grid_planning",
        scene_number: 3,
        title: "The Master Grid Planners",
        subtitle: "The World's Earliest Planned Cities",
        period: "Orthogonal Architecture & The 1:2:4 Brick Ratio",
        narrative: "Imagine strolling down a wide city boulevard 4,500 years ago that is perfectly straight, 10 meters wide, aligned North-to-South, and intersected by cross-streets at exact 90-degree right angles! Harappan urban planning divided cities into a fortified western Citadel for civic assemblies and a sprawling Lower Town for residences. Every building used standardized kiln-fired bricks following a strict mathematical ratio: 1 unit thick, 2 units wide, and 4 units long (1:2:4).",
        curiosity_fact: "Unlike sun-dried mud bricks used in Mesopotamia that dissolved during rains, Harappan baked bricks were moisture-resistant and have survived for millennia.",
        historical_distinction: "Historical Evidence: Burnt brick dimensions excavated at Harappa, Mohenjo-daro, and Lothal exhibit uniform 1:2:4 ratios across centuries.",
        badge_icon: "📐",
        highlight_topic: "City Planning & Masonry",
        svg_type: "grid_planning"
      },
      {
        id: "scene_04_sanitation",
        scene_number: 4,
        title: "The Miracle of Public Hygiene",
        subtitle: "Subterranean Drainage & The Great Bath",
        period: "World's First Underground Sewer Engineering",
        narrative: "The crowning marvel of the Indus civilization was its hygiene infrastructure—unequaled anywhere in the world until the 19th century! Nearly every home featured a private paved bathroom. Wastewater traveled down terracotta chutes into corbelled brick sewer lines buried under street pavements. Inspection manholes with removable limestone covers allowed civic workers to clear blockages. At Mohenjo-daro, the iconic Great Bath was sealed with natural bitumen (asphalt) to create a watertight public pool.",
        curiosity_fact: "Every neighborhood featured soak-pits to separate solid waste from runoff, preventing street contamination.",
        historical_distinction: "Historical Evidence: Intact drainage networks and inspection chambers are documented in ASI excavation reports at Mohenjo-daro, Harappa, and Dholavira.",
        badge_icon: "🚰",
        highlight_topic: "Drainage & Hygiene",
        svg_type: "drainage_system"
      },
      {
        id: "scene_05_trade",
        scene_number: 5,
        title: "Seafarers & The Standard Weights",
        subtitle: "Maritime Docks & Precision Metrology",
        period: "International Trade with Ancient Mesopotamia & the Gulf",
        narrative: "The Harappans were daring international merchants. At Lothal in Gujarat, maritime engineers constructed the world's earliest known tidal dockyard, complete with a water sluice lock to float merchant galleys regardless of tidal ebb and flow. Harappan merchant ships carried etched carnelian beads, fine cotton textiles ('Sindhu'), copper, and ivory across the Arabian Sea to ancient Sumer (Mesopotamia), where clay cuneiform tablets recorded trade with the wealthy land of 'Meluhha'.",
        curiosity_fact: "Commerce was governed by standardized chert cubical weights following a binary sequence: 1, 2, 4, 8, 16, 32... up to decimal ratios for massive bulk trade.",
        historical_distinction: "Historical Evidence: Mesopotamian records directly cite imports from Meluhha, and Indus seals and cubical chert weights have been excavated in Ur and Kish.",
        badge_icon: "⛵",
        highlight_topic: "Maritime Commerce & Weights",
        svg_type: "maritime_trade"
      },
      {
        id: "scene_06_crafts",
        scene_number: 6,
        title: "Master Artisans & Enigmatic Script",
        subtitle: "Bead Kilns, Bronze Sculptures & Steatite Seals",
        period: "Bronze-Age Metallurgy & Undeciphered Inscriptions",
        narrative: "Indus artisans possessed astonishing technical mastery. At Lothal and Chanhudaro, bead factories drilled microscopic holes through hard carnelian stone using diamond-tipped drills and fired them in multi-chamber kilns to produce fiery red gems. Metallurgists used the delicate 'lost-wax' bronze casting process to sculpt the famous 'Dancing Girl of Mohenjo-daro'. Meanwhile, scribes carved hundreds of exquisite steatite stamp seals featuring unicorns, humped zebu bulls, and the meditating Pashupati, alongside 400+ undeciphered pictographic symbols.",
        curiosity_fact: "The Indus script remains one of archaeology's greatest unsolved mysteries, written from right to left with symbolic logograms.",
        historical_distinction: "Historical Evidence: Over 4,000 inscribed seal stones, copper tablets, and the giant 10-symbol wooden signboard of Dholavira have been unearthed.",
        badge_icon: "🦏",
        highlight_topic: "Crafts & Seals",
        svg_type: "crafts_seals"
      },
      {
        id: "scene_07_daily_life",
        scene_number: 7,
        title: "Life in the Living City & Your Mission",
        subtitle: "Peaceful Daily Routines & The Explorer's Gateway",
        period: "Civilian Life & Gamified Archaeological Exploration",
        narrative: "Daily life in a Harappan city was peaceful and industrious. Citizens ate nutritious diets of barley, emmer wheat, chickpeas, and mustard, seasoned with ginger and garlic. Children played with terracotta toy carts, clay whistles, and maze boards. Remarkably, no royal statues, weapons of war, or monuments glorify conquerors. Today, you step into this living bronze-age metropolis not just as a reader, but as an active explorer solving ancient engineering puzzles and unearthing authentic relics!",
        curiosity_fact: "Terracotta toy bullock carts with working rotating wheels found in excavations prove that ancient Indian children learned transport mechanics through play!",
        historical_distinction: "Pedagogical Note: All historical facts, architectural measurements, and artifacts in Bharat Quest are strictly based on ASI archaeological findings. Your avatar profile, interactive quests, and seal rewards are gamified learning simulations designed to bring history to life!",
        badge_icon: "🏺",
        highlight_topic: "Daily Life & Living Quest",
        svg_type: "living_city"
      }
    ];

    this.scenes = this.defaultScenes;
  }

  async init() {
    console.log("Initializing IVC Story Introduction Controller...");
    this.bindGlobalKeys();
    
    // Try to load dynamic story scenes from backend
    try {
      if (window.api && typeof window.api.getIvcStory === 'function') {
        const remoteData = await window.api.getIvcStory();
        if (remoteData && remoteData.scenes && remoteData.scenes.length > 0) {
          // Merge svg_types onto remote scenes
          this.scenes = remoteData.scenes.map((scene, idx) => ({
            ...scene,
            svg_type: this.defaultScenes[idx] ? this.defaultScenes[idx].svg_type : 'river_dawn'
          }));
          this.storyData = remoteData;
        }
      }
    } catch (err) {
      console.warn("Using offline fallback scenes for Story Controller:", err);
    }
  }

  bindGlobalKeys() {
    window.addEventListener('keydown', (e) => {
      const modal = document.getElementById('ivcStoryModal');
      if (!modal || !modal.classList.contains('active')) return;

      if (e.key === 'ArrowRight' || e.key === ' ') {
        e.preventDefault();
        this.nextScene();
      } else if (e.key === 'ArrowLeft') {
        e.preventDefault();
        this.prevScene();
      } else if (e.key === 'Escape') {
        e.preventDefault();
        this.closeStory();
      }
    });
  }

  openStory(sceneIndex = 0) {
    if (window.audio) audio.playChime();
    const modal = document.getElementById('ivcStoryModal');
    if (!modal) return;

    this.currentSceneIndex = Math.max(0, Math.min(sceneIndex, this.scenes.length - 1));
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
    this.renderCurrentScene();

    if (window.app) {
      app.logConsole(`📖 Opened IVC Story Introduction: Scene ${this.currentSceneIndex + 1} of ${this.scenes.length}`);
    }
  }

  closeStory() {
    const modal = document.getElementById('ivcStoryModal');
    if (modal) modal.classList.remove('active');
    document.body.style.overflow = '';
  }

  renderCurrentScene() {
    const scene = this.scenes[this.currentSceneIndex];
    if (!scene) return;

    // 1. Update Header Counters & Progress
    const counterEl = document.getElementById('storySceneCounter');
    const fillEl = document.getElementById('storyProgressFill');
    const total = this.scenes.length;
    const currentNum = this.currentSceneIndex + 1;

    if (counterEl) counterEl.innerText = `Scene ${currentNum} of ${total}`;
    if (fillEl) {
      const pct = (currentNum / total) * 100;
      fillEl.style.width = `${pct}%`;
    }

    // 2. Update Chapter Dots
    const dotsContainer = document.getElementById('storyStepsRow');
    if (dotsContainer) {
      dotsContainer.innerHTML = this.scenes.map((s, idx) => {
        const isCurrent = idx === this.currentSceneIndex;
        const isCompleted = idx < this.currentSceneIndex;
        const cls = isCurrent ? 'active' : (isCompleted ? 'completed' : '');
        return `
          <div class="story-step-dot ${cls}" onclick="storyController.goToScene(${idx})" title="Scene ${idx + 1}: ${s.title}">
            <div class="step-dot-pip"></div>
            <span class="step-dot-label">${idx + 1}. ${s.badge_icon} ${s.highlight_topic}</span>
          </div>
        `;
      }).join('');
    }

    // 3. Render Visual SVG Illustration
    const visualContainer = document.getElementById('storyVisualStage');
    if (visualContainer) {
      visualContainer.innerHTML = `
        <span class="story-visual-topic-pill">${scene.badge_icon} ${scene.highlight_topic}</span>
        ${this.generateSceneIllustration(scene.svg_type)}
      `;
    }

    // 4. Render Narrative & Pedagogy
    const narrativeContainer = document.getElementById('storyNarrativeStage');
    if (narrativeContainer) {
      narrativeContainer.innerHTML = `
        <div class="story-period-tag">
          <span>⏳ ${scene.period}</span>
        </div>
        <h2 class="story-scene-title">${scene.title}</h2>
        <div class="story-scene-subtitle">${scene.subtitle}</div>
        <div class="story-narrative-text">
          ${this.formatNarrativeText(scene.narrative)}
        </div>
        <div class="story-curiosity-box">
          <span class="curiosity-icon">💡</span>
          <div class="curiosity-content">
            <strong>Archaeological Curiosity:</strong> ${scene.curiosity_fact}
          </div>
        </div>
        <div class="story-distinction-badge">
          <span class="distinction-icon">⚖️</span>
          <div>${scene.historical_distinction}</div>
        </div>
      `;
    }

    // 5. Update Footer Buttons
    const prevBtn = document.getElementById('storyPrevBtn');
    const nextBtn = document.getElementById('storyNextBtn');

    if (prevBtn) {
      prevBtn.disabled = this.currentSceneIndex === 0;
      prevBtn.style.opacity = this.currentSceneIndex === 0 ? '0.4' : '1';
    }

    if (nextBtn) {
      if (this.currentSceneIndex === total - 1) {
        // Final scene: Enter the Ancient City button
        nextBtn.className = 'enter-city-hero-btn';
        nextBtn.innerHTML = `<span>🏛️ Enter the Ancient City</span> ➔`;
        nextBtn.onclick = () => this.enterAncientCity();
      } else {
        nextBtn.className = 'ancient-btn btn-primary';
        nextBtn.innerHTML = `<span>Continue Story</span> ➔`;
        nextBtn.onclick = () => this.nextScene();
      }
    }
  }

  formatNarrativeText(text) {
    if (!text) return '';
    // Highlight key educational terms in gold
    return text
      .replace(/(1:2:4)/g, '<strong>$1</strong>')
      .replace(/(Mohenjo-daro|Harappa|Lothal|Dholavira|Kalibangan|Rakhigarhi)/g, '<strong>$1</strong>')
      .replace(/(Great Bath|Meluhha|Dancing Girl|Pashupati|steatite|carnelian|bitumen)/g, '<strong>$1</strong>');
  }

  generateSceneIllustration(type) {
    switch (type) {
      case 'river_dawn':
        return `
          <svg class="story-illustration-svg" viewBox="0 0 320 280">
            <defs>
              <linearGradient id="skyGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#E9C46A" stop-opacity="0.8"/>
                <stop offset="60%" stop-color="#C05A3E" stop-opacity="0.9"/>
                <stop offset="100%" stop-color="#1E1714"/>
              </linearGradient>
              <linearGradient id="riverGrad" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stop-color="#64B5F6"/>
                <stop offset="100%" stop-color="#1D3557"/>
              </linearGradient>
            </defs>
            <rect width="320" height="280" rx="8" fill="url(#skyGrad)"/>
            <circle cx="160" cy="90" r="42" fill="#FFE8A3" opacity="0.85"/>
            <!-- Mountains -->
            <polygon points="20,160 90,80 160,160" fill="#2E211A"/>
            <polygon points="120,160 190,70 260,160" fill="#3D2B22"/>
            <polygon points="220,160 270,100 320,160" fill="#251A15"/>
            <!-- River Indus Basin -->
            <path d="M 160,140 Q 140,180 170,210 T 130,280 L 190,280 Q 230,220 180,180 Z" fill="url(#riverGrad)"/>
            <!-- Ancient Reed Boat -->
            <g transform="translate(145, 195)">
              <path d="M 0,15 C 10,22 25,22 35,15 L 30,12 L 5,12 Z" fill="#D4A373"/>
              <line x1="17" y1="12" x2="17" y2="2" stroke="#FFF" stroke-width="1.5"/>
              <polygon points="17,3 27,8 17,11" fill="#E9C46A"/>
            </g>
            <text x="160" y="260" text-anchor="middle" fill="#FFF" font-family="'Cinzel', serif" font-size="11" font-weight="700">INDUS (SINDHU) BASIN</text>
          </svg>
        `;
      case 'twin_cities':
        return `
          <svg class="story-illustration-svg" viewBox="0 0 320 280">
            <rect width="320" height="280" rx="8" fill="#181310"/>
            <!-- Citadel Mound (Left) -->
            <rect x="25" y="110" width="115" height="130" rx="4" fill="#C05A3E" stroke="#E9C46A" stroke-width="1.5"/>
            <rect x="40" y="80" width="85" height="35" rx="3" fill="#D4A373"/>
            <polygon points="35,80 82,50 130,80" fill="#913B24"/>
            <text x="82" y="102" text-anchor="middle" fill="#120E0C" font-family="'Cinzel', serif" font-weight="800" font-size="10">CITADEL</text>
            <text x="82" y="165" text-anchor="middle" fill="#FFF" font-size="9">Public Assemblies & Granaries</text>
            <!-- Lower Town (Right) -->
            <rect x="160" y="130" width="135" height="110" rx="4" fill="#2E241F" stroke="#776052" stroke-width="1.5"/>
            <rect x="175" y="150" width="45" height="30" fill="#3D2D26" stroke="#C05A3E"/>
            <rect x="235" y="150" width="45" height="30" fill="#3D2D26" stroke="#C05A3E"/>
            <rect x="175" y="195" width="105" height="30" fill="#3D2D26" stroke="#C05A3E"/>
            <text x="227" y="145" text-anchor="middle" fill="#E9C46A" font-family="'Cinzel', serif" font-weight="700" font-size="10">LOWER TOWN</text>
            <text x="227" y="240" text-anchor="middle" fill="#CFC0B4" font-size="8">Residential Grid & Workshops</text>
            <!-- Linking Avenue -->
            <line x1="140" y1="180" x2="160" y2="180" stroke="#E9C46A" stroke-width="3" stroke-dasharray="4,2"/>
          </svg>
        `;
      case 'grid_planning':
        return `
          <svg class="story-illustration-svg" viewBox="0 0 320 280">
            <rect width="320" height="280" rx="8" fill="#1A1412"/>
            <!-- 90-degree Grid Avenues -->
            <rect x="0" y="125" width="320" height="40" fill="#2E241F"/>
            <rect x="135" y="0" width="50" height="280" fill="#2E241F"/>
            <line x1="0" y1="145" x2="320" y2="145" stroke="#E9C46A" stroke-width="1.5" stroke-dasharray="8,6" opacity="0.6"/>
            <line x1="160" y1="0" x2="160" y2="280" stroke="#E9C46A" stroke-width="1.5" stroke-dasharray="8,6" opacity="0.6"/>
            <!-- 4 Corner Multi-story Brick Blocks -->
            <rect x="20" y="20" width="100" height="90" rx="4" fill="#C05A3E" stroke="#D4A373" stroke-width="1.5"/>
            <rect x="200" y="20" width="100" height="90" rx="4" fill="#C05A3E" stroke="#D4A373" stroke-width="1.5"/>
            <rect x="20" y="180" width="100" height="85" rx="4" fill="#C05A3E" stroke="#D4A373" stroke-width="1.5"/>
            <rect x="200" y="180" width="100" height="85" rx="4" fill="#C05A3E" stroke="#D4A373" stroke-width="1.5"/>
            <!-- 1:2:4 Brick Metric Callout -->
            <g transform="translate(160, 145)">
              <circle cx="0" cy="0" r="28" fill="#120E0C" stroke="#E9C46A" stroke-width="2"/>
              <text x="0" y="4" text-anchor="middle" fill="#E9C46A" font-family="'Cinzel', serif" font-weight="800" font-size="11">1:2:4</text>
              <text x="0" y="15" text-anchor="middle" fill="#CFC0B4" font-size="7">RATIO</text>
            </g>
          </svg>
        `;
      case 'drainage_system':
        return `
          <svg class="story-illustration-svg" viewBox="0 0 320 280">
            <rect width="320" height="280" rx="8" fill="#120E0C"/>
            <!-- House Bathroom Wall (Top) -->
            <rect x="40" y="30" width="240" height="60" rx="4" fill="#2E241F" stroke="#C05A3E" stroke-width="1.5"/>
            <text x="160" y="55" text-anchor="middle" fill="#FFF" font-family="'Cinzel', serif" font-size="10">Private Paved Bathroom</text>
            <!-- Downward Vertical Terracotta Waste Pipe Chute -->
            <rect x="148" y="90" width="24" height="60" fill="#C05A3E" stroke="#D4A373"/>
            <path d="M 160,95 L 160,145" stroke="#457B9D" stroke-width="3" stroke-dasharray="4,4"/>
            <!-- Subterranean Street Sewer Canal (Bottom) -->
            <rect x="20" y="150" width="280" height="80" rx="6" fill="#1D3557" stroke="#2A9D8F" stroke-width="2"/>
            <text x="160" y="185" text-anchor="middle" fill="#64B5F6" font-family="'Cinzel', serif" font-weight="700" font-size="11">COVERED STREET DRAIN</text>
            <!-- Removable Inspection Slab Manhole -->
            <rect x="120" y="142" width="80" height="14" rx="2" fill="#D4A373" stroke="#FFF" stroke-width="1"/>
            <text x="160" y="153" text-anchor="middle" fill="#120E0C" font-size="8" font-weight="800">INSPECTION SLAB</text>
            <text x="160" y="215" text-anchor="middle" fill="#A8DADC" font-size="8.5">Bitumen Sealed • Graded Flow to Soak Pits</text>
          </svg>
        `;
      case 'maritime_trade':
        return `
          <svg class="story-illustration-svg" viewBox="0 0 320 280">
            <rect width="320" height="280" rx="8" fill="#151A1E"/>
            <!-- Lothal Tidal Dock Basin -->
            <rect x="30" y="80" width="260" height="150" rx="4" fill="#1D3557" stroke="#E9C46A" stroke-width="1.5"/>
            <!-- Sluice Gate -->
            <rect x="20" y="130" width="20" height="50" fill="#C05A3E" stroke="#D4A373"/>
            <text x="160" y="105" text-anchor="middle" fill="#E9C46A" font-family="'Cinzel', serif" font-size="10" font-weight="700">LOTHAL TIDAL DOCKYARD</text>
            <!-- Harappan Galley Ship -->
            <g transform="translate(100, 125)">
              <path d="M 0,35 C 30,55 90,55 120,35 L 110,25 L 10,25 Z" fill="#913B24" stroke="#D4A373" stroke-width="1.5"/>
              <line x1="60" y1="25" x2="60" y2="0" stroke="#FFF" stroke-width="2"/>
              <polygon points="60,2 100,12 60,22" fill="#E9C46A"/>
              <text x="60" y="44" text-anchor="middle" fill="#FFF" font-size="8" font-weight="700">Meluhha Voyager</text>
            </g>
            <!-- Binary Chert Weight Set -->
            <g transform="translate(45, 238)">
              <rect x="0" y="10" width="12" height="12" fill="#D4A373" stroke="#FFF"/>
              <rect x="18" y="8" width="16" height="16" fill="#D4A373" stroke="#FFF"/>
              <rect x="40" y="4" width="22" height="22" fill="#D4A373" stroke="#FFF"/>
              <text x="120" y="20" fill="#E9C46A" font-size="9" font-family="'Cinzel', serif">Standard Binary Weights (1:2:4:8...)</text>
            </g>
          </svg>
        `;
      case 'crafts_seals':
        return `
          <svg class="story-illustration-svg" viewBox="0 0 320 280">
            <rect width="320" height="280" rx="8" fill="#1C1512"/>
            <!-- Steatite Stamp Seal (Left) -->
            <rect x="25" y="40" width="120" height="120" rx="6" fill="#EAE0D5" stroke="#E9C46A" stroke-width="2"/>
            <text x="85" y="65" text-anchor="middle" fill="#2E241F" font-family="'Cinzel', serif" font-weight="800" font-size="12">🦏 𐤎𐤏𐤐</text>
            <circle cx="85" cy="105" r="28" fill="none" stroke="#913B24" stroke-width="2"/>
            <text x="85" y="112" text-anchor="middle" font-size="28">🦄</text>
            <text x="85" y="150" text-anchor="middle" fill="#2E241F" font-size="8" font-weight="700">UNICORN SEAL</text>
            <!-- Bronze Dancing Girl (Right) -->
            <rect x="175" y="40" width="120" height="120" rx="6" fill="#2A211D" stroke="#2A9D8F" stroke-width="2"/>
            <text x="235" y="95" text-anchor="middle" font-size="44">💃</text>
            <text x="235" y="145" text-anchor="middle" fill="#2A9D8F" font-family="'Cinzel', serif" font-size="8.5" font-weight="700">DANCING GIRL</text>
            <text x="235" y="155" text-anchor="middle" fill="#CFC0B4" font-size="7">Lost-Wax Bronze</text>
            <!-- Carnelian Etched Beads -->
            <g transform="translate(40, 185)">
              <circle cx="20" cy="20" r="14" fill="#C05A3E" stroke="#FFF" stroke-width="1.5"/>
              <circle cx="60" cy="20" r="14" fill="#C05A3E" stroke="#FFF" stroke-width="1.5"/>
              <circle cx="100" cy="20" r="14" fill="#C05A3E" stroke="#FFF" stroke-width="1.5"/>
              <line x1="5" y1="20" x2="235" y2="20" stroke="#E9C46A" stroke-width="1.5"/>
              <text x="175" y="24" fill="#FFF" font-size="9" font-family="'Cinzel', serif">Etched Carnelian</text>
            </g>
          </svg>
        `;
      case 'living_city':
      default:
        return `
          <svg class="story-illustration-svg" viewBox="0 0 320 280">
            <rect width="320" height="280" rx="8" fill="radial-gradient(circle, #3D2D26 0%, #150F0D 100%)"/>
            <!-- Gateway Arch -->
            <path d="M 60,250 L 60,90 Q 160,30 260,90 L 260,250 Z" fill="#2A1E18" stroke="#E9C46A" stroke-width="2.5"/>
            <path d="M 85,250 L 85,115 Q 160,70 235,115 L 235,250 Z" fill="#120E0C" stroke="#C05A3E" stroke-width="1.5"/>
            <!-- Gateway Glow Portal -->
            <circle cx="160" cy="165" r="45" fill="rgba(233, 196, 106, 0.2)" stroke="#E9C46A" stroke-width="1.5"/>
            <text x="160" y="155" text-anchor="middle" font-size="34">🏛️</text>
            <text x="160" y="185" text-anchor="middle" fill="#FFF" font-family="'Cinzel', serif" font-weight="700" font-size="10">LIVING CITY</text>
            <text x="160" y="235" text-anchor="middle" fill="#E9C46A" font-family="'Cinzel', serif" font-weight="800" font-size="12">THE EXPEDITION CALLS</text>
          </svg>
        `;
    }
  }

  nextScene() {
    if (this.currentSceneIndex < this.scenes.length - 1) {
      if (window.audio) audio.playClick();
      this.currentSceneIndex++;
      this.renderCurrentScene();
    } else {
      this.enterAncientCity();
    }
  }

  prevScene() {
    if (this.currentSceneIndex > 0) {
      if (window.audio) audio.playClick();
      this.currentSceneIndex--;
      this.renderCurrentScene();
    }
  }

  goToScene(index) {
    if (index >= 0 && index < this.scenes.length) {
      if (window.audio) audio.playClick();
      this.currentSceneIndex = index;
      this.renderCurrentScene();
    }
  }

  skipStory() {
    if (window.audio) audio.playClick();
    this.enterAncientCity();
  }

  enterAncientCity() {
    if (window.audio) audio.playGong();
    this.closeStory();
    localStorage.setItem('bq_story_completed', 'true');
    this.hasCompletedIntro = true;

    // Transition smoothly to Ancient City tab
    if (window.app) {
      app.logConsole("🏛️ Completed IVC Story Introduction! Entering the Living Ancient City...");
      app.switchTab('tab-city');

      // Award exploration reward if user exists and hasn't received it yet
      if (app.state.user) {
        app.simulateAward(100, 5, null, null);
      }
    }
  }
}

const storyController = new BharatStoryController();
window.storyController = storyController;
