from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.recommend import router as recommend_router

app = FastAPI(
    title="ITEC322 Backend",
    version="0.1.0",
    description="Sprint 1 backend scaffold with placeholder recommendation endpoint.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recommend_router)


@app.get("/api/health")
async def health_check():
    """Simple health endpoint for frontend and local verification."""
    return {"status": "ok", "message": "Backend is running"}
