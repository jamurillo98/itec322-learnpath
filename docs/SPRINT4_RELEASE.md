# Sprint 4 Release — Finalisation and Presentation Readiness

## Release Overview

Sprint 4 finalises LearnPath for project delivery and presentation. Work focused
on recommendation reliability, regression coverage, release documentation, and
presentation preparation. This document records the released/finalised scope
and the release-readiness assessment.

Sprint 3 is officially complete, including Astraea's documented scoped manual
accessibility verification; broader screen-reader coverage and WCAG
conformance remain documented limitations. Sprint 4 is officially complete
with all six team members' contributions recorded below.

## Sprint 4 Objectives

- Address identified recommendation-engine edge cases without changing the
  established API contract or measured ranking results.
- Run final automated validation and verify the frontend production build.
- Record the release outcome, known limitations, and future improvements.
- Prepare concise technical material and a repeatable demonstration for the
  Wednesday presentation.
- Record Sprint 3 closure and its accessibility verification scope.

## Completed Work

- Merged Sprint 4 recommendation-engine fixes and their regression tests.
- Added the recommendation engine model card and documented its behaviour,
  evaluation results, limitations, and future improvement path.
- Prepared the rule-engine presentation notes, speaker guidance, likely
  questions, and a demonstration scenario.
- Reran backend, API, and recommendation regression tests: 52 passed.
- Re-ran the evaluation comparison with no regressions against the recorded
  baseline.
- Built the frontend production bundle successfully.
- Closed Sprint 3 after recording Astraea's scoped accessibility verification
  and its remaining limitations.
- Recorded completion for the Data/Model, backend, and frontend team members.

## Recommendation Engine Improvements

The deterministic, rule-based recommendation engine received two targeted
reliability fixes:

- Whitespace-only keywords are ignored, so blank input cannot match every
  resource or bypass the relevance gate.
- The quality bonus is capped at one point, preventing the default empty-rating
  value from outweighing the learner's requested difficulty.

These fixes address input cases that were not covered by the evaluation set.
They did not change the recorded evaluation results: nDCG@5 remains 0.993,
all four expected-empty cases pass, and no evaluated case regressed.

## Bug Fixes

- **Blank keyword matching:** trimmed blank keywords no longer receive a
  keyword score or allow unrelated resources through relevance filtering.
- **Rating bonus overpowering difficulty:** the quality contribution is capped,
  keeping an empty rating field from unduly changing recommendation order.

Both fixes are covered by Sprint 4 regression tests.

## Testing and Validation

Validation performed for this release:

- `python -m pytest data/test_rule_engine.py data/test_sprint3_regression.py tests/test_api.py -q`
  — 52 tests passed.
- `python evaluate.py --compare` from `data/` — comparison passed; nDCG@5 is
  0.993, expected-empty cases pass 4/4, hard-filter violations are zero, and
  no evaluated case worsened.
- `npm run build` from `frontend/` — production build passed.

The test run reported existing dependency deprecation warnings. They did not
cause failures.

## Release Outcome

The recommendation regression fixes, evaluation guard, frontend production
build, model documentation, presentation material, and team closure record are
in place. Sprints 1 through 4 are officially complete. The documented
accessibility limitations and lack of verified production deployment remain
explicitly stated.

## Known Limitations

- The catalogue contains 30 sample resources across three subjects, and its
  URLs are placeholders.
- The evaluation set contains 21 team-authored cases; results on this set do
  not establish performance on a larger real-world catalogue.
- The fixed subject-alias list is limited, and substring matching can match
  inside longer words.
- Evaluation case E04 retains a known ranking imperfection (nDCG 0.89).
- The API does not currently pass `preferred_format` through to the engine.
- The Sprint 4 browser report marks the whitespace-only keyword check as
  partially verified and empty minimum rating as not tested at API level.
  Automated regression/API tests pass, but those manual observations are not
  represented as comprehensive browser/API coverage.
- The production backend runtime and deployment configuration were assessed,
  but this release does not establish a verified production deployment.
- Accessibility verification was manual and scoped to the workflows listed
  in `SPRINT3_ASTRAEA_ACCESSIBILITY.md`; comprehensive screen-reader coverage
  and formal WCAG conformance are not claimed.

## Future Improvements

- Expand and independently review the evaluation set and resource catalogue.
- Extend subject normalisation and aliases based on reviewed learner needs.
- Address the known E04 ranking imperfection only when changes can be measured
  without regressions.
- Wire the optional preferred-format field through the API if it is in scope.
- Collect real learner feedback before assessing whether a trained ranking
  model is warranted.
- Consider broader screen-reader and accessibility testing if it becomes a
  project requirement.
- If production deployment becomes a release requirement, validate the
  production environment and deployment separately from this assessment.

## Presentation Readiness Summary

The repository includes rule-engine slide content, speaker notes, likely
question guidance, and a repeatable demo scenario. The recommendation tests,
evaluation comparison, and production frontend build pass, providing
reproducible technical evidence for the presentation. Final slide review and
rehearsal should remain aligned with the Wednesday deadline. Sprint 3 and
Sprint 4 closure are recorded separately from the explicitly documented
accessibility and deployment limitations.

## Sprint 4 Completion Statement

Sprint progression is recorded as: Sprint 1 Complete; Sprint 2 Complete;
Sprint 3 Complete (Astraea's scoped accessibility verification completed);
Sprint 4 Complete. The accessibility report's unverified areas remain
limitations and are not represented as passed checks.

## Sprint 4 Closure and Release Validation

### Aarjan Completion Status — Data/Model

- Completed Sprint 4 Data/Model contributions and presentation preparation,
  including the demo scenarios and future-ML material.
- Aarjan's Sprint 4 contribution is complete.

### Nishant Completion Status

- Recommendation reliability improvements were completed.
- Sprint 4 fixes were reviewed, approved, merged, and released.
- Regression tests were implemented.
- Supporting documentation and presentation materials were produced.
- Nishant's Sprint 4 contribution is complete.

### Jasim Completion Status — Backend

- Completed Sprint 4 API validation and regression-test contributions.
- Jasim's Sprint 4 contribution is complete.

### Jerome Completion Status

- Sprint 4 release management activities were completed.
- Release documentation was completed.
- Deployment investigation was performed.
- Backend runtime verification and deployment assessment were conducted.
- Final release validation and presentation-readiness activities were
  completed.
- Jerome's Sprint 4 contribution is complete.

### Astraea Completion Status — Frontend

- Completed Sprint 4 frontend and integration verification, documented in the
  final verification report.
- Astraea's Sprint 4 contribution is complete.

### Maleesha Completion Status — Frontend

- Completed Sprint 4 frontend support and release-readiness contributions as
  confirmed by the team.
- Maleesha's Sprint 4 contribution is complete.

### Deployment Assessment

LearnPath uses a React/Vite frontend and a FastAPI backend. Deployment
verification was investigated as a Sprint 4 release-readiness activity. The
frontend production build completed successfully. Production deployment and
the backend runtime configuration were assessed; the available evidence does
not establish a verified production deployment.

The local frontend-to-API setup is a supported demonstration environment, as
documented in the Sprint 3 frontend verification record. Deployment findings
and remaining verification needs are recorded as future improvement work.
