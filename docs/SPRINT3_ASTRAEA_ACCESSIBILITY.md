# Sprint 3 — Astraea Accessibility Verification

**Project:** LearnPath  
**Sprint:** 3 — Accuracy and Stability  
**Testing date:** 24 October 2026  
**Test environment:** macOS (MacBook Air), Safari, Apple VoiceOver  
**Branch:** `feature/astraea-sprint3-accessibility`  
**Scope:** Manual frontend accessibility verification

## 1. Objective

This report documents manual accessibility testing of the LearnPath web application, focusing on keyboard navigation, screen-reader compatibility, form validation, recommendation results, empty-result feedback, service-error handling, and application recovery.

The purpose was to assess whether users relying on keyboard navigation or assistive technologies can interact with the recommendation interface and understand its feedback.

## 2. Test Environment

- Operating system: macOS
- Browser: Safari
- Screen reader: Apple VoiceOver
- Frontend: React and Vite, running locally at `http://localhost:5173`
- Backend: FastAPI with Uvicorn, running at `http://127.0.0.1:8000`
- Accessibility testing: Manual browser and screen-reader interaction

## 3. Tests Performed and Results

| Test | Result | Observation |
|---|---|---|
| Form field accessibility | Pass | VoiceOver recognised the six form controls and announced their labels and control types during navigation. |
| Submit button accessibility | Pass | VoiceOver identified the Find Recommendations button. |
| Keyboard focus visibility | Pass | Safari displayed a visible focus outline around the submit button. |
| Keyboard-only form submission | Pass | The form was submitted using keyboard navigation, and recommendations appeared. |
| Required-field validation | Pass | Submitting an incomplete form moved focus to the required Subject field and showed a validation message. |
| Successful recommendation display | Pass | Five recommendation results appeared with titles, scores, and resource details. |
| Empty-results visual feedback | Pass | A clear no-results heading and suggestions appeared. |
| Empty-results VoiceOver navigation | Pass | VoiceOver read the no-results heading when navigated to. |
| Service-error visual feedback | Pass | Stopping the backend produced an understandable error message. |
| Service-error VoiceOver navigation | Pass | VoiceOver successfully read the service-error message when navigated to. |
| Backend recovery | Pass | After restarting the backend, a new valid request displayed five recommendations. |

## 4. Keyboard Navigation Verification

Safari's keyboard navigation setting was enabled to allow the Tab key to highlight interactive elements.

The tester navigated through the form controls using the keyboard and reached the Find Recommendations button. The button displayed a clear visible focus indicator.

Pressing Space activated the button. When a required field was empty, Safari displayed the native validation prompt and returned focus to the missing field.

After completing the required inputs, keyboard activation successfully submitted the form and displayed recommendation results.

## 5. Screen-Reader Verification

Apple VoiceOver was used to navigate the LearnPath interface.

VoiceOver identified form controls, including the subject input and recommendation button. Navigation through webpage content was performed using VoiceOver keyboard commands.

The empty-results heading and service-error message were readable through VoiceOver navigation.

These findings confirm that the tested elements can be accessed through the screen reader. They do not establish that every dynamic update is automatically announced.

## 6. Successful Recommendation Test

The successful recommendation test used:

- Subject: programming
- Difficulty: beginner
- Maximum duration: 60 minutes
- Minimum rating: 4
- Keywords: hands-on
- Number of results: 5

The system returned five learning resources. The interface displayed ranked recommendation cards with resource information and scores.

The successful result was also reproduced after the backend recovery test.

## 7. Empty-Results Test

The following search was used:

- Subject: cooking
- Difficulty: beginner
- Maximum duration: 5 minutes
- Minimum rating: 5
- Keywords: empty
- Number of results: 5

LearnPath displayed the heading **No matching resources found** and suggested broadening the subject, increasing the maximum duration, lowering the minimum rating, or using fewer keywords.

VoiceOver successfully read the no-results heading during manual navigation.

## 8. Service-Error Test

The FastAPI backend was deliberately stopped while the frontend remained running.

A recommendation request produced the following message:

"The recommendation service is unavailable right now. Please make sure the backend is running and try again."

The message appeared in a visually distinguishable red-bordered area.

VoiceOver successfully read the error text when the tester navigated to it.

The backend was then restarted using Uvicorn. A new recommendation request returned five results, confirming successful recovery.

## 9. Limitations and Remaining Verification

The following areas were not fully verified during this testing session:

- Whether VoiceOver automatically announces newly displayed success, empty-result, or service-error messages without manual navigation.
- Whether focus consistently moves to the results heading after every submission.
- A complete screen-reader walkthrough of every recommendation card, score description, explanation, and external link.
- Accessibility behaviour in browsers other than Safari.
- Automated accessibility audits and formal WCAG conformance assessment.
- Loading-state announcement and keyboard behaviour during delayed requests.

These items remain follow-up verification activities outside the scoped
manual checks completed in this report; they are not counted as passed tests.

## 10. Conclusion

Manual accessibility testing demonstrated that LearnPath's core recommendation form supports keyboard navigation and submission in Safari, and that key form controls, empty-result feedback, and service-error messages are accessible through Apple VoiceOver navigation.

The application also recovered successfully after the backend was restarted.

The tested behaviours passed, but additional testing is required before claiming comprehensive screen-reader accessibility or WCAG compliance.

**Overall result:** Manual accessibility verification completed for the tested workflows, with explicitly documented limitations.

## Sprint 3 Deliverable Closure

Astraea's scoped manual accessibility verification deliverable is complete.
The tests and their results are documented above. The unverified areas listed
in Section 9 remain limitations: this report does not claim exhaustive
screen-reader coverage or formal WCAG conformance.