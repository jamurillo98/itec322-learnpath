"""FastAPI entry point for the Vercel backend service.

What goes inside:
- API routes exposed by the backend service
- Request validation and calls to the rule engine
"""
import os
import sys
from typing import Any, Dict

from fastapi import FastAPI
from pydantic import BaseModel, Field

# Vercel runs this file from the backend service root; local runs use the repo root.
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from data.rule_engine import RuleEngine


app = FastAPI(title="Rule-based Recommendation Engine API")


class RecommendRequest(BaseModel):
    """Request body for the recommendation endpoint."""

    query: str = Field(min_length=1)
    user_profile: Dict[str, Any] = Field(default_factory=dict)


@app.get("/health")
def health() -> Dict[str, str]:
    """Return a lightweight service health response."""
    return {"status": "ok"}


@app.post("/recommend")
def recommend(payload: RecommendRequest) -> Dict[str, Any]:
    """Return deterministic recommendations based on CSV matching rules."""
    engine = RuleEngine()
    return {
        "query": payload.query,
        "results": engine.recommend(payload.query, payload.user_profile),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
