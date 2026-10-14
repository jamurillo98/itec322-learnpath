# Sprint 2 Release — Rule Engine Expansion + UI Integration

## Release Status
Sprint 2 is complete. Jerome's independent backend contribution is
complete on this branch; frontend, data/model, project-name, and colour-theme
work have been completed and recorded in recent commits (Maleesha: colour theme, documentation updates).

## Overview
Sprint 2 builds directly on the completed vertical slice from Sprint 1.  
The focus of this sprint is to expand the rule engine, integrate backend logic with the frontend UI, refine user-facing behaviour, and strengthen validation and testing across the stack.

This sprint also finalises the selected project identity (**LearnPath**) and the colour theme decision to ensure consistent UI and documentation.

## Objectives
- Expand rule engine with categories + scoring  
- Integrate backend logic with frontend  
- Add loading, error, and result states  
- Strengthen validation  
- Add E2E tests  
- Update documentation  
- Finalise project name  
- Finalise colour theme  

## Tasks

### Backend (Jerome & Jasim)
- [x] Confirmed `POST /api/recommend` uses the validated request model
- [x] Confirmed the route delegates to the canonical `data/rule_engine.py`
- [x] Preserved the `{"recommendations": [...]}` response envelope and
	data-layer recommendation fields
- [x] Added FastAPI metadata and route-level OpenAPI documentation
- [x] Documented the request/response contract, validation behavior, local run
	command, and Swagger URL
- [x] Jasim's regression/validation test is complete: missing `subject` now returns HTTP 422, and the full suite passes with 17 tests passing (PR #12)

### Data/Model (Nishant & Aarjan)
- [x] Add rule categories
- [x] Add scoring logic
- [x] Update fixtures
- [x] Document example inputs
- [x] Ensure rules align with learning-resource theme

### Frontend (Astraea & Maleesha)
- [x] Implement UI state handling
- [x] Implement loading + error states
- [x] Render categories + scores
- [x] Apply chosen colour theme
- [x] Ensure UI text aligns with chosen project name

### Documentation (Maleesha)
- [x] Update README
- [x] Update Sprint_Document.md
- [x] Update SPRINT2_RELEASE.md
- [x] Update API contract

## Decision Items

### 1. Project Name
Winning name updates:
- README  
- API documentation  
- UI landing text  
- Vercel project name  

**Status:** ✓ LearnPath selected as the preferred project name.

### 2. Colour Theme
Chosen theme must be applied to:
- UI components  
- Buttons  
- Backgrounds  
- Accent colours  
- Documentation styling  

**Status:** ✓ Colour theme chosen and applied by Maleesha (see recent commits).

### 3. Alignment Requirements
- **Frontend** must use the chosen colour theme  
- **Data/Model** must ensure rules still align with learning-resource recommendations  
- **Backend** must ensure API text matches the chosen project name  

## Acceptance Criteria

### Backend
- `/api/recommend` returns structured recommendations  
- Validation errors follow updated schema  
- Rule engine integrated with backend  
- Backend tests pass in CI  

### Data
- Rule engine supports multiple rule categories  
- Scoring logic implemented  
- Fixtures updated  
- Example inputs documented  
- Rules align with learning-resource theme  

### Frontend
- UI calls updated `/api/recommend`  
- Results render with categories + scores  
- Error + loading states implemented  
- Layout refined  
- Colour theme applied  

## Sprint 2 Checklists

### Backend
- [x] `/api/recommend` integration and API documentation updated by Jerome
- [x] Existing request validation and HTTP 422 behavior retained
- [x] Canonical rule engine integration retained
- [x] Jasim's regression/validation work is complete

### Data
- [x] Categories added  
- [x] Scoring logic added  
- [x] Fixtures updated  
- [x] Example inputs documented  

### Frontend
- [x] Loading state  
- [x] Error state  
- [x] Results rendering  
- [x] Colour theme applied  

### Docs
- [x] Sprint_Document.md updated  
- [x] SPRINT2_RELEASE.md updated  
- [x] API contract updated  

### Decisions
- [x] Project name chosen (LearnPath)
- [x] Colour theme chosen  

## Sprint 2 Summary
The backend API contribution described above is complete and verified with the
existing backend checks. Jasim's validation and regression testing work is also
complete and documented in PR #12. Data/Model work has been completed and the
frontend implementation is complete with the final colour theme applied. Documentation updates and the final colour-theme decision were completed by Maleesha and are recorded in the repository.
