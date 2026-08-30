from fastapi import APIRouter

from app.models.request_model import RecommendRequest

router = APIRouter(prefix="/api", tags=["recommendations"])


@router.post("/recommend")
async def create_recommendation(payload: RecommendRequest):
    """Placeholder endpoint for Sprint 1.

    This endpoint simply validates the incoming JSON payload and returns a stub
    response. Sprint 2 will add the rule-engine-based recommendation logic here.
    """
    return {
        "status": "accepted",
        "message": "Recommendation request received. Sprint 2 will add rule evaluation and recommendation generation.",
        "request": payload.model_dump(),
        "recommendations": [],
    }
