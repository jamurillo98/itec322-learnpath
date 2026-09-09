"""
Rule-based recommendation engine.

This module intentionally contains no ML code — only deterministic rules.

What goes inside:
- `RuleEngine` class: loads resources, evaluates rules, returns ranked
  results (same public interface as the Sprint 1 scaffold: __init__,
  recommend()).
- Extended in Sprint 1 with: hard filters (max_duration, min_rating),
  weighted scoring (title/topic/tag keyword match, level/difficulty
  match, rating bonus, duration headroom), and human-readable reasons
  for each recommendation.

Backward compatibility notes:
- recommend(query, user_profile, limit) keeps the same signature and
  return shape as the original scaffold: a list of dicts with keys
  id, title, score, url, reason.
- user_profile['level'] still works exactly as before (soft scoring
  bonus). Two new OPTIONAL user_profile keys were added:
    - 'max_duration': int minutes — hard filter, excludes anything longer
    - 'min_rating': float — hard filter, excludes anything rated lower
  Both are optional; existing calls with just {'level': 'beginner'}
  behave the same as the original scaffold.
- The CSV can now optionally include 'duration_minutes' and 'rating'
  columns. If a row doesn't have them, those rules simply contribute 0
  to the score rather than erroring.

See README.md in this folder for documented example inputs and outputs.
"""

import csv
import os
from typing import Any, Dict, List, Optional

# --- Rule weights (tune these during Sprint 3 evaluation) -----------------
TITLE_MATCH_WEIGHT = 3
TOPIC_MATCH_WEIGHT = 2
TAG_MATCH_WEIGHT = 1
LEVEL_MATCH_WEIGHT = 1
RATING_BONUS_WEIGHT = 1.0        # multiplied by (rating - min_rating), if both present
DURATION_HEADROOM_WEIGHT = 1.0   # rewards items comfortably under max_duration, if present


class RuleEngine:
    """A small, explainable rule-based recommender for Sprint 1."""

    def __init__(self, resources_path=None):
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

    def _passes_hard_filters(self, resource: Dict[str, Any], user_profile: Optional[Dict[str, Any]]) -> bool:
        """Optional hard filters: max_duration and min_rating. Both are
        skipped gracefully if the profile or the CSV row doesn't have
        the relevant field, so this never breaks the original scaffold."""
        if not user_profile:
            return True

        max_duration = user_profile.get('max_duration')
        if max_duration is not None:
            duration = self._to_float(resource.get('duration_minutes'))
            if duration is not None and duration > float(max_duration):
                return False

        min_rating = user_profile.get('min_rating')
        if min_rating is not None:
            rating = self._to_float(resource.get('rating'))
            if rating is not None and rating < float(min_rating):
                return False

        return True

    def recommend(self, query: str, user_profile: Dict[str, Any] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Return ranked, explainable recommendations.

        Rules implemented:
        - Keyword match: query tokens appearing in title/topic/tags boost score
          (title=3, topic=2, tags=1) — unchanged from the original scaffold.
        - Level/difficulty match: user_profile['level'] matching the resource's
          level adds +1 — unchanged from the original scaffold.
        - Hard filters (only applied if present in user_profile and the CSV
          row): max_duration, min_rating — resources failing these are excluded
          entirely, not just down-ranked.
        - Rating bonus: resources rated above user_profile['min_rating']
          get extra score proportional to the gap (only if both are present).
        - Duration headroom bonus: resources well under user_profile
          ['max_duration'] score slightly higher (only if both are present).

        See README.md for worked examples of this method's input/output.
        """
        if not query:
            return []

        q = query.lower()
        results = []

        for r in self.resources:
            if not self._passes_hard_filters(r, user_profile):
                continue

            score = 0.0
            reasons = []

            title = r.get('title', '').lower()
            topic = r.get('topic', '').lower()
            tags = r.get('tags', '').lower()
            level = r.get('level', '').lower()

            if q in title:
                score += TITLE_MATCH_WEIGHT
                reasons.append(f"query matched title (+{TITLE_MATCH_WEIGHT})")
            if q in topic:
                score += TOPIC_MATCH_WEIGHT
                reasons.append(f"query matched topic (+{TOPIC_MATCH_WEIGHT})")
            if q in tags:
                score += TAG_MATCH_WEIGHT
                reasons.append(f"query matched tags (+{TAG_MATCH_WEIGHT})")

            if user_profile and 'level' in user_profile:
                pref = str(user_profile.get('level', '')).lower()
                if pref and pref == level:
                    score += LEVEL_MATCH_WEIGHT
                    reasons.append(f"level '{level}' matches preference (+{LEVEL_MATCH_WEIGHT})")

            if user_profile and 'min_rating' in user_profile:
                rating = self._to_float(r.get('rating'))
                min_rating = self._to_float(user_profile.get('min_rating'))
                if rating is not None and min_rating is not None:
                    bonus = RATING_BONUS_WEIGHT * max(0.0, rating - min_rating)
                    if bonus > 0:
                        score += bonus
                        reasons.append(f"rating {rating} exceeds minimum {min_rating} (+{round(bonus, 2)})")

            if user_profile and 'max_duration' in user_profile:
                duration = self._to_float(r.get('duration_minutes'))
                max_duration = self._to_float(user_profile.get('max_duration'))
                if duration is not None and max_duration and max_duration > 0:
                    headroom = max(0.0, (max_duration - duration) / max_duration)
                    bonus = DURATION_HEADROOM_WEIGHT * headroom
                    if bonus > 0:
                        score += bonus
                        reasons.append(f"duration {duration}min has headroom under {max_duration}min budget (+{round(bonus, 2)})")

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
    # Quick local demo — see README.md for the documented version of these examples
    engine = RuleEngine()
    print(engine.recommend('python'))
    print(engine.recommend('python', user_profile={'level': 'beginner', 'max_duration': 60, 'min_rating': 4.0}))
            
