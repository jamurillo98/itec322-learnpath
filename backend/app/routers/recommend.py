from fastapi import APIRouter

from ..engine import recommend_learning_resources
from ..models.request_model import LearningResourceRequest
from ..models.response_model import RecommendationResponse

router = APIRouter()


@router.post(
    "/recommend",
    response_model=RecommendationResponse,
    summary="Recommend learning resources",
    description=(
        "Validates learner preferences and delegates ranking to the canonical "
        "deterministic data-layer rule engine."
    ),
    response_description="The ranked recommendations returned by the rule engine",
)
def recommend(request: LearningResourceRequest) -> RecommendationResponse:
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
