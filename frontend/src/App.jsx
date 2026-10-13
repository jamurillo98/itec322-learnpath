import { useState } from "react";
import InputForm from "./components/InputForm";
import Results from "./components/Results";

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
        throw new Error(data?.detail?.[0]?.msg || `Request failed (${response.status})`);
      }
      if (!data || !Array.isArray(data.recommendations)) {
        throw new Error("The server returned an invalid response.");
      }
      setResults(data.recommendations);
      setStatus("success");
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Unable to load recommendations.");
      setStatus("error");
    }
  };

  return (
    <div style={{ padding: 20, fontFamily: "Arial, sans-serif" }}>
      <h1>LearnPath</h1>
<p>Discover learning resources tailored to your subjects and preferences.</p>
      <InputForm onSubmit={handleSubmit} disabled={status === "loading"} />
      {status === "idle" && <p>Enter your learning preferences to get recommendations.</p>}
      {status === "loading" && <p role="status">Loading recommendations...</p>}
      {error && <p role="alert">{error}</p>}
      {status === "success" && <Results items={results} />}
    </div>
  );
}
