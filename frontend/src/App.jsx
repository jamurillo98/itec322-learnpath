import { useState } from "react";
import InputForm from "./components/InputForm";
import Results from "./components/Results";
import LoadingSpinner from "./components/LoadingSpinner";
import "./theme.css";

export default function App() {
  const [results, setResults] = useState([]);
  const [status, setStatus] = useState("idle");
  const [error, setError] = useState("");

  const handleSubmit = async (payload) => {
    setStatus("loading");
    setError("");
    setResults([]);

    try {
      const response = await fetch("/api/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await response.json().catch(() => null);
      if (!response.ok) {
        throw new Error(
          data?.detail?.[0]?.msg || `Request failed (${response.status})`
        );
      }
      if (!data || !Array.isArray(data.recommendations)) {
        throw new Error("The server returned an invalid response.");
      }
      setResults(data.recommendations);
      setStatus("success");
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Unable to load recommendations."
      );
      setStatus("error");
    }
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
