
export default function Results({ items = [] }) {
  if (!items || items.length === 0) {
    return (
      <p role="status" style={{ marginTop: "24px" }}>
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

  const cardStyle = {
    backgroundColor: "#ffffff",
    border: "1px solid #dddddd",
    borderRadius: "12px",
    padding: "24px",
    marginBottom: "20px",
    boxShadow: "0 2px 8px rgba(0, 0, 0, 0.05)",
    overflowWrap: "anywhere",
  };

  const tagStyle = {
    display: "inline-block",
    padding: "6px 10px",
    backgroundColor: "#f0f0f0",
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

      <p style={{ color: "#555" }}>
        Found {items.length} learning resource
        {items.length !== 1 ? "s" : ""} matching your preferences.
      </p>

      <div>
        {items.map((item, index) => (
          <article
            key={item.id || index}
            style={cardStyle}
          >
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
                  {item.format && (
                    <span style={tagStyle}>{item.format}</span>
                  )}

                  {item.level && (
                    <span style={tagStyle}>{item.level}</span>
                  )}

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
                  }}
                >
                  {typeof item.score === "number"
                    ? item.score
                    : "N/A"}
                </strong>
                <small>Total Score</small>
              </div>
            </div>

            <div style={{ marginTop: "20px" }}>
              <p><strong>Resource ID:</strong> {item.id || "Unavailable"}</p>

              {item.topic && (
                <p><strong>Topic:</strong> {item.topic}</p>
              )}

              {item.rating != null && (
                <p><strong>Rating:</strong> {item.rating} / 5</p>
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
                    {Object.entries(categoryLabels).map(
                      ([key, label]) => (
                        <div
                          key={key}
                          style={{
                            padding: "12px",
                            backgroundColor: "#f8f9fa",
                            border: "1px solid #e5e5e5",
                            borderRadius: "8px",
                          }}
                        >
                          <div
                            style={{
                              fontSize: "13px",
                              color: "#555",
                              marginBottom: "6px",
                            }}
                          >
                            {label}
                          </div>

                          <strong style={{ fontSize: "18px" }}>
                            {typeof item.score_breakdown[key] === "number"
                              ? item.score_breakdown[key]
                              : "N/A"}
                          </strong>
                        </div>
                      )
                    )}
                  </div>
                </div>
              )}

            {item.reason && (
              <p style={{ marginTop: "20px", lineHeight: 1.6 }}>
                <strong>Why recommended:</strong> {item.reason}
              </p>
            )}

            {Array.isArray(item.keywords) &&
              item.keywords.length > 0 && (
                <p>
                  <strong>Keywords:</strong>{" "}
                  {item.keywords.join(", ")}
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
                  backgroundColor: "#333333",
                  color: "#ffffff",
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
