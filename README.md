# LearnPath — A rule-based learning-resource recommendation platform for students

LearnPath is a deterministic learning-resource recommender for videos, articles, and exercises. The current Sprint 1/Sprint 2 implementation uses a React/Vite frontend, a FastAPI backend, and one canonical rule engine implemented in the `data` package.

This repository contains the backend rule engine, example data/fixtures, API routes, and a frontend UI for collecting learning preferences and rendering scored recommendations.

## Branding / Colour theme
We recommend a short-list of accessible colour themes in `docs/colour-theme-shortlist.md`. The frontend team should apply the chosen palette to the UI components and documentation (see Sprint 2 release notes in `docs/SPRINT2_RELEASE.md`).

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

Invalid requests return FastAPI's standard HTTP 422 validation response. `subject` must be non-blank, `difficulty` must be `beginner`, `intermediate`, or `advanced`, duration must be non-negative, and numeric fields must be valid numbers.

## Verification

```text
python -m pytest data/test_rule_engine.py tests/test_api.py -q
cd frontend
npm run build
```

The API tests use FastAPI's in-process test client and do not require Uvicorn to be running.

## Deployment and limitations

`vercel.json` contains the existing Vercel routing metadata for the frontend and `backend/main.py`; no deployment URL is recorded in the repository, so none is claimed here. The sample CSV is intended for local testing and demonstration only.
