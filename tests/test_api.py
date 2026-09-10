import json
from urllib.request import Request, urlopen


def test_recommend_api():
    url = "http://127.0.0.1:8000/api/recommend"

    data = {
        "subject": "python",
        "difficulty": "beginner",
        "max_duration_minutes": 30,
        "min_rating": 4,
        "keywords": ["python"],
        "limit": 5
    }

    request = Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urlopen(request) as response:
        result = json.loads(response.read().decode("utf-8"))

    assert response.status == 200
    assert isinstance(result, list)