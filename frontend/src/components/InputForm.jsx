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
      subject,
      difficulty,
      max_duration_minutes: Number(maxDurationMinutes),
      min_rating: Number(minRating),
      keywords: keywords.split(",").map((keyword) => keyword.trim()).filter(Boolean),
      limit: Number(limit),
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input placeholder="Subject" value={subject} onChange={(e) => setSubject(e.target.value)} required disabled={disabled} />
      <select value={difficulty} onChange={(e) => setDifficulty(e.target.value)} required disabled={disabled}>
        <option value="" disabled>Difficulty</option>
        <option value="beginner">Beginner</option>
        <option value="intermediate">Intermediate</option>
        <option value="advanced">Advanced</option>
      </select>
      <input type="number" min="0" placeholder="Max Duration (minutes)" value={maxDurationMinutes} onChange={(e) => setMaxDurationMinutes(e.target.value)} required disabled={disabled} />
      <input type="number" min="0" max="5" step="0.1" placeholder="Minimum Rating" value={minRating} onChange={(e) => setMinRating(e.target.value)} required disabled={disabled} />
      <input placeholder="Keywords (comma separated)" value={keywords} onChange={(e) => setKeywords(e.target.value)} disabled={disabled} />
      <input type="number" min="1" max="50" placeholder="Limit" value={limit} onChange={(e) => setLimit(e.target.value)} disabled={disabled} />
      <button type="submit" disabled={disabled}>{disabled ? "Loading..." : "Recommend"}</button>
    </form>
  );
}
