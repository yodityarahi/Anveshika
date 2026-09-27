"""
=================================================================
BHARAT QUEST - PHASE 10: FINAL INDUS VALLEY CIVILIZATION CHALLENGE
Models & Archaeological Decision Data Engine
=================================================================
"""
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class DilemmaOption(BaseModel):
    id: str
    title: str
    tagline: str
    description: str
    is_correct: bool
    score_points: int = 100
    pedagogical_feedback: str

class FinalChallengeDilemma(BaseModel):
    id: str
    pillar: str
    title: str
    subtitle: str
    historical_premise: str
    archaeological_context: str
    interactive_instruction: str
    icon: str
    options: List[DilemmaOption]

class FinalChallengeSubmitRequest(BaseModel):
    username: str = Field(..., example="Arjun")
    decisions: Dict[str, str] = Field(..., example={
        "city_planning": "opt_plan_orthogonal",
        "drainage": "opt_drain_three_stage",
        "architecture": "opt_arch_standard_brick",
        "trade": "opt_trade_binary_carnelian",
        "resources": "opt_res_targeted_network",
        "daily_life": "opt_life_guild_consensus"
    })

# -------------------------------------------------------------
# 6 CORE HARAPPAN ARCHAEOLOGICAL CHALLENGE DILEMMAS
# -------------------------------------------------------------
FINAL_CHALLENGE_DILEMMAS: List[Dict[str, Any]] = [
    {
        "id": "city_planning",
        "pillar": "City Planning",
        "title": "The Orthogonal Expansion Dilemma",
        "subtitle": "Zoning & Municipal Alignment for the Lower Town",
        "icon": "📐",
        "historical_premise": "The Harappan Civic Council has commissioned you to design an expanding metropolitan ward along the floodplains of the Indus-Saraswati basin. Flash river spates and seasonal dust storms threaten unstructured growth.",
        "archaeological_context": "Harappan cities like Mohenjo-daro and Harappa pioneered the ancient world's first strict gridiron layout. Broad avenues aligned precisely North-South and East-West, allowing prevailing winds to naturally ventilate streets. The fortified Citadel sat on a high mudbrick platform to the West for flood protection, separated from residential quarters and industrial kilns.",
        "interactive_instruction": "Evaluate the urban layout blueprints. Select the municipal planning strategy that preserves authentic Harappan urbanism:",
        "options": [
            {
                "id": "opt_plan_orthogonal",
                "title": "Orthogonal Cardinal Grid with Elevated Citadel & Wind-Vented Avenues",
                "tagline": "Authentic Mature Harappan Gridiron Masterpiece",
                "description": "Align primary avenues North-South and secondary streets East-West at 90° intersections. Place the administrative Citadel on a high artificial mudbrick terrace to the West, and zone residential quarters with quiet courtyard entrances facing inner lanes.",
                "is_correct": True,
                "score_points": 100,
                "pedagogical_feedback": "Masterful! Cardinal orientation utilized the prevailing winds for natural city cooling and dust clearance, while the elevated western citadel safeguarded administrative centers and food storage from raging river floods."
            },
            {
                "id": "opt_plan_radial",
                "title": "Radial Sprawl Centered on an Autocratic Royal Palace",
                "tagline": "Mesopotamian & Medieval Monarchy Layout",
                "description": "Construct winding radial streets emanating from a central monarch's monumental palace and temple, ignoring wind flow and cardinal angles.",
                "is_correct": False,
                "score_points": 20,
                "pedagogical_feedback": "Incorrect. Harappan cities possessed neither monumental royal palaces nor autocratic monarchs. Unlike Mesopotamia, their layout was deliberately orthogonal and civic-oriented, prioritizing community sanitation and air ventilation over royal grandiosity."
            },
            {
                "id": "opt_plan_riverbank",
                "title": "Unplanned Linear Ribbon Along the Low-Lying Riverbank",
                "tagline": "Unregulated Organic Sprawl",
                "description": "Allow citizens to build residences directly on the unfortified silt banks for immediate water access without flood barriers or setback zones.",
                "is_correct": False,
                "score_points": 10,
                "pedagogical_feedback": "Disastrous! Unprotected low-lying settlements were quickly destroyed by annual Himalayan snowmelt floods. Harappans strictly built massive mudbrick embankments and raised platforms to defend against torrential inundations."
            }
        ]
    },
    {
        "id": "drainage",
        "pillar": "Drainage",
        "title": "The Hydraulic Sanitation Grid",
        "subtitle": "Courtyard-to-Street Wastewater Engineering",
        "icon": "🚰",
        "historical_premise": "Monsoon clouds are gathering. A new residential cluster with private second-storey bathrooms must be connected to the municipal drainage infrastructure without contaminating drinking wells.",
        "archaeological_context": "The Indus Valley civilization possessed the most advanced subterranean sanitation network of antiquity. Wastewater flowed through covered terracotta pipes into settling sumps where heavy sediment settled, before running into brick-lined street sewers covered with removable limestone slabs for municipal maintenance.",
        "interactive_instruction": "Construct the hydraulic drainage pipeline. Select the engineering configuration that prevents domestic backflow and public contamination:",
        "options": [
            {
                "id": "opt_drain_three_stage",
                "title": "Three-Stage Hydraulic Flow: Sloping Sump Jar -> Covered Street Sewer -> Suburban Soak Field",
                "tagline": "Gold-Standard Harappan Municipal Sanitation",
                "description": "Direct private bathroom terracotta chutes down courtyard walls into an earthenware settling jar (sump) to trap heavy solids. The liquid effluent flows into a covered street sewer with removable limestone inspection trapdoors, draining into suburban soakage pits far from freshwater wells.",
                "is_correct": True,
                "score_points": 100,
                "pedagogical_feedback": "Flawless engineering! The settling jar trapped refuse so main street sewers wouldn't clog. Removable limestone covers allowed ancient municipal sanitation workers to perform routine cleanouts—a feat unparalleled until modern Roman and Victorian engineering!"
            },
            {
                "id": "opt_drain_open_gutter",
                "title": "Open Surface Ditches Discharging Directly into Street Canals",
                "tagline": "Exposed Slum Drainage (High Disease Risk)",
                "description": "Dig open ditches along the street curbs that convey domestic wastewater and refuse exposed to open air and flies.",
                "is_correct": False,
                "score_points": 20,
                "pedagogical_feedback": "Incorrect. Harappan municipal authorities strictly prohibited open foul-water gutters. Drainage conduits were universally subterranean or brick-covered with tight tolerances to prevent pest infestation and stench."
            },
            {
                "id": "opt_drain_drinking_well",
                "title": "Deep Drain Infiltration Wells Located Inside Courtyard Kitchens",
                "tagline": "Catastrophic Aquifer Contamination",
                "description": "Bore direct vertical soak pits adjacent to the household drinking water well to absorb bathroom effluent quickly into the immediate ground.",
                "is_correct": False,
                "score_points": 10,
                "pedagogical_feedback": "Extremely dangerous! Digging wastewater sumps directly beside household drinking wells leads to cholera and waterborne pestilence. Harappans meticulously separated freshwater cylindrical wells from wastewater culverts."
            }
        ]
    },
    {
        "id": "architecture",
        "pillar": "Architecture",
        "title": "The Citadel & Great Bath Structural Masonry",
        "subtitle": "Tensile Standardization & Hydraulic Waterproofing",
        "icon": "🏛️",
        "historical_premise": "The Citadel foundation platform and the sacred ritual Great Bath basin must withstand both regional seismic tremors and constant water pressure without leaking or collapsing.",
        "archaeological_context": "Harappan civil engineers mastered dimensional standardization. Kiln-fired bricks across all cities from Gujarat to the Punjab adhered to the rigorous 1:2:4 ratio (thickness:width:length, typically 7x14x28 cm). For water containment, bricks were laid on edge in gypsum mortar and sealed with a thick waterproof layer of natural bitumen (asphalt).",
        "interactive_instruction": "Specify the architectural materials and bonding techniques for the Citadel basin and multi-storey structures:",
        "options": [
            {
                "id": "opt_arch_standard_brick",
                "title": "Standardized 1:2:4 Kiln-Baked Bricks with Bitumen Lining & Gypsum Mortar",
                "tagline": "High-Tensile Waterproof Harappan Masonry",
                "description": "Employ kiln-fired bricks manufactured to the uniform mathematical 1:2:4 ratio laid with alternating English header-and-stretcher bond. Line the Great Bath tank basin with a 3cm continuous membrane of natural bitumen (asphalt) backed by gypsum-lime plaster.",
                "is_correct": True,
                "score_points": 100,
                "pedagogical_feedback": "Perfect architectural execution! The 1:2:4 ratio ensured maximum interlocking shear strength during ground tremors, and natural bitumen produced an impermeable water seal that kept the Great Bath bone-dry behind its walls for over 4,500 years."
            },
            {
                "id": "opt_arch_sun_dried",
                "title": "Raw Sun-Dried Mudbricks Bonded with Untempered River Silt",
                "tagline": "Rapid Erosion Under Moisture",
                "description": "Build the entire water tank and exterior citadel retaining walls with unbaked sun-dried mud bricks to save fuel and kiln wood.",
                "is_correct": False,
                "score_points": 25,
                "pedagogical_feedback": "Incorrect. While sun-dried bricks were occasionally used in dry interior walls and core platforms, hydraulic structures like the Great Bath and street gutters exclusively utilized hard kiln-fired bricks to prevent dissolution under water."
            },
            {
                "id": "opt_arch_unmortared_rubble",
                "title": "Unmortared Random River Cobbles with Timber Lacing",
                "tagline": "Leaky Foundation Failure",
                "description": "Heap rounded river pebbles and loose fieldstones together without mortar or mathematical brick sizes.",
                "is_correct": False,
                "score_points": 15,
                "pedagogical_feedback": "Incorrect. Harappan architecture was defined by precision mathematics and brick standardization. Irregular unmortared cobbles would immediately leak water and collapse under soil surcharge loads."
            }
        ]
    },
    {
        "id": "trade",
        "pillar": "Trade",
        "title": "The Lothal Maritime Export Dispatch",
        "subtitle": "Overseas Metrology & Glyptic Cargo Authentication",
        "icon": "⛵",
        "historical_premise": "A high-prow wooden merchant galley is preparing to depart from the tidal basin of Lothal. The destination is the Mesopotamian port of Ur (Meluhha trade). The cargo must be authenticated and cheat-proofed.",
        "archaeological_context": "Indus merchants maintained extensive overseas trade via the Persian Gulf. Standardized binary chert weights (progressions of 1, 2, 4, 8, 16, 32, 64) ensured fraud-free valuation of luxury goods. Exported commodities included bleached carnelian beads, fine combed cotton textiles, timber, and shell ornaments, all sealed with steatite intaglio stamp seals bearing undeciphered script.",
        "interactive_instruction": "Assemble the export manifest and verification instruments for the Persian Gulf trade voyage:",
        "options": [
            {
                "id": "opt_trade_binary_carnelian",
                "title": "Binary Chert Weights + Bleached Carnelian + Combed Cotton + Steatite Seals",
                "tagline": "Authentic Bronze Age International Trade Protocol",
                "description": "Authenticate parcels of high-grade Gujarat carnelian beads, dyed cotton textiles, and ivory inlays using cubical binary chert weights (1:2:4:8:16 ratio). Affix wet clay bullae over rope knotting and stamp them with steatite unicorn seals.",
                "is_correct": True,
                "score_points": 100,
                "pedagogical_feedback": "Brilliant mercantile governance! Mesopotamian cuneiform tablets explicitly record the arrival of carnelian beads, cotton, and timber from 'Meluhha' (the Indus). The binary chert weight system provided an international standard of exchange centuries before metallic coinage."
            },
            {
                "id": "opt_trade_iron_coins",
                "title": "Iron Cutlery + Stamped Silver Coinage + Spun Silk",
                "tagline": "Severe Historical Anachronism",
                "description": "Pack crates of forged iron swords, stamped silver rupee coins, and Chinese silk robes for exchange with the Sumerians.",
                "is_correct": False,
                "score_points": 15,
                "pedagogical_feedback": "Major historical anachronism! The Indus Valley was a Bronze Age civilization—smelted iron and coined metallic currency were not invented until more than a thousand years later during the 1st millennium BCE."
            },
            {
                "id": "opt_trade_unsealed_grain",
                "title": "Loose Raw Wheat Cargo Without Seals or Standard Weights",
                "tagline": "Unregulated Bulk Shipping with No Guarantees",
                "description": "Send loose sacks of raw grain relying on informal eye estimation of weight and verbal trust with no seal imprints.",
                "is_correct": False,
                "score_points": 20,
                "pedagogical_feedback": "Incorrect. Harappan overseas merchants were famously meticulous. Long-distance sea routes required steatite seal bullae to guarantee tamper-proof security and uniform binary weights to establish exact values."
            }
        ]
    },
    {
        "id": "resources",
        "pillar": "Resources",
        "title": "The Georesource Procurement Expeditions",
        "subtitle": "Raw Material Sourcing Across Regional Geological Networks",
        "icon": "💎",
        "historical_premise": "The artisan beadcraft workshops and metallurgy foundries have depleted their raw material inventories. You must dispatch procurement caravans to authentic Bronze Age supply regions across the subcontinent.",
        "archaeological_context": "The Harappan civilization established targeted outposts and trade corridors to source rare minerals not found in the alluvial plains: Lapis Lazuli from Badakhshan (Shortugai in northern Afghanistan), Copper from the Khetri belt in Rajasthan, Carnelian and Agate from Gujarat, and Conch Shells from the coastal Gulf of Khambhat.",
        "interactive_instruction": "Design the resource expedition map matching materials to their verified historical mining sources:",
        "options": [
            {
                "id": "opt_res_targeted_network",
                "title": "Khetri (Copper) + Shortugai (Lapis Lazuli) + Khambhat (Carnelian & Conch)",
                "tagline": "Archaeologically Grounded Resource Corridor",
                "description": "Dispatch pack caravans to the Khetri mines of Rajasthan for copper ore, traverse the northern passes to Shortugai in Badakhshan for azure lapis lazuli, and collect carnelian nodules and marine conch shells from coastal Gujarat.",
                "is_correct": True,
                "score_points": 100,
                "pedagogical_feedback": "Exact geological accuracy! Excavations at Shortugai on the Oxus River confirm it was a dedicated Harappan trading colony established specifically to monopolize the prestigious Badakhshan lapis lazuli trade route."
            },
            {
                "id": "opt_res_deep_south_iron",
                "title": "Deccan Plateau (Bauxite & Iron) + Ganges Delta (White Marble)",
                "tagline": "Inaccurate Geographic Materials",
                "description": "Send mining teams south into the deep Deccan forest to dig bauxite aluminum and iron ore, and look for white marble along the Ganges delta.",
                "is_correct": False,
                "score_points": 20,
                "pedagogical_feedback": "Incorrect. Bauxite and iron were not extracted or used by the Harappans. The core Harappan civilization was centered along the Indus-Ghaggar-Hakra river system and Gujarat coast, trading with Rajasthan and Central Asia."
            },
            {
                "id": "opt_res_local_alluvium",
                "title": "Rely Only on Local River Silt Mud for All Tools and Ornaments",
                "tagline": "Isolationist Resource Stagnation",
                "description": "Refuse external procurement and attempt to fashion heavy drills, micro-tools, and blue gemstones solely from soft riverbed silt.",
                "is_correct": False,
                "score_points": 10,
                "pedagogical_feedback": "Impossible. The alluvial floodplain provided clay for terracotta and bricks, but zero metallic ores or gemstones. Harappan craft prowess depended entirely on far-reaching procurement networks for copper, chert, and minerals."
            }
        ]
    },
    {
        "id": "daily_life",
        "pillar": "Daily Life",
        "title": "Civic Harmony, Food Security & Daily Governance",
        "subtitle": "Egalitarian Consensus, Granaries & Municipal Harmony",
        "icon": "🌾",
        "historical_premise": "A dispute has arisen between grain cultivators and the artisan merchant guilds regarding the distribution of winter harvest yields and municipal market maintenance in the assembly hall.",
        "archaeological_context": "Unlike the despotic monarchies of Egypt and Mesopotamia with their massive royal tombs and war chariot reliefs, Harappan society exhibits a striking lack of military weapons, royal glorification, or slavery monuments. Evidence points to decentralized civic governance by merchant guilds and civic councils, supported by massive state granaries storing barley, wheat, lentils, and sesame.",
        "interactive_instruction": "Resolve the municipal dispute and set civic policy in accordance with authentic Harappan societal norms:",
        "options": [
            {
                "id": "opt_life_guild_consensus",
                "title": "Guild Assembly Consensus + Standardized Granary Distribution + Civic Bylaws",
                "tagline": "Egalitarian Harappan Civic Consensus",
                "description": "Convene the merchant and agricultural guilds in the Great Pillared Assembly Hall. Distribute emergency grain rations from the elevated Great Granary's ventilated storage bays based on standardized binary cubic capacities, enforcing shared hygiene and trade standards.",
                "is_correct": True,
                "score_points": 100,
                "pedagogical_feedback": "Profound historical understanding! The absence of royal monuments, warrior graves, or depictions of military conquerors suggests Harappan cities maintained social order through civic consensus, shared economic standards, and civic pride in public health."
            },
            {
                "id": "opt_life_military_crackdown",
                "title": "Deploy Royal Chariots & Imprison Guild Leaders in Dungeons",
                "tagline": "Despotic Autocracy (Contradicts Archaeology)",
                "description": "Order the king's standing army of spear-wielding guards to suppress the guilds by force and seize all private food stores for royal banquet feasts.",
                "is_correct": False,
                "score_points": 15,
                "pedagogical_feedback": "Historically false. Archaeologists have found virtually no battlefield weapons, no warrior statues, no royal guard barracks, and no prisons in Harappan cities. Their civilization flourished for over 700 years without imperial warfare."
            },
            {
                "id": "opt_life_monument_tomb",
                "title": "Construct a Massive Pyramid Tomb and Sacrifice Slaves",
                "tagline": "Egyptian Mortuary Cult Confusion",
                "description": "Order thousands of starving artisans to build a gigantic stone pyramid for the governor's afterlife and bury golden treasures with human sacrifices.",
                "is_correct": False,
                "score_points": 10,
                "pedagogical_feedback": "Completely wrong civilization! That describes Old Kingdom Egypt. Harappan burials were modest, typically in simple wooden coffins with a few terracotta pots, reflecting an egalitarian civic ethos that valued living public utilities over mortuary megalomania."
            }
        ]
    }
]

# Historical learning summary synthesis for each pillar
LEARNING_SUMMARY_SYNTHESIS: Dict[str, Dict[str, str]] = {
    "city_planning": {
        "title": "Orthogonal Urban Planning & Cardinal Zoning",
        "key_takeaway": "Harappan metropolises were the ancient world's first planned gridiron cities. Streets intersected at crisp 90° angles to channel prevailing winds for natural air conditioning. Fortified citadels stood on elevated western terraces to guard against seasonal Himalayan river inundations.",
        "archaeological_evidence": "Mohenjo-daro First Avenue (9.1m wide), Harappa Citadel Platform, Kalibangan dual-mound grid."
    },
    "drainage": {
        "title": "Subterranean Hydraulic Sanitation Engineering",
        "key_takeaway": "No ancient society rivaled the sanitation hygiene of the Indus Valley. Multi-stage gravity drainage captured bathroom wastewater into courtyard settling jars to trap solids before channeling liquid effluent through covered street sewers with removable limestone maintenance slabs.",
        "archaeological_evidence": "Mohenjo-daro street sewers, terracotta drain pipes, Dholavira stone-cut storm water reservoirs."
    },
    "architecture": {
        "title": "Standardized 1:2:4 Brick Ratio & Waterproofing",
        "key_takeaway": "Harappan masonry relied on universal mathematical calibration: kiln-baked mud bricks were produced across 1,000+ settlements in the identical 1:2:4 ratio (7 x 14 x 28 cm) for earthquake-resistant interlocking bond. The Great Bath utilized a natural bitumen asphalt membrane that remained watertight for millennia.",
        "archaeological_evidence": "The Great Bath of Mohenjo-daro, Harappan corbelled sewer arches, standardized kiln bricks."
    },
    "trade": {
        "title": "Standardized Metrology & Maritime Long-Distance Commerce",
        "key_takeaway": "Lothal operated the ancient world's first known tidal dockyard with lock gates. International trade with Mesopotamia (Meluhha) was regulated by cubical binary chert weights (1:2:4:8:16...) and tamper-evident clay bullae stamped with steatite unicorn seals.",
        "archaeological_evidence": "Lothal trapezoidal dock basin, Harappan seals discovered in Ur and Kish, binary chert weight sets."
    },
    "resources": {
        "title": "Inter-Regional Geological Sourcing Corridors",
        "key_takeaway": "Lacking local mineral ores in the river plains, Harappans established specialized distant outposts: Shortugai in Badakhshan for azure lapis lazuli, Khetri in Rajasthan for copper, and coastal Gujarat for carnelian and conch shells.",
        "archaeological_evidence": "Shortugai trading colony on the Oxus River, Khetri copper metallurgy slag, Khambhat carnelian bead kilns."
    },
    "daily_life": {
        "title": "Civic Guild Consensus, Sanitation & Egalitarian Living",
        "key_takeaway": "Harappan culture was remarkably peaceful and civic-oriented. Free from militaristic kings, human sacrifice, or despotic monuments, society was managed through merchant guild consensus, communal grain reserves, and an uncompromising civic devotion to public health and cleanliness.",
        "archaeological_evidence": "Absence of military weaponry or royal tombs, Great Granary grain ducts, uniform civilian housing."
    }
}
