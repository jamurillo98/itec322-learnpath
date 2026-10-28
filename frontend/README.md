# Frontend

The React/Vite frontend collects learning preferences, calls `POST {VITE_API_URL}/recommend`, and renders deterministic scored recommendations. It includes idle, loading, HTTP/network/JSON error, empty-results, and success states.

## Run locally

Start the backend from the repository root with `uvicorn backend.main:app --reload`, then run:

```text
cd frontend
npm install
npm run dev
```

When `VITE_API_URL` is unset in development, the frontend uses
`http://127.0.0.1:8000/api` by default. To override it, create a
`frontend/.env.local` file with the backend API base URL, including `/api`:

```text
VITE_API_URL=http://127.0.0.1:8000/api
```

For production, deploy the Python backend separately to a backend host such as
Render, Railway, or Fly.io, then set `VITE_API_URL` in the Vercel project
environment variables to the backend's API base URL (for example,
`https://your-backend.example.com/api`). The backend must allow requests from
the Vercel frontend origin via CORS. Vercel builds and serves only the static
Vite frontend; it does not host the Python API. Build the production assets
with `npm run build`.

The form values are controlled in `src/components/InputForm.jsx`; results are rendered by `src/components/Results.jsx` from the API's `{ "recommendations": [] }` response envelope.
