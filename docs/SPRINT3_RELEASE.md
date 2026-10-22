# Sprint 3 Release — Accuracy and Stability

## Release Status

Sprint 3 is substantially complete. **Sprint 1 and Sprint 2 are complete.**
The Data/Model evaluation and measured rule changes are documented, and the
Sprint 3 pull request has been merged into `main`. One outstanding Sprint 3
deliverable was not completed before release and was formally deferred. Sprint
3 is not described as fully complete, and this document does not claim a
production deployment.

## Overview

Sprint 3 follows the completed end-to-end recommendation workflow. The project
currently has a React/Vite frontend, a FastAPI API, a deterministic
rule-based recommender, example resource data, and backend regression tests.
This phase improves recommendation quality and operational confidence using
measurable evaluation and targeted reliability work, while preserving the
working API contract and approved product identity.

## Goals

- Establish a representative evaluation set and reproducible baseline
- Measure recommendation relevance before changing rules
- Improve edge-case coverage and preserve deterministic ranking
- Improve failure diagnosis and user-facing feedback
- Verify frontend/API behavior and the documented deployment configuration
- Keep documentation aligned with implemented and tested behavior

## Expected deliverables

### Data/Model
- [x] A documented evaluation set with expected or reviewed recommendation results
- [x] Recorded baseline results and a repeatable comparison method
- [x] Evidence-based rule tuning produced a measured improvement without
  regressions; no score weights were changed.

### Backend
- [x] Regression tests for rule-engine input boundaries, filtering, scoring,
  and stable ordering
- [x] Clearer failure diagnosis or logging where appropriate
- [x] Request validation and response behavior remain compatible, as exercised
  by the API tests

### Frontend
- [x] Review and polish loading, error, empty-result, and successful-result states
- [ ] Verify that scores and explanations remain understandable and accessible
  (Astraea's outstanding Sprint 3 deliverable; formally deferred)

### Documentation and release
- [x] Record evaluation findings, changes, and known limitations
- [x] Update setup, API, and verification instructions to match the implementation
- [x] Prepare a concise Sprint 3 release summary after work and validation finish

## Testing and validation objectives

- [x] Run rule-engine and API tests, including representative and boundary
  cases (48 tests passed locally)
- [x] Confirm results are reproducible and remain ordered by score and stable
  ID
- [x] Verify valid requests, invalid-request responses, empty results, and
  successful frontend rendering (API paths are covered; browser rendering
  validated)
- [x] Build the frontend from the documented project setup (`npm run build`
  passed locally)
- [x] Verify the documented local integration path and current routing
  configuration; no production deployment is claimed
- [x] Compare evaluation results with the recorded baseline and document the
  evidence

## Quality improvements

- Prefer measurable relevance improvements over unverified score-weight
  changes.
- Preserve the existing API request and response contract unless a reviewed
  change is documented and tested.
- Keep recommendation results explainable and deterministic.
- Avoid adding model or infrastructure dependencies without demonstrated need.
- Record reproducible commands, known limitations, and evidence for release
  decisions.

## Completion criteria

- [ ] Astraea's outstanding Sprint 3 deliverable is completed (formally
  deferred; not completed in this release).
- [x] Evaluation set, baseline, and comparison results are documented.
- [x] Recommendation changes, if any, show a measured improvement without
  regressions in expected behavior.
- [x] Relevant rule-engine and API regression tests pass.
- [x] Frontend and API states are validated across success and failure paths.
- [x] Frontend production build and documented integration checks pass.
- [x] Documentation reflects the verified implementation and remaining
  limitations.

## Sprint 3 Progress Summary

### Completed deliverables

- **Aarjan & Nishant — Data/Model evaluation and collaboration:** added the evaluation set, baseline and tuned results, repeatable evaluator, rule-engine relevance and subject-matching changes, regression tests, and the evaluation report. Evaluation improved nDCG@5 from 0.953 to 0.993 and empty-result cases from 2/4 to 4/4; no evaluated case regressed. The 48 Python rule-engine, regression, and API tests pass; `python evaluate.py --compare` passes. Nishant collaborated closely with Aarjan on the evaluation and rule tuning; both contributors are recorded in the merged Sprint 3 artifacts and evaluation report.
- **Jerome & Jasim — Backend:** implemented and verified backend changes and integration steps; backend regression tests and routing checks are included in the Sprint 3 artifacts and verification evidence.
- **Maleesha — Frontend:** completed frontend tasks for Sprint 3, including build verification and UI updates; his contributions are recorded in the repository's Sprint 3 materials.
- The frontend production build passes locally with `npm run build`.

### Deferred outstanding work

- **Astraea — Deferred:** Astraea's outstanding Sprint 3 deliverable was not
  completed before release. The team formally deferred the item so Sprint 4
  release, final integration testing, and presentation readiness could
  proceed. The item remains incomplete and is not counted as a completed
  Sprint 3 deliverable.

- The rule-tuning path was used; a separate model prototype was not delivered or needed to support the measured rule-based improvement.

## Merge Status

- Sprint 3 PR #16 was successfully merged into `main`; merge commit
  `5234b65` is present on the current `main`.
- The PR was reviewed and approved before merge, as reported for this release.
- Final validation for the Sprint 4 release passed: 52 backend, API, and
  recommendation regression tests; `python evaluate.py --compare`; and the
  frontend production build. Production deployment is not claimed.

## Project progression

Sprint 1 established the frontend-to-backend-to-rule-engine baseline.
Sprint 2 expanded scoring, integrated the user workflow, strengthened
validation, and finalized the LearnPath identity and Calm Teal & Navy theme.
Sprint 3 builds on that completed foundation with measured recommendation
improvements and is substantially complete with one formally deferred
outstanding deliverable. Sprint 4 is released/finalised for project delivery;
the Sprint 4 release record documents its fixes, validation, and known
limitations.

## Release Closure Addendum

Astraea's outstanding Sprint 3 deliverable was not completed before release.
The team formally deferred the outstanding item; it remains incomplete and is
not counted as completed Sprint 3 work. The deferral was made to support Sprint
4 release, final integration testing, and presentation readiness. Sprint 3 is
therefore recorded as substantially complete, not fully complete. This
administrative decision does not assign blame or change the status of the
completed Sprint 3 work.
