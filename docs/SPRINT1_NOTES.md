# Sprint 1 Notes

**Team:** ITEC322 Group 5
**Sprint:** 1
**Status:** Complete

## What Sprint 1 delivered

Sprint 1 delivered the first working vertical slice of the system:
**frontend → backend → rule engine → deployment**. This confirms the
architecture works end-to-end and establishes the baseline for Sprint 2.

## Team & roles

| Member   | Role                                     |
| -------- | ---------------------------------------- |
| Jerome   | Backend Lead (API, deployment)           |
| Jasim    | Backend Support (tests, CI)              |
| Nishant  | Data/Model Lead (rule engine)            |
| Aarjan   | Data Support (fixtures, evaluation)      |
| Astraea  | Frontend Lead (Vite scaffold, UI)        |
| Maleesha | Docs & UX Support (README, sprint notes) |

## Completed this sprint

- Frontend Vite scaffold builds successfully
- Backend FastAPI scaffold with `POST /api/recommend` endpoint
- Pydantic request model for input validation
- CORS enabled for frontend integration
- Backend health endpoint available
- Deterministic rule engine baseline with stable IDs, sample fixtures, and
  documented example inputs
- Vercel deployment routes `/api/*` to backend, everything else to frontend
- Production domain loads the UI and API requests succeed

## Outstanding at end of Sprint 1

- [x] Frontend: UI calls `/api/recommend`
- [x] Frontend: results render correctly
- [x] Frontend: error states are visible
- [x] Backend tests pass (Jasim)
- [x] Local end-to-end smoke tests (Jasim & Aarjan) — previously blocked pending backend
      integration and Vercel deployment fixes
- [x] Documentation updates (Maleesha)

## Decisions made for Sprint 2 prep

- **Purpose statement finalised:** _"A rule-based learning-resource
  recommendation engine that suggests study materials (videos, articles,
  exercises) based on predefined rules."_
- **Initial colour-theme proposal:** Ocean Blue + White was proposed during
  Sprint 1 planning. The team later approved **Calm Teal & Navy** in Sprint 2;
  see `docs/colour-theme-shortlist.md`.
- **Project name:** not yet finalised — shortlist in progress, vote to be
  held at the start of Sprint 2 (see `docs/PROJECT_NAME_SHORTLIST.md`).

## Carried into Sprint 2

- Rule engine logic expansion (router structure already in place for this)
- Frontend state/error handling and layout polish
- Finalising project name via team vote
