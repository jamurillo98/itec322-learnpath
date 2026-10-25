# Sprint Document — LearnPath

## Project Summary
**Project name:** LearnPath
**Goal:** Deliver an end‑to‑end prototype (frontend → backend → rule engine) by Week 12.
**Sprint status:**
- Sprint 1 Complete
- Sprint 2 Complete
- Sprint 3 Complete (scoped accessibility verification recorded)
- Sprint 4 Complete
**Team size:** 6 members.
**Repo state:** `frontend/` contains the React/Vite client; `backend/` contains the FastAPI API; `data/` contains the canonical deterministic rule engine and sample CSV; `vercel.json` contains static-build routing metadata and an API route to `backend/main.py`. Sprint 4 deployment investigation and backend runtime assessment were conducted; this does not establish a verified production deployment.

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
**Sprint 3 Week 9–10:** Complete — implementation, evaluation, backend and frontend work are merged into `main`. Astraea completed the scoped manual accessibility verification documented in `docs/SPRINT3_ASTRAEA_ACCESSIBILITY.md`; its remaining verification limitations are recorded and are not claimed as passed tests.

- Deliverables: Evaluation and rule tuning; backend and regression testing; frontend work; scoped accessibility verification; release documentation.

**Sprint 4 Week 11–12:** Complete — recommendation reliability fixes, final automated validation, release documentation, and presentation preparation are complete for the full team.

- Release activities: Fix blank-keyword matching and cap the rating bonus; add regression coverage and model-card/presentation material; run the backend/API and recommendation tests, evaluation comparison, and frontend production build. Sprint 3 closure and its documented accessibility scope are recorded in `docs/SPRINT3_RELEASE.md`.

## 🔵 Sprint 1 — Completed (Finalised)

### Sprint 1 Overview
Sprint 1 delivered the first working end-to-end request workflow:
**frontend → backend → rule engine**

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

## Sprint 3 — Complete

Sprint 3 delivered its recommendation evaluation framework, measured rule
improvements, backend changes, regression testing, Maleesha's frontend work,
and Astraea's scoped manual accessibility verification. The implementation
was merged into `main`. The accessibility report records its unverified areas
as limitations; comprehensive screen-reader coverage and WCAG conformance are
not claimed.

See `docs/SPRINT3_RELEASE.md` for the release closure and
`docs/SPRINT3_EVALUATION.md` for the evaluation evidence.

## Sprint 4 — Complete

Sprint 4 addressed two recommendation-engine edge cases: whitespace-only
keywords no longer match resources, and the quality bonus is capped to prevent
an empty rating value from overpowering difficulty. The fixes are covered by
regression tests and documented in the model card. Presentation material
includes rule-engine slide notes and a repeatable demonstration scenario.

Release validation passed:

- Backend, API, and recommendation regression tests: 52 passed.
- Evaluation comparison: nDCG@5 0.993, expected-empty cases 4/4, no case
  regressions, and zero hard-filter violations.
- Frontend production build: passed.

Sprint 4 is complete for project delivery. Aarjan and Nishant completed the
Data/Model work; Jasim and Jerome completed backend work; Astraea and Maleesha
completed frontend work. The deployment assessment is recorded in
`docs/SPRINT4_RELEASE.md`.

### Sprint 4 Closure Note

Recommendation-engine hardening, final validation, deployment investigation,
release activities, and presentation preparation were completed. The frontend
production build passed. Backend runtime verification and deployment
assessment were conducted; no verified production deployment is claimed.

- **Aarjan — Sprint 4 Complete:** Data/Model and presentation contributions.
- **Nishant — Sprint 4 Complete:** recommendation reliability improvements,
  merged fixes, regression tests, supporting documentation, and presentation
  materials.
- **Jasim — Sprint 4 Complete:** backend API validation and regression tests.
- **Jerome — Sprint 4 Complete:** release management and documentation,
  deployment investigation, backend runtime verification and deployment
  assessment, final release validation, and presentation readiness.
- **Astraea — Sprint 4 Complete:** frontend and integration verification.
- **Maleesha — Sprint 4 Complete:** frontend support and release-readiness
  contributions.

See `docs/SPRINT4_RELEASE.md` for the closure and deployment assessment.

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
