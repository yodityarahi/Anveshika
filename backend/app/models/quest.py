from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ArtifactReward(BaseModel):
    id: str
    name: str
    icon: str
    material: str
    origin: str
    importance: str

class QuestChallenge(BaseModel):
    type: str  # rebuild_city | artifact_detective | drainage_flow | trade_network | daily_life_simulation
    instructions: str
    interactive_data: Dict[str, Any]
    hints: Optional[List[str]] = []

class QuestModel(BaseModel):
    quest_id: str
    title: str
    civilization_id: str = "ivc"
    story_context: str
    location: str
    objective: str
    difficulty: str  # Beginner | Intermediate | Advanced
    learning_concept: str
    npc_name: str
    npc_avatar: str = "🧑‍🏫"
    challenge: QuestChallenge
    solution: Any
    reward_xp: int
    reward_tokens: int
    artifact_reward: Optional[ArtifactReward] = None
    badge_reward: Optional[str] = None

class QuestSummary(BaseModel):
    quest_id: str
    title: str
    civilization_id: str
    story_context: str
    location: str
    objective: str
    difficulty: str
    learning_concept: str
    npc_name: str
    npc_avatar: str
    reward_xp: int
    reward_tokens: int
    artifact_reward: Optional[ArtifactReward] = None
    badge_reward: Optional[str] = None
    completed: bool = False

class QuestSubmitRequest(BaseModel):
    username: str
    submission: Dict[str, Any]
    time_taken_seconds: Optional[float] = 30.0
    attempts_count: Optional[int] = 1
    hints_used: Optional[int] = 0

class QuestSubmitResponse(BaseModel):
    success: bool
    is_correct: bool
    feedback: str
    xp_awarded: int = 0
    tokens_awarded: int = 0
    quest_id: str
    artifact_unlocked: Optional[ArtifactReward] = None
    badge_unlocked: Optional[str] = None
    completed_quests_count: int = 0
