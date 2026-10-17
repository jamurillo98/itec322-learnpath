# Sprint 3 — Frontend Verification and Polish

**Owner:** Maleesha (Frontend)
**Branch:** `feature/maleesha-sprint3`
**Date:** 17 October 2026

This document records the Sprint 3 frontend deliverables from
`docs/SPRINT3_RELEASE.md`:

- Review and polish loading, error, empty-result, and successful-result states
- Verify that scores and explanations remain understandable and accessible

Screenshots are in `docs/sprint3-evidence/`.

---

## 1. Test environment

| Item         | Value                                                                                                                |
| ------------ | -------------------------------------------------------------------------------------------------------------------- |
| OS / browser | Windows 11, Microsoft Edge                                                                                           |
| Backend      | `uvicorn backend.main:app --reload` from the repository root, serving `http://127.0.0.1:8000`                        |
| Frontend     | `cd frontend`, `npm install`, `npm run dev` (Vite 5.4.21)                                                            |
| Frontend URL | `http://localhost:5174` (Vite moved from 5173 because that port was already in use; this is expected Vite behaviour) |

---

## 2. Browser verification of UI states

| State                      | Input                                                         | Expected                                                      | Result                                                                                                                                                                                                                                                               | Evidence              |
| -------------------------- | ------------------------------------------------------------- | ------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- |
| Success                    | `programming`, Beginner, max 120 min, min rating 3, 5 results | Five ranked cards with total score, breakdown and explanation | **Pass.** Five results returned in descending score order: R012 (10.37), R001 (10.32), R009 (10.25), R005 (9.9), R010 (9.88)                                                                                                                                         | `success.png`         |
| Empty result               | `cooking`, Beginner, max 5 min, min rating 5                  | Clear "no results" message with guidance                      | **Pass.** "No matching resources found" heading with suggestions to broaden the search                                                                                                                                                                               | `empty.png`           |
| Service error              | Any valid search with the backend stopped                     | Friendly, actionable error                                    | **Pass.** Red error box: "The recommendation service is unavailable right now. Please make sure the backend is running and try again." The Vite terminal logged `http proxy error: /api/recommend ... ECONNREFUSED 127.0.0.1:8000`                                   | `error.png`           |
| Loading                    | Success search with DevTools throttling set to Slow 4G        | Spinner shown while waiting; button disabled                  | **Partly verified.** The request completed in 620 ms and the results then rendered. The loading state was too brief to capture in a screenshot; it is shown while `status === "loading"` (`App.jsx`). A slower throttling profile (3G) can be used to capture it     | `network-request.png` |
| Invalid request (HTTP 422) | Not reachable from the browser                                | —                                                             | **Not exercised in the browser.** The form's HTML validation (`required`, `min`, `max`) blocks invalid input before a request is sent. The 422 path is covered by the backend API tests; the frontend maps 422 responses to a field-specific message (see section 4) | —                     |

**Network evidence:** DevTools showed one `recommend` request, status **200**,
type `fetch`, initiated by `App.jsx:48`, 2.9 kB, 620 ms. This confirms the
browser calls the relative path `/api/recommend` and the Vite proxy forwards it
to the backend.

---

## 3. Scores and explanations: review findings

Reviewing the success state before changes found these problems:

| #   | Problem                                                                                       | Impact                                                                                        |
| --- | --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| 1   | Category scores (e.g. "Relevance 5", "Practicality 0.667") had no description                 | Users could not tell what each number measures or whether it is good                          |
| 2   | The total score was not explained                                                             | It is the sum of the four category scores (5 + 3 + 1.7 + 0.667 = 10.367), but nothing said so |
| 3   | Inconsistent precision (10.367, 0.667, 0.625)                                                 | Harder to scan and compare                                                                    |
| 4   | "Why recommended" was one long semicolon-separated sentence                                   | Hard to read                                                                                  |
| 5   | The ↗ arrow was read aloud as "north east arrow"; links did not warn that they open a new tab | Screen-reader confusion                                                                       |
| 6   | Keyboard and screen-reader focus stayed on the button after a search                          | Users were not taken to, or told about, the results                                           |
| 7   | Error messages were technical ("Request failed (500)")                                        | Not actionable for users                                                                      |
| 8   | The empty state gave no guidance                                                              | Users did not know what to change                                                             |
| 9   | The form, error box, results and header had different widths                                  | Edges did not line up                                                                         |

---

## 4. Changes made

### `frontend/src/components/Results.jsx`

- Each category score shows a one-line explanation:
  - Relevance: "How well it matches your subject and keywords"
  - Level Fit: "How well the difficulty matches your level"
  - Quality: "How far its rating is above your minimum"
  - Practicality: "How well it fits your time limit"
- The summary line explains ranking: each total score is the sum of its four
  category scores, and a higher score means a better match.
- Scores are shown with at most two decimal places (display only; the API
  values are unchanged).
- "Why recommended" is split into a bulleted list.
- The score breakdown uses a description list (`<dl>`, `<dt>`, `<dd>`) so
  assistive technology reads each label with its value.
- Each card is labelled by its title and includes a screen-reader-only rank
  ("Rank 1: ...").
- The ↗ arrow is hidden from screen readers (`aria-hidden`), and each link
  announces "Open Learning Resource for {title} (opens in a new tab)".
- After each search, focus moves to the results heading (or the empty-state
  heading), which also scrolls the results into view.
- The empty state now has a heading and suggestions.

### `frontend/src/App.jsx`

- Network failures: "Could not reach the recommendation service. Check your
  connection and that the backend is running."
- HTTP 5xx: "The recommendation service is unavailable right now. Please make
  sure the backend is running and try again."
- HTTP 422: names the form field, e.g. _Please check "Minimum Rating": ..._
- Unexpected response shape: "The server sent an unexpected response."
- The request contract (`POST /api/recommend`, same payload) is unchanged.

### `frontend/src/theme.css`

- Added `.sr-only`, `.score-hint`, `.reason-list` and `.results-heading` styles.
- Aligned the main column (880px) and header text (848px) so the form, error
  box, results and header share the same edges.

No backend, API contract, rule-engine or data files were changed.

---

## 5. Local frontend-to-API connection

- `frontend/vite.config.js` proxies `/api` to `http://127.0.0.1:8000`, and the
  frontend calls the relative path `/api/recommend`.
- Confirmed in the browser: DevTools showed the `recommend` request returning
  200, and stopping the backend produced the proxy error
  `ECONNREFUSED 127.0.0.1:8000` with the friendly error message on screen.

---

## 6. Build check

`npm run build` must succeed on this branch before merging (CI runs the same
check).

---

## 7. Known limitations

- The invalid-request (422) path was not exercised in the browser, because form
  validation prevents it (covered by API tests).
- Testing used Microsoft Edge on Windows only. Other browsers and a full
  screen-reader walkthrough were not tested.
