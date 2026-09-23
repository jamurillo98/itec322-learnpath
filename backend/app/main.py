from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.recommend import router as recommend_router

app = FastAPI(
    title="Rule-Based Learning Resource Recommendation API",
    description=(
        "Validated recommendations backed by the canonical deterministic "
        "rule engine in data/rule_engine.py."
    ),
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recommend_router, prefix="/api")


@app.get(
    "/api/health",
    summary="Check API health",
    response_description="Current API status",
)
async def health_check():
    """Simple health endpoint for frontend and local verification."""
    return {"status": "ok", "message": "Backend is running"}
