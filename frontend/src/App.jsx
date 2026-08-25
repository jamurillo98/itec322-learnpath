import React, { useState } from "react";
import InputForm from "./components/InputForm";
import Results from "./components/Results";

export default function App() {
  const [results, setResults] = useState([]);

  return (
    <div style={{ padding: 20, fontFamily: "Arial, sans-serif" }}>
      <h1>Rule-based Recommendation — Sprint 1</h1>
      <InputForm onResults={(r) => setResults(r)} />
      <Results items={results} />
    </div>
  );
}
