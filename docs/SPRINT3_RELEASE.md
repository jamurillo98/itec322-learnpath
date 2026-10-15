# Sprint 3 Release — Accuracy and Stability

## Release Status

Sprint 3 is in progress. **Sprint 1 and Sprint 2 are fully completed.** The
Data/Model evaluation and measured rule changes are documented, and the Sprint
3 pull request has been merged into `main`. Frontend runtime and integration
verification and other remaining activities are still open; this is not a
Sprint 3 completion or production-release claim.

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
- [ ] Clearer failure diagnosis or logging where appropriate
- [x] Request validation and response behavior remain compatible, as exercised
  by the API tests

### Frontend
- [ ] Review and polish loading, error, empty-result, and successful-result states
- [ ] Verify that scores and explanations remain understandable and accessible

### Documentation and release
- [x] Record evaluation findings, changes, and known limitations
- [ ] Update setup, API, and verification instructions to match the implementation
- [ ] Prepare a concise Sprint 3 release summary after work and validation finish

## Testing and validation objectives

- [x] Run rule-engine and API tests, including representative and boundary
  cases (48 tests passed locally)
- [x] Confirm results are reproducible and remain ordered by score and stable
  ID
- [ ] Verify valid requests, invalid-request responses, empty results, and
  successful frontend rendering (API paths are covered; browser rendering
  remains unverified)
- [x] Build the frontend from the documented project setup (`npm run build`
  passed locally)
- [ ] Verify the documented local integration path and current routing
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

- [x] Evaluation set, baseline, and comparison results are documented.
- [x] Recommendation changes, if any, show a measured improvement without
  regressions in expected behavior.
- [x] Relevant rule-engine and API regression tests pass.
- [ ] Frontend and API states are validated across success and failure paths.
- [ ] Frontend production build and documented integration checks pass.
- [x] Documentation reflects the verified implementation and remaining
  limitations.

## Sprint 3 Progress Summary

### Completed deliverables

- **Aarjan — Data/Model evaluation and support:** added the evaluation set,
  baseline and tuned results, repeatable evaluator, rule-engine relevance and
  subject-matching changes, regression tests, and the evaluation report.
  Evaluation improved nDCG@5 from 0.953 to 0.993 and empty-result cases from
  2/4 to 4/4; no evaluated case regressed. The 48 Python rule-engine,
  regression, and API tests pass; `python evaluate.py --compare` passes.
- **Jerome — release integration:** merged Sprint 3 PR #16 into `main`
  (merge commit `5234b65`). The repository history does not show a separate
  Sprint 3 implementation commit by Jerome.
- The frontend production build passes locally with `npm run build`.

### In-progress deliverables

- Frontend success, empty-result, and failure states still need browser-level
  validation and review for accessibility and clarity.
- The documented local frontend/API integration path and routing configuration
  still need verification.
- Backend failure-diagnosis/logging work and setup/API/verification-document
  updates are not evidenced as complete.

### Remaining work

- Complete and record frontend/browser and local integration checks.
- Address or explicitly defer the remaining backend diagnostics and
  documentation deliverables before final release.
- **Nishant:** no Sprint 3 implementation or review deliverable attributable
  to Nishant was found in the repository evidence reviewed. The rule changes
  and evaluation artifacts in the merged Sprint 3 work are authored by Aarjan.
- The rule-tuning path was used; a separate model prototype was not delivered
  or needed to support the measured rule-based improvement.

## Merge Status

- Sprint 3 PR #16 was successfully merged into `main`; merge commit
  `5234b65` is present on the current `main`.
- The PR was reviewed and approved before merge, as reported for this release.
- Local verification is ongoing: the Python tests, baseline comparison, and
  frontend production build passed. Frontend runtime/integration verification
  and the remaining Sprint 3 activities are still open.

## Project progression

Sprint 1 established the frontend-to-backend-to-rule-engine baseline.
Sprint 2 expanded scoring, integrated the user workflow, strengthened
validation, and finalized the LearnPath identity and Calm Teal & Navy theme.
Sprint 3 builds on that completed foundation with measured recommendation
improvements; final frontend and integration verification remains in progress.
