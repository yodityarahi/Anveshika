/**
 * Bharat Quest - Living Virtual Museum Controller (Phase 7)
 * Pure HTML5 / CSS3 / Vanilla JavaScript modular architecture
 */
const KID_ARTIFACT_DATA = {
  art_unicorn_seal: {
    name: "Unicorn Stamp Seal",
    site: "Mohenjo-daro",
    period: "Around 4,500 years ago (c. 2600–1900 BCE)",
    purpose: "Traders stamped this carved stone seal into wet clay to tag and protect their packages.",
    fact: "Over 65% of all seals found show this magical one-horned animal standing before a holy brazier!",
    guideQuestion: "Tell me about the Unicorn Seal! Was it a real unicorn or a magical creature?"
  },
  art_painted_pottery: {
    name: "Painted Clay Storage Jar",
    site: "Harappa",
    period: "Around 4,400 years ago (c. 2500–1900 BCE)",
    purpose: "Families used this large clay pot to store grain, cooking oils, and fresh water in their homes.",
    fact: "It was hand-painted with peacocks and pipal tree leaves, and baked in an oven hotter than 1,000°C!",
    guideQuestion: "Tell me about the painted pottery jars! How did they make them so smooth and waterproof?"
  },
  art_mother_goddess: {
    name: "Clay Mother Goddess",
    site: "Mohenjo-daro",
    period: "Around 4,300 years ago (c. 2600–2000 BCE)",
    purpose: "Ancient families kept this figurine in home shrines for good health, family safety, and bumper crops.",
    fact: "The tiny cups on her headdress have smoke marks—ancient families burned oil in them like little lamps!",
    guideQuestion: "Tell me about the clay Mother Goddess! What did ancient families pray to her for?"
  },
  art_standard_brick: {
    name: "Standard Fired Mud Brick",
    site: "Mohenjo-daro & Harappa",
    period: "Around 4,500 years ago (c. 2600–1900 BCE)",
    purpose: "Used to build strong walls, waterproof bathrooms, and the world's first covered street drains.",
    fact: "Every single brick had the exact 1:2:4 ratio, fitting together perfectly just like modern Lego blocks!",
    guideQuestion: "Why were all Harappan bricks made in the exact 1:2:4 ratio across 1,500 kilometers?"
  },
  art_chert_drill: {
    name: "Tiny Stone Micro-Drill & Axe",
    site: "Chanhudaro & Lothal",
    period: "Around 4,200 years ago (c. 2500–1800 BCE)",
    purpose: "Craftspeople used these razor-sharp stone tips to drill tiny holes through hard gemstone beads.",
    fact: "It took nearly two full weeks of spinning this drill to pierce through a single long carnelian bead!",
    guideQuestion: "How did ancient craftspeople drill tiny holes through hard gemstone beads?"
  },
  art_carnelian_necklace: {
    name: "Red Carnelian Bead Necklace",
    site: "Lothal & Mohenjo-daro",
    period: "Around 4,300 years ago (c. 2500–1900 BCE)",
    purpose: "Worn as shining red gemstone jewelry by proud citizens for festivals and daily life.",
    fact: "People loved these beads so much that merchants traded them by boat all the way to Mesopotamia!",
    guideQuestion: "Tell me about the shining carnelian bead necklaces! How were the white patterns etched?"
  },
  art_chert_weights: {
    name: "Cubical Stone Balance Weights",
    site: "Lothal & Harappa",
    period: "Around 4,500 years ago (c. 2600–1900 BCE)",
    purpose: "Merchants placed these smooth stone cubes on balance pans to weigh gold, grains, and goods accurately.",
    fact: "The weights were identical across thousands of miles, so no merchant could cheat another in trade!",
    guideQuestion: "How did the Harappan stone balance weights work, and why were they never faked?"
  },
  art_dancing_girl: {
    name: "The Bronze Dancing Girl",
    site: "Mohenjo-daro",
    period: "Around 4,300 years ago (c. 2300–1750 BCE)",
    purpose: "An ancient bronze sculpture celebrating the grace and confidence of a young performing artist.",
    fact: "Her left arm is stacked with 25 bangles all the way to her shoulder, standing confidently with hand on hip!",
    guideQuestion: "Tell me about the Bronze Dancing Girl! How did ancient sculptors cast bronze from beeswax?"
  }
};

class BharatMuseumController {
  constructor() {
    this.artifacts = [];
    this.activeFilter = 'all';
    this.currentArtifact = null;

    // Built-in fallback catalog for offline reliability
    this.defaultArtifacts = [
      {
        artifact_id: "art_unicorn_seal",
        name: "Steatite Unicorn Stamp Seal",
        category: "seal",
        category_label: "Indus Valley Seal",
        civilization_id: "ivc",
        period: "c. 2600–1900 BCE (Mature Harappan Phase)",
        region: "Lower Indus Basin (Sindh)",
        site: "Mohenjo-daro (DK Area)",
        material: "High-fired Steatite (Soapstone) with White Alkali Glaze",
        dimensions: "2.9 × 2.9 × 0.8 cm",
        possible_purpose: "Used by merchant guilds and civic administrators to impress wet clay tags (bullae) around wrapped trade bales destined for Mesopotamian ports.",
        historical_significance: "The intaglio carving showcases world-class Bronze Age lapidary artistry and preserves 5 pictographic script symbols running from right to left.",
        interesting_fact: "Over 65% of all recovered Indus stamp seals depict this mythical single-horned quadruped standing before a sacred ritual brazier.",
        icon: "🦄",
        svg_type: "seal_unicorn",
        xp_reward: 80,
        discovered: false
      },
      {
        artifact_id: "art_painted_pottery",
        name: "Black-on-Red Painted Storage Urn",
        category: "pottery",
        category_label: "Ceramics & Pottery",
        civilization_id: "ivc",
        period: "c. 2500–1900 BCE",
        region: "Punjab & Saraswati Basin",
        site: "Harappa (Mound AB)",
        material: "Fine levigated alluvial clay, red slip, manganese black pigment",
        dimensions: "58 cm height, 38 cm diameter",
        possible_purpose: "Storing grain reserves, sesame oils, and fermented beverages in domestic courtyards and municipal storehouses.",
        historical_significance: "Demonstrates sophisticated mastery of the fast pottery wheel and high-temperature kiln firing exceeding 1,000°C.",
        interesting_fact: "Painted with interlocking circular geometry, peacocks, pipal tree leaves, and fish scales, reflecting deep reverence for local ecology.",
        icon: "🏺",
        svg_type: "pottery_urn",
        xp_reward: 75,
        discovered: false
      },
      {
        artifact_id: "art_mother_goddess",
        name: "Terracotta Mother Goddess Figurine",
        category: "figurine",
        category_label: "Terracotta Figurine",
        civilization_id: "ivc",
        period: "c. 2600–2000 BCE",
        region: "Lower Indus Basin",
        site: "Mohenjo-daro (HR Area)",
        material: "Hand-modeled terracotta clay with pinched features and applique ornaments",
        dimensions: "18.5 × 7.2 × 4.1 cm",
        possible_purpose: "Domestic household shrine worship and fertility rituals invoking agricultural bounty and maternal protection.",
        historical_significance: "Offers invaluable insights into Harappan personal spirituality, fan-shaped headdresses, disc earrings, and layered bead necklaces.",
        interesting_fact: "Traces of carbon soot found in the pannier-shaped side cups suggest they were used as miniature oil lamps during twilight ceremonies.",
        icon: "🗿",
        svg_type: "terracotta_goddess",
        xp_reward: 75,
        discovered: false
      },
      {
        artifact_id: "art_standard_brick",
        name: "Standardized 1:2:4 Fired Mud Brick",
        category: "brick",
        category_label: "Civic Masonry & Architecture",
        civilization_id: "ivc",
        period: "c. 2600–1900 BCE",
        region: "Alluvial Plains across Indus Basin",
        site: "Harappa & Mohenjo-daro",
        material: "Kiln-fired alluvial clay with straw binder",
        dimensions: "7 × 14 × 28 cm (Strict 1:2:4 Ratio)",
        possible_purpose: "Constructing multi-storey residential walls, fortified Citadel revetments, and waterproof sewer drains.",
        historical_significance: "The universal 1:2:4 mathematical thickness-width-length ratio provided optimal tensile bonding against seismic tremors and floods.",
        interesting_fact: "Identical brick dimensions have been unearthed at sites over 1,500 kilometers apart—from Shortugai in Afghanistan to Lothal in Gujarat.",
        icon: "🧱",
        svg_type: "ancient_brick",
        xp_reward: 70,
        discovered: false
      },
      {
        artifact_id: "art_chert_drill",
        name: "Constricted Micro-Chert Stone Drill & Bronze Axe",
        category: "tool",
        category_label: "Artisan Tools & Metallurgy",
        civilization_id: "ivc",
        period: "c. 2500–1800 BCE",
        region: "Saraswati-Narmada Corridor",
        site: "Chanhudaro & Lothal Workshops",
        material: "Ernestite/chert cryptocrystalline quartz & copper-tin bronze",
        dimensions: "Drill: 3.2 cm length, 1.2 mm tip; Axe: 14.5 cm length",
        possible_purpose: "Microscopic axial drilling of extremely hard gemstone beads (carnelian, agate) and carpentry timber shaping.",
        historical_significance: "Ernestite drills were a proprietary Harappan technological breakthrough that astonished the ancient world with drilling precision under 1 mm.",
        interesting_fact: "A single 6 cm carnelian bead required nearly two full weeks of continuous rotary bow-drilling with these specialized stone micro-bits.",
        icon: "⛏️",
        svg_type: "artisan_tool",
        xp_reward: 75,
        discovered: false
      },
      {
        artifact_id: "art_carnelian_necklace",
        name: "Etched Carnelian Bead Necklace & Bangles",
        category: "ornament",
        category_label: "Jewelry & Lapidary Ornaments",
        civilization_id: "ivc",
        period: "c. 2500–1900 BCE",
        region: "Gulf of Khambhat & Sindh",
        site: "Lothal & Mohenjo-daro",
        material: "Red carnelian stone, white alkali chemical etching, marine conch shell",
        dimensions: "Beads ranging from 1.5 to 7.8 cm in length",
        possible_purpose: "Personal adornment worn by citizens of all genders as markers of civic pride, beauty, and protective talismanic amulets.",
        historical_significance: "White geometric alkali bleaching on crimson carnelian was a technological trade secret that commanded immense wealth in Mesopotamia.",
        interesting_fact: "Found buried inside intact terracotta urns beneath courtyard floors, serving as ancient household jewelry safes.",
        icon: "📿",
        svg_type: "carnelian_necklace",
        xp_reward: 80,
        discovered: false
      },
      {
        artifact_id: "art_chert_weights",
        name: "Standardized Cubical Chert Weights & Clay Bulla",
        category: "trade",
        category_label: "Trade, Currency & Metrology",
        civilization_id: "ivc",
        period: "c. 2600–1900 BCE",
        region: "Major Commercial Trade Hubs",
        site: "Lothal & Harappa",
        material: "Polished banded chert stone & sun-dried clay sealing",
        dimensions: "Base unit weight: 0.857 grams (binary series 1, 2, 4, 8, 16, 32, 64)",
        possible_purpose: "Weighing precious metals (gold, copper), lapis lazuli, and agricultural commodities to calculate municipal exchange values.",
        historical_significance: "Followed a binary metrological progression followed by decimal ratios, standardized with less than 1% variance across the civilization.",
        interesting_fact: "The 16th unit ratio became the direct historical ancestor of the traditional Indian rupee currency division (1 Rupee = 16 Annas).",
        icon: "⚖️",
        svg_type: "trade_weights",
        xp_reward: 85,
        discovered: false
      },
      {
        artifact_id: "art_dancing_girl",
        name: "The Bronze Dancing Girl",
        category: "figurine",
        category_label: "Bronze Metallurgy Masterpiece",
        civilization_id: "ivc",
        period: "c. 2300–1750 BCE",
        region: "Lower Indus Basin",
        site: "Mohenjo-daro (HR Area)",
        material: "Copper-tin bronze alloy (Lost-wax casting technique)",
        dimensions: "10.5 cm height, 5 cm width",
        possible_purpose: "Artistic appreciation, cultural dance commemoration, or personal keepsake of an adolescent performing artist.",
        historical_significance: "The world's earliest masterpiece of cire-perdue (lost-wax casting), capturing dynamic naturalism, confidence, and anatomical grace.",
        interesting_fact: "Her left arm is heavily adorned with 24-25 bangles right up to the shoulder, while her right arm wears only four at the wrist and elbow.",
        icon: "💃",
        svg_type: "dancing_girl",
        xp_reward: 90,
        discovered: false
      }
    ];

    this.artifacts = [...this.defaultArtifacts];
  }

  async init() {
    console.log("Initializing Living Virtual Museum Controller (Phase 7)...");
    await this.fetchArtifacts();
    this.renderMuseumHub();
  }

  async fetchArtifacts() {
    const currentUsername = (window.app && app.state.user) ? app.state.user.username : (localStorage.getItem('bq_username') || 'Arjun');
    try {
      if (window.api && typeof window.api.getMuseumArtifacts === 'function') {
        const remoteArtifacts = await window.api.getMuseumArtifacts(currentUsername, 'ivc');
        if (remoteArtifacts && remoteArtifacts.length >= 7) {
          this.artifacts = remoteArtifacts;
        }
      }
    } catch (err) {
      console.warn("Using offline fallback artifacts:", err);
      // Sync discovered status from app user if available
      if (window.app && app.state.user && app.state.user.stats) {
        const userArtifacts = new Set(app.state.user.stats.discovered_artifacts || []);
        this.artifacts.forEach(a => {
          if (userArtifacts.has(a.artifact_id)) a.discovered = true;
        });
      }
    }
  }

  filterArtifacts(category) {
    if (window.audio) audio.playClick();
    this.activeFilter = category;
    this.renderVitrineGrid();

    document.querySelectorAll('.museum-filter-btn').forEach(btn => {
      if (btn.getAttribute('data-filter') === category) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });
  }

  renderMuseumHub() {
    const container = document.getElementById('museumHubContainer');
    if (!container) return;

    const total = this.artifacts.length;
    const discoveredCount = this.artifacts.filter(a => a.discovered).length;
    const progressPct = total > 0 ? Math.round((discoveredCount / total) * 100) : 0;

    container.innerHTML = `
      <div class="museum-hub-container">
        <!-- Header Bar -->
        <div class="museum-header-bar">
          <div class="museum-header-left">
            <h2><span>🏺</span> Living Virtual Museum of Ancient India</h2>
            <p>Explore authentic excavated relics from Mohenjo-daro, Harappa, Lothal, and Chanhudaro housed in curatorial vitrines.</p>
          </div>
          <div class="museum-progress-meter">
            <span class="museum-meter-label">Gallery Vitrines:</span>
            <span class="museum-meter-val" id="museumMeterCount">${discoveredCount} / ${total} Exhibited</span>
            <div class="museum-meter-track">
              <div class="museum-meter-fill" id="museumMeterFill" style="width: ${progressPct}%;"></div>
            </div>
          </div>
        </div>

        <!-- Category Filter Strip -->
        <div class="museum-filter-strip">
          <button class="museum-filter-btn active" data-filter="all" onclick="museumController.filterArtifacts('all')">
            All Relics (${total})
          </button>
          <button class="museum-filter-btn" data-filter="seal" onclick="museumController.filterArtifacts('seal')">
            Seals
          </button>
          <button class="museum-filter-btn" data-filter="pottery" onclick="museumController.filterArtifacts('pottery')">
            Pottery
          </button>
          <button class="museum-filter-btn" data-filter="figurine" onclick="museumController.filterArtifacts('figurine')">
            Figurines
          </button>
          <button class="museum-filter-btn" data-filter="brick" onclick="museumController.filterArtifacts('brick')">
            Bricks & Masonry
          </button>
          <button class="museum-filter-btn" data-filter="tool" onclick="museumController.filterArtifacts('tool')">
            Tools
          </button>
          <button class="museum-filter-btn" data-filter="ornament" onclick="museumController.filterArtifacts('ornament')">
            Ornaments
          </button>
          <button class="museum-filter-btn" data-filter="trade" onclick="museumController.filterArtifacts('trade')">
            Trade & Metrology
          </button>
        </div>

        <!-- Vitrines Grid -->
        <div class="museum-vitrines-grid" id="museumVitrinesGrid">
          <!-- Populated by renderVitrineGrid() -->
        </div>
      </div>
    `;

    this.renderVitrineGrid();
  }

  renderVitrineGrid() {
    const grid = document.getElementById('museumVitrinesGrid');
    if (!grid) return;

    let filtered = this.artifacts;
    if (this.activeFilter !== 'all') {
      filtered = this.artifacts.filter(a => a.category === this.activeFilter);
    }

    grid.innerHTML = filtered.map(art => {
      const isDiscovered = art.discovered;

      return `
        <div class="museum-vitrine-card ${isDiscovered ? 'unlocked' : 'locked'}" id="vitrineCard_${art.artifact_id}">
          <div class="vitrine-pedestal">
            ${isDiscovered ? '' : `
              <div class="vitrine-lock-overlay">
                <span class="vitrine-lock-icon">🔒</span>
                <span class="vitrine-lock-text">Undiscovered Relic</span>
              </div>
            `}
            <div class="vitrine-svg-stage">
              ${this.generateArtifactSvg(art.svg_type, isDiscovered)}
            </div>
          </div>

          <div class="vitrine-brass-plaque">
            <span class="plaque-category-tag">${art.category_label}</span>
            <div class="plaque-title">${isDiscovered ? art.name : 'Unknown Excavated Specimen'}</div>
            <div class="plaque-provenance">${art.site} • ${art.period}</div>
          </div>

          <div class="vitrine-footer-row">
            <span class="vitrine-status-tag ${isDiscovered ? 'unlocked' : 'locked'}">
              ${isDiscovered ? '✨ Unlocked in Museum' : '🔒 Silhouette'}
            </span>
            <button class="vitrine-inspect-btn" onclick="museumController.openArtifactModal('${art.artifact_id}')">
              <span>🔍 ${isDiscovered ? 'Inspect Curatorial File' : 'Examine Clues'}</span>
            </button>
          </div>
        </div>
      `;
    }).join('');
  }

  generateArtifactSvg(type, isDiscovered) {
    const opacity = isDiscovered ? '1' : '0.35';
    const filter = isDiscovered ? '' : 'filter="url(#silhouetteFilter)"';

    switch (type) {
      case 'seal_unicorn':
        return `
          <svg viewBox="0 0 100 100" class="museum-svg-render" style="opacity: ${opacity};" ${filter}>
            <rect x="10" y="10" width="80" height="80" rx="6" fill="#F4EAD4" stroke="#C9A048" stroke-width="2"/>
            <rect x="14" y="14" width="72" height="72" rx="4" fill="#E8DAC1"/>
            <!-- 5 Indus Script Signs -->
            <text x="50" y="28" text-anchor="middle" font-size="11" font-weight="900" fill="#2E2019" letter-spacing="3">Ψ ⋔ ⨂ ⩘ 𐂂</text>
            <!-- Single Horned Unicorn -->
            <path d="M 28,68 Q 32,52 48,50 Q 56,48 64,42 Q 68,36 72,32 L 80,18" fill="none" stroke="#2E2019" stroke-width="3"/>
            <polygon points="45,50 65,48 70,62 50,68" fill="#B38A58"/>
            <!-- Legs -->
            <line x1="48" y1="68" x2="46" y2="82" stroke="#2E2019" stroke-width="2.5"/>
            <line x1="66" y1="68" x2="68" y2="82" stroke="#2E2019" stroke-width="2.5"/>
            <!-- Incense Brazier -->
            <path d="M 72,62 L 78,62 L 75,72 L 72,82 L 80,82" fill="none" stroke="#A03B26" stroke-width="2"/>
          </svg>
        `;

      case 'pottery_urn':
        return `
          <svg viewBox="0 0 100 100" class="museum-svg-render" style="opacity: ${opacity};" ${filter}>
            <!-- Red Clay Slip Body -->
            <path d="M 30,22 Q 18,50 32,78 Q 50,86 68,78 Q 82,50 70,22 Z" fill="#C05A3E" stroke="#5C2518" stroke-width="2"/>
            <!-- Neck & Rim -->
            <ellipse cx="50" cy="22" rx="20" ry="6" fill="#A03B26" stroke="#5C2518" stroke-width="1.8"/>
            <ellipse cx="50" cy="22" rx="14" ry="4" fill="#3D1A12"/>
            <!-- Black Painted Bands -->
            <path d="M 22,46 Q 50,56 78,46" fill="none" stroke="#1A120E" stroke-width="3"/>
            <path d="M 24,54 Q 50,64 76,54" fill="none" stroke="#1A120E" stroke-width="3"/>
            <!-- Intersecting Circles Motif -->
            <circle cx="50" cy="50" r="10" fill="none" stroke="#1A120E" stroke-width="1.8"/>
            <circle cx="42" cy="50" r="8" fill="none" stroke="#1A120E" stroke-width="1.2"/>
            <circle cx="58" cy="50" r="8" fill="none" stroke="#1A120E" stroke-width="1.2"/>
          </svg>
        `;

      case 'terracotta_goddess':
        return `
          <svg viewBox="0 0 100 100" class="museum-svg-render" style="opacity: ${opacity};" ${filter}>
            <!-- Fan Pannier Headdress -->
            <path d="M 28,26 Q 50,10 72,26 L 68,34 Q 50,24 32,34 Z" fill="#D4A373" stroke="#8C5C38" stroke-width="1.5"/>
            <circle cx="28" cy="26" r="6" fill="#C05A3E"/>
            <circle cx="72" cy="26" r="6" fill="#C05A3E"/>
            <!-- Head & Pinched Features -->
            <ellipse cx="50" cy="38" rx="12" ry="14" fill="#D4A373" stroke="#8C5C38" stroke-width="1.5"/>
            <!-- Pellet Eyes -->
            <circle cx="46" cy="36" r="1.8" fill="#1C1410"/>
            <circle cx="54" cy="36" r="1.8" fill="#1C1410"/>
            <!-- Disc Earrings -->
            <circle cx="36" cy="40" r="4" fill="#E9C46A" stroke="#8C5C38"/>
            <circle cx="64" cy="40" r="4" fill="#E9C46A" stroke="#8C5C38"/>
            <!-- Layered Bead Collar -->
            <path d="M 40,48 Q 50,54 60,48" fill="none" stroke="#E9C46A" stroke-width="3"/>
            <path d="M 38,53 Q 50,60 62,53" fill="none" stroke="#E9C46A" stroke-width="2.5"/>
            <!-- Torso & Girdle -->
            <polygon points="42,56 58,56 64,86 36,86" fill="#C05A3E" stroke="#8C5C38" stroke-width="1.5"/>
          </svg>
        `;

      case 'ancient_brick':
        return `
          <svg viewBox="0 0 100 100" class="museum-svg-render" style="opacity: ${opacity};" ${filter}>
            <!-- 1:2:4 Ratio Isometric Brick -->
            <polygon points="20,40 50,22 80,40 50,58" fill="#D47355" stroke="#7A3622" stroke-width="1.8"/>
            <polygon points="20,40 50,58 50,78 20,60" fill="#A03B26" stroke="#7A3622" stroke-width="1.8"/>
            <polygon points="50,58 80,40 80,60 50,78" fill="#8C301D" stroke="#7A3622" stroke-width="1.8"/>
            <!-- Texture flecks -->
            <circle cx="46" cy="38" r="1.2" fill="#E9C46A"/>
            <circle cx="56" cy="44" r="1.5" fill="#E9C46A"/>
            <text x="50" y="94" text-anchor="middle" font-size="10" font-family="'Cinzel', serif" font-weight="700" fill="#E9C46A">1 : 2 : 4 RATIO</text>
          </svg>
        `;

      case 'artisan_tool':
        return `
          <svg viewBox="0 0 100 100" class="museum-svg-render" style="opacity: ${opacity};" ${filter}>
            <!-- Bronze Celt Axe Head -->
            <polygon points="30,25 65,15 75,45 25,40" fill="#2A9D8F" stroke="#E9C46A" stroke-width="1.8"/>
            <!-- Timber Haft / Handle -->
            <path d="M 45,20 L 75,82" stroke="#8C5C38" stroke-width="7" stroke-linecap="round"/>
            <path d="M 46,28 L 56,26" stroke="#E9C46A" stroke-width="2"/>
            <!-- Constricted Micro Chert Drill Tip -->
            <polygon points="20,75 35,65 38,70 24,80 18,84" fill="#D4A373" stroke="#FFF" stroke-width="1.2"/>
            <circle cx="21" cy="79" r="2" fill="#E9C46A"/>
          </svg>
        `;

      case 'carnelian_necklace':
        return `
          <svg viewBox="0 0 100 100" class="museum-svg-render" style="opacity: ${opacity};" ${filter}>
            <!-- Conch Shell Bangle Ring -->
            <circle cx="50" cy="50" r="38" fill="none" stroke="#F4EAD4" stroke-width="6"/>
            <!-- Etched Carnelian Barrel Beads -->
            <ellipse cx="50" cy="24" rx="16" ry="6" fill="#C05A3E" stroke="#E9C46A" stroke-width="1.5"/>
            <path d="M 40,24 Q 50,21 60,24" stroke="#FFF" stroke-width="1.5" fill="none"/>
            <ellipse cx="26" cy="48" rx="6" ry="12" fill="#C05A3E" stroke="#E9C46A" stroke-width="1.5"/>
            <ellipse cx="74" cy="48" rx="6" ry="12" fill="#C05A3E" stroke="#E9C46A" stroke-width="1.5"/>
            <ellipse cx="50" cy="74" rx="14" ry="6" fill="#C05A3E" stroke="#E9C46A" stroke-width="1.5"/>
          </svg>
        `;

      case 'trade_weights':
        return `
          <svg viewBox="0 0 100 100" class="museum-svg-render" style="opacity: ${opacity};" ${filter}>
            <!-- Balance Beam -->
            <line x1="20" y1="28" x2="80" y2="28" stroke="#E9C46A" stroke-width="2.5"/>
            <circle cx="50" cy="28" r="4" fill="#C05A3E"/>
            <line x1="50" y1="28" x2="50" y2="14" stroke="#E9C46A" stroke-width="2"/>
            <!-- Pans -->
            <path d="M 20,28 L 14,48 L 36,48 Z" fill="none" stroke="#D4A373" stroke-width="1.2"/>
            <path d="M 80,28 L 64,48 L 86,48 Z" fill="none" stroke="#D4A373" stroke-width="1.2"/>
            <!-- Cubical Chert Weights -->
            <rect x="36" y="58" width="28" height="24" fill="#6C757D" stroke="#D4A373" stroke-width="1.5"/>
            <polygon points="36,58 48,50 76,50 64,58" fill="#495057" stroke="#D4A373" stroke-width="1.2"/>
            <polygon points="64,58 76,50 76,74 64,82" fill="#343A40" stroke="#D4A373" stroke-width="1.2"/>
            <text x="50" y="74" text-anchor="middle" font-size="9" font-weight="800" fill="#FFF">16</text>
          </svg>
        `;

      case 'dancing_girl':
        return `
          <svg viewBox="0 0 100 100" class="museum-svg-render" style="opacity: ${opacity};" ${filter}>
            <!-- Slender bronze statuette silhouette -->
            <ellipse cx="50" cy="20" rx="7" ry="9" fill="#2A9D8F" stroke="#1D6A60" stroke-width="1.5"/>
            <!-- Hair Bun -->
            <ellipse cx="58" cy="18" rx="6" ry="6" fill="#1D6A60"/>
            <!-- Torso & Poise -->
            <path d="M 48,29 L 52,50 L 50,82" stroke="#2A9D8F" stroke-width="5" stroke-linecap="round"/>
            <!-- Right Arm Bent with Hand on Hip -->
            <path d="M 47,33 L 40,46 L 49,49" fill="none" stroke="#2A9D8F" stroke-width="3"/>
            <!-- Left Arm Loaded with 24 Bangles Resting on Thigh -->
            <path d="M 53,33 L 64,48 L 56,62" fill="none" stroke="#E9C46A" stroke-width="4.5"/>
            <!-- Neck Choker -->
            <line x1="46" y1="28" x2="54" y2="28" stroke="#E9C46A" stroke-width="2"/>
          </svg>
        `;

      default:
        return `<div style="font-size: 3rem;">🏺</div>`;
    }
  }

  async openArtifactModal(artifactId) {
    if (window.audio) audio.playClick();

    let art = this.artifacts.find(a => a.artifact_id === artifactId);
    const currentUsername = (window.app && app.state.user) ? app.state.user.username : (localStorage.getItem('bq_username') || 'Arjun');

    try {
      if (window.api && typeof window.api.getArtifactDetail === 'function') {
        const remoteArt = await window.api.getArtifactDetail(artifactId, currentUsername);
        if (remoteArt) art = remoteArt;
      }
    } catch (err) {
      console.warn("Using local artifact detail:", err);
    }

    if (!art) return;
    this.currentArtifact = art;

    const modal = document.getElementById('museumArtifactModal');
    if (!modal) return;

    const kid = KID_ARTIFACT_DATA[art.artifact_id];
    const displayName = kid ? kid.name : art.name;
    const displaySite = kid ? kid.site : art.site;
    const displayPeriod = kid ? kid.period : art.period;
    const displayPurpose = kid ? kid.purpose : art.possible_purpose;
    const displayFact = kid ? kid.fact : art.interesting_fact;

    // Header
    document.getElementById('museumModalIcon').innerText = art.icon;
    document.getElementById('museumModalTitle').innerText = art.discovered ? displayName : 'Locked Ancient Relic';
    document.getElementById('museumModalMeta').innerText = `${displaySite} • ${displayPeriod}`;

    // Left SVG
    const svgStage = document.getElementById('museumModalSvgStage');
    if (svgStage) {
      svgStage.innerHTML = this.generateArtifactSvg(art.svg_type, art.discovered);
    }

    // Right Curation Details (5 Clean Points for Young Learners)
    document.getElementById('curatorialPurposeText').innerText = displayPurpose;
    document.getElementById('curatorialSignificanceText').innerText = art.historical_significance;
    document.getElementById('curatorialFactText').innerText = displayFact;

    // Properties Grid
    document.getElementById('propPeriod').innerText = displayPeriod;
    document.getElementById('propSite').innerText = `${displaySite} (${art.region})`;
    document.getElementById('propMaterial').innerText = art.material;
    document.getElementById('propDimensions').innerText = art.dimensions;

    // Footer Discovery Actions
    const discoverBtn = document.getElementById('museumDiscoverActionBtn');
    if (discoverBtn) {
      if (art.discovered) {
        discoverBtn.style.display = 'none';
      } else {
        discoverBtn.style.display = 'flex';
        discoverBtn.innerHTML = `<span>⚡ Excavate & Document Relic (+${art.xp_reward} XP)</span>`;
        discoverBtn.onclick = () => this.discoverArtifact(art.artifact_id);
      }
    }

    modal.classList.add('active');
  }

  closeArtifactModal() {
    if (window.audio) audio.playClick();
    const modal = document.getElementById('museumArtifactModal');
    if (modal) modal.classList.remove('active');
    this.currentArtifact = null;
  }

  askGuideAboutArtifact(artifactId) {
    this.closeArtifactModal();
    if (window.app) {
      window.app.switchTab('tab-ai');
    }
    const kidData = KID_ARTIFACT_DATA[artifactId];
    const question = kidData ? kidData.guideQuestion : "Tell me about this ancient artifact!";
    setTimeout(() => {
      if (window.aiController && typeof window.aiController.quickAsk === 'function') {
        window.aiController.quickAsk(question);
      }
    }, 300);
  }

  playAudioGuide() {
    if (window.audio) {
      audio.playChime();
    }
    if (this.currentArtifact && window.app) {
      app.logConsole(`🎧 [Audio Guide] Narrating: "${this.currentArtifact.name}" - ${this.currentArtifact.historical_significance}`);
    }
    if (window.uxManager && this.currentArtifact) {
      uxManager.showToast({
        title: `Curator Audio Guide: ${this.currentArtifact.name}`,
        message: this.currentArtifact.historical_significance,
        icon: '🎧',
        type: 'info',
        duration: 4500
      });
    }
  }

  async discoverArtifact(artifactId) {
    const currentUsername = (window.app && app.state.user) ? app.state.user.username : (localStorage.getItem('bq_username') || 'Arjun');
    
    try {
      let result = null;
      if (window.api && typeof window.api.discoverArtifact === 'function') {
        result = await window.api.discoverArtifact(artifactId, currentUsername);
      } else {
        // Fallback local discovery
        result = {
          success: true,
          is_new: true,
          xp_awarded: 75,
          message: "New artifact added to your museum collection."
        };
      }

      if (result.is_new) {
        if (window.audio) audio.playFanfare();

        const art = this.artifacts.find(a => a.artifact_id === artifactId);
        const artName = art ? art.name : artifactId;
        const artIcon = art ? art.icon : '🏺';

        // Trigger Phase 11 Polish Animation
        if (window.uxManager) {
          uxManager.triggerArtifactDiscovery(artName, artIcon, result.xp_awarded);
        } else if (window.cityController && typeof cityController.showFloatingXp === 'function') {
          cityController.showFloatingXp(`+${result.xp_awarded} XP`);
        }

        // Update local status
        if (art) art.discovered = true;

        // Sync with app state and refresh MongoDB profile
        if (window.app) {
          app.logConsole(`🏺 EXCAVATED ARTIFACT: "${artName}" (+${result.xp_awarded} XP)`);
          await app.refreshCurrentProfile();
        }

        // Update modal immediately
        this.openArtifactModal(artifactId);
        this.renderMuseumHub();

      } else {
        if (window.audio) audio.playClick();
        if (window.app) {
          app.logConsole(`ℹ️ ${result.message}`);
        }
        if (window.uxManager) {
          uxManager.showToast({
            title: 'Artifact Catalogued',
            message: result.message || 'This relic is already documented in your museum repository.',
            icon: 'ℹ️',
            type: 'warning',
            duration: 3000
          });
        }
      }
    } catch (err) {
      console.error("Artifact discovery error:", err);
      if (window.uxManager) {
        uxManager.showToast({
          title: 'Excavation Error',
          message: err.message,
          icon: '⚠️',
          type: 'error'
        });
      } else {
        alert(`Discovery error: ${err.message}`);
      }
    }
  }
}

const museumController = new BharatMuseumController();
window.museumController = museumController;
