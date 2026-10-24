# Sprint 4 — Astraea Final Verification Report

**Project:** LearnPath  
**Sprint:** Sprint 4 — Finalisation and Presentation Readiness  
**Testing date:** 24 October 2026  
**Test environment:** macOS (MacBook Air), Firefox, Safari, VS Code, Python virtual environment  
**Branch:** `feature/astraea-sprint4-verification`  
**Scope:** Manual frontend verification, integration testing, regression testing, and recommendation evaluation

---

## 1. Objective

This report documents the final verification activities performed for LearnPath during Sprint 4. The purpose was to confirm that the frontend and backend work together, the application responds appropriately to different user inputs, the recommendation results remain understandable, and the automated regression and evaluation checks pass.

The verification builds upon the Sprint 3 accessibility testing and contributes additional evidence for Sprint 4 release and presentation readiness.

## 2. Test Environment

The application was tested locally on macOS using Firefox and Safari.

The frontend uses React and Vite and was accessed through `http://localhost:5173`. The backend uses FastAPI and was run locally through Uvicorn at `http://127.0.0.1:8000`.

VS Code was used to run the development servers, automated tests, and evaluation scripts. Python testing dependencies, including `pytest` and `httpx`, were installed in the project's existing virtual environment.

No production deployment was performed or verified as part of this work.

## 3. Frontend Production Build

The frontend production build was executed using:

```bash
cd frontend
npm run build
```

**Result: PASS**

Vite completed the production build successfully, transforming 35 modules and generating the production assets inside the `dist` directory.

A warning concerning Vite's deprecated CommonJS Node API was displayed, but it did not prevent the build.

This confirms that the frontend could be compiled successfully in the tested local environment.

## 4. Manual Frontend and Integration Testing

| Test | Observed result | Status |
|---|---|---|
| Application loading | LearnPath interface loaded in the browser | PASS |
| Frontend/backend communication | Valid searches produced recommendations through the local API | PASS |
| Successful recommendations | Five ranked resources displayed for eligible searches | PASS |
| Empty-result handling | Appropriate no-results heading and guidance displayed | PASS |
| Subject validation | Empty required subject blocked with a browser validation message | PASS |
| Difficulty selection | Intermediate could be selected successfully | PASS |
| Intermediate recommendations | Eligible Intermediate resources returned | PASS |
| Whitespace-only keywords | Visible first result and score matched the empty-keyword search | PARTIALLY VERIFIED |
| Empty minimum rating | Browser blocked submission with a numeric-field validation message | NOT TESTED AT API LEVEL |
| Zero minimum rating | Search accepted and recommendations displayed | PASS |
| Recommendation explanations | Four category scores and reasons displayed | PASS |
| Resource hyperlink | Opened the expected placeholder destination in a new tab | PASS |
| Keyboard resource-link activation | Resource link opened through keyboard navigation | PASS |

### 4.1 Successful Recommendations

The application returned five recommended learning resources for a valid programming search.

For an Intermediate-level search with a maximum duration of 120 minutes, minimum rating of 3, no keywords, and a result limit of 5, the first recommendation was **Writing Unit Tests with Pytest (R015)**, with a total score of 9.58.

The resource displayed the selected Intermediate difficulty and a duration of 50 minutes.

### 4.2 Empty-Result Handling

A search using cooking, Beginner difficulty, a maximum duration of five minutes, and a minimum rating of five produced no eligible results.

The application displayed the message **"No matching resources found"** and suggested broadening the subject, increasing the duration, lowering the rating requirement, or using fewer keywords.

This confirmed that the empty-result state provides understandable guidance.

### 4.3 Form Validation

Submitting the form with an empty Subject field caused the browser to display **"Please fill out this field."** The Subject field received focus, and the incomplete submission was prevented.

The Difficulty Level dropdown supported changing from Beginner to Intermediate. However, the initial placeholder option could not be selected again after a valid difficulty had been chosen, so that particular missing-selection path was not re-tested.

When the Minimum Rating field was cleared, the browser displayed **"Please enter a number."** This prevented the empty-rating case from being tested through the normal frontend form.

Entering a minimum rating of zero was accepted, and recommendations were displayed successfully.

### 4.4 Whitespace-Only Keyword Test

The Keywords field was tested using three spaces while the other search parameters remained unchanged.

The application returned five results, and the first recommendation, Writing Unit Tests with Pytest, retained its score of 9.58.

This was consistent with the expected behaviour of ignoring whitespace-only keywords. However, the entire five-result ordering was not compared individually.

### 4.5 Recommendation Score Breakdown

The first recommendation displayed:

| Category | Displayed score |
|---|---:|
| Relevance | 5.00 |
| Level Fit | 3.00 |
| Quality | 1.00 |
| Practicality | 0.58 |
| **Total** | **9.58** |

The four displayed category values correctly added up to the total score.

The interface also provided explanations for the subject match, difficulty match, rating contribution, and duration suitability.

The Quality score of 1.00 was consistent with the Sprint 4 quality-bonus cap, although this single browser observation does not independently prove the cap for every input.

### 4.6 Resource Link Verification

The **Open Learning Resource** link for resource R015 opened `example.com/r015` in a separate browser tab.

Keyboard navigation and activation were also tested.

The destination is a placeholder rather than a real learning resource. This is a documented catalogue limitation, not evidence of a failed frontend navigation.

## 5. Automated Regression and API Testing

The following automated test command was executed from the repository root:

```bash
python -m pytest data/test_rule_engine.py data/test_sprint3_regression.py tests/test_api.py -q
```

**Result: PASS — 52 tests passed, 2 warnings, 0.28 seconds.**

The test suite covered the recommendation engine, Sprint 3 regression cases, and FastAPI API behaviour. The two warnings concerned deprecated Pydantic validator syntax and did not cause test failures.

The Python environment initially lacked pytest and httpx. Both packages were installed successfully before the final test run.

## 6. Recommendation Evaluation Comparison

The evaluation was run from the data directory:

```bash
python evaluate.py --compare
```

**Result: PASS**

| Metric | Baseline | Current |
|---|---:|---:|
| Hit@1 | 1.000 | 1.000 |
| MRR | 1.000 | 1.000 |
| nDCG@5 | 0.953 | 0.993 |
| Ideal@5 | 1.000 | 1.000 |
| Expected-empty pass rate | 0.500 | 1.000 |
| Hard-filter violations | 0 | 0 |

All four expected-empty cases passed, and no evaluated cases worsened. nDCG@5 improved by 0.040 relative to the recorded baseline.

These measurements apply to the team's existing evaluation cases and do not establish performance on a larger real-world catalogue.

## 7. Known Limitations

- The catalogue contains 30 sample resources with placeholder URLs.
- The evaluation set contains 21 team-authored cases.
- Testing covered the local demonstration environment, not a verified production deployment.
- The empty minimum-rating submission could not be tested through the browser because form validation blocked it.
- The complete ordering of all five recommendations in the whitespace-only keyword test was not individually compared.
- Full WCAG conformance and exhaustive screen-reader compatibility were not verified.
- Existing dependency deprecation warnings remain.

## 8. Conclusion

Sprint 4 frontend verification and automated testing passed for the documented test scope.

The application displayed successful and empty-result states, accepted tested inputs, presented understandable scoring explanations, and supported resource-link activation.

The frontend production build succeeded, all 52 automated tests passed, and the evaluation comparison showed no regressions.

These findings support LearnPath's local demonstration and presentation readiness. They do not establish production deployment or complete accessibility conformance.

**Overall verification outcome: PASS for the completed and documented test scope.**

This report documents verification evidence only and does not claim application-code changes.