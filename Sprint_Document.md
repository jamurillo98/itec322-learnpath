# Sprint Document — Group 5 Rule Recommendation Engine
## Project Summary
**Project name:** Rule‑based Recommendation Engine (TBD)
**Goal:** Deliver an end‑to‑end prototype (frontend → backend → rule engine) by Week 12.
**Current week:** Week 4 (one week mid‑semester break remaining).
**Team size:** 6 members.
**Repo state:** `frontend/` empty; `backend/` minimal FastAPI; `data/` rule scaffold; `vercel.json` configured.
## Team Roles and Assignments

Jerome — Backend Lead (backend, API, deployment)  
Jasim — Backend Support (tests, validation, CI)  
Nishant — Data/Model Lead (rule engine, dataset)  
Aarjan — Data/Model Support (feature engineering, tests)  
Astraea — Frontend Lead (Vite scaffold, UI)  
Maleesha — Frontend Support (styling, state)
## Timeline and Sprints
**Sprint 1 Week 4–5:** Working skeleton
- Deliverables: Minimal Vite app; `/api/recommend` endpoint; `data/rule_engine.py` returns sample recommendations; Vercel serves UI (no 404).
- Acceptance: Production domain loads UI; UI calls `/api/recommend` and displays results; `npm run build` produces `frontend/dist/`.
**Sprint 2 Week 6–8:** Feature build and model prototype
- Deliverables: User input form; results page; baseline ML prototype or improved rule logic; expanded endpoints.
**Sprint 3 Week 9–10:** Improve accuracy and stability
- Deliverables: Model tuning; caching/preprocessing; unit tests; UI polish.
**Sprint 4 Week 11–12:** Final polish and presentation
- Deliverables: Final UI; final model; README and developer docs; presentation slides and demo script.
## Sprint 1 Overview (Simplified)
Sprint 1 establishes the first working vertical slice of the system:
frontend → backend → rule engine → deployment.

All detailed Sprint 1 release notes, tasks, acceptance criteria, and deployment evidence have been moved to a dedicated file:

**See SPRINT1_RELEASE.md for full Sprint 1 details.**
## Quick Start for Developers
### Frontend
```bash
cd frontend
npm install
npm run dev
npm run build
```
## 1. Extended Project Overview
### 1.1 Product Scope
The project delivers a small rule-based recommendation engine for demonstrating
an end-to-end software workflow. A user interacts with a React and Vite web
interface, the interface sends a validated request to a FastAPI endpoint, and
the API delegates recommendation logic to the data layer.
The first release intentionally favors deterministic behavior over model
complexity. Every team member should be able to run the system locally, inspect
the input and output, and explain the result during the final presentation.
The semester objective is to move from a working skeleton to a tested prototype
with a clear path toward data-driven ranking. The prototype must remain small
enough to deploy and demonstrate reliably.
### 1.2 Architecture Explanation
The frontend owns presentation, browser state, and HTTP requests. It should not
contain recommendation rules or duplicate backend validation.
The backend owns the public API contract, request validation, response shaping,
error handling, and integration with the data layer. It should remain thin and
easy to test.
The data layer owns deterministic rules, feature preparation, sample datasets,
and the future model adapter. It should expose a stable function or service
boundary so the backend does not depend on implementation details.
Vercel hosts the built frontend and exposes the FastAPI function through the API
route. Local development uses Vite for the browser and Uvicorn for the API.
### 1.3 ASCII Architecture Diagram
```text
+----------------------+       POST /api/recommend       +---------------------+
|  Browser             | ------------------------------> |  FastAPI            |
|  React + Vite UI     |                                 |  backend/main.py    |
|  form and results    | <------------------------------ |  validation/JSON     |
+----------------------+       recommendation response   +----------+----------+
																																			|
																																			| calls
																																			v
																													 +---------------------+
																													 |  Data layer         |
																													 |  data/rule_engine   |
																													 |  rules and features |
																													 +----------+----------+
																																			|
																																			v
																													 +---------------------+
																													 |  Sample resources   |
																													 |  CSV/JSON fixtures  |
																													 +---------------------+
								 +-----------------------------------------------+
								 | Vercel                                         |
								 | static frontend build + serverless API route   |
								 +-----------------------------------------------+
```
### 1.4 Request Lifecycle
1. The user enters or confirms values in the frontend form.
2. The frontend serializes the values into the documented request schema.
3. The browser sends a `POST` request to `/api/recommend`.
4. FastAPI parses the JSON body and applies Pydantic validation.
5. The endpoint passes the validated payload to the rule engine.
6. The rule engine evaluates deterministic rules and creates ranked results.
7. FastAPI wraps the list in the documented response object.
8. The frontend renders loading, success, or error state.
### 1.5 Rule-Based Recommendation Engine Overview
The baseline engine is a transparent function that accepts a payload and
returns recommendation dictionaries. Rules should be explicit, deterministic,
and independently testable.
Each recommendation should have a stable identifier, a human-readable title,
and a numeric score. New rules should explain which input values they use and
how a score is assigned.
The baseline must provide useful output for the sample payload, a missing or
default user, and at least one alternate input. It must never depend on random
state or an unavailable external service.
Recommended rule order:
1. Normalize input values.
2. Apply eligibility rules.
3. Generate candidate recommendations.
4. Calculate or assign scores.
5. Sort candidates by score.
6. Return the agreed response shape.
### 1.6 Future ML Model Pathway
The deterministic engine is the first implementation of a future recommender
interface. Later work can introduce feature extraction, a training dataset,
offline evaluation, and a model adapter without changing the API contract.
The proposed migration path is:
1. Record representative inputs and expected recommendations.
2. Add a feature preparation module in `data/`.
3. Define a train/validation split and baseline metrics.
4. Compare an ML model with the current rule baseline.
5. Keep a fallback rule engine for unavailable or low-confidence predictions.
6. Version the model artifact and document its input features.
7. Expose the same response schema through FastAPI.
The team should not add ML dependencies until the rule baseline, tests, and
deployment are stable. Explainability and predictable fallback behavior remain
required even after model experimentation begins.
## 2. Team Responsibilities (Deep Version)
### 2.1 Responsibility Matrix

Member      | Primary Area        | Sprint 1                | Sprint 2                | Sprint 3                | Sprint 4
----------- | ------------------- | ------------------------ | ------------------------ | ------------------------ | ------------------------
Jerome      | Backend + Deployment| API + Vercel            | Endpoint expansion       | Reliability              | Release owner
Jasim       | Backend Support     | Tests + CI              | Validation tests         | Monitoring tests         | Release test
Nishant     | Data + Rules        | Baseline rules          | Feature logic            | Model prototype          | Model story
Aarjan      | Data Support        | Fixtures + smoke tests  | Dataset support          | Evaluation               | Demo data
Astraea     | Frontend Lead       | Vite scaffold           | Form + results UI        | UI refinement            | Demo UI
Maleesha    | Frontend Support    | Docs + styling          | State + layout           | Accessibility            | Presentation assets
### 2.2 Responsibilities Per Sprint
Every owner is responsible for implementation, a focused test or verification,
and a short update in the pull request. Support members should review their
area even when the lead makes the code change.
Sprint 1 establishes the vertical slice. Backend, data, and frontend work must
be integrated before the team claims the sprint complete.
Sprint 2 expands the user workflow. The form, API contract, and rules must be
updated together so a new field is not added in only one layer.
Sprint 3 improves accuracy and stability. The team measures behavior, adds
regression tests, and resolves the highest-impact usability or reliability
issues.
Sprint 4 prepares the release. The team freezes the contract, rehearses the
demo, checks production behavior, and documents known limitations.
### 2.3 Folder Ownership

Folder     | Lead      | Support     | Ownership Boundary
---------- | --------- | ----------- | -----------------------------------------
frontend/  | Astraea   | Maleesha    | UI, browser state, API client
backend/   | Jerome    | Jasim       | HTTP contract, validation, tests
data/      | Nishant   | Aarjan      | Rules, fixtures, future features
docs/      | Maleesha  | All members | Decisions, setup, evidence
Frontend code may call the API but may not import Python or rule files.
Backend code may call the data layer but should not contain UI formatting.
Data code may define recommendation logic but should not depend on FastAPI.
Documentation describes actual behavior and must be updated with contract
changes.
### 2.4 Branch Ownership
The owner of a folder is responsible for keeping its branch current, responding
to review comments, and confirming the acceptance criteria. Ownership does not
prevent another member from contributing; it identifies the first reviewer and
the person who confirms the result.
Branches must contain one coherent change. A branch that modifies multiple
folders must explain the integration reason in its pull request.
### 2.5 Expected Weekly Workload
Each member should plan approximately two to four focused hours per week,
including implementation, review, testing, and documentation. Leads may need
additional time during integration and presentation weeks.
The team should agree on a weekly checkpoint. Before the checkpoint, each
member posts completed work, current blocker, next action, and test evidence.
## 3. Branching Strategy
### 3.1 Naming Conventions
Use short, descriptive branch names based on the change type:
| Prefix | Use | Example |
|---|---|---|
| `feature/` | new behavior | `feature/frontend-form` |
| `fix/` | defect correction | `fix/api-validation` |
| `docs/` | documentation only | `docs/sprint-plan` |
| `test/` | test-only work | `test/recommendation-api` |
Use lowercase names and hyphens. Avoid member names, dates, and vague names
such as `changes` or `work`.
### 3.2 Pull Request Workflow
1. Start from an updated `main` branch.
2. Create a branch using the naming convention.
3. Make the smallest coherent change.
4. Run the relevant local checks.
5. Push the branch and open a pull request.
6. Describe the behavior, files, tests, and known limitations.
7. Request the folder owner and one additional reviewer.
8. Resolve comments and rerun checks.
9. Merge after approval and passing CI.
10. Delete the branch after merge.
### 3.3 Review Guidelines
Reviewers should verify behavior before style. Check the API contract, error
paths, input validation, security-sensitive data, tests, and deployment impact.
Every review should answer these questions:
- Does the change satisfy its acceptance criteria?
- Is the behavior covered by an appropriate check?
- Does it preserve the boundaries between folders?
- Does it introduce an undocumented contract change?
- Is the implementation understandable to another team member?
### 3.4 Merge Rules
Only reviewed pull requests may merge to `main`. CI must pass, unresolved
blocking comments must be absent, and the author must update documentation for
user-visible or contract-visible behavior.
Prefer squash merging for focused tasks. Do not force-push `main`. Resolve
conflicts in the feature branch and rerun the checks before merging.
### 3.5 Folder-to-Branch Mapping
| Work area | Typical branch examples |
|---|---|
| Frontend | `feature/frontend-scaffold`, `fix/frontend-error-state` |
| Backend | `feature/api-recommend`, `fix/api-validation` |
| Data | `feature/rule-baseline`, `feature/model-features` |
| Documentation | `docs/sprint-document`, `docs/api-contract` |
Integration branches are allowed only when a task genuinely crosses boundaries
and the pull request identifies each affected folder.
## 4. Repo Structure Deep Dive
### 4.1 `frontend/`
**Purpose:** Browser application, presentation, state, and API client.
**Sprint 1 required files:**
- `package.json`
- `index.html`
- `vite.config.js`
- `src/main.jsx`
- `src/App.jsx`
- `src/api.js`
**Sprint 2–4 expected files:**
- `src/components/InputForm.jsx`
- `src/components/Results.jsx`
- `src/components/LoadingState.jsx`
- `src/components/ErrorMessage.jsx`
- `src/styles.css`
- focused component tests where the team adopts a test runner
**Integration points:** The frontend calls `/api/recommend` and consumes JSON.
It should use relative URLs so the same code works locally behind a proxy and
in production behind Vercel.
**Example file template:**
```jsx
import { useState } from "react";
import { getRecommendation } from "./api";
export default function App() {
	const [result, setResult] = useState(null);
	const [error, setError] = useState(null);
	async function submit(payload) {
		setError(null);
		try {
			setResult(await getRecommendation(payload));
		} catch (requestError) {
			setError(requestError.message);
		}
	}
	return <main>{error ? <p>{error}</p> : JSON.stringify(result)}</main>;
}
```
### 4.2 `backend/`
**Purpose:** FastAPI application, schemas, endpoint behavior, and API tests.
**Sprint 1 required files:**
- `main.py`
- `requirements.txt`
- `tests/test_api.py`
**Sprint 2–4 expected files:**
- `schemas.py` for request and response models
- `services/recommendation_service.py` for orchestration
- `tests/test_validation.py`
- `tests/test_service.py`
- structured logging configuration if needed
**Integration points:** The backend imports or calls the public data-layer
function. It translates validated request data into the data-layer input and
returns the agreed response without exposing internal objects.
**Example file template:**
```python
from fastapi import FastAPI
from pydantic import BaseModel
from data.rule_engine import recommend
app = FastAPI(title="Group 5 Recommendation API")
class RecommendationInput(BaseModel):
		user: str
@app.post("/api/recommend")
def recommendation_endpoint(payload: RecommendationInput):
		return {"recommendations": recommend(payload.model_dump())}
```
### 4.3 `data/`
**Purpose:** Rules, resource data, feature preparation, and model experiments.
**Sprint 1 required files:**
- `rule_engine.py`
- `sample_resources.csv` when used by a rule
- a small sample input fixture
**Sprint 2–4 expected files:**
- `features.py`
- `dataset.py`
- `evaluation.py`
- model or rule configuration files
- documented sample and edge-case fixtures
**Integration points:** The data layer accepts plain validated data and returns
plain serializable dictionaries. It must not require a web framework.
**Example file template:**
```python
def recommend(payload):
		user = payload.get("user", "guest")
		return [
				{"id": 1, "title": f"Top pick for {user}", "score": 0.95},
				{"id": 2, "title": "Secondary suggestion", "score": 0.75},
		]
```
### 4.4 `docs/`
**Purpose:** Developer onboarding, API details, decisions, testing evidence,
and release notes.
**Sprint 1 required files:** `README.md` or equivalent setup instructions and
the root sprint document.
**Sprint 2–4 expected files:** API contract notes, test evidence, model notes,
deployment runbook, known limitations, and presentation checklist.
**Integration points:** Documentation must reference actual paths and commands.
It should be updated in the same pull request as major behavior changes.
**Example documentation template:**
```markdown
# Feature name
## Purpose
Explain the user-visible behavior.
## Local verification
List the exact command and expected result.
## API or data impact
Describe changed inputs, outputs, and compatibility.
```
## 5. Sprint Breakdown (Week 4–12)
### 5.1 Sprint 1: Working Skeleton, Weeks 4–5
**Goal:** Build and deploy one complete vertical slice.
**Deliverables:** Vite app, API endpoint, deterministic rule engine, smoke
tests, CI check, and a production UI that does not return a 404.
**Tasks:**
1. Scaffold the frontend and confirm `npm run build`.
2. Implement `POST /api/recommend`.
3. Return deterministic sample recommendations.
4. Connect the button or form to the endpoint.
5. Add backend tests and a manual browser check.
6. Verify Vercel routing and deployment.
7. Update setup and sprint documentation.
**Acceptance criteria:**
- `frontend/dist/` is generated by the build command.
- The production domain loads the frontend.
- The frontend can call `/api/recommend`.
- The response contains a list of recommendations.
- Invalid input returns a clear validation response.
- Backend tests pass in CI.
**Dependencies:** The frontend needs the API path and response shape. The API
needs the data function. Vercel verification needs committed frontend files.
**Risks:** Empty frontend directory, mismatched routes, missing dependencies,
and local-only API URLs.
**Mitigation:** Build locally, use relative API paths, test from a clean clone,
and record deployment evidence.
**Expected folder output:**
| Folder | Sprint 1 output |
|---|---|
| `frontend/` | Vite app and successful `dist/` build |
| `backend/` | FastAPI endpoint and tests |
| `data/` | deterministic rule function |
| `docs/` | setup and acceptance evidence |
### 5.2 Sprint 2: Feature Build, Weeks 6–8
**Goal:** Turn the skeleton into a usable input and results workflow.
**Deliverables:** User input form, results view, expanded schema, richer rules,
and a first data or model prototype.
**Tasks:**
1. Agree on the input fields and validation rules.
2. Build reusable form components.
3. Add field-level and request-level errors.
4. Expand the backend models and endpoint tests.
5. Add rule categories or feature preparation.
6. Capture representative fixtures.
7. Update API and user documentation.
**Acceptance criteria:**
- A user can submit valid inputs without editing JSON.
- Invalid inputs are explained near the relevant control.
- Results show titles, scores, and stable ordering.
- The backend rejects malformed requests consistently.
- New rules have tests or documented fixtures.
**Dependencies:** Sprint 1 contract and deployment must be stable enough to
extend. The team must agree on field names before parallel implementation.
**Risks:** Scope expansion, inconsistent names, and rules that are hard to
explain.
**Mitigation:** Freeze a small schema, review examples first, and keep a
deterministic fallback for every path.
**Expected folder output:** Frontend components, backend schemas and tests,
data fixtures and features, and updated documentation.
### 5.3 Sprint 3: Accuracy and Stability, Weeks 9–10
**Goal:** Improve recommendation quality and operational confidence.
**Deliverables:** Tuned rules or baseline model comparison, regression tests,
better loading and error states, and a repeatable verification checklist.
**Tasks:**
1. Define a small evaluation set.
2. Measure baseline results.
3. Tune rules or compare a model prototype.
4. Add tests for edge cases and ordering.
5. Improve API logs and failure diagnosis.
6. Test production-like frontend behavior.
7. Resolve the highest-priority defects.
**Acceptance criteria:**
- Evaluation results are recorded and reproducible.
- Existing API examples remain compatible.
- Known edge cases have expected outcomes.
- UI states do not leave users waiting without feedback.
- Deployment can be checked from a clean environment.
**Dependencies:** Representative data and Sprint 2 fixtures are required.
**Risks:** Overfitting to a tiny sample, silent behavior changes, or unstable
third-party dependencies.
**Mitigation:** Retain the baseline, compare before and after, and pin or
document important dependency versions.
**Expected folder output:** Evaluation or regression assets in `data/`, tests
and logging improvements in `backend/`, polished states in `frontend/`, and a
test evidence note in `docs/`.
### 5.4 Sprint 4: Final Polish, Weeks 11–12
**Goal:** Produce a reliable, understandable demonstration and final handoff.
**Deliverables:** Final UI, final rules or model, deployment runbook, README,
slides, demo script, and known-limitations list.
**Tasks:**
1. Freeze the request and response contract.
2. Run the full local verification checklist.
3. Deploy the release candidate.
4. Test the production domain and API.
5. Fix only release-blocking defects.
6. Rehearse the presentation with timing.
7. Tag or record the demonstrated commit.
**Acceptance criteria:**
- The demo completes from a clean browser session.
- The team can explain the architecture and rules.
- Production frontend and API checks pass.
- Documentation matches the demonstrated build.
- Each member has a defined presentation role.
**Dependencies:** All earlier sprint outputs and an available production URL.
**Risks:** Last-minute changes, deployment drift, and unclear speaking roles.
**Mitigation:** Freeze scope, rehearse from the deployed version, and prepare
screenshots or recorded evidence as a fallback.
**Expected folder output:** Release-ready source in all three code folders,
deployment and presentation documentation, and a final verification record.
## 6. Detailed Sprint 1 Execution Plan
### 6.1 Frontend Scaffold
1. Open a terminal at the repository root.
2. Enter the frontend directory with `cd frontend`.
3. Install dependencies with `npm install`.
4. Confirm the Vite entry point is `src/main.jsx`.
5. Confirm `index.html` contains the root element.
6. Render a heading and a recommendation button.
7. Add an API client that uses `/api/recommend`.
8. Run `npm run dev` and open the shown local URL.
9. Click the button and inspect the browser network panel.
10. Stop the dev server after the visual check.
11. Run `npm run build`.
12. Confirm that `frontend/dist/index.html` exists.
Useful commands:
```bash
cd frontend
npm install
npm run dev
npm run build
npm run preview
```
### 6.2 Backend API
1. Create or activate a Python virtual environment.
2. Install `backend/requirements.txt`.
3. Confirm the FastAPI app imports successfully.
4. Define the request model with a required `user` field.
5. Add `POST /api/recommend`.
6. Call `data.rule_engine.recommend` with validated data.
7. Return `{ "recommendations": [...] }`.
8. Return FastAPI validation errors for malformed requests.
9. Run the API with Uvicorn.
10. Test the endpoint with a browser-independent request.
Useful commands:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload
```
On Windows PowerShell, activate with `.venv\\Scripts\\Activate.ps1`. On
Windows Command Prompt, use `.venv\\Scripts\\activate.bat`.
### 6.3 Rule Engine
1. Read the existing rule scaffold before changing it.
2. Define the accepted plain-dictionary payload.
3. Provide a default user value when appropriate.
4. Create at least two deterministic recommendations.
5. Include stable IDs, titles, and scores.
6. Avoid random values and network calls.
7. Call the function directly with sample input.
8. Add edge-case examples for missing values.
Useful command:
```bash
python -c "from data.rule_engine import recommend; print(recommend({'user': 'sample'}))"
```
### 6.4 Integration Flow
```text
User clicks submit
			 |
			 v
React builds JSON payload
			 |
			 v
POST /api/recommend
			 |
			 v
FastAPI validates Input
			 |
			 v
rule_engine.recommend(payload)
			 |
			 v
FastAPI returns recommendations
			 |
			 v
React renders results or error
```
The first integration test should use the exact payload the frontend sends. A
second test should call the API with an invalid payload and verify the error.
### 6.5 Testing Flow
Run backend tests from the repository root:
```bash
pytest -q
```
Run a manual UI test with the backend available:
1. Start Uvicorn.
2. Start Vite in a second terminal.
3. Open the Vite URL.
4. Submit the sample request.
5. Confirm the result list appears.
6. Stop the API or use an invalid request to check the error state.
7. Run `npm run build` after the browser test.
### 6.6 Deployment Flow
1. Confirm the root `vercel.json` is committed.
2. Confirm the frontend build succeeds locally.
3. Confirm API route and frontend route are both present.
4. Push the reviewed branch or merge to `main`.
5. Wait for the Vercel deployment to finish.
6. Open the production root URL.
7. Open browser developer tools and submit a recommendation.
8. Record the deployment URL, commit, and observed response.
## 7. API Contract
### 7.1 Endpoint
| Method | Path | Purpose |
|---|---|---|
| `POST` | `/api/recommend` | Return ranked recommendations |
The endpoint accepts JSON and should return JSON for both success and validation
failures. The frontend must use the relative path `/api/recommend`.
### 7.2 Request Schema
Sprint 1 request:
```json
{
	"user": "sample"
}
```
| Field | Type | Required | Rules |
|---|---|---|---|
| `user` | string | yes | non-empty after trimming |
Later sprints may add fields, but additions must be documented and tested. The
backend remains the source of truth for validation.
### 7.3 Response Schema
```json
{
	"recommendations": [
		{
			"id": 1,
			"title": "Top pick for sample",
			"score": 0.95
		}
	]
}
```
| Field | Type | Meaning |
|---|---|---|
| `recommendations` | array | ranked result list |
| `id` | integer or string | stable recommendation identifier |
| `title` | string | display label |
| `score` | number | comparable ranking score |
### 7.4 Example Payloads
Valid request:
```json
{"user":"sample"}
```
Valid alternate request:
```json
{"user":"test-user"}
```
Invalid request with missing field:
```json
{}
```
Invalid request with the wrong type:
```json
{"user": 42}
```
### 7.5 Error Handling
Validation failures should use FastAPI's standard `422` response unless the
team explicitly documents a different error envelope. Unexpected server errors
should return an appropriate `5xx` status and should not expose stack traces to
the browser.
The frontend must distinguish loading, successful empty results, validation
errors, network errors, and unexpected server errors. Empty recommendations are
not automatically a network failure.
### 7.6 Frontend Call
```js
export async function getRecommendation(payload) {
	const response = await fetch("/api/recommend", {
		method: "POST",
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify(payload)
	});
	if (!response.ok) {
		throw new Error(`Recommendation request failed: ${response.status}`);
	}
	return response.json();
}
```
## 8. Frontend Prompts
### 8.1 Component Structure Prompt
> Build a small React component structure for a recommendation form and results
> view. Keep components focused, pass data through explicit props, and keep API
> calls outside presentational components. Include loading, empty, success, and
> error states.
### 8.2 API Calls Prompt
> Create a frontend API client for `POST /api/recommend`. Use a relative URL,
> JSON headers, explicit response checking, and an error that includes the HTTP
> status. Do not place rule-engine logic in the browser.
### 8.3 State Management Prompt
> Add local React state for form values, request status, results, and errors.
> Prevent duplicate submissions while a request is in progress and clear stale
> errors when a new request starts.
### 8.4 Error Handling Prompt
> Design accessible error handling for validation failures, network failures,
> server failures, and empty results. Keep the user's input visible so they can
> correct it without starting over.
### 8.5 UI Layout Prompt
> Create a clear, responsive recommendation screen with a heading, short
> description, input area, primary submit action, loading state, and readable
> results. Use simple spacing and strong hierarchy without hiding important
> error text.
### 8.6 Folder Structure Prompt
> Propose a minimal Vite React folder structure for `src/components`, an API
> client, styles, and tests. Keep the structure shallow until repeated patterns
> justify additional folders.
## 9. Backend Prompts
### 9.1 FastAPI Structure Prompt
> Implement a minimal FastAPI application with a typed request model, a
> `POST /api/recommend` endpoint, standard validation responses, and a clear
> import boundary to the data rule engine.
### 9.2 Module Layout Prompt
> Suggest a backend module layout that separates HTTP routes, Pydantic schemas,
> recommendation orchestration, and tests. Do not introduce abstractions that
> are not needed by the current endpoint.
### 9.3 Testing Strategy Prompt
> Write focused FastAPI tests for the health route, a valid recommendation
> request, missing required input, wrong input type, and response shape. Keep
> tests deterministic and independent of a deployed service.
### 9.4 Logging Prompt
> Add minimal useful logging around request handling and failures without
> logging secrets or full sensitive payloads. Use stable event names and include
> enough context to diagnose a production API error.
### 9.5 Rule Engine Integration Prompt
> Connect the FastAPI endpoint to a plain Python recommendation function. Keep
> the web layer responsible for validation and the data layer responsible for
> recommendation logic. Return serializable results and preserve the API
> response contract.
## 10. Data/Model Prompts
### 10.1 Rule Engine Structure Prompt
> Design a deterministic rule engine with input normalization, candidate
> generation, scoring, ordering, and a serializable result. Include examples
> and tests for default and alternate inputs.
### 10.2 Dataset Preparation Prompt
> Prepare a small documented dataset for recommendation experiments. Describe
> each column, identify missing values, preserve a source or fixture version,
> and avoid using personal or secret data.
### 10.3 Transition to ML Prompt
> Propose a gradual transition from rules to an ML baseline. Define features,
> labels, train and validation splits, metrics, confidence thresholds, and a
> deterministic fallback when the model cannot make a reliable prediction.
### 10.4 Backend Data-Layer Prompt
> Define a narrow data-layer function that accepts validated plain data and
> returns plain dictionaries. Keep imports one-way from the backend into the
> data layer and make the function easy to replace with a model adapter later.
## 11. Integration Guide
### 11.1 Local End-to-End Test
Use two terminals from the repository root.
Terminal one:
```bash
uvicorn backend.main:app --reload
```
Terminal two:
```bash
cd frontend
npm run dev
```
Open the Vite URL, submit the form, and confirm a successful response. If the
frontend calls the wrong origin, configure the existing Vite proxy or use the
same local deployment arrangement documented by the team.
### 11.2 Direct API Test
With Uvicorn running, use a request tool such as curl:
```bash
curl -X POST http://127.0.0.1:8000/api/recommend ^
	-H "Content-Type: application/json" ^
	-d "{\"user\":\"sample\"}"
```
On macOS or Linux, use backslashes for line continuation instead of carets.
### 11.3 Debugging API Calls
1. Open browser developer tools.
2. Select the Network tab.
3. Submit the recommendation form.
4. Open the `/api/recommend` request.
5. Inspect method, URL, request body, status, and response body.
6. Compare each value with the API contract.
7. Check the Uvicorn terminal for traceback or validation output.
### 11.4 Common Errors and Fixes
| Symptom | Likely cause | Fix |
|---|---|---|
| frontend 404 | wrong static route | verify Vercel route and build output |
| API 404 | wrong path or function destination | use `/api/recommend` and inspect deployment |
| API 422 | request shape mismatch | compare JSON with the schema |
| browser CORS error | different local origins | use a Vite proxy or configure CORS deliberately |
| build fails | missing npm dependency | run `npm install` and inspect the first error |
| blank page | missing root element or entry import | inspect `index.html` and `src/main.jsx` |
| empty results | rule condition excludes input | test the rule function directly |
| production-only failure | environment or route drift | compare deployed paths with local paths |
### 11.5 Production Test
1. Open the deployed root URL in a private browser window.
2. Confirm the initial HTML and static assets load.
3. Submit a valid sample request.
4. Confirm the network request uses the production `/api/recommend` path.
5. Confirm the response status and recommendation list.
6. Test an invalid request through the UI if the UI supports it.
7. Record the URL, commit, timestamp, and result.
## 12. Deployment Guide
### 12.1 Vercel Configuration
The repository root contains `vercel.json`. The configuration uses the frontend
package as the static build source and sends API requests to the FastAPI entry
point. The frontend catch-all serves the generated `index.html`.
Required deployment facts:
- frontend package path: `frontend/package.json`
- build tool: `@vercel/static-build`
- static output: `dist`
- API destination: `backend/main.py`
- frontend destination: `frontend/dist/index.html`
### 12.2 Build Steps
Run the same build locally before deployment:
```bash
cd frontend
npm install
npm run build
```
Review the generated `dist/` directory and ensure the JavaScript asset paths
resolve from the deployed site.
### 12.3 Troubleshooting 404 Errors
Check the following in order:
1. `vercel.json` is at the repository root.
2. `frontend/package.json` exists and has a `build` script.
3. Vite generates `frontend/dist/index.html`.
4. The static-build configuration uses `distDir: "dist"`.
5. The frontend route comes after the API route.
6. The deployment was created from the intended commit.
7. Browser cache is not hiding a newer deployment.
Do not fix a 404 by changing backend code. First inspect the deployment build
logs and the generated output path.
### 12.4 Verify Production
Use the production URL to check the root page, a nested frontend path if one
exists, and the API request. Capture a screenshot or response evidence for the
Sprint 1 acceptance record.
### 12.5 Test API in Production
```bash
curl -X POST https://YOUR-DOMAIN.example/api/recommend ^
	-H "Content-Type: application/json" ^
	-d "{\"user\":\"production-check\"}"
```
Replace the placeholder domain with the actual deployment URL. Never put API
keys or private data in this command or in committed documentation.
## 13. GitHub Issues Mapping (Updated for Sprint 1 Release)

Issue 1: Scaffold Frontend  
Owner: Astraea  
Branch: feature/frontend-scaffold  
Folder: frontend/  
Description: Create the minimal React + Vite application with a visible heading, request action, and successful production build.  
Acceptance criteria: npm run build succeeds, dist/index.html exists, and the local page renders without console errors.

Issue 2: Implement Recommendation API  
Owner: Jerome  
Branch: feature/api-recommend  
Folder: backend/  
Description: Add the validated POST /api/recommend endpoint and return the agreed recommendation response.  
Acceptance criteria: Valid input returns 200, the response contains a list, and malformed input returns a documented validation error.

Issue 3: Implement Rule Engine Baseline  
Owner: Nishant  
Branch: feature/rule-baseline  
Folder: data/  
Description: Implement deterministic recommendations for sample and alternate user inputs with stable IDs, titles, and scores.  
Acceptance criteria: Direct calls are deterministic, serializable, and covered by representative examples.

Issue 4: Local E2E Smoke Test  
Owners: Jasim & Aarjan  
Branch: test/local-e2e  
Folders: backend/, frontend/  
Description: Verify the browser request reaches the API and results render.  
Acceptance criteria: The smoke-test steps are repeatable, the valid flow passes, and at least one invalid flow is recorded.

Issue 5: Verify Vercel Deployment  
Owner: Jerome  
Branch: fix/vercel-routing  
Files: root vercel.json and deployment evidence  
Description: Verify static build output, API routing, root-page loading, and production recommendation requests.  
Acceptance criteria: Production UI loads, API requests reach FastAPI, and the deployment commit and URL are recorded.

Issue 6: Update README and Sprint Document  
Owner: Maleesha  
Branch: docs/sprint-1  
Files: documentation files only  
Description: Document setup, contract, sprint progress, known limitations, and verification commands.  
Acceptance criteria: A new member can follow the documented commands and the sprint document reflects the actual implementation.
## 14. VS Code Workflow
### 14.1 Recommended Extensions
Use extensions that match the project and team environment:
- Python language support
- Pylance or the team's selected Python analyzer
- ESLint if linting is configured
- Prettier if formatting is adopted by the team
- GitHub Pull Requests and Issues
- GitLens or equivalent Git history tooling, if permitted
- REST Client or an API testing extension
The team should document exact required extensions separately from optional
personal tooling. Do not make a build depend on an editor extension.
### 14.2 Run Frontend and Backend in VS Code
Open two integrated terminals.
Backend terminal:
```bash
uvicorn backend.main:app --reload
```
Frontend terminal:
```bash
cd frontend
npm run dev
```
Use the terminal selector to identify each process. Stop both processes before
switching branches or installing dependencies.
### 14.3 Integrated Terminal Practices
- Start commands from the documented directory.
- Keep the API and frontend logs visible in separate terminals.
- Use a third terminal for tests and Git commands.
- Record the first meaningful error, not only the final stack line.
- Avoid committing virtual environments, `node_modules`, or build output.
### 14.4 Effective Copilot Use
Give Copilot the relevant file, contract, acceptance criteria, and constraints.
Ask for a small change and a focused test. Review generated code line by line,
especially imports, error paths, file paths, and dependency changes.
Useful prompt pattern:
> In `backend/main.py`, implement only the documented `POST /api/recommend`
> contract. Preserve existing routes, use the existing data function, and add
> focused tests for valid and invalid input. Do not modify frontend or data code.
Ask Copilot to explain a failing test before accepting a broad rewrite. Keep
the human owner responsible for architecture and acceptance decisions.
### 14.5 Test API Inside VS Code
Use the REST Client extension or a terminal request. A minimal request file can
contain:
```http
POST http://127.0.0.1:8000/api/recommend
Content-Type: application/json
{
	"user": "vscode-check"
}
```
Compare the returned status, headers, and JSON with the API contract.
## 15. Final Presentation Plan (Week 12)
### 15.1 Demo Flow
1. Introduce the problem and the recommendation goal.
2. Show the three-layer architecture diagram.
3. Open the deployed frontend.
4. Submit a representative user input.
5. Explain the returned recommendations and scores.
6. Show the API request in developer tools or a prepared request.
7. Explain one rule from the data layer.
8. Show a validation or error case.
9. Summarize testing and deployment evidence.
10. Discuss the future ML pathway and limitations.
### 15.2 Slide Structure
| Slide | Topic | Speaker |
|---|---|---|
| 1 | project goal and team | Member 6 |
| 2 | user workflow | Member 5 |
| 3 | architecture | Jerome |
| 4 | API contract | Member 4 |
| 5 | rule engine | Nishant |
| 6 | data and future ML | Aarjan |
| 7 | testing and deployment | Jerome or Member 4 |
| 8 | live demo and conclusion | all as assigned |
### 15.3 Talking Points
- The system demonstrates a complete request path.
- The API contract keeps frontend and data concerns separate.
- The baseline is deterministic and explainable.
- Validation prevents malformed input from reaching business logic.
- Tests cover the health path, recommendation path, and invalid requests.
- Vercel serves the built frontend and routes API calls to FastAPI.
- The design supports a future model without requiring a new frontend contract.
- Current limitations are acknowledged rather than hidden.
### 15.4 Roles During Presentation
The primary presenter introduces the product and controls the slides. The
frontend presenter operates the browser demo. The backend presenter explains
the request and response. The data presenter explains rules and future ML.
One member should monitor the deployed URL and be ready with a prepared
response or screenshot if the live service is unavailable. Another member
should answer implementation and testing questions.
### 15.5 Live Demo Instructions
Before presenting:
1. Open the production URL in a private window.
2. Confirm static assets load.
3. Submit the known-good sample input.
4. Confirm the results are visible.
5. Open a prepared API request in a second tab.
6. Keep screenshots and response examples available offline.
7. Close unrelated tabs and notifications.
During the demo, narrate the request flow while the result is loading. Do not
edit source files or install dependencies live. If the network fails, use the
prepared evidence and explain the intended production check honestly.
### 15.6 Final Release Checklist
- [ ] Frontend build succeeds from a clean install.
- [ ] Backend tests pass.
- [ ] Rule engine output is deterministic.
- [ ] API request and response match documentation.
- [ ] Vercel root page loads.
- [ ] Production API request succeeds.
- [ ] Validation error behavior is understood.
- [ ] README and sprint document are current.
- [ ] Presentation slides match the deployed implementation.
- [ ] Demo fallback evidence is ready.
### Backend
```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload
```
## Definition of Done for Sprint 1
- Frontend builds and `dist/` exists.
- Production domain serves UI.
- UI calls backend and receives deterministic recommendations.
- Basic tests for backend pass.
## Communication and Workflow
- Create GitHub issues for each Sprint 1 task and assign owners.
- Use branches `feature/<area>-<short>` for work (e.g., `feature/frontend-scaffold`).
- Open PRs for review and merge to `main` when CI passes.
---
## Reference Files
### `frontend/package.json`
```json
{
	"name": "verifai-frontend",
	"version": "0.1.0",
	"private": true,
	"scripts": {
		"dev": "vite",
		"build": "vite build",
		"preview": "vite preview"
	},
	"dependencies": {
		"react": "^18.2.0",
		"react-dom": "^18.2.0"
	},
	"devDependencies": {
		"vite": "^5.0.0"
	}
}
```
### `frontend/index.html`
```html
<!doctype html>
<html>
	<head>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1.0" />
		<title>Rule Recommendation Engine</title>
	</head>
	<body>
		<div id="root"></div>
		<script type="module" src="/src/main.jsx"></script>
	</body>
</html>
```
### `frontend/vite.config.js`
```js
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
export default defineConfig({
	plugins: [react()],
	build: {
		outDir: "dist"
	}
});
```
### `frontend/src/main.jsx`
```jsx
import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
createRoot(document.getElementById("root")).render(<App />);
```
### `frontend/src/App.jsx`
```jsx
import React, { useState } from "react";
import { getRecommendation } from "./api";
export default function App() {
	const [result, setResult] = useState(null);
	const [loading, setLoading] = useState(false);
	const [error, setError] = useState(null);
	async function handleClick() {
		setLoading(true);
		setError(null);
		try {
			const res = await getRecommendation();
			setResult(res);
		} catch (e) {
			setError("Failed to fetch recommendation");
		} finally {
			setLoading(false);
		}
	}
	return (
		<div style={{ padding: 24, fontFamily: "system-ui, Arial" }}>
			<h1>Rule Recommendation Engine</h1>
			<p>Click the button to get a sample recommendation from the backend.</p>
			<button onClick={handleClick} disabled={loading}>
				{loading ? "Loading..." : "Get Recommendation"}
			</button>
			{error && <div style={{ color: "crimson", marginTop: 12 }}>{error}</div>}
			{result && (
				<pre style={{ marginTop: 16, background: "#f6f8fa", padding: 12 }}>
					{JSON.stringify(result, null, 2)}
				</pre>
			)}
		</div>
	);
}
```
### `frontend/src/api.js`
```js
export async function getRecommendation() {
	const resp = await fetch("/api/recommend", {
		method: "POST",
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify({ user: "sample" })
	});
	if (!resp.ok) throw new Error("Network response was not ok");
	return resp.json();
}
```
### `backend/main.py`
```python
from fastapi import FastAPI
from pydantic import BaseModel
from data.rule_engine import recommend
app = FastAPI(title="Group 5 Recommendation API")
class Input(BaseModel):
		user: str
@app.get("/")
def root():
		return {"status": "ok", "message": "Backend running"}
@app.post("/api/recommend")
def recommend_endpoint(payload: Input):
		result = recommend(payload.dict())
		return {"recommendations": result}
```
### `backend/requirements.txt`
```text
fastapi
uvicorn
python-dotenv
```
### `backend/tests/test_api.py`
```python
from fastapi.testclient import TestClient
from backend.main import app
client = TestClient(app)
def test_root():
		resp = client.get("/")
		assert resp.status_code == 200
		assert resp.json().get("status") == "ok"
def test_recommend():
		resp = client.post("/api/recommend", json={"user": "test"})
		assert resp.status_code == 200
		data = resp.json()
		assert "recommendations" in data
		assert isinstance(data["recommendations"], list)
```
### `data/rule_engine.py`
```python
# Minimal deterministic rule engine for Sprint 1
def recommend(payload):
		"""
		payload example: {"user": "sample"}
		Returns a list of recommendation dicts.
		"""
		user = payload.get("user", "guest")
		# Simple deterministic rules for demo
		base = [
				{"id": 1, "title": f"Top pick for {user}", "score": 0.95},
				{"id": 2, "title": "Secondary suggestion", "score": 0.75}
		]
		return base
```
### `data/sample_input.json`
```json
{
	"user": "sample"
}
```
### `docs/README.md`
```markdown
# Group 5 Rule Recommendation Engine
## Quick start
### Frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev` (development)
4. `npm run build` (production build)
### Backend
1. `python -m venv .venv`
2. `source .venv/bin/activate`  # macOS/Linux
3. `pip install -r backend/requirements.txt`
4. `uvicorn backend.main:app --reload`
## Project structure
- `frontend/` — React + Vite app
- `backend/` — FastAPI app and tests
- `data/` — rule engine and sample data
- `docs/` — documentation and sprint doc
## How to run full local integration
1. Build frontend: `cd frontend && npm install && npm run build`
2. Start backend: `uvicorn backend.main:app --reload`
3. Preview frontend: `npx serve frontend/dist` or use `vite preview`
4. Open browser and test the UI calling `/api/recommend`
## Contribution
- Use feature branches `feature/<area>-<short>`
- Create PRs and assign reviewers
- Add issues for tasks and assign owners
```
### `.github/ISSUE_TEMPLATE.md`
```markdown
---
name: Task
about: Create a task for Sprint 1
title: "[TASK] "
labels: ["task"]
assignees: []
---
**Summary**
A short summary of the task.
**Owner**
@username
**Description**
- What to do
- Acceptance criteria
**Steps**
1. Step one
2. Step two
**Notes**
Any additional context or links
```
### `.github/workflows/ci.yml`
```yaml
name: CI
on:
	push:
		branches: [ main ]
	pull_request:
		branches: [ main ]
jobs:
	test-backend:
		runs-on: ubuntu-latest
		steps:
			- uses: actions/checkout@v4
			- name: Set up Python
				uses: actions/setup-python@v4
				with:
					python-version: "3.10"
			- name: Install dependencies
				run: |
					python -m venv .venv
					. .venv/bin/activate
					pip install -r backend/requirements.txt
					pip install pytest
			- name: Run tests
				run: |
					. .venv/bin/activate
					pytest -q
```
