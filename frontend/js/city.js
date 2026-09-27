/**
 * Bharat Quest - 2D Interactive Ancient City Controller (Phase 5)
 * Pure HTML5 / CSS3 / Vanilla JavaScript modular architecture
 */
class AncientCityController {
  constructor() {
    this.locations = [];
    this.activeFilter = 'all';
    this.selectedLocationId = null;
    this.discoveredLocations = new Set(
      JSON.parse(localStorage.getItem('bq_discovered_city_locations') || '[]')
    );
    this.examinedObjects = new Set(
      JSON.parse(localStorage.getItem('bq_examined_objects') || '[]')
    );

    // Built-in fallback registry for instantaneous & offline reliability
    this.defaultLocations = [
      {
        id: "residential_area",
        name: "Residential Area",
        subtitle: "Courtyard Dwellings & Domestic Privacy",
        site: "Mohenjo-daro & Harappa",
        zone: "Lower Town",
        icon: "🏡",
        level_required: 1,
        status: "unlocked",
        coordinates: { x: 740, y: 390 },
        svg_coords: "M 670,300 L 890,300 L 890,520 L 670,520 Z",
        historical_explanation: "Harappan residential architecture was focused on domestic privacy and environmental adaptation. Multi-story homes were constructed with burnt bricks around central open-air courtyards. Windows never faced the dusty main avenues, and doorways opened into quiet side alleys. Nearly every home had its own terracotta bathroom, water well, and staircase leading to upper living quarters or a flat sleeping roof.",
        interactive_objects: [
          {
            id: "obj_storage_jar",
            name: "Painted Terracotta Storage Urn",
            icon: "🏺",
            category: "Household Ceramic",
            description: "Large black-on-red ceramic jar treated with fine red slip and painted with intersecting circles and peacock motifs, used to store grains, oils, and well water.",
            archaeological_fact: "Excavated from residential floor levels across Mohenjo-daro HR area.",
            xp_reward: 35
          },
          {
            id: "obj_spindle_whorl",
            name: "Terracotta Spindle Whorl",
            icon: "🧵",
            category: "Domestic Textile Tool",
            description: "Perforated clay flywheel used for spinning raw Indus cotton ('Sindhu') into fine textile threads for household garments.",
            archaeological_fact: "Proves that textile weaving was a widespread domestic cottage industry.",
            xp_reward: 40
          },
          {
            id: "obj_toy_cart",
            name: "Clay Toy Bullock Cart",
            icon: "🪅",
            category: "Ancient Play & Learning",
            description: "Terracotta model cart with working rotating wooden axle pegs and miniature clay oxen, showing how children learned transportation mechanics.",
            archaeological_fact: "Among the most common playful artifacts found in Harappan residential ruins.",
            xp_reward: 45
          }
        ],
        quests: [
          {
            id: "quest_domestic_water",
            title: "Domestic Water Circulation",
            description: "Trace the path of fresh well water from the courtyard cistern to the second-story private bathing room.",
            reward_xp: 180,
            reward_tokens: 6
          }
        ],
        discovery_reward: { xp: 75, tokens: 5 }
      },
      {
        id: "main_street",
        name: "Main Street",
        subtitle: "The 10-Meter Orthogonal Boulevard",
        site: "Mohenjo-daro (First Street)",
        zone: "Lower Town",
        icon: "🛣️",
        level_required: 1,
        status: "unlocked",
        coordinates: { x: 500, y: 340 },
        svg_coords: "M 440,80 L 560,80 L 560,600 L 440,600 Z",
        historical_explanation: "The grand thoroughfare of the metropolis ran strictly North-to-South for over half a kilometer, measuring nearly 10 meters wide—broad enough for two bullock carts to pass abreast without slowing down. It formed the central axis of the city's rigid cardinal grid plan, flanked by standard 1:2:4 burnt-brick street corners designed to prevent carts from chipping wall plaster.",
        interactive_objects: [
          {
            id: "obj_standard_brick",
            name: "Standardized 1:2:4 Fired Brick",
            icon: "🧱",
            category: "Civic Masonry",
            description: "Standard kiln-fired clay brick measuring exactly 7 × 14 × 28 cm. The strict 1:2:4 ratio ensured optimal interlocking bond strength in seismic alluvial soils.",
            archaeological_fact: "Identical dimensions have been recorded across sites 1,000 km apart.",
            xp_reward: 35
          },
          {
            id: "obj_cart_rut",
            name: "Compacted Bullock Cart Rut",
            icon: "🛞",
            category: "Ancient Infrastructure",
            description: "Preserved wheel-track impression in the hardened mud street floor, matching the exact gauge of modern Indian village bullock carts.",
            archaeological_fact: "Wheel gauge measurements at Harappa and Mohenjo-daro average 1.1 meters.",
            xp_reward: 40
          },
          {
            id: "obj_street_lamp_post",
            name: "Municipal Lamp Post Niche",
            icon: "🕯️",
            category: "Civic Amenities",
            description: "Recessed brick niches carved into exterior avenue corners where terracotta oil lamps illuminated night patrols and street navigation.",
            archaeological_fact: "Earliest known municipal street lighting architecture in world history.",
            xp_reward: 45
          }
        ],
        quests: [
          {
            id: "quest_orthogonal_avenue",
            title: "The Orthogonal Grid Survey",
            description: "Survey the 90-degree intersection of First Street with East-West Avenue to verify cardinal orientation.",
            reward_xp: 200,
            reward_tokens: 8
          }
        ],
        discovery_reward: { xp: 75, tokens: 5 }
      },
      {
        id: "drainage_system",
        name: "Drainage System",
        subtitle: "Subterranean Corbelled Sewer Network",
        site: "Harappa & Mohenjo-daro",
        zone: "Lower Town",
        icon: "🚰",
        level_required: 1,
        status: "unlocked",
        coordinates: { x: 575, y: 520 },
        svg_coords: "M 530,460 L 670,460 L 670,590 L 530,590 Z",
        historical_explanation: "The crowning achievement of Harappan civil engineering was its subterranean drainage network—unrivaled worldwide until the 19th century! Paved household bathrooms discharged wastewater through vertical terracotta chutes embedded inside exterior walls into covered street channels. Channels were built with corbelled brick arches, gentle hydraulic gradients, and removable limestone slabs for inspection and municipal cleaning.",
        interactive_objects: [
          {
            id: "obj_corbelled_arch",
            name: "Corbelled Brick Sewer Arch",
            icon: "🏛️",
            category: "Hydraulic Engineering",
            description: "Inverted V-shaped corbelled brick vault engineered to withstand heavy street cart traffic while allowing rapid storm runoff flow.",
            archaeological_fact: "Main sewer trunks were deep enough for a human municipal inspector to stand inside.",
            xp_reward: 40
          },
          {
            id: "obj_inspection_slab",
            name: "Limestone Inspection Slab",
            icon: "🪨",
            category: "Sanitation Maintenance",
            description: "Heavy dressing limestone cover fitted over street drains. Workers lifted these slabs at regular intervals to remove accumulated silt and debris.",
            archaeological_fact: "Demonstrates municipal civic administration and regular maintenance schedules.",
            xp_reward: 45
          },
          {
            id: "obj_soak_pit_jar",
            name: "Perforated Sump Sediment Jar",
            icon: "🧪",
            category: "Water Filtration",
            description: "Large porous terracotta vessel placed at drain junctions to catch heavy sediment while permitting filtered wastewater to percolate safely into the ground.",
            archaeological_fact: "Prevents urban sewage pooling and waterborne diseases.",
            xp_reward: 45
          }
        ],
        quests: [
          {
            id: "quest_hydraulic_flow",
            title: "Drainage Flow Restoration",
            description: "Clear the silted inspection manhole to restore subterranean flow from the residential bathroom to the soak pit.",
            reward_xp: 250,
            reward_tokens: 10
          }
        ],
        discovery_reward: { xp: 75, tokens: 5 }
      },
      {
        id: "great_bath",
        name: "Great Bath",
        subtitle: "The Bitumen-Sealed Ritual Pool",
        site: "Mohenjo-daro",
        zone: "Citadel",
        icon: "🏊",
        level_required: 1,
        status: "unlocked",
        coordinates: { x: 260, y: 330 },
        svg_coords: "M 150,220 L 370,220 L 370,440 L 150,440 Z",
        historical_explanation: "Located on the fortified Western Citadel mound, the Great Bath is a monumental 12 × 7 meter brick basin descending 2.4 meters via broad brick staircases at north and south. The basin was made completely watertight using finely dressed bricks laid in gypsum mortar and sealed behind a 3-centimeter thick backing of natural bitumen (asphalt)—the earliest known synthetic waterproofing in the world.",
        interactive_objects: [
          {
            id: "obj_bitumen_seam",
            name: "Natural Bitumen Waterproofing Seam",
            icon: "🛡️",
            category: "Ancient Material Science",
            description: "Intact layer of natural petroleum pitch (bitumen) applied between outer and inner brick skins to guarantee complete water impermeability.",
            archaeological_fact: "Bitumen was imported from Baluchistan or Mesopotamian tar pits.",
            xp_reward: 50
          },
          {
            id: "obj_bath_stairs",
            name: "Stepped Brick Staircase",
            icon: "🪜",
            category: "Sacred Architecture",
            description: "Carefully angled brick stairways leading bathers down into the ritual basin, originally fitted with timber treads.",
            archaeological_fact: "Surrounded by a pillared veranda and eight private changing rooms with drain outlets.",
            xp_reward: 40
          },
          {
            id: "obj_drain_culvert",
            name: "Corbelled Vaulted Drain Outlet",
            icon: "🌊",
            category: "Hydraulic Culvert",
            description: "Massive arched culvert measuring 1.8 meters high that emptied the entire 160,000-liter pool into the western slope of the mound.",
            archaeological_fact: "Allowed the Great Bath to be completely drained and refilled with fresh well water.",
            xp_reward: 45
          }
        ],
        quests: [
          {
            id: "quest_ritual_purification",
            title: "Secrets of the Great Bath",
            description: "Investigate the bitumen sealing layer and discover how ancient engineers filled and drained the pool.",
            reward_xp: 260,
            reward_tokens: 10
          }
        ],
        discovery_reward: { xp: 80, tokens: 6 }
      },
      {
        id: "granary_area",
        name: "Storage/Granary Area",
        subtitle: "State Grain Reserve & Threshing Platforms",
        site: "Harappa & Mohenjo-daro",
        zone: "Citadel",
        icon: "🌾",
        level_required: 1,
        status: "unlocked",
        coordinates: { x: 230, y: 140 },
        svg_coords: "M 130,70 L 330,70 L 330,200 L 130,200 Z",
        historical_explanation: "Perched on the citadel edge near river loading docks, the Great Granary was a massive brick podium measuring over 50 meters in length. It was divided into 12 storage halls separated by air circulation flues beneath timber platforms, keeping harvested grain cool and dry from humid river fogs. Nearby circular brick threshing floors allowed central workers to pound wheat and barley.",
        interactive_objects: [
          {
            id: "obj_barley_grains",
            name: "Carbonized Six-Row Barley & Wheat",
            icon: "🌾",
            category: "Botanical Remains",
            description: "Charred cereal grains of six-row barley (Hordeum vulgare) and emmer wheat preserved in subterranean storage pits for over 4 millennia.",
            archaeological_fact: "Botanical analysis proves massive agricultural yields along the fertile Indus silt.",
            xp_reward: 40
          },
          {
            id: "obj_air_flue",
            name: "Underfloor Air Ventilation Flue",
            icon: "🌬️",
            category: "Food Preservation Engineering",
            description: "Raised sleeper walls creating continuous airflow beneath grain floors to prevent mildew, dampness, and insect infestation.",
            archaeological_fact: "Architectural principle identical to modern grain silos.",
            xp_reward: 45
          },
          {
            id: "obj_threshing_floor",
            name: "Circular Brick Threshing Platform",
            icon: "⭕",
            category: "Agricultural Processing",
            description: "Concentric circle brick pavement with a central hollow for a heavy wooden mortar pestle, where laborers threshed grain stalks.",
            archaeological_fact: "Found in neat rows north of the Citadel at Harappa.",
            xp_reward: 45
          }
        ],
        quests: [
          {
            id: "quest_granary_security",
            title: "The Granary Ventilation Audit",
            description: "Inspect the air flues and verify grain storage capacity to protect the metropolis against monsoon droughts.",
            reward_xp: 220,
            reward_tokens: 8
          }
        ],
        discovery_reward: { xp: 75, tokens: 5 }
      },
      {
        id: "marketplace",
        name: "Marketplace",
        subtitle: "The Commercial Bazaar & Seal Weighing Hub",
        site: "Mohenjo-daro & Lothal",
        zone: "Lower Town",
        icon: "🏪",
        level_required: 1,
        status: "unlocked",
        coordinates: { x: 700, y: 170 },
        svg_coords: "M 590,90 L 810,90 L 810,260 L 590,260 Z",
        historical_explanation: "The bustling economic nerve center of the city. Here, farmers, craftspeople, and international merchants exchanged agricultural surplus for marine shells, lapis lazuli, turquoise, and copper. Transactions were regulated by municipal weights made of cut chert cubes, and trade consignments were secured by wet clay tags stamped with steatite intaglio seals.",
        interactive_objects: [
          {
            id: "obj_chert_weights",
            name: "Set of Cubical Chert Weights",
            icon: "⚖️",
            category: "Metrology & Commerce",
            description: "Cube-shaped weights of dense, polished grey chert stone following binary progression: 1, 2, 4, 8, 16, 32, 64 (where 1 unit = 0.857 grams).",
            archaeological_fact: "Standardized across the entire civilization with an accuracy margin below 1%.",
            xp_reward: 50
          },
          {
            id: "obj_unicorn_seal",
            name: "Steatite Unicorn Stamp Seal",
            icon: "🪙",
            category: "Trade Identification Seal",
            description: "Square steatite stamp seal depicting the sacred mythical unicorn before an incense brazier, surmounted by 5 pictographic script characters.",
            archaeological_fact: "Most common seal motif, used by trade guilds to authenticate merchant packages.",
            xp_reward: 55
          },
          {
            id: "obj_shell_bangles",
            name: "Turbinella Pyrum Shell Bangles",
            icon: "🐚",
            category: "Coastal Luxury Good",
            description: "Polished conch bangles carved from sea shells gathered in the Gulf of Kutch, prized by citizens across northern cities.",
            archaeological_fact: "Traded inland up to 1,500 km away from coastal waters.",
            xp_reward: 40
          }
        ],
        quests: [
          {
            id: "quest_merchant_balance",
            title: "The Master of Weights",
            description: "Calibrate the chert balance scales against 16-unit weights to verify an incoming copper merchant shipment.",
            reward_xp: 240,
            reward_tokens: 10
          }
        ],
        discovery_reward: { xp: 80, tokens: 6 }
      },
      {
        id: "craft_workshop",
        name: "Craft Workshop",
        subtitle: "Bead Kilns & Lost-Wax Bronze Metallurgy",
        site: "Lothal & Chanhudaro",
        zone: "Lower Town",
        icon: "⚒️",
        level_required: 1,
        status: "unlocked",
        coordinates: { x: 880, y: 240 },
        svg_coords: "M 820,130 L 960,130 L 960,350 L 820,350 Z",
        historical_explanation: "Harappan specialized workshops operated with industrial precision. At bead factories, craftsmen used microscopic diamond-tipped drills (chert stone drills) to perforate hard carnelian stones and fired them in multi-stage kilns to achieve vibrant crimson hues. Metallurgists cast copper and tin bronze into tools, weapons, and sculptures using the complex lost-wax technique.",
        interactive_objects: [
          {
            id: "obj_carnelian_bead",
            name: "Etched Carnelian Barrel Bead",
            icon: "💎",
            category: "Lapidary Art",
            description: "Crimson carnelian stone drilled with microscopic axial holes and chemically etched with white alkali wave designs.",
            archaeological_fact: "High-value export prized by royal courts in Ur (Mesopotamia) and Dilmun.",
            xp_reward: 50
          },
          {
            id: "obj_bronze_crucible",
            name: "Lost-Wax Casting Crucible & Mold",
            icon: "💃",
            category: "High Bronze Metallurgy",
            description: "Refractory clay crucible and beeswax mold used to cast bronze masterpieces like the world-famous 'Dancing Girl of Mohenjo-daro'.",
            archaeological_fact: "Shows advanced knowledge of copper-tin-arsenic alloying.",
            xp_reward: 55
          },
          {
            id: "obj_pottery_wheel",
            name: "Artisan Terracotta Pottery Wheel",
            icon: "🏺",
            category: "Ceramic Production",
            description: "Heavy clay foot-wheel used to throw thin-walled, high-tensile earthenware vessels with glazed black-on-red floral motifs.",
            archaeological_fact: "Consistent firing temperatures above 1,000°C achieved in Harappan kilns.",
            xp_reward: 45
          }
        ],
        quests: [
          {
            id: "quest_lost_wax_casting",
            title: "Master of the Lost Wax",
            description: "Prepare the beeswax figurine and heat the bronze crucible to cast an ancient statuette.",
            reward_xp: 250,
            reward_tokens: 10
          }
        ],
        discovery_reward: { xp: 80, tokens: 6 }
      }
    ];

    this.locations = this.defaultLocations;
  }

  async init() {
    console.log("Initializing Interactive 2D Ancient City Controller (Phase 5)...");
    
    // Attempt dynamic fetch from backend
    try {
      if (window.api && typeof window.api.getLocations === 'function') {
        const remoteLocations = await window.api.getLocations();
        if (remoteLocations && remoteLocations.length >= 7) {
          // Merge svg coordinates
          this.locations = remoteLocations.map((loc, idx) => ({
            ...loc,
            svg_coords: this.defaultLocations[idx] ? this.defaultLocations[idx].svg_coords : "M 0,0 L 100,0 L 100,100 L 0,100 Z",
            coordinates: this.defaultLocations[idx] ? this.defaultLocations[idx].coordinates : { x: 500, y: 300 }
          }));
        }
      }
    } catch (err) {
      console.warn("Using offline fallback city locations:", err);
    }

    this.renderCityStage();
    this.updateDiscoveryCounters();
  }

  // Extensibility: allow plugins or expansions to add additional locations
  registerLocation(locationData) {
    if (!locationData.id) return;
    this.locations.push(locationData);
    this.renderCityStage();
    this.updateDiscoveryCounters();
  }

  renderCityStage() {
    const container = document.getElementById('cityStageContainer');
    if (!container) return;

    container.innerHTML = `
      <div class="city-exploration-container">
        <!-- City HUD Bar -->
        <div class="city-hud-bar">
          <div class="city-hud-left">
            <div class="city-title-group">
              <h3><span>🏛️</span> Harappan Metropolis Explorer</h3>
              <p>Click on any district to inspect authentic architectural ruins & examine excavated relics</p>
            </div>
          </div>

          <!-- Sector Filter Chips -->
          <div class="city-filter-strip">
            <button class="city-filter-btn ${this.activeFilter === 'all' ? 'active' : ''}" onclick="cityController.filterLocations('all')">
              <span>All Sectors (${this.locations.length})</span>
            </button>
            <button class="city-filter-btn ${this.activeFilter === 'Citadel' ? 'active' : ''}" onclick="cityController.filterLocations('Citadel')">
              <span>Citadel Mound</span>
            </button>
            <button class="city-filter-btn ${this.activeFilter === 'Lower Town' ? 'active' : ''}" onclick="cityController.filterLocations('Lower Town')">
              <span>Lower Town Grid</span>
            </button>
          </div>

          <!-- Discovery Progress Meter -->
          <div class="city-discovery-counter" title="Track visited Harappan sectors">
            <span class="discovery-label">Exploration Progress:</span>
            <span class="discovery-val" id="cityDiscoveryText">${this.discoveredLocations.size} / ${this.locations.length}</span>
            <div class="discovery-bar-track">
              <div class="discovery-bar-fill" id="cityDiscoveryFill" style="width: ${(this.discoveredLocations.size / this.locations.length) * 100}%"></div>
            </div>
          </div>
        </div>

        <!-- 2D Interactive City Canvas Card -->
        <div class="city-viewport-card">
          ${this.generateCitySvg()}
          
          <!-- Contextual Floating Hover Card -->
          <div class="city-hover-dossier" id="cityHoverCard" style="display: none;">
            <!-- Populated on hover -->
          </div>
        </div>
      </div>
    `;

    this.bindSvgInteractions();
  }

  generateCitySvg() {
    return `
      <svg class="city-svg-stage" viewBox="0 0 1000 680" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <!-- Brick Pattern -->
          <pattern id="cityBrickPattern" width="16" height="10" patternUnits="userSpaceOnUse">
            <rect width="16" height="10" fill="#2E2019" stroke="#3D2B22" stroke-width="0.8"/>
            <line x1="0" y1="5" x2="16" y2="5" stroke="#3D2B22" stroke-width="0.8"/>
            <line x1="8" y1="0" x2="8" y2="5" stroke="#3D2B22" stroke-width="0.8"/>
            <line x1="16" y1="5" x2="16" y2="10" stroke="#3D2B22" stroke-width="0.8"/>
          </pattern>

          <!-- Water Pattern -->
          <linearGradient id="bathWaterGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#48CAE4" stop-opacity="0.85"/>
            <stop offset="100%" stop-color="#0077B6" stop-opacity="0.95"/>
          </linearGradient>

          <!-- Smoke Glow -->
          <filter id="cityGlow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="5" result="blur"/>
            <feComposite in="SourceGraphic" in2="blur" operator="over"/>
          </filter>
        </defs>

        <!-- Base Soil & Fortified Metropolis Enclosure -->
        <rect width="1000" height="680" rx="10" fill="#181310"/>
        
        <!-- Alluvial Plains Background Contour -->
        <path d="M 0,0 L 1000,0 L 1000,680 L 0,680 Z" fill="url(#cityBrickPattern)" opacity="0.35"/>

        <!-- Western River Quay / River Channel -->
        <path d="M 0,20 C 60,80 80,260 50,440 C 30,560 60,650 80,680 L 0,680 Z" fill="#152836" stroke="#2A9D8F" stroke-width="2" opacity="0.85"/>
        <text x="35" y="320" transform="rotate(-90 35 320)" fill="#64B5F6" font-family="'Cinzel', serif" font-size="10" font-weight="700" letter-spacing="2">
          RIVER QUAY CANAL
        </text>

        <!-- Fortified Western Citadel Mound Elevation -->
        <path d="M 100,40 L 400,40 L 400,640 L 100,640 Z" fill="#221814" stroke="#776052" stroke-width="2" stroke-dasharray="6,4"/>
        <text x="250" y="30" text-anchor="middle" fill="#E9C46A" font-family="'Cinzel', serif" font-weight="800" font-size="11" letter-spacing="2">
          ▲ WESTERN CITADEL (ELEVATED CIVIC MOUND) ▲
        </text>

        <!-- Eastern Lower Town Area -->
        <text x="730" y="30" text-anchor="middle" fill="#D4A373" font-family="'Cinzel', serif" font-weight="700" font-size="11" letter-spacing="2">
          EASTERN LOWER TOWN (RESIDENTIAL & BAZAAR GRID)
        </text>

        <!-- Major 90-degree Grid Avenues (Streets) -->
        <!-- First Street / Main North-South Avenue -->
        <rect x="470" y="50" width="60" height="580" fill="#1C1512" stroke="#4A3A31" stroke-width="1.5"/>
        <line x1="500" y1="50" x2="500" y2="630" stroke="#E9C46A" stroke-width="1.5" stroke-dasharray="8,6" opacity="0.4"/>
        <!-- East-West Cross Avenues -->
        <rect x="400" y="270" width="580" height="36" fill="#1C1512" stroke="#4A3A31" stroke-width="1.2"/>
        <rect x="400" y="470" width="580" height="36" fill="#1C1512" stroke="#4A3A31" stroke-width="1.2"/>

        <!-- ===================================================
             THE 7 INTERACTIVE CITY LOCATIONS
             =================================================== -->
        ${this.locations.map(loc => this.renderLocationMarkup(loc)).join('')}
      </svg>
    `;
  }

  renderLocationMarkup(loc) {
    const isDiscovered = this.discoveredLocations.has(loc.id);
    const coords = loc.coordinates;

    // Filter check
    if (this.activeFilter !== 'all' && loc.zone !== this.activeFilter) {
      return '';
    }

    let sectorGraphic = '';
    
    // Custom architectural silhouettes for each zone
    if (loc.id === 'great_bath') {
      sectorGraphic = `
        <!-- Great Bath Pool Basin -->
        <rect x="180" y="250" width="160" height="140" rx="4" fill="#0F141A" stroke="#C05A3E" stroke-width="2"/>
        <rect class="bath-water-ripple" x="200" y="270" width="120" height="100" rx="3" fill="url(#bathWaterGrad)"/>
        <!-- Steps North & South -->
        <line x1="220" y1="270" x2="300" y2="270" stroke="#FFF" stroke-width="2"/>
        <line x1="230" y1="275" x2="290" y2="275" stroke="#FFF" stroke-width="2"/>
        <line x1="220" y1="370" x2="300" y2="370" stroke="#FFF" stroke-width="2"/>
        <line x1="230" y1="365" x2="290" y2="365" stroke="#FFF" stroke-width="2"/>
        <!-- Cloister Columns -->
        <circle cx="170" cy="240" r="4" fill="#E9C46A"/>
        <circle cx="350" cy="240" r="4" fill="#E9C46A"/>
        <circle cx="170" cy="400" r="4" fill="#E9C46A"/>
        <circle cx="350" cy="400" r="4" fill="#E9C46A"/>
      `;
    } else if (loc.id === 'granary_area') {
      sectorGraphic = `
        <!-- 12 Granary Brick Storage Blocks -->
        <g opacity="0.9">
          <rect x="150" y="90" width="35" height="25" fill="#C05A3E" stroke="#D4A373"/>
          <rect x="195" y="90" width="35" height="25" fill="#C05A3E" stroke="#D4A373"/>
          <rect x="240" y="90" width="35" height="25" fill="#C05A3E" stroke="#D4A373"/>
          <rect x="150" y="125" width="35" height="25" fill="#C05A3E" stroke="#D4A373"/>
          <rect x="195" y="125" width="35" height="25" fill="#C05A3E" stroke="#D4A373"/>
          <rect x="240" y="125" width="35" height="25" fill="#C05A3E" stroke="#D4A373"/>
          <!-- Circular Threshing Floors -->
          <circle cx="295" cy="110" r="12" fill="none" stroke="#E9C46A" stroke-width="1.8"/>
          <circle cx="295" cy="140" r="12" fill="none" stroke="#E9C46A" stroke-width="1.8"/>
        </g>
      `;
    } else if (loc.id === 'main_street') {
      sectorGraphic = `
        <!-- Cart Tracks & Corner Chamfers -->
        <line x1="485" y1="120" x2="485" y2="540" stroke="#776052" stroke-width="2" stroke-dasharray="4,4"/>
        <line x1="515" y1="120" x2="515" y2="540" stroke="#776052" stroke-width="2" stroke-dasharray="4,4"/>
      `;
    } else if (loc.id === 'drainage_system') {
      sectorGraphic = `
        <!-- Subterranean Canal Cutaway -->
        <rect x="545" y="475" width="110" height="95" rx="4" fill="#102535" stroke="#2A9D8F" stroke-width="1.8"/>
        <path d="M 555,520 Q 600,500 645,520" fill="none" stroke="#64B5F6" stroke-width="3" stroke-dasharray="6,3"/>
        <circle cx="600" cy="520" r="8" fill="#D4A373" stroke="#FFF"/>
      `;
    } else if (loc.id === 'residential_area') {
      sectorGraphic = `
        <!-- Multi-room Courtyard Houses -->
        <rect x="690" y="320" width="80" height="80" fill="#2E2019" stroke="#C05A3E" stroke-width="1.5"/>
        <rect x="715" y="345" width="30" height="30" fill="#181310" stroke="#D4A373"/>
        <rect x="785" y="320" width="80" height="80" fill="#2E2019" stroke="#C05A3E" stroke-width="1.5"/>
        <rect x="810" y="345" width="30" height="30" fill="#181310" stroke="#D4A373"/>
        <rect x="735" y="415" width="90" height="80" fill="#2E2019" stroke="#C05A3E" stroke-width="1.5"/>
      `;
    } else if (loc.id === 'marketplace') {
      sectorGraphic = `
        <!-- Bazaar Square & Stalls -->
        <rect x="610" y="110" width="180" height="130" fill="#2A1E17" stroke="#E9C46A" stroke-width="1.5"/>
        <rect x="630" y="130" width="35" height="25" fill="#D4A373"/>
        <rect x="680" y="130" width="35" height="25" fill="#C05A3E"/>
        <rect x="730" y="130" width="35" height="25" fill="#D4A373"/>
        <!-- Balance Scale Icon -->
        <text x="700" y="205" text-anchor="middle" font-size="24">⚖️</text>
      `;
    } else if (loc.id === 'craft_workshop') {
      sectorGraphic = `
        <!-- Artisan Quarter & Kiln -->
        <rect x="840" y="150" width="105" height="175" fill="#2A1E17" stroke="#D4A373" stroke-width="1.5"/>
        <circle cx="890" cy="190" r="16" fill="#C05A3E" stroke="#E9C46A" stroke-width="2"/>
        <circle class="kiln-smoke-particle" cx="890" cy="180" r="6" fill="#FFF"/>
        <circle cx="890" cy="250" r="14" fill="#3D2D26" stroke="#2A9D8F" stroke-width="1.8"/>
        <text x="890" y="255" text-anchor="middle" font-size="12">🏺</text>
      `;
    }

    return `
      <g class="city-location-zone ${this.selectedLocationId === loc.id ? 'active-selected' : ''}" 
         id="zoneGroup_${loc.id}" 
         data-location-id="${loc.id}">
        
        <!-- Interactive Hitbox Polygon -->
        <path class="city-zone-polygon" d="${loc.svg_coords}"/>
        
        <!-- Architectural Details -->
        ${sectorGraphic}

        <!-- Interactive Beacon / Radar Pin -->
        <g class="city-zone-beacon" transform="translate(${coords.x}, ${coords.y})">
          <circle class="beacon-pulse-ring" cx="0" cy="0" r="10"></circle>
          <circle class="beacon-core" cx="0" cy="0" r="9"></circle>
          <text x="0" y="4" text-anchor="middle" font-size="10">${loc.icon}</text>
          
          <!-- Label Banner -->
          <rect x="-65" y="15" width="130" height="22" rx="4" fill="rgba(18, 14, 12, 0.9)" stroke="#E9C46A" stroke-width="1"/>
          <text class="beacon-text" x="0" y="30" text-anchor="middle">
            ${isDiscovered ? '✓ ' : '✨ '}${loc.name}
          </text>
        </g>
      </g>
    `;
  }

  bindSvgInteractions() {
    this.locations.forEach(loc => {
      const el = document.getElementById(`zoneGroup_${loc.id}`);
      if (!el) return;

      el.addEventListener('mouseenter', (e) => this.onHoverLocation(loc));
      el.addEventListener('mouseleave', () => this.onLeaveLocation());
      el.addEventListener('click', (e) => {
        this.selectLocation(loc.id, e);
      });
    });
  }

  onHoverLocation(loc) {
    if (window.audio) audio.playClick();
    const hoverCard = document.getElementById('cityHoverCard');
    if (!hoverCard) return;

    const isDiscovered = this.discoveredLocations.has(loc.id);

    hoverCard.style.display = 'block';
    hoverCard.innerHTML = `
      <h4><span>${loc.icon}</span> ${loc.name}</h4>
      <div style="font-size: 0.72rem; color: var(--color-sandstone); font-weight: 700; text-transform: uppercase; margin-bottom: 4px;">
        ${loc.zone} • ${loc.site}
      </div>
      <p>${loc.subtitle}</p>
      <span class="city-hover-hint">
        ${isDiscovered ? '✨ CLICK TO INSPECT ARTIFACTS & RELICS' : '⭐ UNDISCOVERED AREA • CLICK TO EXPLORE (+75 XP)'}
      </span>
    `;
  }

  onLeaveLocation() {
    const hoverCard = document.getElementById('cityHoverCard');
    if (hoverCard) hoverCard.style.display = 'none';
  }

  selectLocation(locationId, event = null) {
    const loc = this.locations.find(l => l.id === locationId);
    if (!loc) return;

    this.selectedLocationId = locationId;

    // Trigger Discovery if first time!
    if (!this.discoveredLocations.has(locationId)) {
      this.triggerDiscovery(loc, event);
    } else {
      if (window.audio) audio.playChime();
    }

    this.openInspectorModal(loc);
    this.renderCityStage(); // Re-render to update active status
  }

  async triggerDiscovery(loc, event = null) {
    this.discoveredLocations.add(loc.id);
    localStorage.setItem(
      'bq_discovered_city_locations',
      JSON.stringify(Array.from(this.discoveredLocations))
    );

    if (window.audio) audio.playFanfare();

    const xpEarned = loc.discovery_reward ? loc.discovery_reward.xp : 75;
    const tokensEarned = loc.discovery_reward ? loc.discovery_reward.tokens : 5;

    // Show floating XP text & discovery toast
    if (window.uxManager) {
      uxManager.spawnXpAnimation(xpEarned, event ? event.target : null);
      uxManager.triggerLocationDiscovery(loc.name, loc.icon, xpEarned);
    } else {
      this.showFloatingXp(`+${xpEarned} XP`, event);
      this.showDiscoveryToast(loc.name, xpEarned, tokensEarned);
    }
    this.updateDiscoveryCounters();

    // Sync progress with backend via Phase 8 Gamification API
    if (window.app && app.state.user) {
      try {
        const username = app.state.user.username;
        const res = await api.exploreLocation(username, loc.id);
        
        if (res && res.is_new) {
          app.logConsole(`🧭 SURVEYED SECTOR: "${loc.name}" (+${res.xp_awarded} XP, +${res.tokens_awarded} Seals)`);
          
          // Check for Level Up!
          if (res.level_up && res.level_up.level_up_occurred) {
            if (window.uxManager) {
              uxManager.triggerLevelUp(res.level_up.new_level, res.level_up.new_title);
            }
            setTimeout(() => {
              if (window.gamificationController) {
                gamificationController.showLevelUpModal(res.level_up);
              }
            }, 600);
          }
          
          // Check for newly unlocked badges (e.g. Heritage Explorer or Master Planner)
          if (res.newly_unlocked_badges && res.newly_unlocked_badges.length > 0) {
            res.newly_unlocked_badges.forEach(badgeId => {
              const badgeLabel = badgeId.replace('badge_', '').replace(/_/g, ' ').toUpperCase();
              app.logConsole(`🏅 NEW BADGE EARNED: ${badgeLabel}!`);
              if (window.uxManager) {
                uxManager.triggerBadgeUnlock(badgeLabel, '🏅');
              }
            });
          }
          
          // Reload user profile to update HUD in real time
          await app.loadUserProfile(username);
        }
      } catch (err) {
        console.warn('Exploration sync note:', err);
        // Fallback local award
        app.simulateAward(xpEarned, tokensEarned, null, null);
      }
    }
  }

  updateDiscoveryCounters() {
    const countText = document.getElementById('cityDiscoveryText');
    const fillBar = document.getElementById('cityDiscoveryFill');
    const total = this.locations.length;
    const current = this.discoveredLocations.size;

    if (countText) countText.innerText = `${current} / ${total}`;
    if (fillBar) {
      const pct = Math.round((current / total) * 100);
      fillBar.style.width = `${pct}%`;
    }
  }

  openInspectorModal(loc) {
    const modal = document.getElementById('cityInspectorModal');
    if (!modal) return;

    // Header
    const iconEl = document.getElementById('inspectorIcon');
    const titleEl = document.getElementById('inspectorTitle');
    const zoneEl = document.getElementById('inspectorZone');
    const historyEl = document.getElementById('inspectorHistoryText');
    const objectsContainer = document.getElementById('inspectableObjectsGrid');
    const questsContainer = document.getElementById('inspectorQuestsContainer');

    if (iconEl) iconEl.innerText = loc.icon;
    if (titleEl) titleEl.innerText = loc.name;
    if (zoneEl) zoneEl.innerText = `${loc.zone} • ${loc.site}`;

    const sectorGuides = {
      'residential_area': {
        action: 'Peek inside an ancient house to see the courtyard, private bathroom, and stairs.',
        facts: [
          'Houses were built with strong baked bricks around cool, open-air courtyards.',
          'Doors opened into quiet side alleys so dust from the main street stayed outside.',
          'Almost every home had its own tiled bathroom connected to street drains!'
        ],
        didYouKnow: 'Indus houses had upstairs bedrooms and flat roofs for sleeping on summer nights!'
      },
      'main_street': {
        action: 'Walk down First Street to see the 10-meter wide boulevard and bullock cart ruts.',
        facts: [
          'Streets were 10 meters wide—broad enough for two ox-carts to pass easily!',
          'Avenues crossed at exact 90° right angles, forming the world\'s neatest city grid.',
          'Corners of street buildings were rounded so cart wheels wouldn\'t chip the walls.'
        ],
        didYouKnow: 'Indus cities had public lamp posts with oil lamps on street corners for night lighting!'
      },
      'drainage_system': {
        action: 'Follow the water from home bathrooms through covered brick sewers to outside the city.',
        facts: [
          'Wash water flowed through clay wall pipes into covered brick street drains.',
          'Underground channels were covered with flat stone slabs that workers lifted to clean.',
          'Wastewater was filtered in soak jars before discharging safely away from homes.'
        ],
        didYouKnow: 'This was the world\'s first covered sanitation system—unmatched until the Roman Empire!'
      },
      'great_bath': {
        action: 'Look at the giant ritual bath with waterproof brick seams and stepped staircases.',
        facts: [
          'A huge ceremonial public swimming pool lined with tightly fitted baked bricks.',
          'Ancient builders spread natural tar (bitumen) between bricks so water never leaked!',
          'Two wide staircases led into the pool, surrounded by quiet changing rooms.'
        ],
        didYouKnow: 'The Great Bath was filled with fresh water from a special well, and had a giant drainage tunnel!'
      },
      'granary_area': {
        action: 'Check the food supply of wheat, barley, lentils, sesame, and sweet dates.',
        facts: [
          'A giant raised brick hall used to store grain for the whole city.',
          'Engineered with air vents underneath to keep grain dry, cool, and safe from floods.',
          'Stored winter and summer harvests to protect citizens during dry seasons.'
        ],
        didYouKnow: 'Farmers paid taxes in wheat and barley, which fed city workers and bead artisans!'
      },
      'marketplace': {
        action: 'Trade precious goods like carnelian beads, sea shells, and check standard weights.',
        facts: [
          'A buzzing commercial hub where traders bought cotton clothes, beads, pots, and food.',
          'Merchants used polished cubic stone weights so no buyer or seller was cheated.',
          'Ships brought goods from as far as Mesopotamia and Central Asia!'
        ],
        didYouKnow: 'Every Indus market used the exact same balance weights, across over 1,000 kilometers!'
      },
      'craft_workshop': {
        action: 'Watch artisans work with bead drills, potter wheels, and bronze lost-wax casting.',
        facts: [
          'World-famous artisans drilled tiny holes through gemstone carnelian beads.',
          'Potters turned red clay into painted jars using fast pottery wheels.',
          'Sculptors cast bronze statues like the Dancing Girl using lost-wax molds.'
        ],
        didYouKnow: 'Harappan bead-makers used special micro-drills made of ultra-hard stone found in Gujarat!'
      }
    };

    const guide = sectorGuides[loc.id] || {
      action: 'Explore this ancient area to discover how Harappan citizens lived.',
      facts: [loc.historical_explanation],
      didYouKnow: 'Indus Valley cities were among the most advanced in the ancient world!'
    };

    if (historyEl) {
      historyEl.innerHTML = `
        <div class="kid-sector-modal-content">
          <div class="kid-sector-action-box" style="background: rgba(46, 196, 182, 0.12); border-left: 3px solid #2EC4B6; padding: 8px 12px; border-radius: 6px; margin-bottom: 10px; font-size: 0.88rem; color: #E0FBFC;">
            <strong>🎯 Thing to Do:</strong> ${guide.action}
          </div>
          <ul style="margin: 8px 0 12px 18px; padding: 0; line-height: 1.5; color: #F8F9FA; font-size: 0.88rem;">
            ${guide.facts.map(f => `<li style="margin-bottom: 4px;">✨ ${f}</li>`).join('')}
          </ul>
          <div class="kid-sector-didyouknow" style="background: rgba(245, 158, 11, 0.12); border-left: 3px solid #F59E0B; padding: 8px 12px; border-radius: 6px; margin-bottom: 12px; font-size: 0.84rem; color: #FDE68A;">
            <strong>💡 Did you know?</strong> ${guide.didYouKnow}
          </div>
          <button class="ancient-btn btn-secondary" style="width: 100%; justify-content: center; padding: 8px;" onclick="cityController.askGuideAboutSector('${loc.id}')">
            <span>🧭 Ask Heritage Guide About This Area ➔</span>
          </button>
        </div>
      `;
    }

    // Render Inspectable Archaeological Objects
    if (objectsContainer) {
      objectsContainer.innerHTML = (loc.interactive_objects || []).map((obj, idx) => {
        const isExamined = this.examinedObjects.has(obj.id);
        return `
          <div class="inspectable-object-card" id="objCard_${obj.id}">
            <div>
              <div class="object-card-top">
                <div class="object-card-icon">${obj.icon}</div>
                <div>
                  <div class="object-card-title">${obj.name}</div>
                  <div class="object-card-category">${obj.category}</div>
                </div>
              </div>
              <p class="object-card-desc" style="margin-top: 8px;">${obj.description}</p>
            </div>
            <div>
              <div class="object-fact-pill" style="margin-bottom: 10px;">
                <strong>Evidence:</strong> ${obj.archaeological_fact}
              </div>
              <button class="inspect-action-btn ${isExamined ? 'examined' : ''}" 
                      onclick="cityController.inspectObject('${loc.id}', '${obj.id}', event)">
                <span>${isExamined ? '✓ Examined & Documented' : `🔍 Inspect Relic (+${obj.xp_reward} XP)`}</span>
              </button>
            </div>
          </div>
        `;
      }).join('');
    }

    // Render Quests
    if (questsContainer) {
      questsContainer.innerHTML = (loc.quests || []).map(q => `
        <div class="quest-item-card">
          <div class="quest-item-info">
            <h5>📜 ${q.title}</h5>
            <p>${q.description}</p>
            <div class="quest-reward-tags">
              <span class="reward-tag">⭐ +${q.reward_xp} XP</span>
              <span class="reward-tag">🪙 +${q.reward_tokens} Seals</span>
            </div>
          </div>
          <button class="ancient-btn btn-primary" onclick="cityController.startQuest('${q.id}')">
            <span>Start Challenge ➔</span>
          </button>
        </div>
      `).join('');
    }

    modal.classList.add('active');
  }

  closeInspectorModal() {
    const modal = document.getElementById('cityInspectorModal');
    if (modal) modal.classList.remove('active');
  }

  askGuideAboutSector(sectorId) {
    this.closeInspectorModal();
    if (window.app) {
      window.app.switchTab('tab-ai');
    }
    const sectorQuestions = {
      'citadel_mound': "Tell me about the Citadel Mound! What was it used for?",
      'great_bath': "Tell me about the Great Bath! How was it built waterproof?",
      'granary_complex': "Tell me about the Great Granary! How did they store grains?",
      'lower_town_grid': "Why were Harappan streets and houses built in a grid pattern?",
      'drainage_system': "Why are Harappan covered drains so famous and special?",
      'commercial_bazaar': "How did Harappan merchants weigh and trade their goods?",
      'craft_workshop': "How did ancient artisans make carnelian beads and bronze statues?"
    };
    const question = sectorQuestions[sectorId] || "Tell me about this part of the ancient city!";
    setTimeout(() => {
      if (window.aiController && typeof window.aiController.quickAsk === 'function') {
        window.aiController.quickAsk(question);
      }
    }, 300);
  }

  inspectObject(locationId, objectId, event = null) {
    if (this.examinedObjects.has(objectId)) {
      if (window.audio) audio.playClick();
      return;
    }

    const loc = this.locations.find(l => l.id === locationId);
    if (!loc) return;
    const obj = (loc.interactive_objects || []).find(o => o.id === objectId);
    if (!obj) return;

    this.examinedObjects.add(objectId);
    localStorage.setItem(
      'bq_examined_objects',
      JSON.stringify(Array.from(this.examinedObjects))
    );

    if (window.audio) audio.playChime();
    if (window.uxManager) {
      uxManager.spawnXpAnimation(obj.xp_reward, event ? event.target : null);
      uxManager.showToast({
        title: `Relic Documented: ${obj.name}`,
        message: `${obj.archaeological_fact}`,
        icon: obj.icon || '🔍',
        type: 'success',
        duration: 3500
      });
    } else {
      this.showFloatingXp(`+${obj.xp_reward} XP`, event);
    }

    // Update button in UI
    const card = document.getElementById(`objCard_${objectId}`);
    if (card) {
      const btn = card.querySelector('.inspect-action-btn');
      if (btn) {
        btn.className = 'inspect-action-btn examined';
        btn.innerHTML = '<span>✓ Examined & Documented</span>';
      }
    }

    // Sync with app XP
    if (window.app && app.state.user) {
      app.simulateAward(obj.xp_reward, 2, null, null);
      app.logConsole(`🔍 Inspected Relic: "${obj.name}" (+${obj.xp_reward} XP)`);
    }
  }

  startQuest(questId) {
    if (window.audio) audio.playGong();
    this.closeInspectorModal();
    if (window.app) {
      app.logConsole(`🚀 Embarking on Quest Challenge: "${questId}"`);
      app.switchTab('tab-quests');
    }

    if (window.questController) {
      // Map location quest IDs to the 5 core quest challenges
      let targetQuestId = questId;
      if (questId.includes('drain') || questId.includes('water') || questId.includes('purification')) {
        targetQuestId = 'quest_03_drainage_challenge';
      } else if (questId.includes('merchant') || questId.includes('balance') || questId.includes('trade')) {
        targetQuestId = 'quest_04_ancient_trade';
      } else if (questId.includes('lost_wax') || questId.includes('granary') || questId.includes('life')) {
        targetQuestId = 'quest_05_life_in_ivc';
      } else if (questId.includes('rebuild') || questId.includes('avenue') || questId.includes('city') || questId.includes('grid')) {
        targetQuestId = 'quest_01_rebuild_city';
      } else {
        targetQuestId = 'quest_02_lost_artifact';
      }

      setTimeout(() => {
        questController.openQuestChallenge(targetQuestId);
      }, 300);
    }
  }

  filterLocations(filterType) {
    if (window.audio) audio.playClick();
    this.activeFilter = filterType;
    this.renderCityStage();
  }

  showFloatingXp(text, event = null) {
    const el = document.createElement('div');
    el.className = 'floating-xp-particle';
    el.innerText = text;

    let x = window.innerWidth / 2;
    let y = window.innerHeight / 2;

    if (event && event.clientX) {
      x = event.clientX;
      y = event.clientY;
    }

    el.style.left = `${x}px`;
    el.style.top = `${y}px`;

    document.body.appendChild(el);
    setTimeout(() => el.remove(), 1600);
  }

  showDiscoveryToast(locationName, xp, seals) {
    const banner = document.getElementById('cityDiscoveryToast');
    if (!banner) return;

    const textEl = banner.querySelector('.discovery-toast-text');
    if (textEl) {
      textEl.innerHTML = `
        <h4>🌟 Sector Discovered!</h4>
        <p>${locationName} Unlocked (+${xp} XP, +${seals} Seals)</p>
      `;
    }

    banner.classList.add('active');
    setTimeout(() => {
      banner.classList.remove('active');
    }, 3500);
  }
}

const cityController = new AncientCityController();
window.cityController = cityController;
