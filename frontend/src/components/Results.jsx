export default function Results({ items = [] }) {
  if (!items || items.length === 0) {
    return (
      <p role="status" className="text-muted" style={{ marginTop: "24px" }}>
        No matching learning resources were found.
      </p>
    );
  }

  const categoryLabels = {
    relevance: "Relevance",
    level_fit: "Level Fit",
    quality: "Quality",
    practicality: "Practicality",
  };

  // Background, border, teal top line and shadow come from the .card class in theme.css
  const cardStyle = {
    padding: "24px",
    marginBottom: "20px",
    overflowWrap: "anywhere",
  };

  const tagStyle = {
    display: "inline-block",
    padding: "6px 10px",
    backgroundColor: "var(--lp-primary-soft)",
    color: "var(--lp-primary-dark)",
    borderRadius: "6px",
    fontSize: "13px",
    textTransform: "capitalize",
  };

  return (
    <section
      aria-label="Learning recommendations"
      style={{
        maxWidth: "850px",
        marginTop: "32px",
      }}
    >
      <h2>Recommended Learning Resources</h2>

      <p style={{ color: "var(--lp-muted)" }}>
        Found {items.length} learning resource
        {items.length !== 1 ? "s" : ""} matching your preferences.
      </p>

      <div>
        {items.map((item, index) => (
          <article key={item.id || index} className="card" style={cardStyle}>
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "flex-start",
                gap: "16px",
                flexWrap: "wrap",
              }}
            >
              <div style={{ flex: "1 1 200px" }}>
                <h3 style={{ marginTop: 0, marginBottom: "12px" }}>
                  {item.title || "Untitled resource"}
                </h3>

                <div
                  style={{
                    display: "flex",
                    gap: "8px",
                    flexWrap: "wrap",
                  }}
                >
                  {item.format && <span style={tagStyle}>{item.format}</span>}

                  {item.level && <span style={tagStyle}>{item.level}</span>}

                  {item.duration_minutes != null && (
                    <span style={tagStyle}>
                      {item.duration_minutes} minutes
                    </span>
                  )}
                </div>
              </div>

              <div style={{ textAlign: "right" }}>
                <strong
                  style={{
                    display: "block",
                    fontSize: "25px",
                    color: "var(--lp-primary-dark)",
                  }}
                >
                  {typeof item.score === "number" ? item.score : "N/A"}
                </strong>
                <small className="text-muted">Total Score</small>
              </div>
            </div>

            <div style={{ marginTop: "20px" }}>
              <p>
                <strong>Resource ID:</strong> {item.id || "Unavailable"}
              </p>

              {item.topic && (
                <p>
                  <strong>Topic:</strong> {item.topic}
                </p>
              )}

              {item.rating != null && (
                <p>
                  <strong>Rating:</strong> {item.rating} / 5
                </p>
              )}
            </div>

            {item.score_breakdown &&
              typeof item.score_breakdown === "object" && (
                <div style={{ marginTop: "20px" }}>
                  <h4>Score Breakdown</h4>

                  <div
                    style={{
                      display: "grid",
                      gridTemplateColumns:
                        "repeat(auto-fit, minmax(min(100%, 160px), 1fr))",
                      gap: "12px",
                    }}
                  >
                    {Object.entries(categoryLabels).map(([key, label]) => (
                      <div
                        key={key}
                        style={{
                          padding: "12px",
                          backgroundColor: "var(--lp-bg)",
                          border: "1px solid var(--lp-border)",
                          borderRadius: "8px",
                        }}
                      >
                        <div
                          style={{
                            fontSize: "13px",
                            color: "var(--lp-muted)",
                            marginBottom: "6px",
                          }}
                        >
                          {label}
                        </div>

                        <strong
                          style={{
                            fontSize: "18px",
                            color: "var(--lp-primary-dark)",
                          }}
                        >
                          {typeof item.score_breakdown[key] === "number"
                            ? item.score_breakdown[key]
                            : "N/A"}
                        </strong>
                      </div>
                    ))}
                  </div>
                </div>
              )}

            {item.reason && (
              <p style={{ marginTop: "20px", lineHeight: 1.6 }}>
                <strong>Why recommended:</strong> {item.reason}
              </p>
            )}

            {Array.isArray(item.keywords) && item.keywords.length > 0 && (
              <p>
                <strong>Keywords:</strong> {item.keywords.join(", ")}
              </p>
            )}

            {item.url && (
              <a
                href={item.url}
                target="_blank"
                rel="noopener noreferrer"
                style={{
                  display: "inline-block",
                  marginTop: "12px",
                  padding: "10px 16px",
                  backgroundColor: "var(--lp-primary-dark)",
                  color: "var(--lp-on-primary)",
                  borderRadius: "8px",
                  textDecoration: "none",
                  fontWeight: "600",
                }}
              >
                Open Learning Resource ↗
              </a>
            )}
          </article>
        ))}
      </div>
    </section>
  );
}
