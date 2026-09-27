from fastapi import APIRouter

router = APIRouter(prefix="/ivc", tags=["Civilization & Locations"])

@router.get("/overview")
def get_ivc_overview():
    return {
        "civilization": "Indus Valley Civilization (Harappan Civilization)",
        "period": "c. 2600 BCE – 1900 BCE (Mature Harappan Phase)",
        "geography": "Indus and Ghaggar-Hakra River Basins (Northwest Indian Subcontinent)",
        "key_sites": [
            {"name": "Mohenjo-daro", "specialty": "The Great Bath & Subterranean Corbelled Drainage"},
            {"name": "Harappa", "specialty": "Urban Grid Architecture & Great Granaries"},
            {"name": "Lothal", "specialty": "World's Earliest Known Tidal Dockyard & Bead Factory"},
            {"name": "Dholavira", "specialty": "Master Water Reservoirs & Large Signboard Inscription"},
            {"name": "Kalibangan", "specialty": "Furrowed Agricultural Fields & Fire Altars"}
        ],
        "hallmarks": [
            "Precision fired brick masonry (1:2:4 ratio)",
            "Closed street drains with inspection manholes",
            "Standardized binary-decimal chert weights",
            "Steatite carved stamp seals for maritime commerce"
        ]
    }

@router.get("/story")
def get_ivc_story():
    """
    Returns the 7-part interactive, story-driven introduction for the Indus Valley Civilization.
    Each scene introduces core historical facts, archaeological discoveries, and clear distinction
    between archaeological evidence and gamified learning mechanics.
    """
    return {
        "title": "Indus Valley Civilization: The Living Bronze-Age Metropolis",
        "civilization": "Indus Valley Civilization",
        "era": "c. 2600 BCE – 1900 BCE (Mature Harappan Phase)",
        "total_scenes": 7,
        "scenes": [
            {
                "id": "scene_01_dawn",
                "scene_number": 1,
                "title": "The Dawn Along the Sindhu",
                "subtitle": "A Colossal Bronze-Age Civilization Awakens",
                "period": "c. 2600 BCE – 1900 BCE • Mature Harappan Phase",
                "narrative": "Over 4,500 years ago, while the Egyptian Pyramids were young and Stonehenge was being erected, a breathtaking civilization flourished across the fertile river valleys of ancient Bharat. Spanning over 1 million square kilometers—larger than ancient Egypt and Mesopotamia combined—the Indus Valley Civilization was built along the mighty snow-fed Indus (Sindhu) and the ancient Saraswati (Ghaggar-Hakra) river basins.",
                "curiosity_fact": "Archaeologists have identified over 1,000 Harappan settlements across modern-day India (Gujarat, Rajasthan, Haryana, Punjab) and Pakistan.",
                "historical_distinction": "Historical Evidence: Carbon dating and stratigraphy confirm thriving mature urban phases from 2600 to 1900 BCE without signs of monarchical palaces or standing imperial armies.",
                "badge_icon": "🌅",
                "highlight_topic": "Geography & Historical Era"
            },
            {
                "id": "scene_02_metropolises",
                "scene_number": 2,
                "title": "The Great Metropolises",
                "subtitle": "Twin Cities and Vast Trade Centers",
                "period": "Major Urban Settlements Across the River Valleys",
                "narrative": "Instead of isolated rural hamlets, Harappan society was anchored by massive, meticulously organized metropolises. Mohenjo-daro commanded the southern Indus in Sindh, while Harappa dominated the northern river routes of the Ravi. In Gujarat, Lothal served as a bustling maritime gateway, while Dholavira stood as an island fortress in the Rann of Kutch with monumental stone architecture. Farther east, Kalibangan and Rakhigarhi guarded the fertile plains.",
                "curiosity_fact": "Rakhigarhi in Haryana is now known to be the largest Harappan site, sprawling across more than 350 hectares!",
                "historical_distinction": "Historical Evidence: Consistent city layouts, brick dimensions, and weights across thousands of miles point to shared standards and civic governance.",
                "badge_icon": "🏛️",
                "highlight_topic": "Major Settlements"
            },
            {
                "id": "scene_03_grid_planning",
                "scene_number": 3,
                "title": "The Master Grid Planners",
                "subtitle": "The World's Earliest Planned Cities",
                "period": "Orthogonal Architecture & The 1:2:4 Brick Ratio",
                "narrative": "Imagine strolling down a wide city boulevard 4,500 years ago that is perfectly straight, 10 meters wide, aligned North-to-South, and intersected by cross-streets at exact 90-degree right angles! Harappan urban planning divided cities into a fortified western Citadel for civic assemblies and a sprawling Lower Town for residences. Every building used standardized kiln-fired bricks following a strict mathematical ratio: 1 unit thick, 2 units wide, and 4 units long (1:2:4).",
                "curiosity_fact": "Unlike sun-dried mud bricks used in Mesopotamia that dissolved during rains, Harappan baked bricks were moisture-resistant and have survived for millennia.",
                "historical_distinction": "Historical Evidence: Burnt brick dimensions excavated at Harappa, Mohenjo-daro, and Lothal exhibit uniform 1:2:4 ratios across centuries.",
                "badge_icon": "📐",
                "highlight_topic": "City Planning & Masonry"
            },
            {
                "id": "scene_04_sanitation",
                "scene_number": 4,
                "title": "The Miracle of Public Hygiene",
                "subtitle": "Subterranean Drainage & The Great Bath",
                "period": "World's First Underground Sewer Engineering",
                "narrative": "The crowning marvel of the Indus civilization was its hygiene infrastructure—unequaled anywhere in the world until the 19th century! Nearly every home featured a private paved bathroom. Wastewater traveled down terracotta chutes into corbelled brick sewer lines buried under street pavements. Inspection manholes with removable limestone covers allowed civic workers to clear blockages. At Mohenjo-daro, the iconic Great Bath was sealed with natural bitumen (asphalt) to create a watertight public pool.",
                "curiosity_fact": "Every neighborhood featured soak-pits to separate solid waste from runoff, preventing street contamination.",
                "historical_distinction": "Historical Evidence: Intact drainage networks and inspection chambers are documented in ASI excavation reports at Mohenjo-daro, Harappa, and Dholavira.",
                "badge_icon": "🚰",
                "highlight_topic": "Drainage & Hygiene"
            },
            {
                "id": "scene_05_trade",
                "scene_number": 5,
                "title": "Seafarers & The Standard Weights",
                "subtitle": "Maritime Docks & Precision Metrology",
                "period": "International Trade with Ancient Mesopotamia & the Gulf",
                "narrative": "The Harappans were daring international merchants. At Lothal in Gujarat, maritime engineers constructed the world's earliest known tidal dockyard, complete with a water sluice lock to float merchant galleys regardless of tidal ebb and flow. Harappan merchant ships carried etched carnelian beads, fine cotton textiles ('Sindhu'), copper, and ivory across the Arabian Sea to ancient Sumer (Mesopotamia), where clay cuneiform tablets recorded trade with the wealthy land of 'Meluhha'.",
                "curiosity_fact": "Commerce was governed by standardized chert cubical weights following a binary sequence: 1, 2, 4, 8, 16, 32... up to decimal ratios for massive bulk trade.",
                "historical_distinction": "Historical Evidence: Mesopotamian records directly cite imports from Meluhha, and Indus seals and cubical chert weights have been excavated in Ur and Kish.",
                "badge_icon": "⛵",
                "highlight_topic": "Maritime Commerce & Weights"
            },
            {
                "id": "scene_06_crafts",
                "scene_number": 6,
                "title": "Master Artisans & Enigmatic Script",
                "subtitle": "Bead Kilns, Bronze Sculptures & Steatite Seals",
                "period": "Bronze-Age Metallurgy & Undeciphered Inscriptions",
                "narrative": "Indus artisans possessed astonishing technical mastery. At Lothal and Chanhudaro, bead factories drilled microscopic holes through hard carnelian stone using diamond-tipped drills and fired them in multi-chamber kilns to produce fiery red gems. Metallurgists used the delicate 'lost-wax' bronze casting process to sculpt the famous 'Dancing Girl of Mohenjo-daro'. Meanwhile, scribes carved hundreds of exquisite steatite stamp seals featuring unicorns, humped zebu bulls, and the meditating Pashupati, alongside 400+ undeciphered pictographic symbols.",
                "curiosity_fact": "The Indus script remains one of archaeology's greatest unsolved mysteries, written from right to left with symbolic logograms.",
                "historical_distinction": "Historical Evidence: Over 4,000 inscribed seal stones, copper tablets, and the giant 10-symbol wooden signboard of Dholavira have been unearthed.",
                "badge_icon": "🦏",
                "highlight_topic": "Crafts & Seals"
            },
            {
                "id": "scene_07_daily_life",
                "scene_number": 7,
                "title": "Life in the Living City & Your Mission",
                "subtitle": "Peaceful Daily Routines & The Explorer's Gateway",
                "period": "Civilian Life & Gamified Archaeological Exploration",
                "narrative": "Daily life in a Harappan city was peaceful and industrious. Citizens ate nutritious diets of barley, emmer wheat, chickpeas, and mustard, seasoned with ginger and garlic. Children played with terracotta toy carts, clay whistles, and maze boards. Remarkably, no royal statues, weapons of war, or monuments glorify conquerors. Today, you step into this living bronze-age metropolis not just as a reader, but as an active explorer solving ancient engineering puzzles and unearthing authentic relics!",
                "curiosity_fact": "Terracotta toy bullock carts with working rotating wheels found in excavations prove that ancient Indian children learned transport mechanics through play!",
                "historical_distinction": "Pedagogical Note: All historical facts, architectural measurements, and artifacts in Bharat Quest are strictly based on ASI archaeological findings. Your avatar profile, interactive quests, and seal rewards are gamified learning simulations designed to bring history to life!",
                "badge_icon": "🏺",
                "highlight_topic": "Daily Life & Living Quest"
            }
        ]
    }

@router.get("/civilizations")
def list_civilizations():
    """
    Returns all ancient Indian civilization realms on the National Heritage Map.
    Only Indus Valley Civilization (IVC) is active in this SIH prototype;
    other historical eras demonstrate system architecture and future scalability.
    """
    return [
        {
            "id": "ivc",
            "name": "Indus Valley Civilization",
            "subtitle": "The Bronze-Age Urban Metropolis",
            "era": "c. 2600 – 1900 BCE (Mature Harappan)",
            "status": "unlocked",
            "region": "Northwest Bharat (Indus & Ghaggar-Hakra River Basins)",
            "description": "The world's earliest planned cities featuring right-angle grid streets, subterranean covered drainage, standardized binary weights, and international maritime trade.",
            "major_sites": ["Mohenjo-daro", "Harappa", "Lothal", "Dholavira", "Kalibangan", "Rakhigarhi"],
            "artifacts_preview": ["Pashupati Seal", "The Dancing Girl", "Chert Cubical Weights", "Terracotta Toy Cart"],
            "color": "#E9C46A"
        },
        {
            "id": "vedic",
            "name": "Vedic Realm & Saraswati Basin",
            "subtitle": "Era of Hymns, Iron & Early Janapadas",
            "era": "c. 1500 – 600 BCE",
            "status": "locked",
            "region": "Sapta-Sindhu & Upper Gangetic Plains",
            "description": "Composition of the Vedas, Painted Grey Ware ceramics, iron metallurgy, and philosophical treatises.",
            "lock_reason": "Locked in Prototype • Coming in Bharat Quest Expansion Pack",
            "color": "#9381FF"
        },
        {
            "id": "maurya",
            "name": "Mauryan Empire & Magadha",
            "subtitle": "The Imperial Wheel & Pan-Indian Unity",
            "era": "c. 322 – 185 BCE",
            "status": "locked",
            "region": "Central & Eastern Bharat (Pataliputra)",
            "description": "Chanakya's Arthashastra, Ashokan edicts, grand stone pillars, and diplomatic embassies across the ancient world.",
            "lock_reason": "Locked in Prototype • Coming in Bharat Quest Expansion Pack",
            "color": "#38B000"
        },
        {
            "id": "gupta",
            "name": "Gupta Classical Golden Age",
            "subtitle": "The Renaissance of Science & Arts",
            "era": "c. 319 – 543 CE",
            "status": "locked",
            "region": "Gangetic Heartland & Malwa",
            "description": "Aryabhata's astronomical treatises, discovery of decimal zero, Kalidasa's poetry, and Ajanta frescoes.",
            "lock_reason": "Locked in Prototype • Coming in Bharat Quest Expansion Pack",
            "color": "#FFB703"
        },
        {
            "id": "chola",
            "name": "Imperial Chola Maritime Realm",
            "subtitle": "Masters of the Indian Ocean",
            "era": "c. 848 – 1279 CE",
            "status": "locked",
            "region": "Southern Peninsula & Coromandel Coast",
            "description": "Monumental living granite temples, maritime trade across Southeast Asia, and lost-wax bronze sculptures.",
            "lock_reason": "Locked in Prototype • Coming in Bharat Quest Expansion Pack",
            "color": "#FB8500"
        }
    ]

@router.get("/locations")
def list_locations():
    """
    Returns the 7 core interactive locations of the Harappan Metropolis for Phase 5.
    Includes historical explanations, inspectable archaeological objects, and related quests.
    """
    return [
        {
            "id": "residential_area",
            "name": "Residential Area",
            "subtitle": "Courtyard Dwellings & Domestic Privacy",
            "site": "Mohenjo-daro & Harappa",
            "zone": "Lower Town",
            "icon": "🏡",
            "level_required": 1,
            "status": "unlocked",
            "coordinates": {"x": 72, "y": 62},
            "historical_explanation": "Harappan residential architecture was focused on domestic privacy and environmental adaptation. Multi-story homes were constructed with burnt bricks around central open-air courtyards. Windows never faced the dusty main avenues, and doorways opened into quiet side alleys. Nearly every home had its own terracotta bathroom, water well, and staircase leading to upper living quarters or a flat sleeping roof.",
            "interactive_objects": [
                {
                    "id": "obj_storage_jar",
                    "name": "Painted Terracotta Storage Urn",
                    "icon": "🏺",
                    "category": "Household Ceramic",
                    "description": "Large black-on-red ceramic jar treated with fine red slip and painted with intersecting circles and peacock motifs, used to store grains, oils, and well water.",
                    "archaeological_fact": "Excavated from residential floor levels across Mohenjo-daro HR area.",
                    "xp_reward": 35
                },
                {
                    "id": "obj_spindle_whorl",
                    "name": "Terracotta Spindle Whorl",
                    "icon": "🧵",
                    "category": "Domestic Textile Tool",
                    "description": "Perforated clay flywheel used for spinning raw Indus cotton ('Sindhu') into fine textile threads for household garments.",
                    "archaeological_fact": "Proves that textile weaving was a widespread domestic cottage industry.",
                    "xp_reward": 40
                },
                {
                    "id": "obj_toy_cart",
                    "name": "Clay Toy Bullock Cart",
                    "icon": "🪅",
                    "category": "Ancient Play & Learning",
                    "description": "Terracotta model cart with working rotating wooden axle pegs and miniature clay oxen, showing how children learned transportation mechanics.",
                    "archaeological_fact": "Among the most common playful artifacts found in Harappan residential ruins.",
                    "xp_reward": 45
                }
            ],
            "quests": [
                {
                    "id": "quest_domestic_water",
                    "title": "Domestic Water Circulation",
                    "description": "Trace the path of fresh well water from the courtyard cistern to the second-story private bathing room.",
                    "reward_xp": 180,
                    "reward_tokens": 6
                }
            ],
            "discovery_reward": {"xp": 75, "tokens": 5}
        },
        {
            "id": "main_street",
            "name": "Main Street",
            "subtitle": "The 10-Meter Orthogonal Boulevard",
            "site": "Mohenjo-daro (First Street)",
            "zone": "Lower Town",
            "icon": "🛣️",
            "level_required": 1,
            "status": "unlocked",
            "coordinates": {"x": 50, "y": 50},
            "historical_explanation": "The grand thoroughfare of the metropolis ran strictly North-to-South for over half a kilometer, measuring nearly 10 meters wide—broad enough for two bullock carts to pass abreast without slowing down. It formed the central axis of the city's rigid cardinal grid plan, flanked by standard 1:2:4 burnt-brick street corners designed to prevent carts from chipping wall plaster.",
            "interactive_objects": [
                {
                    "id": "obj_standard_brick",
                    "name": "Standardized 1:2:4 Fired Brick",
                    "icon": "🧱",
                    "category": "Civic Masonry",
                    "description": "Standard kiln-fired clay brick measuring exactly 7 × 14 × 28 cm. The strict 1:2:4 ratio ensured optimal interlocking bond strength in seismic alluvial soils.",
                    "archaeological_fact": "Identical dimensions have been recorded across sites 1,000 km apart.",
                    "xp_reward": 35
                },
                {
                    "id": "obj_cart_rut",
                    "name": "Compacted Bullock Cart Rut",
                    "icon": "🛞",
                    "category": "Ancient Infrastructure",
                    "description": "Preserved wheel-track impression in the hardened mud street floor, matching the exact gauge of modern Indian village bullock carts.",
                    "archaeological_fact": "Wheel gauge measurements at Harappa and Mohenjo-daro average 1.1 meters.",
                    "xp_reward": 40
                },
                {
                    "id": "obj_street_lamp_post",
                    "name": "Municipal Lamp Post Niche",
                    "icon": "🕯️",
                    "category": "Civic Amenities",
                    "description": "Recessed brick niches carved into exterior avenue corners where terracotta oil lamps illuminated night patrols and street navigation.",
                    "archaeological_fact": "Earliest known municipal street lighting architecture in world history.",
                    "xp_reward": 45
                }
            ],
            "quests": [
                {
                    "id": "quest_orthogonal_avenue",
                    "title": "The Orthogonal Grid Survey",
                    "description": "Survey the 90-degree intersection of First Street with East-West Avenue to verify cardinal orientation.",
                    "reward_xp": 200,
                    "reward_tokens": 8
                }
            ],
            "discovery_reward": {"xp": 75, "tokens": 5}
        },
        {
            "id": "drainage_system",
            "name": "Drainage System",
            "subtitle": "Subterranean Corbelled Sewer Network",
            "site": "Harappa & Mohenjo-daro",
            "zone": "Lower Town",
            "icon": "🚰",
            "level_required": 1,
            "status": "unlocked",
            "coordinates": {"x": 58, "y": 72},
            "historical_explanation": "The crowning achievement of Harappan civil engineering was its subterranean drainage network—unrivaled worldwide until the 19th century! Paved household bathrooms discharged wastewater through vertical terracotta chutes embedded inside exterior walls into covered street channels. Channels were built with corbelled brick arches, gentle hydraulic gradients, and removable limestone slabs for inspection and municipal cleaning.",
            "interactive_objects": [
                {
                    "id": "obj_corbelled_arch",
                    "name": "Corbelled Brick Sewer Arch",
                    "icon": "🏛️",
                    "category": "Hydraulic Engineering",
                    "description": "Inverted V-shaped corbelled brick vault engineered to withstand heavy street cart traffic while allowing rapid storm runoff flow.",
                    "archaeological_fact": "Main sewer trunks were deep enough for a human municipal inspector to stand inside.",
                    "xp_reward": 40
                },
                {
                    "id": "obj_inspection_slab",
                    "name": "Limestone Inspection Slab",
                    "icon": "🪨",
                    "category": "Sanitation Maintenance",
                    "description": "Heavy dressing limestone cover fitted over street drains. Workers lifted these slabs at regular intervals to remove accumulated silt and debris.",
                    "archaeological_fact": "Demonstrates municipal civic administration and regular maintenance schedules.",
                    "xp_reward": 45
                },
                {
                    "id": "obj_soak_pit_jar",
                    "name": "Perforated Sump Sediment Jar",
                    "icon": "🧪",
                    "category": "Water Filtration",
                    "description": "Large porous terracotta vessel placed at drain junctions to catch heavy sediment while permitting filtered wastewater to percolate safely into the ground.",
                    "archaeological_fact": "Prevents urban sewage pooling and waterborne diseases.",
                    "xp_reward": 45
                }
            ],
            "quests": [
                {
                    "id": "quest_hydraulic_flow",
                    "title": "Drainage Flow Restoration",
                    "description": "Clear the silted inspection manhole to restore subterranean flow from the residential bathroom to the soak pit.",
                    "reward_xp": 250,
                    "reward_tokens": 10
                }
            ],
            "discovery_reward": {"xp": 75, "tokens": 5}
        },
        {
            "id": "great_bath",
            "name": "Great Bath",
            "subtitle": "The Bitumen-Sealed Ritual Pool",
            "site": "Mohenjo-daro",
            "zone": "Citadel",
            "icon": "🏊",
            "level_required": 1,
            "status": "unlocked",
            "coordinates": {"x": 28, "y": 36},
            "historical_explanation": "Located on the fortified Western Citadel mound, the Great Bath is a monumental 12 × 7 meter brick basin descending 2.4 meters via broad brick staircases at north and south. The basin was made completely watertight using finely dressed bricks laid in gypsum mortar and sealed behind a 3-centimeter thick backing of natural bitumen (asphalt)—the earliest known synthetic waterproofing in the world.",
            "interactive_objects": [
                {
                    "id": "obj_bitumen_seam",
                    "name": "Natural Bitumen Waterproofing Seam",
                    "icon": "🛡️",
                    "category": "Ancient Material Science",
                    "description": "Intact layer of natural petroleum pitch (bitumen) applied between outer and inner brick skins to guarantee complete water impermeability.",
                    "archaeological_fact": "Bitumen was imported from Baluchistan or Mesopotamian tar pits.",
                    "xp_reward": 50
                },
                {
                    "id": "obj_bath_stairs",
                    "name": "Stepped Brick Staircase",
                    "icon": "🪜",
                    "category": "Sacred Architecture",
                    "description": "Carefully angled brick stairways leading bathers down into the ritual basin, originally fitted with timber treads.",
                    "archaeological_fact": "Surrounded by a pillared veranda and eight private changing rooms with drain outlets.",
                    "xp_reward": 40
                },
                {
                    "id": "obj_drain_culvert",
                    "name": "Corbelled Vaulted Drain Outlet",
                    "icon": "🌊",
                    "category": "Hydraulic Culvert",
                    "description": "Massive arched culvert measuring 1.8 meters high that emptied the entire 160,000-liter pool into the western slope of the mound.",
                    "archaeological_fact": "Allowed the Great Bath to be completely drained and refilled with fresh well water.",
                    "xp_reward": 45
                }
            ],
            "quests": [
                {
                    "id": "quest_ritual_purification",
                    "title": "Secrets of the Great Bath",
                    "description": "Investigate the bitumen sealing layer and discover how ancient engineers filled and drained the pool.",
                    "reward_xp": 260,
                    "reward_tokens": 10
                }
            ],
            "discovery_reward": {"xp": 80, "tokens": 6}
        },
        {
            "id": "granary_area",
            "name": "Storage/Granary Area",
            "subtitle": "State Grain Reserve & Threshing Platforms",
            "site": "Harappa & Mohenjo-daro",
            "zone": "Citadel",
            "icon": "🌾",
            "level_required": 1,
            "status": "unlocked",
            "coordinates": {"x": 22, "y": 20},
            "historical_explanation": "Perched on the citadel edge near river loading docks, the Great Granary was a massive brick podium measuring over 50 meters in length. It was divided into 12 storage halls separated by air circulation flues beneath timber platforms, keeping harvested grain cool and dry from humid river fogs. Nearby circular brick threshing floors allowed central workers to pound wheat and barley.",
            "interactive_objects": [
                {
                    "id": "obj_barley_grains",
                    "name": "Carbonized Six-Row Barley & Wheat",
                    "icon": "🌾",
                    "category": "Botanical Remains",
                    "description": "Charred cereal grains of six-row barley (Hordeum vulgare) and emmer wheat preserved in subterranean storage pits for over 4 millennia.",
                    "archaeological_fact": "Botanical analysis proves massive agricultural yields along the fertile Indus silt.",
                    "xp_reward": 40
                },
                {
                    "id": "obj_air_flue",
                    "name": "Underfloor Air Ventilation Flue",
                    "icon": "🌬️",
                    "category": "Food Preservation Engineering",
                    "description": "Raised sleeper walls creating continuous airflow beneath grain floors to prevent mildew, dampness, and insect infestation.",
                    "archaeological_fact": "Architectural principle identical to modern grain silos.",
                    "xp_reward": 45
                },
                {
                    "id": "obj_threshing_floor",
                    "name": "Circular Brick Threshing Platform",
                    "icon": "⭕",
                    "category": "Agricultural Processing",
                    "description": "Concentric circle brick pavement with a central hollow for a heavy wooden mortar pestle, where laborers threshed grain stalks.",
                    "archaeological_fact": "Found in neat rows north of the Citadel at Harappa.",
                    "xp_reward": 45
                }
            ],
            "quests": [
                {
                    "id": "quest_granary_security",
                    "title": "The Granary Ventilation Audit",
                    "description": "Inspect the air flues and verify grain storage capacity to protect the metropolis against monsoon droughts.",
                    "reward_xp": 220,
                    "reward_tokens": 8
                }
            ],
            "discovery_reward": {"xp": 75, "tokens": 5}
        },
        {
            "id": "marketplace",
            "name": "Marketplace",
            "subtitle": "The Commercial Bazaar & Seal Weighing Hub",
            "site": "Mohenjo-daro & Lothal",
            "zone": "Lower Town",
            "icon": "🏪",
            "level_required": 1,
            "status": "unlocked",
            "coordinates": {"x": 45, "y": 68},
            "historical_explanation": "The bustling economic nerve center of the city. Here, farmers, craftspeople, and international merchants exchanged agricultural surplus for marine shells, lapis lazuli, turquoise, and copper. Transactions were regulated by municipal weights made of cut chert cubes, and trade consignments were secured by wet clay tags stamped with steatite intaglio seals.",
            "interactive_objects": [
                {
                    "id": "obj_chert_weights",
                    "name": "Set of Cubical Chert Weights",
                    "icon": "⚖️",
                    "category": "Metrology & Commerce",
                    "description": "Cube-shaped weights of dense, polished grey chert stone following binary progression: 1, 2, 4, 8, 16, 32, 64 (where 1 unit = 0.857 grams).",
                    "archaeological_fact": "Standardized across the entire civilization with an accuracy margin below 1%.",
                    "xp_reward": 50
                },
                {
                    "id": "obj_unicorn_seal",
                    "name": "Steatite Unicorn Stamp Seal",
                    "icon": "🪙",
                    "category": "Trade Identification Seal",
                    "description": "Square steatite stamp seal depicting the sacred mythical unicorn before an incense brazier, surmounted by 5 pictographic script characters.",
                    "archaeological_fact": "Most common seal motif, used by trade guilds to authenticate merchant packages.",
                    "xp_reward": 55
                },
                {
                    "id": "obj_shell_bangles",
                    "name": "Turbinella Pyrum Shell Bangles",
                    "icon": "🐚",
                    "category": "Coastal Luxury Good",
                    "description": "Polished conch bangles carved from sea shells gathered in the Gulf of Kutch, prized by citizens across northern cities.",
                    "archaeological_fact": "Traded inland up to 1,500 km away from coastal waters.",
                    "xp_reward": 40
                }
            ],
            "quests": [
                {
                    "id": "quest_merchant_balance",
                    "title": "The Master of Weights",
                    "description": "Calibrate the chert balance scales against 16-unit weights to verify an incoming copper merchant shipment.",
                    "reward_xp": 240,
                    "reward_tokens": 10
                }
            ],
            "discovery_reward": {"xp": 80, "tokens": 6}
        },
        {
            "id": "craft_workshop",
            "name": "Craft Workshop",
            "subtitle": "Bead Kilns & Lost-Wax Bronze Metallurgy",
            "site": "Lothal & Chanhudaro",
            "zone": "Lower Town",
            "icon": "⚒️",
            "level_required": 1,
            "status": "unlocked",
            "coordinates": {"x": 78, "y": 42},
            "historical_explanation": "Harappan specialized workshops operated with industrial precision. At bead factories, craftsmen used microscopic diamond-tipped drills (chert stone drills) to perforate hard carnelian stones and fired them in multi-stage kilns to achieve vibrant crimson hues. Metallurgists cast copper and tin bronze into tools, weapons, and sculptures using the complex lost-wax technique.",
            "interactive_objects": [
                {
                    "id": "obj_carnelian_bead",
                    "name": "Etched Carnelian Barrel Bead",
                    "icon": "💎",
                    "category": "Lapidary Art",
                    "description": "Crimson carnelian stone drilled with microscopic axial holes and chemically etched with white alkali wave designs.",
                    "archaeological_fact": "High-value export prized by royal courts in Ur (Mesopotamia) and Dilmun.",
                    "xp_reward": 50
                },
                {
                    "id": "obj_bronze_crucible",
                    "name": "Lost-Wax Casting Crucible & Mold",
                    "icon": "💃",
                    "category": "High Bronze Metallurgy",
                    "description": "Refractory clay crucible and beeswax mold used to cast bronze masterpieces like the world-famous 'Dancing Girl of Mohenjo-daro'.",
                    "archaeological_fact": "Shows advanced knowledge of copper-tin-arsenic alloying.",
                    "xp_reward": 55
                },
                {
                    "id": "obj_pottery_wheel",
                    "name": "Artisan Terracotta Pottery Wheel",
                    "icon": "🏺",
                    "category": "Ceramic Production",
                    "description": "Heavy clay foot-wheel used to throw thin-walled, high-tensile earthenware vessels with glazed black-on-red floral motifs.",
                    "archaeological_fact": "Consistent firing temperatures above 1,000°C achieved in Harappan kilns.",
                    "xp_reward": 45
                }
            ],
            "quests": [
                {
                    "id": "quest_lost_wax_casting",
                    "title": "Master of the Lost Wax",
                    "description": "Prepare the beeswax figurine and heat the bronze crucible to cast an ancient statuette.",
                    "reward_xp": 250,
                    "reward_tokens": 10
                }
            ],
            "discovery_reward": {"xp": 80, "tokens": 6}
        }
    ]

