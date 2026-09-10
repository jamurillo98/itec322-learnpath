from fastapi import APIRouter

from app.engine import recommend_learning_resources
from app.models.request_model import LearningResourceRequest

router = APIRouter()


@router.post("/recommend")
def recommend(request: LearningResourceRequest):
    return recommend_learning_resources(
        request.subject,
        request.difficulty,
        request.max_duration_minutes,
        request.min_rating,
        request.keywords,
        request.limit,
    )
