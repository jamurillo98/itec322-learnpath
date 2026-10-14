# Sprint 2 Notes

**Team:** ITEC322 Group 5
**Project:** LearnPath
**Sprint:** 2
**Status:** Complete

## What Sprint 2 delivered

Sprint 2 completed the integrated learning-resource recommendation workflow.
The React/Vite frontend collects learning preferences and displays results
from the FastAPI backend, which delegates recommendation scoring to the
canonical deterministic rule engine.

## Team & roles

| Member   | Role                                     |
| -------- | ---------------------------------------- |
| Jerome   | Backend Lead (API, documentation, deployment configuration) |
| Jasim    | Backend Support (validation, regression tests) |
| Nishant  | Data/Model Lead (rule engine, scoring)   |
| Aarjan   | Data/Model Support (fixtures, evaluation) |
| Astraea  | Frontend Lead (form, results UI)         |
| Maleesha | Frontend Support (UI states, theme, documentation) |

## Completed this sprint

- Backend `/api/recommend` integration with the validated request model and
  canonical `data/rule_engine.py`
- Structured recommendation responses retained in the
  `{"recommendations": [...]}` envelope
- Rule categories, score breakdowns, deterministic ordering, and expanded
  sample-resource fixtures
- Frontend integration with loading, error, empty-result, and recommendation
  states
- Regression and validation coverage, including HTTP 422 behavior for a
  missing `subject`
- API and example-input documentation updates
- Vercel routing configuration for API requests to the backend and other
  requests to the frontend; this records configuration, not a newly verified
  production deployment
- Sprint and project-identity documentation updates

## Decisions made

- **Official project name:** **LearnPath**
- **Final approved colour theme:** **Calm Teal & Navy**
- **Recommendation approach:** deterministic, explainable, rule-based scoring
  remains the canonical implementation

## Testing and validation

The Sprint 2 release records 17 passing tests for the backend validation and
rule-engine regression suite. It also confirms that the API schema,
recommendation response envelope, and frontend integration remain aligned.
The release notes identify the tested behavior and API documentation in
`docs/SPRINT2_RELEASE.md`.

## Sprint 2 outcome

Sprint 2 is complete. The integrated frontend/backend workflow, rule-engine
expansion, validation, testing, branding decisions, deployment-routing
configuration, and documentation updates are recorded in the repository.
Sprint 3 can now focus on measured recommendation quality and operational
stability.
