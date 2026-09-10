"""
Rule-based Learning Resource Recommendation Engine.

This module intentionally contains no ML code — only deterministic rules.

Design notes for the report (System Modelling & Design sections):

- The engine is a pure function of (learner request) -> ranked results.
  Given the same inputs it always produces the same output — that's
  what makes it "deterministic" and testable, as opposed to a trained
  ML model that could vary run to run.
- Hard filters (max_duration_minutes, min_rating) reject resources
  outright before scoring — this models constraints that must never
  be violated (e.g. don't recommend a 10-hour course to someone with
  a 60-minute session).
- Soft scoring rules (subject, difficulty, keywords, rating, duration
  headroom) add weighted points — this models preference-based ranking
  rather than hard exclusion.
- Weights are named constants so they're easy to justify and tune
  during evaluation (Sprint 3).
- No web framework dependency — this module can be called from FastAPI,
  a CLI, or a test suite without modification.
"""

import csv
import os
from typing import Any, Dict, List, Optional

# --- Rule weights (tune these during evaluation) ---------------------------
SUBJECT_MATCH_WEIGHT = 5.0
DIFFICULTY_EXACT_MATCH_WEIGHT = 3.0
DIFFICULTY_ADJACENT_MATCH_WEIGHT = 1.0   # one level off (e.g. beginner vs intermediate)
KEYWORD_MATCH_WEIGHT = 1.5               # per matching keyword
RATING_BONUS_WEIGHT = 1.0                # multiplied by (rating - min_rating)
DURATION_HEADROOM_WEIGHT = 1.0           # rewards resources comfortably under time budget

DIFFICULTY_ORDER = {"beginner": 0, "intermediate": 1, "advanced": 2}


class RuleEngine:
    """A small, explainable rule-based recommender for learning resources."""

    def __init__(self, resources_path: Optional[str] = None):
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
        self.resources_path = resources_path or os.path.join(repo_root, "sample_resources.csv")
        self.resources = self._load_resources()

    def _load_resources(self) -> List[Dict[str, Any]]:
        items = []
        if not os.path.exists(self.resources_path):
            return items
        with open(self.resources_path, newline='', encoding='utf-8') as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                items.append(row)
        return items

    @staticmethod
    def _to_float(value, default=None):
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    @staticmethod
    def _difficulty_score(preferred: str, actual: str):
        """Exact difficulty match scores highest; one level off gets partial credit."""
        if preferred not in DIFFICULTY_ORDER or actual not in DIFFICULTY_ORDER:
            return 0.0, None
        gap = abs(DIFFICULTY_ORDER[actual] - DIFFICULTY_ORDER[preferred])
        if gap == 0:
            return DIFFICULTY_EXACT_MATCH_WEIGHT, f"difficulty '{actual}' matches exactly"
        if gap == 1:
            return DIFFICULTY_ADJACENT_MATCH_WEIGHT, f"difficulty '{actual}' is close to preferred '{preferred}'"
        return 0.0, None

    def recommend_learning_resources(
        self,
        subject: str,
        difficulty: Optional[str] = None,
        max_duration_minutes: Optional[float] = None,
        min_rating: Optional[float] = None,
        keywords: Optional[List[str]] = None,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Recommend learning resources based on subject, difficulty,
        available time, minimum quality, and keywords.

        Hard filters (resources failing these are excluded entirely,
        not just down-ranked):
        - max_duration_minutes: resources longer than this are excluded
        - min_rating: resources rated lower than this are excluded

        Soft scoring rules (add weighted points):
        - subject match against the resource's topic
        - difficulty match: exact scores highest, one level off gets
          partial credit, otherwise no bonus
        - keyword match against the resource's tags, per match
        - rating bonus: resources rated above min_rating score higher
        - duration headroom: resources well under max_duration_minutes
          score slightly higher

        Returns a list of dicts (id, title, score, url, reason), sorted
        by score descending, then by id ascending as a stable tiebreaker
        so output never depends on input ordering.
        """
        keywords = keywords or []
        results = []

        for r in self.resources:
            duration = self._to_float(r.get('duration_minutes'))
            if max_duration_minutes is not None and duration is not None and duration > float(max_duration_minutes):
                continue  # hard filter: too long

            rating = self._to_float(r.get('rating'))
            if min_rating is not None and rating is not None and rating < float(min_rating):
                continue  # hard filter: rated too low

            score = 0.0
            reasons: List[str] = []

            topic = r.get('topic', '').lower()
            tags = r.get('tags', '').lower()
            level = r.get('level', '').lower()

            if subject and subject.strip().lower() in topic:
                score += SUBJECT_MATCH_WEIGHT
                reasons.append(f"subject '{subject}' matches topic (+{SUBJECT_MATCH_WEIGHT})")

            if difficulty:
                diff_score, diff_reason = self._difficulty_score(difficulty.strip().lower(), level)
                if diff_score > 0:
                    score += diff_score
                    reasons.append(f"{diff_reason} (+{diff_score})")

            matched_keywords = [k for k in keywords if k and k.strip().lower() in tags]
            if matched_keywords:
                bonus = KEYWORD_MATCH_WEIGHT * len(matched_keywords)
                score += bonus
                reasons.append(f"{len(matched_keywords)} matching keyword(s): {matched_keywords} (+{bonus})")

            if min_rating is not None and rating is not None:
                bonus = RATING_BONUS_WEIGHT * max(0.0, rating - float(min_rating))
                if bonus > 0:
                    score += bonus
                    reasons.append(f"rating {rating} exceeds minimum {min_rating} (+{round(bonus, 2)})")

            if max_duration_minutes is not None and duration is not None and float(max_duration_minutes) > 0:
                headroom = max(0.0, (float(max_duration_minutes) - duration) / float(max_duration_minutes))
                bonus = DURATION_HEADROOM_WEIGHT * headroom
                if bonus > 0:
                    score += bonus
                    reasons.append(f"duration {duration}min has headroom under {max_duration_minutes}min (+{round(bonus, 2)})")

            if score > 0:
                results.append({
                    "id": r.get('id'),
                    "title": r.get('title'),
                    "score": round(score, 3),
                    "url": r.get('url'),
                    "reason": "; ".join(reasons) if reasons else f"Matched with score {score}",
                })

        results.sort(key=lambda x: (-x['score'], x['id'] or ''))
        return results[:limit]


if __name__ == '__main__':
    engine = RuleEngine()
    for r in engine.recommend_learning_resources(
        subject='programming', difficulty='beginner',
        max_duration_minutes=60, min_rating=4.0, keywords=['hands-on']
    ):
        print(r)
