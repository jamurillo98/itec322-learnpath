from typing import List, Literal

from pydantic import BaseModel, Field, StrictStr, validator


class LearningResourceRequest(BaseModel):
    subject: StrictStr
    difficulty: Literal["beginner", "intermediate", "advanced"]
    max_duration_minutes: float = Field(ge=0)
    min_rating: float = Field(ge=0, le=5)
    keywords: List[StrictStr]
    limit: int = Field(default=5, ge=1, le=50)

    @validator("subject")
    def subject_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("subject must not be empty")
        return value

    @validator("keywords")
    def keywords_must_be_strings(cls, value: List[str]) -> List[str]:
        if any(not isinstance(keyword, str) for keyword in value):
            raise TypeError("keywords must be a list of strings")
        return [keyword.strip() for keyword in value]
