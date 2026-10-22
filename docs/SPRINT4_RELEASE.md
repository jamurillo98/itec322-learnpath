# Sprint 4 Release — Finalisation and Presentation Readiness

## Release Overview

Sprint 4 finalises LearnPath for project delivery and presentation. Work focused
on recommendation reliability, regression coverage, release documentation, and
presentation preparation. Sprint 4 is released/finalised; this status does not
claim a production deployment.

Sprint 3 is substantially complete. Astraea's outstanding Sprint 3 deliverable
was not completed before release and has been formally deferred. The deferral
allows Sprint 4 release activities, final integration testing, and presentation
readiness to proceed without describing Sprint 3 as fully complete.

## Sprint 4 Objectives

- Address identified recommendation-engine edge cases without changing the
  established API contract or measured ranking results.
- Run final automated validation and verify the frontend production build.
- Record the release outcome, known limitations, and future improvements.
- Prepare concise technical material and a repeatable demonstration for the
  Wednesday presentation.
- Formally document the outstanding Sprint 3 deliverable as deferred.

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
- Recorded Sprint 3 as substantially complete, with Astraea's outstanding
  deliverable formally deferred.

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
cause failures. Production deployment is not claimed by this release.

## Release Outcome

Sprint 4 is released/finalised for project delivery. The recommendation
regression fixes, evaluation guard, frontend production build, model
documentation, and presentation material are in place. Sprint 3 remains
substantially complete, with one outstanding Astraea deliverable formally
deferred rather than marked complete.

## Known Limitations

- The catalogue contains 30 sample resources across three subjects, and its
  URLs are placeholders.
- The evaluation set contains 21 team-authored cases; results on this set do
  not establish performance on a larger real-world catalogue.
- The fixed subject-alias list is limited, and substring matching can match
  inside longer words.
- Evaluation case E04 retains a known ranking imperfection (nDCG 0.89).
- The API does not currently pass `preferred_format` through to the engine.
- Production deployment and its backend runtime configuration are not verified
  by this release.
- Astraea's outstanding Sprint 3 deliverable remains deferred and incomplete.

## Future Improvements

- Expand and independently review the evaluation set and resource catalogue.
- Extend subject normalisation and aliases based on reviewed learner needs.
- Address the known E04 ranking imperfection only when changes can be measured
  without regressions.
- Wire the optional preferred-format field through the API if it is in scope.
- Collect real learner feedback before assessing whether a trained ranking
  model is warranted.
- Revisit the deferred Sprint 3 deliverable in a later planning decision.
- Verify production deployment separately if deployment becomes a release
  requirement.

## Presentation Readiness Summary

The repository includes rule-engine slide content, speaker notes, likely
question guidance, and a repeatable demo scenario. The recommendation tests,
evaluation comparison, and production frontend build pass, providing
reproducible technical evidence for the presentation. Final slide review and
rehearsal should remain aligned with the Wednesday deadline. The deferred
Sprint 3 item is explicitly distinguished from completed work.

## Sprint 4 Completion Statement

Sprint 4 is released/finalised for project delivery and presentation
preparation. Sprint 1 and Sprint 2 are complete; Sprint 3 is substantially
complete with one deferred outstanding deliverable; Sprint 4 is released and
finalised. The deferred Sprint 3 work is not represented as completed.
