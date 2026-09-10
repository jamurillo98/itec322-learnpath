export default function Results({ items = [] }) {
  if (!items || items.length === 0) return <p>No results yet.</p>;

  return (
    <ul>
      {items.map((item, index) => (
        <li key={item.id || index}>
          <strong>{item.subject}</strong> - {item.difficulty}
          <br />
          Duration: {item.duration_minutes} mins
          <br />
          Rating: {item.rating}
          <br />
          Keywords: {item.keywords.join(", ")}
        </li>
      ))}
    </ul>
  );
}
