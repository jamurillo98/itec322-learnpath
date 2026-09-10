import { useState } from "react";

export default function InputForm({ onSubmit }) {
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
      <input placeholder="Subject" value={subject} onChange={(e) => setSubject(e.target.value)} required />
      <input placeholder="Difficulty" value={difficulty} onChange={(e) => setDifficulty(e.target.value)} required />
      <input type="number" min="0" placeholder="Max Duration (minutes)" value={maxDurationMinutes} onChange={(e) => setMaxDurationMinutes(e.target.value)} required />
      <input type="number" min="0" max="5" step="0.1" placeholder="Minimum Rating" value={minRating} onChange={(e) => setMinRating(e.target.value)} required />
      <input placeholder="Keywords (comma separated)" value={keywords} onChange={(e) => setKeywords(e.target.value)} />
      <input type="number" min="1" placeholder="Limit" value={limit} onChange={(e) => setLimit(e.target.value)} />
      <button type="submit">Recommend</button>
    </form>
  );
}
