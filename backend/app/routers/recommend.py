from fastapi import APIRouter

from ..engine import recommend_learning_resources
from ..models.request_model import LearningResourceRequest

router = APIRouter()


@router.post("/recommend")
def recommend(request: LearningResourceRequest):
    return {
        "recommendations": recommend_learning_resources(
            request.subject,
            request.difficulty,
            request.max_duration_minutes,
            request.min_rating,
            request.keywords,
            request.limit,
        )
    }
