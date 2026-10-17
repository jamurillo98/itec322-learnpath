import { useEffect, useRef } from "react";

// What each score category measures, in plain language for users.
const CATEGORY_INFO = [
  {
    key: "relevance",
    label: "Relevance",
    hint: "How well it matches your subject and keywords",
  },
  {
    key: "level_fit",
    label: "Level Fit",
    hint: "How well the difficulty matches your level",
  },
  {
    key: "quality",
    label: "Quality",
    hint: "How far its rating is above your minimum",
  },
  {
    key: "practicality",
    label: "Practicality",
    hint: "How well it fits your time limit",
  },
];

// Show at most 2 decimal places (10.367 -> 10.37, 3 -> 3).
const formatScore = (value) =>
  typeof value === "number" && Number.isFinite(value)
    ? Number(value.toFixed(2)).toString()
    : "N/A";

// Split the backend's "a; b; c" explanation into separate points.
const splitReason = (reason) =>
  typeof reason === "string"
    ? reason
        .split(";")
        .map((part) => part.trim())
        .filter(Boolean)
    : [];

export default function Results({ items = [] }) {
  const headingRef = useRef(null);

  // Move keyboard and screen-reader focus to the results after each search.
  useEffect(() => {
    headingRef.current?.focus();
  }, [items]);

  if (!items || items.length === 0) {
    return (
      <section
        aria-label="Learning recommendations"
        style={{ marginTop: "24px" }}
      >
        <h2 ref={headingRef} tabIndex={-1} className="results-heading">
          No matching resources found
        </h2>
        <p className="text-muted">
          Try a broader subject, a longer maximum duration, a lower minimum
          rating, or fewer keywords.
        </p>
      </section>
    );
  }

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
      <h2 ref={headingRef} tabIndex={-1} className="results-heading">
        Recommended Learning Resources
      </h2>

      <p style={{ color: "var(--lp-muted)" }}>
        Found {items.length} learning resource
        {items.length !== 1 ? "s" : ""} matching your preferences, ranked from
        best to weakest match. Each total score is the sum of its four category
        scores; a higher score means a better match.
      </p>

      <div>
        {items.map((item, index) => {
          const reasons = splitReason(item.reason);

          return (
            <article
              key={item.id || index}
              className="card"
              style={cardStyle}
              aria-labelledby={`resource-title-${index}`}
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
                  <h3
                    id={`resource-title-${index}`}
                    style={{ marginTop: 0, marginBottom: "12px" }}
                  >
                    <span className="sr-only">Rank {index + 1}: </span>
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
                    {formatScore(item.score)}
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

                    <dl
                      style={{
                        display: "grid",
                        gridTemplateColumns:
                          "repeat(auto-fit, minmax(min(100%, 160px), 1fr))",
                        gap: "12px",
                        margin: 0,
                      }}
                    >
                      {CATEGORY_INFO.map(({ key, label, hint }) => (
                        <div
                          key={key}
                          style={{
                            padding: "12px",
                            backgroundColor: "var(--lp-bg)",
                            border: "1px solid var(--lp-border)",
                            borderRadius: "8px",
                          }}
                        >
                          <dt
                            style={{
                              fontSize: "13px",
                              color: "var(--lp-muted)",
                              marginBottom: "6px",
                            }}
                          >
                            {label}
                          </dt>

                          <dd style={{ margin: 0 }}>
                            <strong
                              style={{
                                fontSize: "18px",
                                color: "var(--lp-primary-dark)",
                              }}
                            >
                              {formatScore(item.score_breakdown[key])}
                            </strong>
                            <span className="score-hint">{hint}</span>
                          </dd>
                        </div>
                      ))}
                    </dl>
                  </div>
                )}

              {reasons.length > 0 && (
                <div style={{ marginTop: "20px" }}>
                  <strong>Why recommended:</strong>
                  <ul className="reason-list">
                    {reasons.map((reason) => (
                      <li key={reason}>{reason}</li>
                    ))}
                  </ul>
                </div>
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
                  Open Learning Resource <span aria-hidden="true">↗</span>
                  <span className="sr-only">
                    {" "}
                    for {item.title || "this resource"} (opens in a new tab)
                  </span>
                </a>
              )}
            </article>
          );
        })}
      </div>
    </section>
  );
}
