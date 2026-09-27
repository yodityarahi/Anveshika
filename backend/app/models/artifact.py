from pydantic import BaseModel
from typing import Optional, List

class ArtifactModel(BaseModel):
    artifact_id: str
    name: str
    category: str  # seal | pottery | figurine | brick | tool | ornament | trade
    category_label: str
    civilization_id: str = "ivc"
    period: str
    region: str
    site: str
    material: str
    dimensions: str
    possible_purpose: str
    historical_significance: str
    interesting_fact: str
    icon: str
    svg_type: str
    xp_reward: int = 75
    discovered: bool = False
    discovery_date: Optional[str] = None

class ArtifactDiscoverRequest(BaseModel):
    username: str

class ArtifactDiscoverResponse(BaseModel):
    success: bool
    is_new: bool
    message: str
    xp_awarded: int
    artifact: ArtifactModel
    total_discovered: int
    collection_size: int
