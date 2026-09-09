"""
Rule-based recommendation engine.

This module intentionally contains no ML code — only deterministic rules.

What goes inside:
- `RuleEngine` class: loads resources, evaluates rules, returns ranked
  results.
- `recommend(query, user_profile, limit)` — the original Sprint 1
  interface (query string + optional level/max_duration/min_rating
  profile). Unchanged, already reviewed and merged — kept for backward
  compatibility with anything already using it.
- `recommend_from_request(project_type, budget, priorities, notes, limit)`
  — NEW. Matches the exact field names used by the frontend form
  (InputForm.jsx) and the backend's RecommendRequest model, so the
  backend can call this directly with no translation layer needed.

See README.md in this folder for documented example inputs and outputs
for both methods.
"""

import csv
import os
from typing import Any, Dict, List, Optional

# --- Rule weights for recommend() (tune during Sprint 3 evaluation) -------
TITLE_MATCH_WEIGHT = 3
TOPIC_MATCH_WEIGHT = 2
TAG_MATCH_WEIGHT = 1
LEVEL_MATCH_WEIGHT = 1
RATING_BONUS_WEIGHT = 1.0
DURATION_HEADROOM_WEIGHT = 1.0

# --- Rule weights for recommend_from_request() -----------------------------
PROJECT_TYPE_MATCH_WEIGHT = 3      # project_type matching a resource's topic
PRIORITY_MATCH_WEIGHT = 2          # per matching priority/tag
BUDGET_HEADROOM_WEIGHT = 1.0       # rewards resources comfortably under budget


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

    # --- Original Sprint 1 interface (unchanged, merged, reviewed) --------

    def _passes_hard_filters(self, resource: Dict[str, Any], user_profile: Optional[Dict[str, Any]]) -> bool:
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
        """Original Sprint 1 method. See README.md for documented examples."""
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

    # --- NEW: matches frontend/backend field names directly ----------------

    def recommend_from_request(
        self,
        project_type: str,
        budget: float = None,
        priorities: List[str] = None,
        notes: Optional[str] = None,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Recommend resources using the exact field names the frontend
        form (InputForm.jsx) and backend (RecommendRequest) already use
        — no translation layer needed to call this from the API.

        Rules:
        - Hard filter: resources costing more than `budget` are excluded
          entirely (only applied if the CSV row has a 'cost' value and
          budget is provided).
        - project_type match: compared against each resource's `topic`
          field (soft bonus).
        - priorities match: each priority string is compared against the
          resource's `tags` (soft bonus per match).
        - budget headroom: resources well under budget score slightly
          higher, same idea as the duration headroom rule.
        - notes: not currently used by any rule (free text, no
          established mapping yet) — accepted for API compatibility and
          future use, but does not affect scoring.

        Returns the same shape as recommend(): id, title, score, url, reason.
        """
        priorities = priorities or []
        results = []

        for r in self.resources:
            cost = self._to_float(r.get('cost'))
            if budget is not None and cost is not None and cost > float(budget):
                continue  # hard filter: over budget

            score = 0.0
            reasons = []

            topic = r.get('topic', '').lower()
            tags = r.get('tags', '').lower()

            if project_type and project_type.strip().lower() in topic:
                score += PROJECT_TYPE_MATCH_WEIGHT
                reasons.append(f"project_type '{project_type}' matches topic (+{PROJECT_TYPE_MATCH_WEIGHT})")

            matched_priorities = [p for p in priorities if p and p.strip().lower() in tags]
            if matched_priorities:
                bonus = PRIORITY_MATCH_WEIGHT * len(matched_priorities)
                score += bonus
                reasons.append(f"{len(matched_priorities)} matching priorit{'y' if len(matched_priorities)==1 else 'ies'}: {matched_priorities} (+{bonus})")

            if budget is not None and cost is not None and float(budget) > 0:
                headroom = max(0.0, (float(budget) - cost) / float(budget))
                bonus = BUDGET_HEADROOM_WEIGHT * headroom
                if bonus > 0:
                    score += bonus
                    reasons.append(f"cost {cost} has headroom under budget {budget} (+{round(bonus, 2)})")

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
    print(engine.recommend('python'))
    print(engine.recommend_from_request(
        project_type='programming', budget=50, priorities=['hands-on', 'self-paced']
    ))
