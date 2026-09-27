from pydantic import BaseModel
from typing import Any, Dict, Optional

class PuzzleVerifyRequest(BaseModel):
    solution: Any
    solve_time_seconds: float
    hints_used: int = 0

class PuzzleVerifyResponse(BaseModel):
    success: bool
    message: str
    xp_awarded: int
    tokens_awarded: int
    next_action: Optional[str] = None
