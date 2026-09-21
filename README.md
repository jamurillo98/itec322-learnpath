# Rule-Based Learning Resource Recommendation Engine (TBD)

A deterministic learning-resource recommender for videos, articles, and exercises. The current Sprint 1 implementation uses a React/Vite frontend, a FastAPI backend, and one canonical rule engine in `data/rule_engine.py` backed by `data/sample_resources.csv`.

## Setup

### Backend

From the repository root:

```text
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r backend\requirements.txt
python -m pip install pytest httpx
uvicorn backend.main:app --reload
```

The API is available at `http://127.0.0.1:8000`.

### Frontend

In a second terminal:

```text
cd frontend
npm install
npm run dev
```

Vite proxies `/api` requests to the local backend. The production frontend can be built with `npm run build`.

## API

`GET /api/health` returns:

```json
{"status":"ok","message":"Backend is running"}
```

`POST /api/recommend` accepts:

```json
{
  "subject": "python",
  "difficulty": "beginner",
  "max_duration_minutes": 60,
  "min_rating": 4,
  "keywords": ["python"],
  "limit": 5
}
```

The response is deterministic and sorted by descending score, then ascending ID:

```json
{
  "recommendations": [
    {
      "id": "R001",
      "title": "Intro to Python Programming",
      "score": 8.5,
      "url": "https://example.com/r001",
      "reason": "...",
      "duration_minutes": 45,
      "rating": 4.7,
      "keywords": ["python", "coding-basics", "self-paced"]
    }
  ]
}
```

Invalid requests return FastAPI's standard HTTP 422 validation response. `subject` must be non-blank, `difficulty` must be `beginner`, `intermediate`, or `advanced`, duration must be non-negative, rating must be 0 through 5, keywords must be strings, and limit must be 1 through 50.

## Verification

```text
python -m pytest data/test_rule_engine.py tests/test_api.py -q
cd frontend
npm run build
```

The API tests use FastAPI's in-process test client and do not require Uvicorn to be running.

## Deployment and limitations

`vercel.json` contains the existing Vercel routing metadata for the frontend and `backend/main.py`; no deployment URL is recorded in the repository, so none is claimed here. The sample CSV is intentionally small, the rules are not personalized by user history, and the frontend has no authentication or persistence. Project naming remains TBD until the team records a final decision.
