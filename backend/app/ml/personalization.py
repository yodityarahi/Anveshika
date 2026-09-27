"""
=================================================================
BHARAT QUEST - PHASE 9: AI/ML PERSONALIZATION ENGINE
Scikit-Learn Powered Quest Recommender, Adaptive Difficulty Classifier,
and Explainable Learning Progress Analyzer.
=================================================================
"""

import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from typing import List, Dict, Any, Optional

PROTOTYPE_DISCLAIMER = (
    "Experimental prototype personalization system powered by Scikit-Learn. "
    "Designed to adaptively personalize heritage quests and difficulty based on initial student interaction telemetry."
)

# -------------------------------------------------------------
# 1. QUEST RECOMMENDER (Nearest Neighbors & Content Matching)
# -------------------------------------------------------------
QUEST_CATALOG_METADATA = [
    {
        "quest_id": "quest_01_rebuild_city",
        "title": "Rebuild the Ancient City",
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

class QuestRecommender:
    """
    Recommends suitable ancient Indus Valley quests using Scikit-Learn NearestNeighbors.
    Computes player skill vectors and finds optimal next challenges matching learning gaps.
    """
    def __init__(self):
        self.quests = QUEST_CATALOG_METADATA
        self.quest_map = {q["quest_id"]: q for q in self.quests}
        self.feature_matrix = np.array([q["feature_vector"] for q in self.quests])
        self.nn_model = NearestNeighbors(n_neighbors=len(self.quests), metric="cosine")
        self.nn_model.fit(self.feature_matrix)

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
        target_vector = np.array([
            0.2, 0.2, 0.2, 0.2, 0.2,
            target_diff,
            min(1.0, xp / 2000.0)
        ]).reshape(1, -1)

        # Query NearestNeighbors
        distances, indices = self.nn_model.kneighbors(target_vector)

        # Pick the nearest uncompleted quest
        best_candidate = None
        best_score = 0.75
        for dist, idx in zip(distances[0], indices[0]):
            candidate = self.quests[idx]
            if candidate["quest_id"] not in completed:
                best_candidate = candidate
                best_score = round(max(0.5, 1.0 - float(dist)), 2)
                break

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
class AdaptiveDifficultyClassifier:
    """
    Classifies a student's gameplay telemetry and recommends dynamic difficulty:
    - Easy: Extra hints, simplified clues, assisted step guides.
    - Medium: Standard balanced historical challenge.
    - Hard: Reduced time, single-attempt bonus, +50% Steatite Seal rewards.
    """
    def __init__(self):
        self.labels = ["Easy", "Medium", "Hard"]
        self.clf = DecisionTreeClassifier(max_depth=4, random_state=42)
        self.scaler = StandardScaler()
        self._train_prototype_model()

    def _train_prototype_model(self):
        # Synthetic calibrated educational training dataset (120 samples)
        # Features: [accuracy (0-1), avg_solve_time_sec, attempts_per_quest, player_level, hint_count]
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

        # Struggling or novice performers -> "Easy" (class 0)
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

        feat = np.array([[acc, time_sec, attempts, level, hints]])
        feat_scaled = self.scaler.transform(feat)
        pred_idx = int(self.clf.predict(feat_scaled)[0])
        probabilities = self.clf.predict_proba(feat_scaled)[0]
        confidence = round(float(probabilities[pred_idx]), 2)
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
                "badge_color": "#2A9D8F",
                "tag": "Assisted Exploration",
                "time_limit_sec": 180,
                "hints_allowed": 3,
                "bonus_seals": 0,
                "guidance": "Enhanced pedagogical hints enabled. Take your time inspecting archaeological evidence!"
            },
            "Medium": {
                "badge_color": "#E9C46A",
                "tag": "Standard Field Excavation",
                "time_limit_sec": 120,
                "hints_allowed": 2,
                "bonus_seals": 2,
                "guidance": "Balanced challenge reflecting authentic Harappan archaeological problem solving."
            },
            "Hard": {
                "badge_color": "#E76F51",
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


# -------------------------------------------------------------
# 3. LEARNING PROGRESS ANALYZER (Knowledge Matrix)
# -------------------------------------------------------------
class LearningProgressAnalyzer:
    """
    Synthesizes learner telemetry into a multi-pillar Harappan Knowledge Matrix.
    """
    DOMAINS = [
        {
            "id": "urban_planning",
            "name": "Urban Planning & Architecture",
            "icon": "📐",
            "quest_id": "quest_01_rebuild_city",
            "site_id": "main_street",
            "art_id": "art_standard_brick",
            "desc": "Orthogonal grid avenues, 1:2:4 burnt brick ratios, and cardinal town zoning."
        },
        {
            "id": "epigraphy",
            "name": "Epigraphy & Material Classification",
            "icon": "🦏",
            "quest_id": "quest_02_lost_artifact",
            "site_id": "residential_area",
            "art_id": "art_unicorn_seal",
            "desc": "Steatite talc mineralogy, intaglio unicorn carving, and logosyllabic seal script."
        },
        {
            "id": "sanitation",
            "name": "Hydraulic Sanitation Engineering",
            "icon": "🚰",
            "quest_id": "quest_03_drainage_flow",
            "site_id": "drainage_system",
            "art_id": "art_standard_brick",
            "desc": "Subterranean corbelled brick sewers, soak pits, and Great Bath bitumen waterproofing."
        },
        {
            "id": "trade",
            "name": "Maritime Commerce & Metrology",
            "icon": "⛵",
            "quest_id": "quest_04_trade_network",
            "site_id": "marketplace",
            "art_id": "art_chert_weights",
            "desc": "Standardized binary chert weights, Lothal tidal dock, and international Sumerian trade."
        },
        {
            "id": "daily_life",
            "name": "Daily Life, Culture & Governance",
            "icon": "🏺",
            "quest_id": "quest_05_daily_life",
            "site_id": "craft_workshop",
            "art_id": "art_mother_goddess",
            "desc": "Barley & wheat agriculture, carnelian beadcraft, and peaceful consensus governance."
        }
    ]

    def analyze(self, player_stats: dict) -> Dict[str, Any]:
        completed_quests = set(player_stats.get("completed_quests", []))
        discovered_artifacts = set(player_stats.get("discovered_artifacts", []))
        explored_locations = set(player_stats.get("explored_locations", []))

        domain_results = []
        total_score = 0

        for d in self.DOMAINS:
            score = 0
            # 50% for solving the domain quest
            if d["quest_id"] in completed_quests:
                score += 50
            # 25% for surveying the corresponding city zone
            if d["site_id"] in explored_locations:
                score += 25
            # 25% for excavating the related museum relic
            if d["art_id"] in discovered_artifacts:
                score += 25

            total_score += score

            if score >= 90:
                status = "Master Conservator"
            elif score >= 60:
                status = "Competent Explorer"
            elif score >= 25:
                status = "Developing Apprentice"
            else:
                status = "Novice Scholar"

            domain_results.append({
                "id": d["id"],
                "name": d["name"],
                "icon": d["icon"],
                "mastery_percentage": score,
                "status": status,
                "summary": d["desc"]
            })

        avg_mastery = round(total_score / len(self.DOMAINS), 1)

        # Identify strengths & growth areas
        sorted_domains = sorted(domain_results, key=lambda x: x["mastery_percentage"], reverse=True)
        top_strength = sorted_domains[0]
        growth_area = sorted_domains[-1]

        summary_text = (
            f"Demonstrating strong acumen in {top_strength['name']} ({top_strength['mastery_percentage']}% mastery). "
            f"Recommended focus area: {growth_area['name']} to unlock complete Harappan Civilization balance."
        )

        return {
            "overall_knowledge_index": avg_mastery,
            "domains": domain_results,
            "top_strength": top_strength["name"],
            "growth_area": growth_area["name"],
            "pedagogical_summary": summary_text,
            "algorithm": "Multi-Criteria Pedagogical Knowledge Tracer",
            "prototype_disclaimer": PROTOTYPE_DISCLAIMER
        }

# Global singleton instances
quest_recommender = QuestRecommender()
difficulty_classifier = AdaptiveDifficultyClassifier()
progress_analyzer = LearningProgressAnalyzer()
