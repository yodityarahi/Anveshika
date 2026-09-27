from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class BadgeInfo(BaseModel):
    id: str
    name: str
    description: str
    icon: str
    category: str
    criteria: Optional[str] = None
    unlocked: bool = False
    unlocked_at: Optional[str] = None
    progress_current: Optional[int] = None
    progress_target: Optional[int] = None

class UserRegisterRequest(BaseModel):
    username: str = Field(..., min_length=2, max_length=30, example="Arjun")
    age: int = Field(14, ge=8, le=99, example=14)
    avatar: str = Field("🧑‍🎓", example="🧑‍🎓")
    archetype: str = Field("Town Architect", example="Town Architect")
    password: Optional[str] = Field("1234", min_length=3, max_length=50)

class UserLoginRequest(BaseModel):
    username: str = Field(..., example="Arjun")
    password: Optional[str] = Field("1234")

class UserUpdateRequest(BaseModel):
    age: Optional[int] = Field(None, ge=8, le=99)
    avatar: Optional[str] = None
    archetype: Optional[str] = None

class UserStats(BaseModel):
    xp: int = 150
    level: int = 1
    seal_tokens: int = 15
    unlocked_zones: List[str] = ["citadel_gateway", "citadel_great_bath"]
    completed_quests: List[str] = []
    badges: List[str] = ["badge_apprentice_excavator"]
    discovered_artifacts: List[str] = []
    explored_locations: List[str] = []
    unlocked_content: List[str] = ["unlock_lower_town", "unlock_common_vitrines"]
    progress_percentage: float = 0.0

class LevelProgress(BaseModel):
    current_level: int
    level_title: Optional[str] = "Apprentice Explorer"
    description: Optional[str] = None
    current_xp: int
    level_min_xp: int
    level_max_xp: int
    xp_in_level: int
    xp_needed_in_level: int
    xp_to_next_level: Optional[int] = None
    progress_percentage: float
    unlocked_perks: Optional[List[str]] = None

class UserProfileResponse(BaseModel):
    username: str
    age: int
    avatar: str
    archetype: str
    token: Optional[str] = None
    stats: UserStats
    level_progress: LevelProgress
    badges_details: List[BadgeInfo]
    overall_progress: Optional[Dict[str, Any]] = None
    unlocked_content: Optional[List[Dict[str, Any]]] = None
    created_at: str
    last_login_at: Optional[str] = None