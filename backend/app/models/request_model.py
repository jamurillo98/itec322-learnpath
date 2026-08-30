from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict


class RecommendRequest(BaseModel):
    """Request payload for the recommendation endpoint.

    Sprint 1 only validates the accepted request shape. The business rule logic for
    calculating recommendations will be implemented in Sprint 2.
    """

    model_config = ConfigDict(extra="forbid")

    project_type: str = Field(..., min_length=1, description="Type of project or use case.")
    budget: int = Field(..., ge=0, description="Available budget for the project.")
    priorities: List[str] = Field(default_factory=list, description="Priority goals for the recommendation request.")
    notes: Optional[str] = Field(default=None, description="Optional notes or context for the request.")
