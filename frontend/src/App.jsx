import { useState } from "react";
import InputForm from "./components/InputForm";
import Results from "./components/Results";
import LoadingSpinner from "./components/LoadingSpinner";
import "./theme.css";

const API_BASE_URL =
  import.meta.env.VITE_API_URL?.replace(/\/+$/, "") ||
  (import.meta.env.DEV ? "http://127.0.0.1:8000/api" : "");

// Friendly names for the API's field names, used in validation messages.
const FIELD_LABELS = {
  subject: "Subject",
  difficulty: "Difficulty Level",
  max_duration_minutes: "Maximum Duration",
  min_rating: "Minimum Rating",
  keywords: "Keywords",
  limit: "Number of Results",
};

// Turn an unsuccessful HTTP response into a message a user can act on.
function describeHttpError(status, data) {
  if (status === 422) {
    const first = Array.isArray(data?.detail) ? data.detail[0] : null;
    if (first?.msg) {
      const field = Array.isArray(first.loc)
        ? first.loc[first.loc.length - 1]
        : null;
      const label = FIELD_LABELS[field];
      return label ? `Please check "${label}": ${first.msg}.` : `${first.msg}.`;
    }
    return "Some of your inputs are not valid. Please check the form and try again.";
  }
  if (status >= 500) {
    return "The recommendation service is unavailable right now. Please make sure the backend is running and try again.";
  }
  return `The request could not be completed (error ${status}). Please try again.`;
}

export default function App() {
  const [results, setResults] = useState([]);
  const [status, setStatus] = useState("idle");
  const [error, setError] = useState("");

  const handleSubmit = async (payload) => {
    setStatus("loading");
    setError("");
    setResults([]);

    if (!API_BASE_URL) {
      setError(
        "The recommendation service is not configured. Please set the VITE_API_URL environment variable."
      );
      setStatus("error");
      return;
    }

    let response;
    try {
      response = await fetch(`${API_BASE_URL}/recommend`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
    } catch {
      setError(
        "Could not reach the recommendation service. Check your connection and that the backend is running."
      );
      setStatus("error");
      return;
    }

    const data = await response.json().catch(() => null);

    if (!response.ok) {
      setError(describeHttpError(response.status, data));
      setStatus("error");
      return;
    }

    if (!data || !Array.isArray(data.recommendations)) {
      setError("The server sent an unexpected response. Please try again.");
      setStatus("error");
      return;
    }

    setResults(data.recommendations);
    setStatus("success");
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>LearnPath</h1>
        <p>
          Discover learning resources tailored to your subjects and preferences.
        </p>
      </header>

      <main className="app-main">
        <InputForm onSubmit={handleSubmit} disabled={status === "loading"} />
        {status === "idle" && (
          <p className="text-muted">
            Enter your learning preferences to get recommendations.
          </p>
        )}
        {status === "loading" && (
          <LoadingSpinner message="Finding the best resources for you..." />
        )}
        {error && (
          <p className="error-message" role="alert">
            {error}
          </p>
        )}
        {status === "success" && <Results items={results} />}
      </main>
    </div>
  );
}
