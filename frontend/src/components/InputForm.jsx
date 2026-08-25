import React, { useState } from "react";

// Placeholder input form. In Sprint 1 this will collect a free-text query
// and POST it to the backend `/recommend` endpoint.

export default function InputForm({ onResults = () => {} }) {
  const [query, setQuery] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    // Minimal local mock until backend integration
    // Replace with fetch('/recommend') when backend is running
    const mock = [
      { id: 1, title: "Sample Resource A", reason: "Matched keyword" },
    ];
    onResults(mock);
  };

  return (
    <form onSubmit={submit} style={{ marginBottom: 16 }}>
      <input
        aria-label="query"
        type="text"
        value={query}
        placeholder="Enter a topic or need"
        onChange={(e) => setQuery(e.target.value)}
        style={{ padding: 8, width: "60%", marginRight: 8 }}
      />
      <button type="submit">Recommend</button>
    </form>
  );
}
