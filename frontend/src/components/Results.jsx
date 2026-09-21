export default function Results({ items = [] }) {
  if (!items || items.length === 0) return <p>No matching learning resources were found.</p>;

  return (
    <ul>
      {items.map((item, index) => (
        <li key={item.id || index}>
          <strong>{item.title || "Untitled resource"}</strong>
          <div>ID: {item.id || "Unavailable"}</div>
          <div>Score: {typeof item.score === "number" ? item.score : "Unavailable"}</div>
          {item.url && <div><a href={item.url} target="_blank" rel="noreferrer">Open resource</a></div>}
          <div>{item.reason || "No explanation provided."}</div>
          {item.duration_minutes != null && <div>Duration: {item.duration_minutes} minutes</div>}
          {item.rating != null && <div>Rating: {item.rating}</div>}
          {Array.isArray(item.keywords) && item.keywords.length > 0 && <div>Keywords: {item.keywords.join(", ")}</div>}
        </li>
      ))}
    </ul>
  );
}
