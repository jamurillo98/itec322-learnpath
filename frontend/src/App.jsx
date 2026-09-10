import { useState } from "react";
import InputForm from "./components/InputForm";
import Results from "./components/Results";

export default function App() {
  const [results, setResults] = useState([]);

  const handleSubmit = async (payload) => {
    const response = await fetch("/api/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await response.json();
    setResults(data);
  };

  return (
    <div style={{ padding: 20, fontFamily: "Arial, sans-serif" }}>
      <h1>Learning Resource Recommendations</h1>
      <InputForm onSubmit={handleSubmit} />
      <Results items={results} />
    </div>
  );
}
