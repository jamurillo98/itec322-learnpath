# Frontend

The React/Vite frontend collects learning preferences, calls `POST /api/recommend`, and renders deterministic scored recommendations. It includes idle, loading, HTTP/network/JSON error, empty-results, and success states.

## Run locally

Start the backend from the repository root with `uvicorn backend.main:app --reload`, then run:

```text
cd frontend
npm install
npm run dev
```

The Vite development server proxies `/api` to `http://127.0.0.1:8000`. Build the production assets with `npm run build`.

The form values are controlled in `src/components/InputForm.jsx`; results are rendered by `src/components/Results.jsx` from the API's `{ "recommendations": [] }` response envelope.
