import csv
from pathlib import Path
from typing import Any, Dict, List


RESOURCE_FILE = Path(__file__).resolve().parents[2] / "data" / "sample_resources.csv"


def _number(value: str, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def recommend_learning_resources(
    subject: str,
    difficulty: str,
    max_duration_minutes: int,
    min_rating: float,
    keywords: List[str],
    limit: int,
) -> List[Dict[str, Any]]:
    requested_keywords = [keyword.strip().lower() for keyword in keywords if keyword.strip()]
    results = []

    with RESOURCE_FILE.open(newline="", encoding="utf-8") as resource_file:
        for resource in csv.DictReader(resource_file):
            duration = _number(resource.get("duration_minutes"))
            rating = _number(resource.get("rating"))
            tags = [tag.strip() for tag in resource.get("tags", "").split(";") if tag.strip()]
            searchable_text = " ".join(
                [resource.get("title", ""), resource.get("topic", ""), *tags]
            ).lower()

            if duration > max_duration_minutes or rating < min_rating:
                continue
            if subject.strip().lower() not in searchable_text:
                continue
            if difficulty.strip() and difficulty.strip().lower() != resource.get("level", "").lower():
                continue
            if requested_keywords and not all(keyword in searchable_text for keyword in requested_keywords):
                continue

            results.append(
                {
                    "subject": resource.get("topic", subject),
                    "difficulty": resource.get("level", difficulty),
                    "duration_minutes": int(duration),
                    "rating": rating,
                    "keywords": tags,
                    "id": resource.get("id"),
                    "title": resource.get("title"),
                    "url": resource.get("url"),
                }
            )

    return results[:limit]