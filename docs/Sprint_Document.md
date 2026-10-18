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

... (rest of document unchanged) ...

### 5.3 Sprint 3: Accuracy and Stability, Weeks 9–10
**Status:** In progress — majority complete, merged into `main` (Sprint 3 PR merged). One remaining frontend verification task (see Remaining work).

**Goal:** Improve recommendation quality and operational confidence.
**Deliverables (progress):** Tuned rules and evaluation artifacts; regression tests; backend reliability updates; frontend build verification.

Completed / recorded items
- Data/model evaluation and tuning: Aarjan & Nishant — evaluation set, baseline comparison, and evidence-based tuning recorded (nDCG improvements recorded).  
- Backend deliverables: Jerome & Jasim — backend changes, regression tests, and routing checks implemented and verified.  
- Frontend build: Maleesha — production build verification and UI updates recorded.  
- Tests: Rule-engine and API regression tests pass locally and are recorded in the Sprint 3 release artifacts.

Remaining / outstanding
- Astraea — Frontend verification, browser-level accessibility review, and final UI polish remain outstanding and block final Sprint 3 acceptance. These items are scheduled for immediate completion; if deferred, they will be explicitly recorded and moved into Sprint 4 work items.

**Acceptance criteria (current):**
- Evaluation results recorded and reproducible.  
- API and backend tests pass.  
- Frontend production build generated.  
- Browser-level verification and accessibility review (Astraea) pending.

**Notes:** Sprint 3 implementation is merged; the Sprint 3 release document (`docs/SPRINT3_RELEASE.md`) contains the authoritative list of evidence and the merged artifacts. The team should complete the remaining frontend verification before claiming Sprint 3 complete; otherwise, the item will be carried into Sprint 4 with explicit acceptance criteria.

### 5.4 Sprint 4: Final Polish, Weeks 11–12
**Goal:** Produce a reliable, understandable demonstration and final handoff.

**Deliverables (including pending post‑Sprint‑3 tasks):** Final UI; final rules or model; deployment runbook; README; slides; demo script; and Vercel backend runtime configuration and verification.

New / Pending items moved from Sprint 3
- Vercel backend deployment verification: configure the backend as a Vercel Python serverless function (or deploy backend elsewhere and point frontend at the URL), ensure dependencies are installed (requirements.txt location), and verify that `/api/health` and `/api/recommend` respond on the preview and production domains. This task is tracked as a Sprint 4 item to be completed after Astraea's Sprint 3 deliverables finish (or concurrently if the team prefers).

**Acceptance criteria additions for Sprint 4:**
- Production preview deployment shows frontend assets and a working backend API endpoint.  
- Vercel build logs indicate the Python build step completed and dependencies were installed.  
- Final accessibility review and UI polish are complete.

... (rest of document unchanged) ...
