# Sprint 2 Release — Rule Engine Expansion + UI Integration

## Release Status
Sprint 2 is still in progress. Jerome's independent backend contribution is
complete on this branch; frontend, data/model, project-name, and colour-theme
work remain separate team responsibilities unless their evidence is recorded
elsewhere in the repository.

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
- Add rule categories  
- Add scoring logic  
- Update fixtures  
- Document example inputs  
- Ensure rules align with learning-resource theme  

### Frontend (Astraea & Maleesha)
- Implement UI state handling  
- Implement loading + error states  
- Render categories + scores  
- Apply chosen colour theme  
- Ensure UI text aligns with chosen project name  

### Documentation (Maleesha)
- Update README  
- Update Sprint_Document.md  
- Update API contract  
- Add Sprint 2 release notes  

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

**Status:** Pending

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
- [ ] Categories added  
- [ ] Scoring logic added  
- [ ] Fixtures updated  
- [ ] Example inputs documented  

### Frontend
- [ ] Loading state  
- [ ] Error state  
- [ ] Results rendering  
- [ ] Colour theme applied  

### Docs
- [ ] Sprint_Document.md updated  
- [ ] SPRINT2_RELEASE.md updated  
- [ ] API contract updated  

### Decisions
- [x] Project name chosen (LearnPath)
- [ ] Colour theme chosen  

## Sprint 2 Summary
The backend API contribution described above is complete and verified with the
existing backend checks. Jasim's validation and regression testing work is also
complete and documented in PR #12. Sprint 2 as a whole is not claimed complete:
the repository still requires evidence for the data/model categories and
scoring, frontend work, documentation ownership items, and the colour-theme
decision.