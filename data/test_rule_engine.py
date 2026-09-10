"""
test_rule_engine.py
--------------------
Tests for the Rule-Based Learning Resource Recommendation Engine.

Run with:  pytest test_rule_engine.py -v
"""

import pytest

from rule_engine import RuleEngine


@pytest.fixture
def engine():
    return RuleEngine()


# --- Determinism -------------------------------------------------------

def test_recommend_is_deterministic(engine):
    r1 = engine.recommend_learning_resources(subject='mathematics', difficulty='intermediate', keywords=['theory'])
    r2 = engine.recommend_learning_resources(subject='mathematics', difficulty='intermediate', keywords=['theory'])
    assert [r['id'] for r in r1] == [r['id'] for r in r2]
    assert [r['score'] for r in r1] == [r['score'] for r in r2]


def test_output_independent_of_input_order(engine):
    original = engine.recommend_learning_resources(subject='programming', difficulty='beginner')
    engine.resources = list(reversed(engine.resources))
    shuffled = engine.recommend_learning_resources(subject='programming', difficulty='beginner')
    assert [r['id'] for r in original] == [r['id'] for r in shuffled]


# --- Hard filters --------------------------------------------------------

def test_max_duration_minutes_excludes_long_resources(engine):
    results = engine.recommend_learning_resources(subject='', max_duration_minutes=50)
    for r in results:
        resource = next(x for x in engine.resources if x['id'] == r['id'])
        assert float(resource['duration_minutes']) <= 50


def test_min_rating_excludes_low_rated_resources(engine):
    results = engine.recommend_learning_resources(subject='', min_rating=4.5)
    for r in results:
        resource = next(x for x in engine.resources if x['id'] == r['id'])
        assert float(resource['rating']) >= 4.5


# --- Scoring rules ---------------------------------------------------------

def test_subject_match_increases_score(engine):
    programming_score = next(
        r['score'] for r in engine.recommend_learning_resources(subject='programming', keywords=[])
        if r['id'] == 'R001'
    )
    no_subject_score = next(
        (r['score'] for r in engine.recommend_learning_resources(subject='', keywords=[]) if r['id'] == 'R001'),
        0
    )
    assert programming_score > no_subject_score


def test_exact_difficulty_scores_higher_than_adjacent(engine):
    results = engine.recommend_learning_resources(subject='', difficulty='intermediate', keywords=[])
    exact_match = next(r for r in results if r['id'] == 'R006')  # intermediate
    adjacent_match = next(r for r in results if r['id'] == 'R001')  # beginner
    assert exact_match['score'] > adjacent_match['score']


def test_keyword_match_reflected_in_reason(engine):
    results = engine.recommend_learning_resources(subject='programming', keywords=['hands-on'])
    assert any('matching keyword' in r['reason'] for r in results)


def test_recommend_returns_at_most_limit(engine):
    results = engine.recommend_learning_resources(subject='programming', limit=2)
    assert len(results) <= 2


def test_no_criteria_returns_empty(engine):
    """With no subject, difficulty, keywords, or filters, nothing should score > 0."""
    assert engine.recommend_learning_resources(subject='') == []


def test_impossible_duration_filter_returns_empty(engine):
    results = engine.recommend_learning_resources(subject='programming', max_duration_minutes=1)
    assert results == []


if __name__ == '__main__':
    import sys
    sys.exit(pytest.main([__file__, '-v']))
