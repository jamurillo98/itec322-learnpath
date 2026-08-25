# Backend (Sprint 1)

This folder contains the minimal Python FastAPI backend service for Sprint 1 and Vercel.

What goes inside:
- `main.py`: FastAPI application entry point with endpoints
- `requirements.txt`: Python dependencies

How to run (local development):

1. Create a virtual environment and activate it.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app from the repository root: `uvicorn backend.main:app --reload`

Notes:
- The backend uses a rule engine located in `/data/rule_engine.py` to generate recommendations.
- Vercel routes `/api/*` requests to this service through the root `vercel.json`.
- This is a placeholder implementation for Sprint 1.
