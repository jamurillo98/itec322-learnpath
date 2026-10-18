# Sprint Document — LearnPath

## Project Summary
**Project name:** LearnPath
**Goal:** Deliver an end‑to‑end prototype (frontend → backend → rule engine) by Week 12.
**Current status:** Sprint 1 and Sprint 2 are complete. Sprint 3 work has been implemented and merged; most Sprint 3 deliverables are complete (data/model, backend, and frontend build verification) but one frontend verification task owned by Astraea remains outstanding. Sprint 4 will include final polish and a post‑Sprint‑3 Vercel deployment task to resolve the backend runtime configuration.
**Team size:** 6 members.
**Repo state:** `frontend/` contains the React/Vite client; `backend/` contains the FastAPI API; `data/` contains the canonical deterministic rule engine and sample CSV; `vercel.json` contains the static‑build routing metadata for the frontend and an API route to `backend/main.py` (deployment runtime for the backend requires verification).

## Team Roles and Assignments

Jerome — Backend Lead (backend, API, deployment)  
Jasim — Backend Support (tests, validation, CI)  
Nishant — Data/Model Lead (rule engine, dataset)  
Aarjan — Data/Model Support (feature engineering, tests)  
Astraea — Frontend Lead (Vite scaffold, UI)  
Maleesha — Frontend Support (styling, state)

## Timeline and Sprints
**Sprint 1:** Complete — end-to-end frontend, API, and rule-engine baseline.  
**Sprint 2 Week 6–8:** Complete — integrated recommendation workflow, expanded rule categories and scoring, validation, UI states, and approved branding.  
**Sprint 3 Week 9–10:** In progress — majority of Sprint 3 work implemented and merged into `main`. Data/model evaluation and rule tuning, backend changes, tests, and a successful frontend production build are recorded; one remaining frontend verification and accessibility review task remains.  
- Deliverables: Model tuning; caching/preprocessing; unit tests; UI polish; deployment verification (deferred to Sprint 4 for the backend runtime fix).  
**Sprint 4 Week 11–12:** Planned — final polish, deployment verification, and presentation.  
- Deliverables: Final UI; final rules or model; README and developer docs; presentation slides and demo script; Vercel backend runtime deployment and verification (pending post‑Sprint‑3).

## 🔵 Sprint 1 — Completed (Finalised)

### Sprint 1 Overview
Sprint 1 delivered the first working vertical slice of the system:  
**frontend → backend → rule engine → deployment**

**Status:** ✔ Completed and verified; see `docs/SPRINT1_RELEASE.md`.  
**Evidence:** `data/test_rule_engine.py`, `tests/test_api.py`, `.github/workflows/ci.yml`, and the frontend production build.

### Sprint 1 Completion Checklist
- ✔ Frontend scaffold built  
- ✔ FastAPI `/api/recommend` and `/api/health` endpoints implemented
- ✔ Validated request model and HTTP 422 behavior implemented
- ✔ Backend delegates to the canonical `data/rule_engine.py` implementation
- ✔ Self-contained API and rule-engine tests pass
- ✔ Frontend request, error, loading, empty, and result states implemented
- ✔ CI runs Python tests and the frontend build
- ✔ Documentation reflects the current contract and limitations
- ✔ Release notes published in `docs/SPRINT1_RELEASE.md`

## 🟦 Sprint 2 — Completed (Weeks 6–8)

### Status: ✔ Completed
Sprint 2 is complete. Its backend, data/model, frontend, validation, and
documentation deliverables are recorded in `docs/SPRINT2_RELEASE.md`.
The integrated workflow retains the documented API response envelope and
uses the canonical rule engine.

### Sprint 2 Goals
- [x] Expand rule engine with categories and score breakdowns
- [x] Integrate the backend recommendation API with the frontend
- [x] Implement loading, error, empty, and result states
- [x] Strengthen validation and schema consistency
- [x] Validate the integrated workflow and automated test suite
- [x] Update project documentation
- [x] Confirm the project name: **LearnPath**
- [x] Approve the colour theme: **Calm Teal & Navy**

### Sprint 2 Deliverables
- [x] Rule engine with multiple scoring categories and score breakdowns
- [x] `/api/recommend` integrated with the canonical rule engine
- [x] Frontend recommendation flow with loading, error, and result states
- [x] Validated API schema and documented request/response behavior
- [x] Expanded sample resources and documented example inputs
- [x] Sprint and API documentation updated
- [x] Official project name selected: **LearnPath**
- [x] Final colour theme approved and applied: **Calm Teal & Navy**

### Sprint 2 Tasks

#### Backend (Jerome & Jasim)
- [x] Improve and document `/api/recommend`
- [x] Preserve request validation and HTTP 422 behavior
- [x] Add regression/validation coverage
- [x] Integrate the canonical rule engine
- [x] Update API documentation

#### Data/Model (Nishant & Aarjan)
- [x] Add rule categories and scoring logic
- [x] Update fixtures and document example inputs
- [x] Keep recommendations aligned with learning resources

#### Frontend (Astraea & Maleesha)
- [x] Implement UI state, loading, and error handling
- [x] Render recommendation categories and scores
- [x] Apply the approved colour theme
- [x] Align user-facing text with the project name

#### Documentation (Maleesha)
- [x] Update README and API contract
- [x] Update Sprint_Document.md and SPRINT2_RELEASE.md
- [x] Record the Sprint 2 release outcomes

### Sprint 2 Acceptance Criteria

#### Backend
- [x] `/api/recommend` returns structured recommendations
- [x] Validation errors follow the request schema
- [x] Rule engine integrated with backend
- [x] Backend tests pass

#### Data
- [x] Rule engine supports multiple scoring categories
- [x] Scoring logic implemented
- [x] Fixtures updated
- [x] Example inputs documented
- [x] Rules align with learning-resource recommendations

#### Frontend
- [x] UI calls `/api/recommend`
- [x] Results render with categories and scores
- [x] Error and loading states implemented
- [x] Layout refined
- [x] Approved colour theme applied

### Sprint 2 Decision Items

#### 1. Project Name
**Decision:** **LearnPath** is the official project name. Repository README and
UI references use the selected name.

#### 2. Colour Theme
**Decision:** **Calm Teal & Navy**, selected from
`docs/colour-theme-shortlist.md` and applied in the frontend.

#### 3. Alignment Requirements
- [x] Frontend uses the approved colour theme
- [x] Data/model rules recommend learning resources
- [x] Project-facing documentation and UI use LearnPath

### Sprint 2 Checklist

#### Backend
- [x] `/api/recommend` integration and OpenAPI documentation updated by Jerome
- [x] Existing validated request model and HTTP 422 behavior retained
- [x] Route delegates to the canonical `data/rule_engine.py` implementation
- [x] Jasim's validation/regression testing completed; the release records 17 passing tests

#### Data
- [x] Categories added
- [x] Scoring logic added
- [x] Fixtures updated
- [x] Example inputs documented

#### Frontend
- [x] Loading state
- [x] Error state
- [x] Results rendering
- [x] Calm Teal & Navy theme applied

#### Docs
- [x] Sprint_Document.md and SPRINT2_RELEASE.md record completed work
- [x] API contract documents request/response schemas and validation behavior
- [x] LearnPath project identity and final theme are recorded

#### Decisions
- [x] Project name chosen: LearnPath
- [x] Colour theme chosen: Calm Teal & Navy

### Sprint 2 Outcome
The frontend and backend recommendation workflow is integrated with the
expanded deterministic rule engine. API validation, regression coverage,
frontend state handling, deployment routing configuration, and documentation
are complete. See `docs/SPRINT2_RELEASE.md` and `docs/SPRINT2_NOTES.md`.

All detailed Sprint 1 tasks, acceptance criteria, execution plan, and release notes are documented in:

**docs/SPRINT1_RELEASE.md**

## Quick Start for Developers

### Frontend
```bash
cd frontend
npm install
npm run dev
npm run build
```

### Backend and API contract
From the repository root, run `uvicorn backend.main:app --reload`. Swagger UI is
available at `http://127.0.0.1:8000/docs` and the OpenAPI schema is at
`http://127.0.0.1:8000/openapi.json`.

`POST /api/recommend` accepts the request shown below and returns the exact
... (file continues as before) ...
