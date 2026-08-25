# Backend (Sprint 1)

This folder contains the minimal Python FastAPI backend for Sprint 1.

What goes inside:
- `app/main.py`: FastAPI application with endpoints
- `requirements.txt`: Python dependencies

How to run (local development):

1. Create a virtual environment and activate it.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `python -m backend.app.main` or `uvicorn backend.app.main:app --reload`

Notes:
- The backend uses a rule engine located in `/data/rule_engine.py` to generate recommendations.
- This is a placeholder implementation for Sprint 1.
