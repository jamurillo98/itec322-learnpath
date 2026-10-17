from pathlib import Path
import sys

from fastapi.testclient import TestClient

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "backend"))
sys.path.insert(0, str(REPOSITORY_ROOT))

from app.main import app
from data.rule_engine import RuleEngine


client = TestClient(app)


def request_payload(**overrides):
    payload = {
        "subject": "python",
        "difficulty": "beginner",
        "max_duration_minutes": 60,
        "min_rating": 4,
        "keywords": ["python"],
        "limit": 5,
    }
    payload.update(overrides)
    return payload


def test_health():
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_valid_recommendation_response_shape_and_scores():
    response = client.post("/api/recommend", json=request_payload())
    body = response.json()

    assert response.status_code == 200
    assert set(body) == {"recommendations"}
    assert body["recommendations"]

    assert {
        "id",
        "title",
        "score",
        "url",
        "reason",
    }.issubset(body["recommendations"][0])

    assert all(
        isinstance(item["score"], (int, float))
        for item in body["recommendations"]
    )


def test_recommendations_are_deterministically_sorted():
    payload = request_payload(
        subject="programming",
        difficulty="beginner",
        keywords=[],
    )

    first = client.post("/api/recommend", json=payload).json()
    second = client.post("/api/recommend", json=payload).json()

    assert first == second

    actual_order = [
        (item["score"], item["id"])
        for item in first["recommendations"]
    ]

    expected_order = sorted(
        actual_order,
        key=lambda item: (-item[0], item[1]),
    )

    assert actual_order == expected_order


def test_invalid_requests_return_422():
    invalid_payloads = [
        {"subject": "   "},
        {"difficulty": "expert"},
        {"max_duration_minutes": -1},
        {"min_rating": 5.1},
        {"min_rating": -0.1},
        {"limit": 0},
        {"limit": 51},
        {"keywords": ["python", 3]},
    ]

    for invalid in invalid_payloads:
        response = client.post(
            "/api/recommend",
            json=request_payload(**invalid),
        )

        assert response.status_code == 422, invalid


def test_invalid_limit_returns_422():
    response = client.post(
        "/api/recommend",
        json=request_payload(limit=1000),
    )

    assert response.status_code == 422


def test_missing_subject_returns_422():
    payload = request_payload()
    del payload["subject"]

    response = client.post("/api/recommend", json=payload)

    assert response.status_code == 422


def test_empty_recommendations():
    response = client.post(
        "/api/recommend",
        json=request_payload(max_duration_minutes=0),
    )

    assert response.status_code == 200
    assert response.json() == {"recommendations": []}


def test_api_uses_canonical_rule_engine():
    payload = request_payload()

    expected = RuleEngine().recommend_learning_resources(
        subject=payload["subject"],
        difficulty=payload["difficulty"],
        max_duration_minutes=60.0,
        min_rating=4.0,
        keywords=payload["keywords"],
        limit=payload["limit"],
    )

    response = client.post("/api/recommend", json=payload)

    assert response.status_code == 200
    actual = response.json()["recommendations"]

    assert actual == expected