from typing import List

from pydantic import BaseModel


class LearningResourceRequest(BaseModel):
    subject: str
    difficulty: str
    max_duration_minutes: int
    min_rating: float
    keywords: List[str]
    limit: int = 5
