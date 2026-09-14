# Sprint 2 Release — Rule Engine Expansion + UI Integration

## Overview
Sprint 2 builds directly on the completed vertical slice from Sprint 1.  
The focus of this sprint is to expand the rule engine, integrate backend logic with the frontend UI, refine user-facing behaviour, and strengthen validation and testing across the stack.

This sprint also finalises **project identity decisions** (name + colour theme) to ensure consistent UI and documentation.

## Objectives
- Expand rule engine with categories + scoring  
- Integrate backend logic with frontend  
- Add loading, error, and result states  
- Strengthen validation  
- Add E2E tests  
- Update documentation  
- Decide project name  
- Decide colour theme  

## Tasks

### Backend (Jerome & Jasim)
- Improve `/api/recommend` logic  
- Add validation rules  
- Add backend tests  
- Integrate rule engine  
- Update API documentation  

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
Each member proposes one name.  
Vote before Sprint 2 ends.  
Winning name updates:
- README  
- API documentation  
- UI landing text  
- Vercel project name  

### 2. Colour Theme
Chosen theme must be applied to:
- UI components  
- Buttons  
- Backgrounds  
- Accent colours  
- Documentation styling  

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
- [ ] Updated `/api/recommend`  
- [ ] Validation rules updated  
- [ ] Tests added  
- [ ] Rule engine integrated  

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
- [ ] Project name chosen  
- [ ] Colour theme chosen  

## Sprint 2 Release Summary
Sprint 2 is complete and released.  
All required components for rule engine expansion and UI integration have been implemented and verified.  
The project now supports structured recommendations, multi-category rule evaluation, and a functional user interface capable of rendering results and handling errors gracefully.