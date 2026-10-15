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
FORMAT_MATCH_WEIGHT = 2.0                # resource format matches the learner's preferred format

DIFFICULTY_ORDER = {"beginner": 0, "intermediate": 1, "advanced": 2}

# --- Subject matching (Sprint 3) -------------------------------------------
# Learners type free text ("data science", "maths", "python"), but the CSV
# stores hyphenated topics ("data-science") and tags. Subject text is
# therefore normalised (case, hyphens, spacing), a few common short forms
# are expanded, and every word of the subject must appear in the resource's
# topic, tags or title.
SUBJECT_ALIASES = {
    "maths": "mathematics",
    "math": "mathematics",
    "ml": "machine learning",
    "js": "javascript",
    "stats": "statistics",
}

# When the learner supplies a subject or keywords, a resource must match at
# least one of them to be recommended. Difficulty, rating, duration and format
# only *rank* relevant resources; they must not make unrelated ones appear.
REQUIRE_RELEVANCE_SIGNAL = True

# --- Resource categories (Sprint 2) ----------------------------------------
# Every resource has a `format` category in the CSV.
VALID_FORMATS = ("video", "article", "exercise")

# --- Rule categories (Sprint 2) --------------------------------------------
# Each scoring rule belongs to exactly one category. The engine returns a
# per-category `score_breakdown` so the UI and report can show *why* a
# resource ranked where it did, not just its total score.
#
#   relevance    -> subject match + keyword match
#   level_fit    -> difficulty match
#   quality      -> rating bonus
#   practicality -> duration headroom + format match
RULE_CATEGORIES = ("relevance", "level_fit", "quality", "practicality")


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
    def _normalise(text: str) -> str:
        """Lower-case and treat hyphens/underscores/semicolons as spaces."""
        for ch in "-_;":
            text = text.replace(ch, " ")
        return " ".join(text.lower().split())

    @classmethod
    def _subject_matches(cls, subject: str, topic: str, tags: str, title: str) -> bool:
        """True if every word of the (alias-expanded) subject appears in topic, tags or title."""
        wanted = cls._normalise(subject)
        wanted = SUBJECT_ALIASES.get(wanted, wanted)
        if not wanted:
            return False
        haystack = cls._normalise(f"{topic} {tags} {title}")
        return all(word in haystack for word in wanted.split())

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
        preferred_format: Optional[str] = None,
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
        - format match (optional `preferred_format`: video, article or
          exercise): matching resources get a bonus

        Rules are grouped into RULE_CATEGORIES and each result carries a
        `score_breakdown` dict; its values always add up to `score`.

        Returns a list of dicts (id, title, score, score_breakdown, url,
        reason, format, topic, level, ...), sorted by score descending,
        then by id ascending as a stable tiebreaker so output never
        depends on input ordering.
        """
        keywords = keywords or []
        fmt_pref = (preferred_format or "").strip().lower()
        if fmt_pref and fmt_pref not in VALID_FORMATS:
            raise ValueError(f"preferred_format must be one of {VALID_FORMATS}")
        results = []

        for r in self.resources:
            duration = self._to_float(r.get('duration_minutes'))
            if max_duration_minutes is not None and duration is not None and duration > float(max_duration_minutes):
                continue  # hard filter: too long

            rating = self._to_float(r.get('rating'))
            if min_rating is not None and rating is not None and rating < float(min_rating):
                continue  # hard filter: rated too low

            breakdown = {category: 0.0 for category in RULE_CATEGORIES}
            reasons: List[str] = []

            topic = r.get('topic', '').lower()
            title_text = r.get('title', '') or ''
            tags = r.get('tags', '').lower()
            level = r.get('level', '').lower()
            fmt = (r.get('format') or '').strip().lower()

            # relevance: subject
            subject_matched = bool(subject) and self._subject_matches(subject, topic, tags, title_text)
            if subject_matched:
                breakdown["relevance"] += SUBJECT_MATCH_WEIGHT
                reasons.append(f"subject '{subject}' matches topic (+{SUBJECT_MATCH_WEIGHT})")

            # level_fit: difficulty
            if difficulty:
                diff_score, diff_reason = self._difficulty_score(difficulty.strip().lower(), level)
                if diff_score > 0:
                    breakdown["level_fit"] += diff_score
                    reasons.append(f"{diff_reason} (+{diff_score})")

            # relevance: keywords
            matched_keywords = [k for k in keywords if k and k.strip().lower() in tags]
            has_content_criteria = bool(subject and subject.strip()) or any(k and k.strip() for k in keywords)
            if REQUIRE_RELEVANCE_SIGNAL and has_content_criteria and not (subject_matched or matched_keywords):
                continue  # asked for a subject/keywords but this resource matches neither
            if matched_keywords:
                bonus = KEYWORD_MATCH_WEIGHT * len(matched_keywords)
                breakdown["relevance"] += bonus
                reasons.append(f"{len(matched_keywords)} matching keyword(s): {matched_keywords} (+{bonus})")

            # quality: rating above the minimum
            if min_rating is not None and rating is not None:
                bonus = RATING_BONUS_WEIGHT * max(0.0, rating - float(min_rating))
                if bonus > 0:
                    breakdown["quality"] += bonus
                    reasons.append(f"rating {rating} exceeds minimum {min_rating} (+{round(bonus, 2)})")

            # practicality: time headroom
            if max_duration_minutes is not None and duration is not None and float(max_duration_minutes) > 0:
                headroom = max(0.0, (float(max_duration_minutes) - duration) / float(max_duration_minutes))
                bonus = DURATION_HEADROOM_WEIGHT * headroom
                if bonus > 0:
                    breakdown["practicality"] += bonus
                    reasons.append(f"duration {duration}min has headroom under {max_duration_minutes}min (+{round(bonus, 2)})")

            # practicality: preferred format
            if fmt_pref and fmt == fmt_pref:
                breakdown["practicality"] += FORMAT_MATCH_WEIGHT
                reasons.append(f"format '{fmt}' matches preferred format (+{FORMAT_MATCH_WEIGHT})")

            breakdown = {k: round(v, 3) for k, v in breakdown.items()}
            score = round(sum(breakdown.values()), 3)

            if score > 0:
                results.append({
                    "id": r.get('id'),
                    "title": r.get('title'),
                    "score": score,
                    "score_breakdown": breakdown,
                    "url": r.get('url'),
                    "reason": "; ".join(reasons) if reasons else f"Matched with score {score}",
                    "format": fmt or None,
                    "topic": topic or None,
                    "level": level or None,
                    "duration_minutes": duration,
                    "rating": rating,
                    "keywords": [tag.strip() for tag in r.get('tags', '').split(';') if tag.strip()],
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
