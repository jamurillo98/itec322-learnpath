"""
test_rule_engine.py
--------------------
Tests for RuleEngine — covers both the original Sprint 1 scaffold
behaviour (keyword matching, level bonus) and the new extensions
(hard filters, rating/duration scoring).

Run with:  pytest test_rule_engine.py -v
"""

import pytest

from rule_engine import RuleEngine


@pytest.fixture
def engine():
    return RuleEngine()


# --- Original scaffold behaviour (must not regress) -------------------------

def test_empty_query_returns_empty_list(engine):
    assert engine.recommend('') == []


def test_keyword_match_on_title(engine):
    results = engine.recommend('python')
    assert any(r['id'] == 'R001' for r in results)


def test_results_are_ranked_by_score_descending(engine):
    results = engine.recommend('python')
    scores = [r['score'] for r in results]
    assert scores == sorted(scores, reverse=True)


def test_level_preference_boosts_matching_items(engine):
    with_level = {r['id']: r['score'] for r in engine.recommend('python', user_profile={'level': 'beginner'})}
    without_level = {r['id']: r['score'] for r in engine.recommend('python', user_profile=None)}
    assert with_level.get('R001', 0) >= without_level.get('R001', 0)


def test_limit_is_respected(engine):
    results = engine.recommend('a', limit=2)
    assert len(results) <= 2


# --- New extensions -----------------------------------------------------------

def test_max_duration_hard_filter_excludes_long_resources(engine):
    results = engine.recommend('hands-on', user_profile={'max_duration': 60})
    for r in results:
        resource = next(row for row in engine.resources if row['id'] == r['id'])
        assert float(resource['duration_minutes']) <= 60


def test_min_rating_hard_filter_excludes_low_rated_resources(engine):
    results = engine.recommend('theory', user_profile={'min_rating': 4.3})
    for r in results:
        resource = next(row for row in engine.resources if row['id'] == r['id'])
        assert float(resource['rating']) >= 4.3


def test_recommend_is_deterministic(engine):
    result_1 = engine.recommend('python', user_profile={'level': 'beginner', 'max_duration': 100})
    result_2 = engine.recommend('python', user_profile={'level': 'beginner', 'max_duration': 100})
    assert [r['id'] for r in result_1] == [r['id'] for r in result_2]
    assert [r['score'] for r in result_1] == [r['score'] for r in result_2]


def test_reason_field_explains_the_score(engine):
    results = engine.recommend('python', user_profile={'level': 'beginner'})
    assert all('reason' in r and r['reason'] for r in results)


if __name__ == '__main__':
    import sys
    sys.exit(pytest.main([__file__, '-v']))
