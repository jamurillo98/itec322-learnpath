import React, { useState } from "react";

export default function InputForm({ onResults = () => {} }) {
  const [projectType, setProjectType] = useState("");
  const [budget, setBudget] = useState("");
  const [priorities, setPriorities] = useState("");
  const [notes, setNotes] = useState("");

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const submit = async (e) => {
    e.preventDefault();

    setLoading(true);
    setError("");
    setMessage("");

    const payload = {
      project_type: projectType,
      budget: Number(budget),
      priorities: priorities
        .split(",")
        .map((item) => item.trim())
        .filter(Boolean),
      notes: notes || null,
    };

    try {
      const response = await fetch("/api/recommend", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error("Request failed");
      }

      const data = await response.json();

      onResults(data.recommendations || []);
      setMessage(data.message || "Request accepted.");
    } catch (err) {
      onResults([]);
      setError("Unable to get recommendations. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={submit} style={{ marginBottom: 16 }}>
      <div style={{ marginBottom: 10 }}>
        <label>
          Project type:
          <input
            type="text"
            value={projectType}
            onChange={(e) => setProjectType(e.target.value)}
            required
            style={{ marginLeft: 8, padding: 8 }}
          />
        </label>
      </div>

      <div style={{ marginBottom: 10 }}>
        <label>
          Budget:
          <input
            type="number"
            min="0"
            value={budget}
            onChange={(e) => setBudget(e.target.value)}
            required
            style={{ marginLeft: 8, padding: 8 }}
          />
        </label>
      </div>

      <div style={{ marginBottom: 10 }}>
        <label>
          Priorities:
          <input
            type="text"
            value={priorities}
            onChange={(e) => setPriorities(e.target.value)}
            placeholder="speed, simplicity"
            style={{ marginLeft: 8, padding: 8 }}
          />
        </label>
      </div>

      <div style={{ marginBottom: 10 }}>
        <label>
          Notes:
          <input
            type="text"
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            style={{ marginLeft: 8, padding: 8 }}
          />
        </label>
      </div>

      <button type="submit" disabled={loading}>
        {loading ? "Loading..." : "Recommend"}
      </button>

      {message && (
        <p style={{ marginTop: 10 }}>
          {message}
        </p>
      )}

      {error && (
        <p style={{ marginTop: 10 }}>
          {error}
        </p>
      )}
    </form>
  );
}
