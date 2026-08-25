"""
Simple rule-based recommendation engine.

This module intentionally contains no ML code — only deterministic rules.

What goes inside:
- `RuleEngine` class: loads resources, evaluates simple rules, returns ranked results
- Small, easy-to-understand matching rules for Sprint 1
"""
import csv
import os
from typing import List, Dict, Any


class RuleEngine:
    """A very small rule-based recommender for Sprint 1."""

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

    def recommend(self, query: str, user_profile: Dict[str, Any] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Return simple keyword-matching recommendations.

        Rules implemented (examples):
        - If query tokens appear in `topic` or `title`, boost score
        - If user_profile contains `level`, prefer matching level
        - Simple substring matching only
        """
        if not query:
            return []

        q = query.lower()
        results = []
        for r in self.resources:
            score = 0
            title = r.get('title', '').lower()
            topic = r.get('topic', '').lower()
            tags = r.get('tags', '').lower()
            level = r.get('level', '').lower()

            if q in title:
                score += 3
            if q in topic:
                score += 2
            if q in tags:
                score += 1

            # user profile rule example
            if user_profile and 'level' in user_profile:
                pref = str(user_profile.get('level', '')).lower()
                if pref and pref == level:
                    score += 1

            if score > 0:
                results.append({"id": r.get('id'), "title": r.get('title'), "score": score, "url": r.get('url'), "reason": f"Matched with score {score}"})

        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:limit]


if __name__ == '__main__':
    # Quick local demo
    engine = RuleEngine()
    print(engine.recommend('python'))
