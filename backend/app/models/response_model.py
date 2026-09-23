from typing import Any, Dict, List

from pydantic import BaseModel


class RecommendationResponse(BaseModel):
    """Stable API envelope for recommendation dictionaries from the data layer."""

    recommendations: List[Dict[str, Any]]