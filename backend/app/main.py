"""
Minimal FastAPI backend starter.

What goes inside:
- API endpoints for the rule-based recommendation engine
- Wiring to `data/rule_engine.py` to evaluate rules
- Input validation and simple example routes
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import sys
import os

# Make sure the repo root is on sys.path so we can import data.rule_engine
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

try:
    from data.rule_engine import RuleEngine
except Exception:
    RuleEngine = None  # placeholder if import fails in new repo


app = FastAPI(title="Rule-based Recommendation Engine - Backend")


class RecommendRequest(BaseModel):
    query: str
    user_profile: Dict[str, Any] = {}


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/recommend")
def recommend(payload: RecommendRequest):
    """Return a list of recommended resources using rule-based logic.

    This is a minimal starter that delegates to `data/rule_engine.RuleEngine` when available.
    """
    if RuleEngine is None:
        raise HTTPException(status_code=500, detail="RuleEngine not available. See backend README.")

    engine = RuleEngine()
    results = engine.recommend(query=payload.query, user_profile=payload.user_profile)
    return {"query": payload.query, "results": results}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
