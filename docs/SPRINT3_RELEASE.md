# Sprint 3 Release — Accuracy and Stability

## Release Status

Sprint 3 is officially complete. **Sprints 1 and 2 are also complete.** The
Data/Model evaluation, measured rule changes, backend and frontend work, and
Astraea's scoped manual accessibility verification are documented, and the
Sprint 3 pull request has been merged into `main`. Accessibility findings and
the limits of the verification are recorded; comprehensive screen-reader
coverage and WCAG conformance are not claimed. This document does not claim a
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
- [x] Complete and document scoped manual accessibility verification of key
  form, keyboard, results, empty-state, and service-error workflows
  (Astraea; see `SPRINT3_ASTRAEA_ACCESSIBILITY.md`). Broader screen-reader
  coverage and WCAG conformance remain outside the verified scope.

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

- [x] Scoped manual accessibility verification is documented, with remaining
  screen-reader coverage and WCAG conformance explicitly recorded as
  limitations rather than completed tests.
- [x] Evaluation set, baseline, and comparison results are documented.
- [x] Recommendation changes, if any, show a measured improvement without
  regressions in expected behavior.
- [x] Relevant rule-engine and API regression tests pass.
- [x] Successful, empty-result, and service-error frontend/API paths are
  validated. The loading UI is implemented and reviewed; its browser capture
  was partial because the request completed too quickly (see
  `SPRINT3_FRONTEND_VERIFICATION.md`).
- [x] Frontend production build and documented integration checks pass.
- [x] Documentation reflects the verified implementation and remaining
  limitations.

## Sprint 3 Progress Summary

### Completed deliverables

- **Aarjan & Nishant — Data/Model evaluation and collaboration:** added the evaluation set, baseline and tuned results, repeatable evaluator, rule-engine relevance and subject-matching changes, regression tests, and the evaluation report. Evaluation improved nDCG@5 from 0.953 to 0.993 and empty-result cases from 2/4 to 4/4; no evaluated case regressed. The 48 Python rule-engine, regression, and API tests pass; `python evaluate.py --compare` passes. Nishant collaborated closely with Aarjan on the evaluation and rule tuning; both contributors are recorded in the merged Sprint 3 artifacts and evaluation report.
- **Jerome & Jasim — Backend:** implemented and verified backend changes and integration steps; backend regression tests and routing checks are included in the Sprint 3 artifacts and verification evidence.
- **Maleesha — Frontend:** completed frontend tasks for Sprint 3, including build verification and UI updates; his contributions are recorded in the repository's Sprint 3 materials.
- **Astraea — Frontend accessibility verification:** completed the documented
  manual verification of keyboard navigation, form controls, validation,
  successful and empty results, service-error feedback, and recovery. The
  report records that comprehensive traversal of every result and automatic
  announcement of every dynamic update were not verified; no WCAG-conformance
  claim is made.
- Frontend verification notes that the loading-state browser capture was
  partial; the implemented state is visible in the UI code, and this
  limitation is not represented as a fully captured manual test.
- The frontend production build passes locally with `npm run build`.
- The rule-tuning path was used; a separate model prototype was not delivered
  or needed to support the measured rule-based improvement.

### Remaining accessibility limitations

- The report does not establish automatic announcements for every dynamic
  update, full traversal of every recommendation-card element, cross-browser
  screen-reader behavior, automated accessibility-audit results, or formal
  WCAG conformance. These limits are documented and are not represented as
  passed tests; the assigned scoped manual verification is complete.

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
improvements and the documented scoped accessibility verification. Sprint 3
is officially complete with the verification limitations recorded. Sprint 4
is officially complete for project delivery; the Sprint 4 release record
documents its fixes, validation, team completion, and known limitations.

## Release Closure

Astraea completed the scoped manual accessibility verification documented in
`SPRINT3_ASTRAEA_ACCESSIBILITY.md`. The report's unverified areas remain
explicitly listed limitations and are not converted into passed checks.
Together with the completed Data/Model, backend, frontend, regression, and
release work, this closes Sprint 3. No comprehensive WCAG or production
deployment claim is made.
