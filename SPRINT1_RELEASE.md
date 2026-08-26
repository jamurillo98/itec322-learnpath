# Sprint 1 Release — Simple, Clear, Role‑Specific

## Overview
Sprint 1 delivers the first working vertical slice:
frontend → backend → rule engine → deployment.
This release proves the architecture works end‑to‑end.

## Roles and Responsibilities
- **Jerome** — Backend Lead (API, deployment)
- **Jasim** — Backend Support (tests, CI)
- **Nishant** — Data/Model Lead (rule engine)
- **Aarjan** — Data Support (fixtures, evaluation)
- **Astraea** — Frontend Lead (Vite scaffold, UI)
- **Maleesha** — Docs & UX Support (README, sprint notes)

## Sprint 1 Branches
| Purpose | Branch | Folder |
|---------|--------|--------|
| Frontend scaffold | feature/frontend-scaffold | frontend/ |
| API endpoint | feature/api-recommend | backend/ |
| Rule engine baseline | feature/rule-baseline | data/ |
| Local E2E smoke tests | test/local-e2e | backend/, frontend/ |
| Vercel routing fixes | fix/vercel-routing | repo root |
| Docs updates | docs/sprint-1 | repo root |

## Tasks and Owners
- Scaffold frontend — **Astraea**
- Implement `/api/recommend` — **Jerome**
- Rule engine baseline — **Nishant**
- Local E2E tests — **Jasim & Aarjan**
- Vercel deployment check — **Jerome**
- Documentation updates — **Maleesha**

## Acceptance Criteria
### Backend (Jerome & Jasim)
- POST /api/recommend implemented
- Validation errors return correct schema
- Deterministic rule engine integration
- Backend tests pass in CI

### Data (Nishant & Aarjan)
- Deterministic rule engine with stable IDs
- Sample fixtures created
- Example inputs documented

### Frontend (Astraea & Maleesha)
- Vite scaffold builds successfully
- UI calls /api/recommend
- Results render correctly
- Error states visible

## Deployment Checklist
- Frontend build succeeds (`dist/` exists)
- Backend tests pass
- Production domain loads UI
- Production API request succeeds
- Documentation updated

## Sprint 1 Release Summary
Sprint 1 is complete and released.  
All required vertical-slice components are implemented and verified.  
This release forms the baseline for Sprint 2 development.
