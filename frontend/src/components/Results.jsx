import React from "react";

// Placeholder Results component. Render a simple list of recommendations.

export default function Results({ items = [] }) {
  if (!items || items.length === 0) {
    return <div>No recommendations yet.</div>;
  }

  return (
    <div>
      <h2>Recommendations</h2>
      <ul>
        {items.map((it) => (
          <li key={it.id}>
            <strong>{it.title}</strong>
            <div style={{ fontSize: 12, color: "#555" }}>{it.reason}</div>
          </li>
        ))}
      </ul>
    </div>
  );
}
