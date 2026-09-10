"""
test_rule_engine.py
--------------------
Tests for RuleEngine — covers the original recommend() method
(keyword matching, level bonus, hard filters) plus the new
recommend_from_request() method that matches frontend/backend fields
directly (project_type, budget, priorities, notes).

Run with:  pytest test_rule_engine.py -v
"""

import pytest

from rule_engine import RuleEngine


@pytest.fixture
def engine():
    return RuleEngine()


# --- Original method (must not regress) --------------------------------

def test_empty_query_returns_empty_list(engine):
    assert engine.recommend('') == []


def test_keyword_match_on_title(engine):
    results = engine.recommend('python')
    assert any(r['id'] == 'R001' for r in results)


def test_max_duration_hard_filter_excludes_long_resources(engine):
    results = engine.recommend('hands-on', user_profile={'max_duration': 60})
    for r in results:
        resource = next(row for row in engine.resources if row['id'] == r['id'])
        assert float(resource['duration_minutes']) <= 60


def test_original_recommend_is_deterministic(engine):
    r1 = engine.recommend('python', user_profile={'level': 'beginner'})
    r2 = engine.recommend('python', user_profile={'level': 'beginner'})
    assert [r['id'] for r in r1] == [r['id'] for r in r2]


# --- New: recommend_from_request() (matches frontend/backend fields) ----

def test_recommend_from_request_returns_results(engine):
    results = engine.recommend_from_request(project_type='programming', budget=100, priorities=[])
    assert len(results) > 0


def test_budget_hard_filter_excludes_over_budget_resources(engine):
    results = engine.recommend_from_request(project_type='', budget=10, priorities=[])
    for r in results:
        resource = next(row for row in engine.resources if row['id'] == r['id'])
        assert float(resource['cost']) <= 10


def test_priorities_matching_boosts_score(engine):
    with_priority = {
        r['id']: r['score']
        for r in engine.recommend_from_request(project_type='programming', budget=100, priorities=['hands-on'])
    }
    without_priority = {
        r['id']: r['score']
        for r in engine.recommend_from_request(project_type='programming', budget=100, priorities=[])
    }
    assert with_priority.get('R005', 0) > without_priority.get('R005', 0)


def test_recommend_from_request_is_deterministic(engine):
    r1 = engine.recommend_from_request(project_type='programming', budget=50, priorities=['hands-on'])
    r2 = engine.recommend_from_request(project_type='programming', budget=50, priorities=['hands-on'])
    assert [r['id'] for r in r1] == [r['id'] for r in r2]
    assert [r['score'] for r in r1] == [r['score'] for r in r2]


def test_no_budget_means_no_budget_filter(engine):
    """If budget is None, nothing should be excluded on cost grounds."""
    results = engine.recommend_from_request(project_type='programming', budget=None, priorities=[])
    result_ids = {r['id'] for r in results}
    assert 'R008' in result_ids or len(results) == len(
        [r for r in engine.resources if 'programming' in r['topic'].lower()]
    )


def test_notes_field_accepted_but_does_not_error(engine):
    """notes has no scoring rule yet, but the method should accept it without breaking."""
    results = engine.recommend_from_request(
        project_type='programming', budget=100, priorities=[], notes="just exploring options"
    )
    assert isinstance(results, list)


if __name__ == '__main__':
    import sys
    sys.exit(pytest.main([__file__, '-v']))
