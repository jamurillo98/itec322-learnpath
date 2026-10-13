
import { useState } from "react";

export default function InputForm({ onSubmit, disabled = false }) {
  const [subject, setSubject] = useState("");
  const [difficulty, setDifficulty] = useState("");
  const [maxDurationMinutes, setMaxDurationMinutes] = useState("");
  const [minRating, setMinRating] = useState("");
  const [keywords, setKeywords] = useState("");
  const [limit, setLimit] = useState(5);

  const handleSubmit = (e) => {
    e.preventDefault();

    onSubmit({
      subject: subject.trim(),
      difficulty,
      max_duration_minutes: Number(maxDurationMinutes),
      min_rating: Number(minRating),
      keywords: keywords
        .split(",")
        .map((keyword) => keyword.trim())
        .filter(Boolean),
      limit: Number(limit),
    });
  };

  const fieldStyle = {
    width: "100%",
    padding: "12px",
    border: "1px solid #ccc",
    borderRadius: "8px",
    fontSize: "15px",
    boxSizing: "border-box",
    backgroundColor: "#fff",
    color: "#222",
  };

  const labelStyle = {
    display: "block",
    marginBottom: "7px",
    fontWeight: "600",
    fontSize: "14px",
  };

  return (
    <form
      onSubmit={handleSubmit}
      style={{
        maxWidth: "800px",
        padding: "24px",
        border: "1px solid #ddd",
        borderRadius: "12px",
        backgroundColor: "#f8f9fa",
      }}
    >
      <h2 style={{ marginTop: 0 }}>Find Your Learning Resources</h2>

      <p style={{ color: "#555" }}>
        Enter your learning preferences to discover suitable resources.
      </p>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(min(100%, 240px), 1fr))",
          gap: "20px",
        }}
      >
        <div>
          <label htmlFor="subject" style={labelStyle}>Subject</label>
          <input
            id="subject"
            style={fieldStyle}
            placeholder="e.g. programming"
            value={subject}
            onChange={(e) => setSubject(e.target.value)}
            required
            disabled={disabled}
          />
        </div>

        <div>
          <label htmlFor="difficulty" style={labelStyle}>Difficulty Level</label>
          <select
            id="difficulty"
            style={fieldStyle}
            value={difficulty}
            onChange={(e) => setDifficulty(e.target.value)}
            required
            disabled={disabled}
          >
            <option value="" disabled>Select difficulty</option>
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>
        </div>

        <div>
          <label htmlFor="duration" style={labelStyle}>Maximum Duration (minutes)</label>
          <input
            id="duration"
            type="number"
            min="1"
            style={fieldStyle}
            placeholder="e.g. 60"
            value={maxDurationMinutes}
            onChange={(e) => setMaxDurationMinutes(e.target.value)}
            required
            disabled={disabled}
          />
        </div>

        <div>
          <label htmlFor="rating" style={labelStyle}>Minimum Rating</label>
          <input
            id="rating"
            type="number"
            min="0"
            max="5"
            step="0.1"
            style={fieldStyle}
            placeholder="e.g. 4.0"
            value={minRating}
            onChange={(e) => setMinRating(e.target.value)}
            required
            disabled={disabled}
          />
        </div>

        <div>
          <label htmlFor="keywords" style={labelStyle}>Keywords (Optional)</label>
          <input
            id="keywords"
            style={fieldStyle}
            placeholder="e.g. python, hands-on"
            value={keywords}
            onChange={(e) => setKeywords(e.target.value)}
            disabled={disabled}
          />
        </div>

        <div>
          <label htmlFor="limit" style={labelStyle}>Number of Results</label>
          <input
            id="limit"
            type="number"
            min="1"
            max="50"
            style={fieldStyle}
            value={limit}
            onChange={(e) => setLimit(e.target.value)}
            required
            disabled={disabled}
          />
        </div>
      </div>

      <button
        type="submit"
        disabled={disabled}
        style={{
          marginTop: "24px",
          padding: "12px 24px",
          backgroundColor: disabled ? "#aaa" : "#333",
          color: "#fff",
          border: "none",
          borderRadius: "8px",
          fontSize: "16px",
          fontWeight: "600",
          cursor: disabled ? "not-allowed" : "pointer",
        }}
      >
        {disabled ? "Loading Recommendations..." : "Find Recommendations"}
      </button>
    </form>
  );
}
