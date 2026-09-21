# Sprint 1 Release

## Status

Sprint 1 is complete on the `fix/sprint1-completion` branch, pending review. The repository contains a working frontend-to-backend-to-rule-engine vertical slice, self-contained automated tests, a production frontend build, and CI configuration.

The project name remains **TBD**. No deployment URL is claimed because none is present in repository metadata.

## Delivered behavior

- `GET /api/health` returns a service status response.
- `POST /api/recommend` validates learning preferences and returns `{ "recommendations": [...] }`.
- Recommendation logic is implemented only in `data/rule_engine.py`; `backend/app/engine.py` is a compatibility wrapper.
- Recommendations contain `id`, `title`, `score`, `url`, and `reason`, with duration, rating, and keyword metadata when available.
- Results are deterministic, scored, and sorted by descending score followed by ascending ID.
- The frontend supports idle, loading, HTTP error, network error, invalid JSON, empty-results, and successful result states.
- `.github/workflows/ci.yml` runs backend tests and the frontend build for pushes and pull requests.

## Evidence and commands

From the repository root:

```text
python -m pytest data/test_rule_engine.py tests/test_api.py -q
```

Expected result: all rule-engine and API tests pass without starting Uvicorn.

```text
cd frontend
npm ci
npm run build
```

Expected result: Vite creates the production bundle in the ignored `frontend/dist/` directory.

For local use, start the API with `uvicorn backend.main:app --reload`, then start the frontend with `cd frontend && npm run dev`. Vite proxies `/api` to the local API.

## Repository evidence

- Canonical rules and CSV loading: `data/rule_engine.py`, `data/sample_resources.csv`
- API implementation: `backend/app/main.py`, `backend/app/routers/recommend.py`, `backend/app/models/request_model.py`
- Automated tests: `data/test_rule_engine.py`, `tests/test_api.py`
- Frontend behavior: `frontend/src/App.jsx`, `frontend/src/components/InputForm.jsx`, `frontend/src/components/Results.jsx`
- CI: `.github/workflows/ci.yml`

## Remaining limitations

The recommendation catalogue is a small sample CSV and there is no authentication, persistence, user history, or external resource verification. The Vercel configuration is retained, but deployment has not been asserted because the repository does not record a live URL. Sprint 2 may expand the dataset, UI styling, and recommendation rules without changing this documented response envelope.
