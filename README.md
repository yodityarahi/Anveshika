# Anveshika: Interactive Living Museum of Indian Heritage

**Smart India Hackathon (SIH) • Problem Statement: 26208**  
**Theme:** Gamified Indian Heritage Learning Platform  
**Civilization Focus:** Indus Valley Civilization (IVC / Harappan Civilization, c. 2600–1900 BCE)

---

## 🏛️ Project Overview

Anveshika transforms the textbook-based learning of ancient Indian history into an immersive, interactive living museum and quest-driven exploration game designed for students aged 10–18.

### Core Gameplay Loop
**Explore → Interact → Solve → Learn → Earn → Collect → Unlock**

---

## 🛠️ Technology Stack

* **Frontend:** HTML5, CSS3, Vanilla JavaScript (ES6+), Web Audio API (procedural synthesis)
* **Backend:** Python 3, FastAPI, Uvicorn
* **Database:** MongoDB (with automatic in-memory `mongomock` fallback for frictionless hackathon evaluation)
* **AI/ML Layer:** Scikit-Learn (Adaptive Quest Recommender, Dynamic Difficulty Adjustment, Learner Archetype Clustering)

---

## 🚀 Quick Start Guide (Local Setup)

### 1. Prerequisites
* Python 3.10+ installed
* Git

### 2. Activate Virtual Environment & Install Dependencies
```bash
# Activate existing virtual environment
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1

# Or install dependencies
pip install -r backend/requirements.txt
```

### 3. Run the Backend & Game Server
```bash
python backend/run.py
```
* The FastAPI server will start at `http://127.0.0.1:8000`
* Open `http://127.0.0.1:8000` in any web browser to play!

### 4. Direct API Health Check
Visit:
```
http://127.0.0.1:8000/api/health
```
You will receive live JSON diagnostics detailing the server and database status:
```json
{
  "status": "healthy",
  "app_name": "Anveshika: Interactive Living Museum of Indian Heritage",
  "version": "2.0.0",
  "sih_problem": "26208",
  "civilization": "Indus Valley Civilization (IVC)",
  "database": {
    "status": "healthy",
    "connected": true,
    "engine": "mongomock (In-Memory Fallback with /tmp state persistence)"
  }
}
```

---

## 📂 Project Architecture

```
Bharat_quest/
├── backend/
│   ├── app/
│   │   ├── config.py           # Application settings
│   │   ├── database.py         # PyMongo + mongomock connection manager
│   │   ├── main.py             # FastAPI app, static mounts, exception handlers
│   │   ├── models/             # Pydantic schemas (User, Quest, Artifact, Gamification, Puzzle)
│   │   ├── routes/             # REST API routers (/auth, /user, /ivc, /quests, /museum, /gamification, /ai)
│   │   └── ml/                 # Scikit-learn AI modules
│   └── run.py                  # One-command server runner
├── frontend/
│   ├── index.html              # Game HUD, Main Dashboard & Interactive Map
│   ├── css/
│   │   ├── style.css           # Ancient terracotta/sandstone color palette
│   │   ├── game-ui.css         # HUD, buttons, cards, status badges
│   │   ├── map.css             # Antique cartographic map styling & animations
│   │   ├── story.css           # Story Introduction Theater styling & animations
│   │   ├── city.css            # 2D Ancient City SVG viewport, ripples & particle styling
│   │   ├── quests.css          # Quests hub, challenge stage & forensic detective styling
│   │   ├── museum.css          # Vitrine exhibit pedestals, spotlights & curatorial styling
│   │   ├── gamification.css    # Level-up modal, badges showcase & 3-pillar progress styling
│   │   ├── ai-engine.css       # AI recommendation, difficulty badges & knowledge matrix styling
│   │   ├── final-challenge.css # Interactive dilemma carousel & graduation summary styling
│   │   └── animations-ux.css   # Phase 11: Motion design, transitions, ripples, floats & toasts
│   └── js/
│       ├── api.js              # Centralized REST API client
│       ├── audio.js            # Native procedural Web Audio sound synthesizer
│       ├── map.js              # Interactive India Map & IVC modal controller
│       ├── story.js            # 7-Scene Interactive Story Theater controller
│       ├── city.js             # 2D Interactive Ancient City controller & SVG stage
│       ├── quests.js           # Reusable Quest & Challenge controller & interactive puzzles
│       ├── museum.js           # Living Virtual Museum controller & SVG exhibit renders
│       ├── gamification.js     # Level-up modal, badges filter & mastery controller
│       ├── ai-engine.js        # AI recommendation, adaptive difficulty & ML simulation controller
│       ├── final-challenge.js  # Phase 10 Final Challenge & graduation controller
│       ├── ux-polish.js        # Phase 11: UI/UX polish manager, toasts, particles & feedback
│       └── app.js              # State manager & live backend communication
└── README.md
```

---

## 🧭 Phase 3 Feature Showcase: Dashboard & Interactive Map

1. **Main Anveshika Dashboard**:
   * **Explorer Identity**: Live Player Name, animated Avatar ring, and Specialization Archetype badge.
   * **Explorer Level & Rank**: Dynamically calculated title (from *Bronze-Age Novice* to *Harappan Legend*).
   * **XP Progress Bar**: Animated ratio bar showing current XP vs. level ceiling.
   * **Completed Quests Counter**: Live tracking of historical missions solved (out of 5).
   * **Artifacts Collected Counter**: Live tracking of excavated museum relics (out of 8).
   * **Badges of Honor Counter**: Tracking of unlocked hallmarks (out of 8).
   * **Overall Heritage Progress %**: Comprehensive metric weighted across level, quests, artifacts, and badges.

2. **Interactive National Heritage Map (Ancient India)**:
   * **Active Civilization Spotlight**: The **Indus Valley Civilization** is rendered with a pulsing golden contour and patterned terrain fill.
   * **Future Scalability Previews**: Later historical eras (Vedic Realm, Mauryan Empire, Gupta Classical Age, Imperial Chola Realm) are rendered with dashed borders and locked badges.
   * **Hydrological River Lifelines**: Vivid paths for the Indus (Sindhu), Ghaggar-Hakra (Saraswati paleochannel), Ganga, Yamuna, and Narmada.
   * **Interactive Excavation Pins**: Mohenjo-daro, Harappa, Lothal, Dholavira, Kalibangan, and Rakhigarhi with radar pulses and excavation dossiers.
   * **Contextual Hover Card**: Instant tooltip previewing civilizational hallmarks on cursor hover.

---

## 📜 Phase 4 Feature Showcase: IVC Story Introduction Theater

1. **Engaging 7-Scene Interactive Storyline**:
   * **Scene 1 (Dawn Along the Sindhu)**: Introduces the civilization's scale (>1M sq km), perennial snow-fed river cradle, and historical timeline (*c. 2600–1900 BCE Mature Harappan Phase*).
   * **Scene 2 (The Great Metropolises)**: Major urban centers (*Mohenjo-daro, Harappa, Lothal, Dholavira, Kalibangan, Rakhigarhi*) and the Citadel vs. Lower Town structure.
   * **Scene 3 (The Master Grid Planners)**: 10m wide boulevards intersecting at exact 90° right angles and the standardized mathematical **1:2:4 brick ratio**.
   * **Scene 4 (The Miracle of Public Hygiene)**: Private paved household bathrooms, vertical wall chutes, subterranean covered street sewers with inspection manholes, and the bitumen-waterproofed Great Bath.
   * **Scene 5 (Seafarers & Standard Weights)**: Lothal's tidal dockyard with sluice gates, maritime trade with ancient Sumer (Mesopotamia) as *Meluhha*, and standardized binary chert weights (1:2:4:8:16:32...).
   * **Scene 6 (Master Artisans & Enigmatic Script)**: Microscopic drilled carnelian beads, lost-wax bronze casting (*Dancing Girl*), and steatite intaglio stamp seals with 400+ undeciphered pictographic symbols.
   * **Scene 7 (Daily Life & Living Quest)**: Peaceful civilian routines, wholesome diet (barley, wheat, lentils), terracotta toys, and the call to enter the living city.

2. **Multimodal Visual & Interactive Features**:
   * **Custom Vector Illustrations (SVG)**: Rich, animated illustrations for each scene (river sunrise, twin cities, orthogonal street grid, sewer cutaway, tidal dock, artisan seals, and city portal).
   * **Progress Indicators**: Header scene counter (*Scene 1 of 7*), smooth percentage progress bar, and clickable chapter step pips.
   * **Flexible Controls**: "Continue Story ➔", "⬅️ Previous", "Skip to City ➔", and full keyboard support (Left/Right arrow keys & Spacebar).
   * **Historical Responsibility Callout**: Clear distinction between genuine ASI archaeological findings and gamified learning simulations on every card.
   * **City Gateway**: The final card features the grand **“🏛️ Enter the Ancient City”** button, seamlessly transitioning the explorer into the Harappan city environment with ancient gong acoustics.

---

## 🏛️ Phase 5 Feature Showcase: Interactive Indus Valley Ancient City

1. **Pure Web-Standards 2D Interactive Metropolis**:
   * Built strictly using semantic **HTML5**, **CSS3 Keyframe Animations**, and an **SVG Vector Graphics Engine** managed by Vanilla JavaScript (`AncientCityController`).
   * Absolutely **NO Three.js**, WebGL engines, or external framework dependencies—delivers lightning-fast 60fps performance on any student device.

2. **The 7 Authentic Archaeological Sectors**:
   * **Residential Area (Lower Town)**: Multi-room courtyard houses, private terracotta bathrooms, staircase access, and domestic privacy architectures.
   * **Main Street (Lower Town)**: The 10-meter wide North-South orthogonal boulevard designed for two-way bullock cart traffic with rounded wall chamfers.
   * **Drainage System (Lower Town)**: Precision-engineered subterranean covered sewer cutaways, soak pits, sediment traps, and limestone inspection manholes.
   * **Great Bath (Citadel Mound)**: The sacred public ritual pool lined with bitumen tar sealant, gypsum mortar, cloister verandas, and dual staircase descents.
   * **Storage/Granary Area (Citadel)**: 12 brick granary storage blocks mounted on raised sleeper walls with air ventilation flues and circular threshing floors.
   * **Marketplace (Lower Town)**: Commercial bazaar square with merchant stalls, chert balance weighing stations, and steatite intaglio trade seals.
   * **Craft Workshop (Lower Town)**: High-temperature bead kilns, micro-diamond drills for carnelian etching, and lost-wax bronze metallurgy crucibles.

3. **Gamified Exploration & Archaeological Inspection**:
   * **Exploration Discovery Rewards**: First visit to any sector awards **+75–80 XP** and **+5–6 Steatite Seals**, accompanied by fanfare audio, floating XP particle animations, and a discovery toast banner.
   * **Relic Inspector Drawer/Modal**: Displays verified Archaeological Survey of India (ASI) historical explanations and provenance.
   * **Inspectable Objects**: Each sector contains 3 inspectable relics with detailed archaeological facts, evidence tags, and XP inspection rewards.
   * **Related Quests Integration**: Each sector links directly to syllabus-aligned story missions and engineering challenges.
   * **Sector Filters**: Quick-filtering between *All Sectors*, *Citadel Mound*, and *Lower Town Grid*.
   * **Modular Extensibility**: Built with a clean `registerLocation()` API allowing easy registration of future excavated sites (such as Lothal dockyard or Dholavira reservoirs).

---

## 📜 Phase 6 Feature Showcase: Quest & Challenge System

1. **Reusable, Multi-Civilization Quest Architecture**:
   * Designed with a universal JSON/Pydantic schema (`quest_id`, `civilization_id`, `story_context`, `location`, `objective`, `difficulty`, `learning_concept`, `challenge`, `solution`, `reward_xp`, `reward_tokens`, `artifact_reward`, `badge_reward`).
   * Supports plugging in future civilizations (Vedic, Maurya, Gupta, Chola) with zero structural code changes.

2. **The 5 Core Interactive Archaeological Quests**:
   * **Quest 1: Rebuild the Ancient City**:
     * *Story & Location*: Lower Town & Citadel Mound with Master Surveyor Siddhu.
     * *Challenge*: Reconstruct Harappan zoning by placing Houses (courtyard dwellings on quiet alleys), Roads (10m wide 90° avenues), Drainage (subterranean brick sewers), and Public Areas (elevated Citadel).
     * *Learning Concept*: Indus Valley urban planning, cardinal alignment, and 1:2:4 mathematical proportions.
     * *Reward*: **+300 XP**, **+8 Seals**, *"Harappan Architectural Measuring Rod"*, *"Master Town Architect"* badge.
   * **Quest 2: The Lost Artifact**:
     * *Story & Location*: Artisan Quarter & Citadel Ruins with Chief Archaeologist Rao.
     * *Challenge*: Analyze 3 diagnostic forensic clues (soft metamorphic steatite talc stone, unicorn intaglio carving before an incense burner, right-to-left pictographic signs for maritime shipping bullae) to identify the Steatite Unicorn Stamp Seal.
     * *Learning Concept*: Pottery, glyptic seals, metallurgy, and material classification.
     * *Reward*: **+320 XP**, **+8 Seals**, *"Steatite Unicorn Stamp Seal"*, *"Harappan Epigraphist"* badge.
   * **Quest 3: The Drainage Challenge**:
     * *Story & Location*: Lower Town Street Drainage Grid during monsoon spate.
     * *Challenge*: Arrange the 4 chronological stages of the hydraulic sanitation pipeline: (1) Sloping bathroom floor & wall conduit -> (2) Courtyard settling sump & soak jar -> (3) Covered street collector sewer with limestone slabs -> (4) Suburban corbelled culvert & soakage pit outflow.
     * *Learning Concept*: Sanitation, gravity-flow hydraulic engineering, and public health infrastructure.
     * *Reward*: **+350 XP**, **+10 Seals**, *"Interlocking Terracotta Sewer Conduit"*, *"Hydraulic Master Engineer"* badge.
   * **Quest 4: Ancient Trade & The Maritime Highway**:
     * *Story & Location*: Lothal Tidal Dockyard & Marketplace with Port Master Kanha.
     * *Challenge*: Match 4 commodities to verified trade partners: Carnelian & Cotton -> Mesopotamia (Ur/Kish); Lapis Lazuli -> Shortugai Outpost (Badakhshan); Copper Ingot -> Khetri Mines (Rajasthan); Conch Shell Bangles -> Lothal & Gulf of Khambhat.
     * *Learning Concept*: Bronze Age commerce, international trade routes, and standardized binary metrology.
     * *Reward*: **+340 XP**, **+9 Seals**, *"Standardized Cubical Chert Weights"*, *"Grand Maritime Merchant"* badge.
   * **Quest 5: Life in the Indus Valley**:
     * *Story & Location*: Residential Courtyards, Bazaars & Fields with Resident Meera.
     * *Challenge*: Make 3 authentic choices: (1) Morning diet of barley flatbread, lentils, sesame, and dates (no New World potatoes/chillies); (2) Micro-drilling carnelian beads in Chanhudaro (Bronze Age, no iron/coal); (3) Civic governance through merchant guild consensus without standing armies or monarchies.
     * *Learning Concept*: Daily life, nutrition, egalitarian social organization, and peaceful governance.
     * *Reward*: **+360 XP**, **+10 Seals**, *"Terracotta Toy Bullock Cart"*, *"Living Heritage Sage"* badge.

3. **Server-Side Grading & Live MongoDB Persistence**:
   * Evaluated through FastAPI `POST /api/quests/{quest_id}/submit`.
   * Automatically updates player XP, level, `completed_quests`, `discovered_artifacts`, and `badges` directly into MongoDB (with seamless `mongomock` fallback).
   * Spawns celebration fanfare audio, floating XP particles, and updates HUD progress in real time.

---

## 🏺 Phase 7 Feature Showcase: Artifact Collection & Living Virtual Museum

1. **Comprehensive 8-Exhibit Curated Artifact Repository**:
   * Covers all 7 required historical categories with archaeological fidelity:
     * **1. Indus Valley Seal** (`art_unicorn_seal`): The Pashupati / Steatite Unicorn Seal — glyptic stamp seal carved with fine copper chisels and coated with glazed alkali; used on maritime trade bullae.
     * **2. Pottery** (`art_painted_pottery`): Red-and-Black Painted Terracotta Storage Jar — wheel-thrown slipped vessel adorned with intersecting circles, pipal leaves, and peacocks.
     * **3. Terracotta Figure** (`art_mother_goddess`): Mother Goddess Terracotta Figurine — hand-pinched iconic deity with a fan-shaped headdress, pellet eyes, and miniature appliquéd necklaces.
     * **4. Ancient Brick** (`art_standard_brick`): Standardized Kiln-Baked Mudbrick — mathematically calibrated 1:2:4 ratio (7 x 14 x 28 cm) ensuring structural tensile strength against seismic and flood forces.
     * **5. Tool** (`art_chert_drill`): Ernestite Chert Micro-Drill Bit — ultra-dense micro-drilling tool crafted from Rohri Hills chert, capable of boring 1mm concentric holes through hard carnelian.
     * **6. Ornament** (`art_carnelian_necklace`): Bleached Carnelian Bead Necklace — luxury prestige jewel fired in terracotta kilns with alkali juice to produce permanent white geometric lattices.
     * **7. Trade-Related Artifact** (`art_chert_weights`): Binary Chert Metrological Weight System — cubical polished chert weights following strict binary progressions (1, 2, 4, 8, 16, 32, 64) for gold, lapis lazuli, and grains.
     * **8. Bronze Metallurgy Masterpiece** (`art_dancing_girl`): The "Dancing Girl" of Mohenjo-daro — lost-wax (*cire perdue*) bronze cast capturing naturalistic poise, bangled arm, and relaxed contrapposto posture.

2. **Living Virtual Museum Experience**:
   * **Rotunda Gallery with Glass Vitrines**: Dramatic lighting with animated spotlight cones, velvet plinths, and polished brass plaques.
   * **Custom Procedural SVG Renderings**: Every single artifact features authentic, scalable 2D vector illustrations with authentic textures, shading, and symbols—zero external image dependencies.
   * **Comprehensive Curatorial Dossier Modal**:
     * Inspect button launches a high-fidelity modal detailing:
       - **Artifact Name & Classification**
       - **Historical Period & Date Range** (Mature Harappan, c. 2600–1900 BCE)
       - **Excavation Region & Provenance Site** (Mohenjo-daro, Harappa, Lothal, Chanhudaro, Rohri)
       - **Possible Functional Purpose**
       - **Historical Significance & Curatorial Analysis**
       - **Interesting Archaeological Fact**
       - **Discovery Status** (Discovered with timestamp badge / Undiscovered silhouette vitrine)
   * **Procedural Text-to-Speech Curatorial Audio Guide**: Native Web Speech synthesis providing hands-free narration of artifact histories for accessibility.
   * **Dynamic Category Filtering**: Seamlessly filter between *All Exhibits*, *Glyptic & Seals*, *Ceramics & Terracotta*, *Tools & Architecture*, *Adornment & Jewelry*, and *Weights & Trade*.

3. **Strict Duplicate-Proof Discovery Engine**:
   * Live FastAPI endpoint `POST /api/museum/discover/{artifact_id}`:
     * When discovered for the first time: awards +150 to +250 XP, adds the artifact ID to the player's MongoDB profile (`stats.discovered_artifacts`), triggers audio fanfare, and spawns floating golden particles.
     * When already discovered: returns `is_new: false`, awards **0 XP**, and safely prevents duplicate entries or XP inflation in MongoDB.
   * Seamless bidirectional integration: artifacts earned in Quests or City exploration instantly unlock their respective pedestals in the Virtual Museum.

---

## 🎖️ Phase 8 Feature Showcase: Gamification, Progression & Badges System

1. **Reasonable, Calibrated XP Rules**:
   * **Quests Solved**: **+300 to +360 XP** & **+8 to +10 Steatite Seals** (Mastery of town planning, forensic epigraphy, drainage, and maritime trade).
   * **Artifacts Excavated**: **+150 to +250 XP** (Excavating and curating authentic Harappan museum vitrine relics).
   * **Ancient City Sectors Surveyed**: **+75 XP** & **+5 Seals** (First-time physical exploration of the 7 ancient city zones with strict repeat-visit duplicate prevention).
   * **Interactive Objects Examined**: **+40 to +50 XP** (Micro-inspection of corbelled arches, limestone drain slabs, and bead drills).

2. **5-Tier Archaeological Level Progression & Unlockable Content**:
   * **Level 1 — Apprentice Explorer** (0 – 499 XP): Access to Lower Town Grid, residential alleys, introductory quests, and public museum vitrines.
   * **Level 2 — Field Archaeologist** (500 – 1,199 XP): Access to western Citadel Mound, The Great Bath, granary vaults, hydraulic sanitation challenge, and Lothal maritime trade networks.
   * **Level 3 — Master Surveyor** (1,200 – 2,199 XP): Access to Life in Indus Valley daily simulation quest, curatorial text-to-speech audio guides, and artisan craft workshops.
   * **Level 4 — Senior Epigraphist** (2,200 – 3,499 XP): Unlocks *The Harappan Secret Inscription Chamber* analyzing the 10-symbol Dholavira Signboard and undeciphered script, and qualification for the Indus Valley Expert badge.
   * **Level 5 — Living Heritage Sage** (3,500+ XP): Unlocks *Vedic Realm & Saraswati Basin Sneak Peek*, Grand Living Heritage Sage golden halo, and Master Curator Hall of Fame access.

3. **12-Medal Badges Suite with Dynamic Unlock Criteria & Progress Bars**:
   * **Artifact Hunter** (`badge_artifact_hunter`): Excavate and document at least 4 unique Indus Valley relics in the Virtual Museum.
   * **Master Planner** (`badge_master_planner`): Solve the urban grid challenge or survey the 90° First Avenue and residential quarters.
   * **Heritage Explorer** (`badge_heritage_explorer`): Survey all 7 core excavated archaeological sectors of the Harappan Metropolis.
   * **Indus Valley Expert** (`badge_indus_expert`): Attain Level 3+, solve 3+ quests, discover 5+ relics, and explore all 7 city sectors.
   * *Plus 8 thematic hallmarks*: Apprentice Excavator, Harappan Hydraulic Engineer, Indus Epigraphist & Scribe, Lothal Maritime Merchant, Lost-Wax Metallurgist, Citadel Guardian, Harappan Agronomist, and Living Heritage Sage.

4. **Transparent 3-Pillar IVC Mastery Percentage Formula**:
   $$\text{Mastery \%} = \min\left(100\%, \left[\frac{\text{Quests Completed}}{5} \times 35\%\right] + \left[\frac{\text{Relics Discovered}}{8} \times 35\%\right] + \left[\frac{\text{Sectors Surveyed}}{7} \times 30\%\right]\right)$$
   * Live dashboard widget displays an itemized 3-pillar breakdown in real time with individual progress bars and weighted contributions.

5. **Spectacular Level-Up Celebrations & Secret Lore Vault**:
   * Animated ray particle backdrop, spinning crest ring, procedural audio fanfare, and itemized unlocked perks listing.
   * Restricted archaeological archive modal for Level 4+ scholars detailing the Dholavira Signboard and 1:2:4 masonry mathematics.
---

## 🤖 Phase 9 Feature Showcase: AI/ML Personalization Engine

1. **Content-Based Quest Recommender (`NearestNeighbors` with Cosine Similarity)**:
   * **Domain Vector Space**: Quests are vectorized across 5 Harappan archaeological domains (*Urban Planning & Architecture*, *Epigraphy & Material Classification*, *Hydraulic Sanitation Engineering*, *Maritime Commerce & Metrology*, *Daily Life, Culture & Governance*) + normalized difficulty + XP reward weight.
   * **Skill Matching**: Recommender queries Scikit-Learn `NearestNeighbors(n_neighbors=5, metric="cosine")` with the player's dynamic target vector based on their level, solve accuracy, and uncompleted quests.
   * **Explainable Pedagogy**: Returns the best match along with an explainable educational reason (e.g. why a hydraulic engineering quest is recommended after mastering city street grids).
   * **Replay & Mastery Loop**: If all 5 quests are completed, gracefully provides replay recommendations with historical curiosity prompts rather than crashing.

2. **Adaptive Difficulty Classifier (`DecisionTreeClassifier`)**:
   * **Real Telemetry Signal**: Classifies player performance using 5 calibrated telemetry metrics:
     * `solve_accuracy_rate` (% of first-attempt correct answers)
     * `avg_solve_time` (seconds taken per challenge)
     * `attempts_per_quest` (average attempts before success)
     * `player_level` (current archaeological rank 1–5)
     * `hints_used` (number of hints requested)
   * **3-Tier Dynamic Adjustment**:
     * **Easy Mode (Assisted)**: Extra contextual hints, extended time limits, and foundational step-by-step guidance.
     * **Medium Mode (Standard)**: Balanced challenge reflecting authentic archaeological problem-solving.
     * **Hard Mode (Time-Pressured / Scholar)**: Zero hints, time pressure, and bonus Steatite Seals rewards.
   * **Explainable Factors**: Discloses the exact factors driving the classification directly in the dashboard UI.

3. **5-Pillar Harappan Knowledge Matrix (`LearningProgressAnalyzer`)**:
   * Analyzes player mastery across the 5 core Harappan knowledge pillars.
   * Calculates an **Overall Knowledge Index (%)**, identifies the student's **Top Strength**, and points out their **Growth Area** for targeted learning.

4. **Interactive ML Simulation Lab (Live Model Playground)**:
   * Accessible in the dedicated **AI Engine Tab** (`#tab-ai`).
   * Provides live interactive sliders for *Solve Accuracy (20–100%)*, *Average Solve Time (10–150s)*, *Attempts per Quest (1.0–4.0)*, and *Student Level (1–5)*.
   * Allows hackathon judges and educators to simulate different student personas and observe instant Scikit-Learn model classification and adaptive changes in real time.

5. **Ethical AI & Prototype Transparency**:
   * Prominently displays an educational prototype disclaimer:
     > *"Experimental prototype personalization system powered by Scikit-Learn for SIH evaluation. Continuously adapts as you solve Harappan archaeological challenges."*
   * Avoids deceptive black-box accuracy claims, prioritizing transparency, explainability, and pedagogical support.

---

## 👑 Phase 10 Feature Showcase: Final Indus Valley Civilization Challenge

1. **Interactive Municipal Governor / Master Architect Simulation**:
   * Synthesizes all 6 core historical learning pillars into an authentic decision-making trial instead of a shallow multiple-choice quiz:
     * **1. City Planning**: Resolve orthogonal cardinal grid orientation, 90° avenues aligned with prevailing winds, and the elevated western citadel for flood refuge.
     * **2. Drainage Engineering**: Construct the 3-stage hydraulic sanitation pipeline (sloping bathroom chute -> courtyard soak jar / sump -> covered street sewer with limestone maintenance slabs).
     * **3. Architecture & Materials**: Specify 1:2:4 standardized kiln-fired bricks (7 x 14 x 28 cm) with bitumen asphalt waterproofing for the Great Bath and gypsum-lime mortar.
     * **4. Trade & Metrology**: Authorize the Lothal maritime export manifest for Mesopotamia (Ur), utilizing cubical binary chert weights (1:2:4:8:16...) and steatite unicorn seals on clay bullae.
     * **5. Georesource Sourcing**: Dispatch procurement caravans along authentic Bronze Age geological corridors: Shortugai (Lapis Lazuli), Khetri (Copper), and Khambhat (Carnelian & Conch).
     * **6. Daily Life & Governance**: Resolve grain reserve allocations and municipal disputes through merchant guild consensus in the pillared assembly hall without royal monuments, standing armies, or dynastic autocracy.

2. **Responsive Procedural SVG Blueprints**:
   * Every dilemma features an interactive visual diagram (orthogonal street grid blueprint, 3-stage hydraulic flow diagram, 1:2:4 brick bond inspector, Lothal ship & balance scale, trade corridor route map, and pillared civic council hall).

3. **Comprehensive Post-Challenge Graduation Screen**:
   * Displays all required summary metrics:
     * **Final Score & Percentage** (up to 600 pts, with honorary ranks such as *"Grand Archaeological Governor of the Indus Valley"*).
     * **XP Earned** (**+500 XP** capstone bonus & level progression).
     * **Artifacts Discovered** (catalog of all excavated museum vitrine relics).
     * **Quests Completed** (checklist of all solved Harappan missions).
     * **Badges Earned** (showcase of all earned badges).
     * **Areas Explored** (survey of all 7 ancient city sectors).
     * **Comprehensive 6-Pillar Learning Summary Dossier** (key takeaways and archaeological field evidence).

4. **Capstone Achievement: "Indus Valley Explorer"**:
   * Awards the ultimate milestone badge **Indus Valley Explorer** (`badge_indus_explorer`) with a glowing animated crest.
   * Full graduation results, scores, and decision evaluations are persisted permanently directly into MongoDB.
   * Built-in **"Print / Save Official Certificate"** functionality generates a printable Certificate of Harappan Heritage Mastery.

---

## ✨ Phase 11 Feature Showcase: UI/UX & Animation Polish

1. **Fluid Page & Tab Transitions**:
   * Silky cubic-bezier (`0.2, 0.8, 0.2, 1`) tab transitions with staggered card entry (`@keyframes slideFadeUp`).
   * Eliminates abrupt screen switches for an immersive educational adventure game experience.

2. **Tactile Button & Ripple Effects**:
   * Interactive buttons feature subtle sheen sweeps on hover (`::before`), active depression feedback, and expanding radial ripple waves (`@keyframes rippleAnimation`).

3. **Floating XP Gain Particles & HUD Surge**:
   * Anytime XP is earned (quests, relics, sectors, inspections), a dynamic floating badge drifts upward (`@keyframes floatXpGain`) accompanied by an electric pulse on the HUD XP bar (`@keyframes xpBarFlash`) and audio chime.

4. **Celebration Suites (Level-Up & Badge Unlock)**:
   * Level-Up triggers a springy modal banner pop (`@keyframes levelUpPop`), rotating celestial sunburst rays (`@keyframes spinSunburst`), and golden confetti particle cascades (`@keyframes sparkleExplode`).
   * Badge Unlocks showcase a 3D medal flip (`@keyframes medalFlip`) with harmonic fanfare cues.

5. **Discovery & Exploration Feedback**:
   * Relic excavations trigger glowing pedestal shimmers, victory fanfare, and vitrine auto-updates.
   * Sector surveys project animated radar beacons (`@keyframes beaconRipple`) across the 2D ancient city.

6. **Quest Completion Ancient Seal Stamp**:
   * Solving archaeological challenges stamps the parchment with an authentic rotating Harappan terracotta seal impression (`@keyframes sealStampDrop`).

7. **Ancient Sandstone Toast Notification System**:
   * Non-blocking sliding notifications (`@keyframes toastSlideIn` & `toastSlideOut`) with animated countdown timer bars (`toastCountdown`) and procedural audio feedback.

8. **Loading, Skeleton & Error States**:
   * Terracotta skeleton shimmering gradient sweep (`@keyframes ancientSkeletonSweep`) during network fetches.
   * Indus Harappan wheel loading spinners (`@keyframes spinnerRotate`) and tactile shake feedback (`@keyframes shakeKeyframe`) on missing inputs or validation errors.

9. **Accessibility & Responsive Design**:
   * Strictly adheres to `@media (prefers-reduced-motion: reduce)` for motion-sensitive users.
   * Enforces 44px minimum touch targets and responsive breakpoints for tablets (<768px) and mobile viewports (<480px).
   * 100% pure semantic HTML5, CSS3, and Vanilla JavaScript—no external styling frameworks.

---

## 👥 Hackathon Presentation Highlights
* **Zero Configuration Friction:** If local MongoDB Community server is not active, the system automatically falls back to `mongomock`, guaranteeing zero errors during judge evaluations.
* **Pure Web Standards:** Built strictly with semantic HTML5, CSS3 keyframe animations, and Vanilla JavaScript—no Three.js, React, or complex build tooling overhead.
* **Lightweight Performance:** 60fps rendering without heavyweight 3D or JS framework bloat.
* **Pedagogically Rigorous:** Clear separation of authentic historical archaeological facts from interactive simulation gameplay elements.