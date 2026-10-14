import "./LoadingSpinner.css";

/**
 * LoadingSpinner
 * Shown while the frontend waits for /api/recommend.
 *
 * Usage:
 *   {loading && <LoadingSpinner />}
 *   {loading && <LoadingSpinner message="Finding resources for you..." />}
 */
export default function LoadingSpinner({
  message = "Finding the best resources for you...",
}) {
  return (
    <div className="loading-spinner" role="status" aria-live="polite">
      <div className="loading-spinner__circle" aria-hidden="true" />
      <p className="loading-spinner__text">{message}</p>
    </div>
  );
}
