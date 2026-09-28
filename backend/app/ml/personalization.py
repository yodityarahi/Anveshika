"""
=================================================================
ANVESHIKA - PHASE 9: AI/ML PERSONALIZATION ENGINE
Scikit-Learn Powered Quest Recommender, Adaptive Difficulty Classifier,
and Explainable Learning Progress Analyzer.
Includes robust pure-Python fallbacks for serverless deployments.
=================================================================
"""

import math
from typing import List, Dict, Any, Optional

try:
    import numpy as np
    from sklearn.neighbors import NearestNeighbors
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.preprocessing import StandardScaler
    HAS_SKLEARN = True
except Exception:
    HAS_SKLEARN = False

PROTOTYPE_DISCLAIMER = (
    "Experimental prototype personalization system powered by Scikit-Learn & Educational ML models. "
    "Designed to adaptively personalize heritage quests and difficulty based on student interaction telemetry."
)

# -------------------------------------------------------------
# 1. QUEST RECOMMENDER (Nearest Neighbors & Content Matching)
# -------------------------------------------------------------
QUEST_CATALOG_METADATA = [
    {
        "quest_id": "quest_01_rebuild_city",
        "title": "Build the Ancient City",
        "difficulty": "Beginner",
        "difficulty_num": 1.0,
        "domain": "Urban Planning & Architecture",
        "domain_index": 0,
        "reward_xp": 300,
        "feature_vector": [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.30]  # [Urban, Epigraphy, Sanitation, Trade, Daily, Diff, XP/1000]
    },
    {
        "quest_id": "quest_02_lost_artifact",
        "title": "The Lost Artifact",
        "difficulty": "Intermediate",
        "difficulty_num": 2.0,
        "domain": "Epigraphy & Material Classification",
        "domain_index": 1,
        "reward_xp": 320,
        "feature_vector": [0.0, 1.0, 0.0, 0.0, 0.0, 2.0, 0.32]
    },
    {
        "quest_id": "quest_03_drainage_flow",
        "title": "The Drainage Challenge",
        "difficulty": "Intermediate",
        "difficulty_num": 2.0,
        "domain": "Hydraulic Sanitation & Engineering",
        "domain_index": 2,
        "reward_xp": 350,
        "feature_vector": [0.0, 0.0, 1.0, 0.0, 0.0, 2.0, 0.35]
    },
    {
        "quest_id": "quest_04_trade_network",
        "title": "Ancient Trade & Maritime Highway",
        "difficulty": "Intermediate",
        "difficulty_num": 2.0,
        "domain": "Maritime Commerce & Metrology",
        "domain_index": 3,
        "reward_xp": 340,
        "feature_vector": [0.0, 0.0, 0.0, 1.0, 0.0, 2.0, 0.34]
    },
    {
        "quest_id": "quest_05_daily_life",
        "title": "Life in the Indus Valley",
        "difficulty": "Advanced",
        "difficulty_num": 3.0,
        "domain": "Daily Life, Culture & Governance",
        "domain_index": 4,
        "reward_xp": 360,
        "feature_vector": [0.0, 0.0, 0.0, 0.0, 1.0, 3.0, 0.36]
    }
]

def _cosine_dist(v1: list, v2: list) -> float:
    dot = sum(a * b for a, b in zip(v1, v2))
    norm1 = math.sqrt(sum(a * a for a in v1))
    norm2 = math.sqrt(sum(b * b for b in v2))
    if norm1 == 0 or norm2 == 0:
        return 1.0
    similarity = max(-1.0, min(1.0, dot / (norm1 * norm2)))
    return 1.0 - similarity

class QuestRecommender:
    """
    Recommends suitable ancient Indus Valley quests using Scikit-Learn NearestNeighbors.
    Computes player skill vectors and finds optimal next challenges matching learning gaps.
    """
    def __init__(self):
        self.quests = QUEST_CATALOG_METADATA
        self.quest_map = {q["quest_id"]: q for q in self.quests}
        if HAS_SKLEARN:
            try:
                self.feature_matrix = np.array([q["feature_vector"] for q in self.quests])
                self.nn_model = NearestNeighbors(n_neighbors=len(self.quests), metric="cosine")
                self.nn_model.fit(self.feature_matrix)
            except Exception:
                self.nn_model = None
        else:
            self.nn_model = None

    def recommend(self, player_stats: dict) -> Dict[str, Any]:
        completed = set(player_stats.get("completed_quests", []))
        level = player_stats.get("level", 1)
        xp = player_stats.get("xp", 150)
        history = player_stats.get("quest_history", [])

        # Calculate accuracy from history
        if history:
            correct_count = sum(1 for h in history if h.get("is_correct"))
            accuracy = correct_count / len(history)
        else:
            accuracy = 0.85  # default baseline

        # If all quests completed
        if len(completed) >= len(self.quests):
            return {
                "has_recommendation": True,
                "all_completed": True,
                "recommended_quest": self.quests[4],
                "confidence_score": 0.98,
                "reason": "You have mastered all 5 core Harappan quests! Replay 'Life in the Indus Valley' to explore alternate historical daily choices.",
                "algorithm": "Content-Based Vector Cosine Similarity (Scikit-Learn NearestNeighbors)",
                "prototype_disclaimer": PROTOTYPE_DISCLAIMER
            }

        # Find uncompleted candidate quests
        uncompleted = [q for q in self.quests if q["quest_id"] not in completed]

        # Target difficulty based on level and accuracy
        if accuracy >= 0.85 and level >= 3:
            target_diff = 3.0
        elif accuracy >= 0.65 or level >= 2:
            target_diff = 2.0
        else:
            target_diff = 1.0

        # Construct player target preference vector
        target_list = [
            0.2, 0.2, 0.2, 0.2, 0.2,
            target_diff,
            min(1.0, xp / 2000.0)
        ]

        best_candidate = None
        best_score = 0.80

        if self.nn_model is not None and HAS_SKLEARN:
            try:
                target_vector = np.array(target_list).reshape(1, -1)
                distances, indices = self.nn_model.kneighbors(target_vector)
                for dist, idx in zip(distances[0], indices[0]):
                    candidate = self.quests[idx]
                    if candidate["quest_id"] not in completed:
                        best_candidate = candidate
                        best_score = round(max(0.5, 1.0 - float(dist)), 2)
                        break
            except Exception:
                best_candidate = None

        # Fallback pure-Python cosine distance
        if not best_candidate:
            scored = []
            for q in self.quests:
                if q["quest_id"] not in completed:
                    dist = _cosine_dist(target_list, q["feature_vector"])
                    scored.append((dist, q))
            if scored:
                scored.sort(key=lambda x: x[0])
                best_score = round(max(0.5, 1.0 - scored[0][0]), 2)
                best_candidate = scored[0][1]

        if not best_candidate:
            best_candidate = uncompleted[0]

        # Generate explainable educational rationale
        reasons = {
            "quest_01_rebuild_city": "Recommended as your foundational quest to master cardinal 90° urban avenues and Harappan zoning.",
            "quest_02_lost_artifact": "Recommended to develop forensic epigraphy skills through steatite talc mineralogy and unicorn intaglio clues.",
            "quest_03_drainage_flow": "Your architectural progress shows readiness for subterranean hydraulic engineering and public hygiene systems.",
            "quest_04_trade_network": "Matches your growing commerce interests—explore international shipping from Lothal dockyards to Mesopotamia.",
            "quest_05_daily_life": "Advanced immersion quest analyzing domestic nutrition, beadcraft kilns, and peaceful civic consensus."
        }
        reason = reasons.get(best_candidate["quest_id"], "Optimal match for your current level and archaeological learning pace.")

        return {
            "has_recommendation": True,
            "all_completed": False,
            "recommended_quest_id": best_candidate["quest_id"],
            "title": best_candidate["title"],
            "difficulty": best_candidate["difficulty"],
            "domain": best_candidate["domain"],
            "reward_xp": best_candidate["reward_xp"],
            "confidence_score": best_score,
            "reason": reason,
            "algorithm": "Content-Based Vector Cosine Similarity (Scikit-Learn NearestNeighbors)",
            "prototype_disclaimer": PROTOTYPE_DISCLAIMER
        }


# -------------------------------------------------------------
# 2. ADAPTIVE DIFFICULTY CLASSIFIER (Decision Tree)
# -------------------------------------------------------------
class DifficultyClassifier:
    """
    Classifies player skill and dynamically adapts puzzle parameters:
    - Easy: Extended time, extra pedagogical hints, safety net.
    - Medium: Standard timing, baseline hints, balanced rewards.
    - Hard: Reduced time, single-attempt bonus, +50% Steatite Seal rewards.
    """
    def __init__(self):
        self.labels = ["Easy", "Medium", "Hard"]
        if HAS_SKLEARN:
            try:
                self.clf = DecisionTreeClassifier(max_depth=4, random_state=42)
                self.scaler = StandardScaler()
                self._train_prototype_model()
            except Exception:
                self.clf = None
        else:
            self.clf = None

    def _train_prototype_model(self):
        np.random.seed(42)
        X = []
        y = []

        # High performers -> "Hard" (class 2)
        for _ in range(40):
            acc = np.random.uniform(0.85, 1.0)
            time_sec = np.random.uniform(15.0, 35.0)
            attempts = np.random.uniform(1.0, 1.2)
            lvl = np.random.randint(2, 6)
            hints = np.random.choice([0, 1], p=[0.85, 0.15])
            X.append([acc, time_sec, attempts, lvl, hints])
            y.append(2)

        # Moderate performers -> "Medium" (class 1)
        for _ in range(40):
            acc = np.random.uniform(0.60, 0.84)
            time_sec = np.random.uniform(35.0, 85.0)
            attempts = np.random.uniform(1.2, 2.2)
            lvl = np.random.randint(1, 4)
            hints = np.random.choice([0, 1, 2], p=[0.3, 0.5, 0.2])
            X.append([acc, time_sec, attempts, lvl, hints])
            y.append(1)

        # Struggling performers -> "Easy" (class 0)
        for _ in range(40):
            acc = np.random.uniform(0.20, 0.59)
            time_sec = np.random.uniform(70.0, 150.0)
            attempts = np.random.uniform(2.0, 4.0)
            lvl = np.random.randint(1, 3)
            hints = np.random.choice([1, 2, 3], p=[0.2, 0.4, 0.4])
            X.append([acc, time_sec, attempts, lvl, hints])
            y.append(0)

        X = np.array(X)
        y = np.array(y)
        self.scaler.fit(X)
        X_scaled = self.scaler.transform(X)
        self.clf.fit(X_scaled, y)

    def classify(self, telemetry: dict) -> Dict[str, Any]:
        acc = float(telemetry.get("accuracy_rate", 0.80))
        time_sec = float(telemetry.get("avg_solve_time", 45.0))
        attempts = float(telemetry.get("attempts_per_quest", 1.2))
        level = int(telemetry.get("player_level", 1))
        hints = int(telemetry.get("hints_used", 0))

        confidence = 0.88
        if self.clf is not None and HAS_SKLEARN:
            try:
                feat = np.array([[acc, time_sec, attempts, level, hints]])
                feat_scaled = self.scaler.transform(feat)
                pred_idx = int(self.clf.predict(feat_scaled)[0])
                probabilities = self.clf.predict_proba(feat_scaled)[0]
                confidence = round(float(probabilities[pred_idx]), 2)
                recommended_tier = self.labels[pred_idx]
            except Exception:
                pred_idx = self._rule_based_classify(acc, time_sec, attempts, level)
                recommended_tier = self.labels[pred_idx]
        else:
            pred_idx = self._rule_based_classify(acc, time_sec, attempts, level)
            recommended_tier = self.labels[pred_idx]

        factors = [
            f"Solve Accuracy: {round(acc * 100, 1)}%",
            f"Avg Time: {round(time_sec, 1)}s",
            f"Avg Attempts: {round(attempts, 1)}"
        ]
        if hints > 0:
            factors.append(f"Hints Consulted: {hints}")

        tier_config = {
            "Easy": {
                "badge_color": "#2DD4BF",
                "tag": "Assisted Exploration",
                "time_limit_sec": 180,
                "hints_allowed": 3,
                "bonus_seals": 0,
                "guidance": "Enhanced pedagogical hints enabled. Take your time inspecting archaeological evidence!"
            },
            "Medium": {
                "badge_color": "#D4AF37",
                "tag": "Standard Field Excavation",
                "time_limit_sec": 120,
                "hints_allowed": 2,
                "bonus_seals": 2,
                "guidance": "Balanced challenge reflecting authentic Harappan archaeological problem solving."
            },
            "Hard": {
                "badge_color": "#E05638",
                "tag": "Master Epigraphist Mode",
                "time_limit_sec": 75,
                "hints_allowed": 1,
                "bonus_seals": 5,
                "guidance": "High-velocity challenge. Single-attempt bonus with +5 Steatite Seals reward!"
            }
        }

        return {
            "recommended_difficulty": recommended_tier,
            "confidence_score": confidence,
            "decision_factors": factors,
            "tier_settings": tier_config[recommended_tier],
            "algorithm": "Decision Tree Classifier (Scikit-Learn)",
            "prototype_disclaimer": PROTOTYPE_DISCLAIMER
        }

    def _rule_based_classify(self, acc: float, time_sec: float, attempts: float, level: int) -> int:
        if acc >= 0.85 and time_sec <= 40.0 and attempts <= 1.3:
            return 2  # Hard
        elif acc >= 0.60 and time_sec <= 90.0:
            return 1  # Medium
        return 0  # Easy


# -------------------------------------------------------------
# 3. LEARNING PROGRESS ANALYZER (Knowledge Matrix)
# -------------------------------------------------------------
class LearningProgressAnalyzer:
    """
    Synthesizes learner telemetry into a multi-pillar Harappan Knowledge Matrix.
    Computes mastery percentages across 5 core heritage domains.
    """
    DOMAINS = [
        {
            "id": "urban_planning",
            "name": "Urban Planning & Architecture",
            "icon": "📐",
            "description": "Grid-iron streets, 1:2:4 burnt brick ratios, citadel mounds, and cardinal avenues.",
            "associated_quests": ["quest_01_rebuild_city"]
        },
        {
            "id": "epigraphy_material",
            "name": "Epigraphy & Material Classification",
            "icon": "🏺",
            "description": "Steatite stamp seals, Indus script glyphs, micro-bead pyrotechnology, and terracotta figurines.",
            "associated_quests": ["quest_02_lost_artifact"]
        },
        {
            "id": "hydraulic_engineering",
            "name": "Hydraulic Sanitation & Engineering",
            "icon": "🚰",
            "description": "Covered brick sewers, courtyard soak jars, Great Bath bitumen tank, and fresh water wells.",
            "associated_quests": ["quest_03_drainage_flow"]
        },
        {
            "id": "trade_metrology",
            "name": "Maritime Commerce & Metrology",
            "icon": "⚖️",
            "description": "Binary chert cubical weights, Lothal tidal dockyard, Persian Gulf seals, and lapis lazuli routes.",
            "associated_quests": ["quest_04_trade_network"]
        },
        {
            "id": "daily_life_culture",
            "name": "Daily Life, Culture & Governance",
            "icon": "🌾",
            "description": "Barley/wheat agriculture, carnelian bead making, absence of royal palaces, and community consensus.",
            "associated_quests": ["quest_05_daily_life"]
        }
    ]

    def analyze(self, player_stats: dict) -> Dict[str, Any]:
        completed_quests = set(player_stats.get("completed_quests", []))
        discovered_artifacts = set(player_stats.get("discovered_artifacts", []))
        history = player_stats.get("quest_history", [])
        level = player_stats.get("level", 1)

        matrix = []
        overall_mastery_sum = 0

        for d in self.DOMAINS:
            # Score 1: Quest completion (40%)
            q_count = len(d["associated_quests"])
            completed_in_domain = sum(1 for q in d["associated_quests"] if q in completed_quests)
            quest_score = (completed_in_domain / q_count) * 40.0 if q_count > 0 else 0.0

            # Score 2: Telemetry accuracy in domain (40%)
            domain_history = [h for h in history if h.get("quest_id") in d["associated_quests"]]
            if domain_history:
                correct = sum(1 for h in domain_history if h.get("is_correct"))
                accuracy_score = (correct / len(domain_history)) * 40.0
            else:
                accuracy_score = 30.0 if completed_in_domain > 0 else 10.0

            # Score 3: Exploration & artifact discovery bonus (20%)
            art_bonus = min(20.0, len(discovered_artifacts) * 4.0)

            total_mastery = round(min(100.0, quest_score + accuracy_score + art_bonus), 1)
            overall_mastery_sum += total_mastery

            if total_mastery >= 80.0:
                status_tier = "Mastered"
                color = "#2DD4BF"
            elif total_mastery >= 50.0:
                status_tier = "Proficient"
                color = "#D4AF37"
            elif total_mastery >= 20.0:
                status_tier = "Apprentice"
                color = "#38BDF8"
            else:
                status_tier = "Unexplored"
                color = "#94A3B8"

            matrix.append({
                "domain_id": d["id"],
                "name": d["name"],
                "icon": d["icon"],
                "description": d["description"],
                "mastery_percentage": total_mastery,
                "status_tier": status_tier,
                "color": color,
                "quests_completed": f"{completed_in_domain}/{q_count}",
                "pedagogical_insight": self._get_pedagogical_insight(d["id"], total_mastery)
            })

        avg_mastery = round(overall_mastery_sum / len(self.DOMAINS), 1)
        top_domain = max(matrix, key=lambda x: x["mastery_percentage"]) if matrix else None
        top_strength = top_domain["name"] if top_domain else "Urban Planning & Architecture"

        return {
            "overall_knowledge_index": avg_mastery,
            "overall_knowledge_mastery": avg_mastery,
            "top_strength": top_strength,
            "mastery_tier": "Senior Harappan Scholar" if avg_mastery >= 75 else ("Archaeological Apprentice" if avg_mastery >= 40 else "Initiate Field Explorer"),
            "domains": matrix,
            "algorithm": "Multi-Criteria Pedagogical Telemetry Synthesis",
            "prototype_disclaimer": PROTOTYPE_DISCLAIMER
        }

    def _get_pedagogical_insight(self, domain_id: str, mastery: float) -> str:
        if mastery >= 80.0:
            return "Exemplary mastery demonstrated! Excellent conceptual retention of archaeological evidence."
        elif mastery >= 50.0:
            return "Solid working understanding. Review related museum vitrines to consolidate foundational epigraphy."
        elif mastery >= 20.0:
            return "Basic familiarity established. Complete the sector quest to deepen structural knowledge."
        else:
            return "Recommended for upcoming exploration. Begin with introductory site surveys."


# Singleton instances for route injection
quest_recommender = QuestRecommender()
difficulty_classifier = DifficultyClassifier()
progress_analyzer = LearningProgressAnalyzer()
