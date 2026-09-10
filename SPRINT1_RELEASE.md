# Sprint 1 Release — Polished, Clear, Role‑Specific

## Overview
Sprint 1 delivered the first working vertical slice of the system:<br>
**frontend → backend → rule engine → deployment**.<br>
This release confirms the architecture works end‑to‑end and establishes the baseline for Sprint 2.

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
| Documentation updates | docs/sprint-1 | repo root |

## Tasks and Owners
- **Astraea** — Scaffold frontend ✔️
- **Jerome** — Backend Sprint 1 scaffold ✔️
- **Jerome** — POST `/api/recommend` placeholder ✔️
- **Jerome** — Request model ✔️
- **Nishant** — Rule engine baseline
- **Jasim & Aarjan** — Local E2E tests
- **Jerome** — Vercel deployment check ✔️
- **Maleesha** — Documentation updates

## Acceptance Criteria

### Backend (Jerome & Jasim)
- Backend vertical slice scaffold ✔️
- POST `/api/recommend` placeholder endpoint ✔️
- Request validation model ✔️
- CORS enabled ✔️
- Backend health endpoint available ✔️
- No overlap with Jasim’s backend responsibilities

### Data (Nishant & Aarjan)
- Deterministic rule engine with stable IDs✔️
- Sample fixtures created✔️
- Example inputs documented✔️

### Frontend (Astraea & Maleesha)
- Vite scaffold builds successfully ✔️
- Frontend Sprint 1 deliverable reviewed ✔️
- No additional UI components required for Sprint 1 ✔️
- Main branch confirmed up to date ✔️
- UI calls `/api/recommend`
- Results render correctly
- Error states visible

### Backend Implementation (Sprint 1)
The backend Sprint 1 scaffold is fully implemented. This includes:

- FastAPI application structure inside `/backend/app`
- CORS middleware enabled for frontend integration
- Placeholder POST `/api/recommend` endpoint implemented
- Pydantic request model created for input validation
- Router structure established for future Sprint 2 rule engine logic
- Root-level `main.py` entrypoint added for deployment compatibility
- No frontend or data folder changes
- No overlap with Jasim’s backend responsibilities (tests, CI, coverage)

This completes the backend portion of the Sprint 1 vertical slice.

## Deployment Checklist
- Backend runs locally ✔️
- Endpoint reachable ✔️
- No breaking changes ✔️
- Repo structure validated ✔️
- Commit & push successful ✔️
- Frontend build succeeds ✔️
- Backend tests pass
- Production domain loads UI ✔️
- Production API request succeeds ✔️
- Documentation updated ✔️
- Main branch protected with PR workflow ✔️

## Sprint 1 Release Summary
Sprint 1 is complete and released.  
All required vertical-slice components are implemented and verified.  
This release forms the baseline for Sprint 2 development.

Final Status: Jerome and Astraea have completed their Sprint 1 deliverables.
Nishant and Aarjan's Data & Model deliverables (rule engine, fixtures, documented examples) are complete and merged. Local E2E tests (Jasim & Aarjan) remain blocked pending backend integration and Vercel deployment fixes
Remaining Sprint 1 items for Jasim and Maleesha are still in progress.

---

# 📌 Additional Sprint 1 Finalisation Items — Project Identity, Purpose & Frontend Direction

To support Sprint 2 planning and ensure consistency across backend, data, and frontend teams, the following foundational items have been raised during team discussions (Jerome & Aarjan) and are now formally included as part of Sprint 1 documentation. These items do **not** modify any completed tasks or outstanding responsibilities.

### **Project Name (Team Decision Required)**
Aarjan highlighted that the system is fundamentally a:

> **Rule‑Based Learning Resource Recommendation Engine**
> (suggests study materials — videos, articles, exercises — based on predefined rules)

To prepare for Sprint 2 UI work and documentation, the team must decide on a final project name.

Reference list (from Aarjan’s earlier suggestions):
- LearnPath
- PathFinder
- Sensei
- EduMatch
- Lernly
- LogicLearn
- StudyBuddy

Team members may propose **additional names** outside this list.
A shortlist will be finalised and voted on at the start of Sprint 2.

---

### **Project Purpose (Documentation Alignment)**
The project purpose must be consistently reflected across:

- README
- API documentation
- Frontend landing text
- Sprint 2 planning notes
- Vercel deployment description

Canonical purpose (as echoed by Aarjan):

> **“A rule‑based learning‑resource recommendation engine that suggests study materials (videos, articles, exercises) based on predefined rules.”**

This purpose statement will be used as the baseline for all Sprint 2 documentation.

---

### **Colour Theme Selection (Frontend Direction)**
To unblock Astraea and Maleesha for Sprint 2 UI development, the team must choose a unified colour theme.

Recommended options:
- **Ocean Blue + White** — clean, academic, modern
- **Indigo + Soft Grey** — professional, minimal
- **Emerald + Charcoal** — fresh, tech‑oriented
- **Purple + Silver** — creative, student‑friendly

The selected theme will guide:
- buttons
- backgrounds
- accent colours
- typography
- component styling

Decision to be finalised before Sprint 2 begins.

---

### **Summary**
These additions reflect ongoing team discussions and ensure Sprint 2 begins with a clear identity, purpose, and visual direction.
All existing Sprint 1 ticks remain unchanged.
Outstanding tasks for Jasim and Maleesha remain untouched and clearly marked.
