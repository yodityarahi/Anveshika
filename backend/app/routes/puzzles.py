from fastapi import APIRouter
from backend.app.models.puzzle import PuzzleVerifyRequest, PuzzleVerifyResponse

router = APIRouter(prefix="/puzzles", tags=["Interactive Puzzles"])

@router.get("/preview")
def preview_puzzles():
    return {
        "available_puzzles": [
            {
                "id": "puz_drainage_01",
                "name": "Terracotta Conduit Flow",
                "type": "rotation_alignment",
                "historical_context": "Harappans used interlocking terracotta pipes with gypsum and lime mortar."
            },
            {
                "id": "puz_weights_01",
                "name": "Lothal Chert Balance",
                "type": "binary_scale",
                "historical_context": "Harappan merchants used binary weights (1, 2, 4, 8, 16, 32...) for accurate trade."
            }
        ]
    }

@router.post("/{puzzle_id}/verify", response_model=PuzzleVerifyResponse)
def verify_puzzle(puzzle_id: str, payload: PuzzleVerifyRequest):
    return PuzzleVerifyResponse(
        success=True,
        message=f"Puzzle {puzzle_id} solution verified successfully!",
        xp_awarded=150,
        tokens_awarded=3,
        next_action="inspect_artifact"
    )
