"""Minimal FastAPI entrypoint for the Vercel backend service."""
from fastapi import FastAPI


app = FastAPI()


@app.get("/api/recommend")
def recommend():
    """Return a placeholder response until recommendation rules are connected."""
    return {"message": "Backend is running", "recommendations": []}
