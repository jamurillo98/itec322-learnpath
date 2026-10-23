from pathlib import Path
import sys
from fastapi.testclient import TestClient
# Add the repository paths so the tests can import the application and rule engine.
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "backend"))
sys.path.insert(0, str(REPOSITORY_ROOT))
from app.main import app
from data.rule_engine import RuleEngine
client = TestClient(app)
def request_payload(**overrides):
    """Return a valid recommendation request with optional overrides."""
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
    """The health endpoint should return HTTP 200."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
def test_valid_recommendation_response_shape_and_scores():
    """A valid request should return recommendations with the expected fields."""
    response = client.post(
        "/api/recommend",
        json=request_payload(),
    )
    assert response.status_code == 200
    body = response.json()
    assert set(body) == {"recommendations"}
    assert body["recommendations"]
    required_fields = {
        "id",
        "title",
        "score",
        "url",
        "reason",
    }
    for recommendation in body["recommendations"]:
        assert required_fields.issubset(recommendation)
        assert isinstance(recommendation["score"], (int, float))
def test_recommendations_are_deterministically_sorted():
    """Repeated identical requests should produce identical results."""
    payload = request_payload(
        subject="programming",
        difficulty="beginner",
        keywords=[],
    )
    first_response = client.post(
        "/api/recommend",
        json=payload,
    )
    second_response = client.post(
        "/api/recommend",
        json=payload,
    )
    assert first_response.status_code == 200
    assert second_response.status_code == 200
    assert first_response.json() == second_response.json()
    recommendations = first_response.json()["recommendations"]
    actual_order = [
        (item["score"], item["id"])
        for item in recommendations
    ]
    expected_order = sorted(
        actual_order,
        key=lambda item: (-item[0], item[1]),
    )
    assert actual_order == expected_order
def test_invalid_requests_return_422():
    """Invalid field values should be rejected by request validation."""
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
    for invalid_payload in invalid_payloads:
        response = client.post(
            "/api/recommend",
            json=request_payload(**invalid_payload),
        )
        assert response.status_code == 422, (
            f"Expected HTTP 422 for {invalid_payload}, "
            f"but received {response.status_code}: {response.text}"
        )
def test_invalid_limit_returns_422():
    """A recommendation limit above the supported maximum is rejected."""
    response = client.post(
        "/api/recommend",
        json=request_payload(limit=1000),
    )
    assert response.status_code == 422
def test_missing_subject_returns_422():
    """The API should reject a request without a subject."""
    payload = request_payload()
    del payload["subject"]
    response = client.post(
        "/api/recommend",
        json=payload,
    )
    assert response.status_code == 422
def test_empty_recommendations():
    """A request with no eligible resources should return an empty list."""
    response = client.post(
        "/api/recommend",
        json=request_payload(max_duration_minutes=0),
    )
    assert response.status_code == 200
    assert response.json() == {"recommendations": []}
def test_api_uses_canonical_rule_engine():
    """The API results should match the canonical rule engine."""
    payload = request_payload()
    expected = RuleEngine().recommend_learning_resources(
        subject=payload["subject"],
        difficulty=payload["difficulty"],
        max_duration_minutes=60.0,
        min_rating=4.0,
        keywords=payload["keywords"],
        limit=payload["limit"],
    )
    response = client.post(
        "/api/recommend",
        json=payload,
    )
    assert response.status_code == 200
    assert response.json()["recommendations"] == expected