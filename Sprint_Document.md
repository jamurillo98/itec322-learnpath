# Sprint Document — Group 5 Rule Recommendation Engine

## Project Summary
**Project name:** Rule‑based Recommendation Engine (TBD)
**Goal:** Deliver an end‑to‑end prototype (frontend → backend → rule engine) by Week 12.
**Current week:** Week 4 (one week mid‑semester break remaining).
**Team size:** 6 members.
**Repo state:** `frontend/` empty; `backend/` minimal FastAPI; `data/` rule scaffold; `vercel.json` configured.

## Team Roles and Assignments
- **Jerome** — Backend Lead (backend, API, deployment)
- **Member 4** — Backend Support (tests, validation, CI)
- **Nishant** — Data/Model Lead (rule engine, dataset)
- **Aarjan** — Data/Model Support (feature engineering, tests)
- **Member 5** — Frontend Lead (Vite scaffold, UI)
- **Member 6** — Frontend Support (styling, state)

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

## Sprint 1 Tasks and Owners
1. **Scaffold frontend** — Member 5
2. **Implement /api/recommend** — Jerome
3. **Implement rule engine baseline** — Nishant
4. **Local integration and tests** — Member 4 & Aarjan
5. **Vercel deployment check** — Jerome
6. **Documentation and issues** — Member 6

## Quick Start for Developers
### Frontend
```bash
cd frontend
npm install
npm run dev
npm run build
```

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
