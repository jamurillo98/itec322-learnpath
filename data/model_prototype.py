"""
model_prototype.py — Sprint 3 model prototype (comparison only).

A content-based similarity model: each resource and each learner request
is turned into a TF-IDF vector of words (topic, tags, level, format and
title), and resources are ranked by cosine similarity to the request.

Why this model:
- It is a standard, explainable baseline from information retrieval.
- It needs no training labels and no extra libraries (pure Python), so it
  can be compared fairly with the rule engine on the same evaluation set.
- It applies the SAME hard filters as the rule engine, so any difference
  in results comes from ranking, not from filtering.

It is NOT used by the API. The rule engine stays the production
recommender; this file exists so the two can be compared in evaluation.
"""

import math
import re
from collections import Counter
from typing import Dict, List, Optional

from rule_engine import RuleEngine

_TOKEN = re.compile(r"[a-z0-9]+")


def _tokens(text: str) -> List[str]:
    return _TOKEN.findall((text or "").lower())


class SimilarityModel:
    def __init__(self, resources_path: Optional[str] = None):
        self.resources = RuleEngine(resources_path).resources
        docs = {r["id"]: self._resource_tokens(r) for r in self.resources}
        n = len(docs)
        df = Counter(t for toks in docs.values() for t in set(toks))
        self.idf = {t: math.log((1 + n) / (1 + c)) + 1.0 for t, c in df.items()}
        self.vectors = {rid: self._vector(toks) for rid, toks in docs.items()}

    @staticmethod
    def _resource_tokens(r: Dict) -> List[str]:
        return (_tokens(r.get("topic")) + _tokens(r.get("tags", "").replace(";", " "))
                + _tokens(r.get("level")) + _tokens(r.get("format")) + _tokens(r.get("title")))

    def _vector(self, toks: List[str]) -> Dict[str, float]:
        tf = Counter(toks)
        vec = {t: c * self.idf.get(t, 0.0) for t, c in tf.items()}
        norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
        return {t: v / norm for t, v in vec.items()}

    def recommend_learning_resources(self, subject: str, difficulty: Optional[str] = None,
                                     max_duration_minutes: Optional[float] = None,
                                     min_rating: Optional[float] = None,
                                     keywords: Optional[List[str]] = None, limit: int = 10,
                                     preferred_format: Optional[str] = None) -> List[Dict]:
        query = _tokens(subject) + _tokens(difficulty or "") + _tokens(preferred_format or "")
        for k in keywords or []:
            query += _tokens(k)
        qvec = self._vector(query)
        results = []
        for r in self.resources:
            duration = RuleEngine._to_float(r.get("duration_minutes"))
            rating = RuleEngine._to_float(r.get("rating"))
            if max_duration_minutes is not None and duration is not None and duration > float(max_duration_minutes):
                continue
            if min_rating is not None and rating is not None and rating < float(min_rating):
                continue
            rvec = self.vectors[r["id"]]
            score = sum(w * rvec.get(t, 0.0) for t, w in qvec.items())
            if score > 0:
                results.append({"id": r["id"], "title": r.get("title"), "score": round(score, 4),
                                "reason": "content similarity to request"})
        results.sort(key=lambda x: (-x["score"], x["id"]))
        return results[:limit]
