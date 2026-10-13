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
    # limit=50 so both resources are returned regardless of dataset size
    results = engine.recommend_learning_resources(subject='', difficulty='intermediate', keywords=[], limit=50)
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


# --- Sprint 2: categories, score breakdown, fixtures ----------------------

from rule_engine import RULE_CATEGORIES, VALID_FORMATS


def test_every_resource_has_valid_format(engine):
    for r in engine.resources:
        assert r['format'] in VALID_FORMATS, f"{r['id']} has invalid format {r['format']!r}"


def test_fixtures_cover_every_format_and_level(engine):
    combos = {(r['format'], r['level']) for r in engine.resources}
    for fmt in VALID_FORMATS:
        for level in ('beginner', 'intermediate', 'advanced'):
            assert (fmt, level) in combos, f"no {level} {fmt} in fixtures"


def test_resource_ids_are_unique(engine):
    ids = [r['id'] for r in engine.resources]
    assert len(ids) == len(set(ids))


def test_score_breakdown_has_all_categories(engine):
    results = engine.recommend_learning_resources(subject='programming', difficulty='beginner')
    assert results
    for r in results:
        assert set(r['score_breakdown']) == set(RULE_CATEGORIES)


def test_score_breakdown_sums_to_total_score(engine):
    results = engine.recommend_learning_resources(
        subject='data-science', difficulty='intermediate', max_duration_minutes=90,
        min_rating=4.0, keywords=['python'], preferred_format='video', limit=50,
    )
    assert results
    for r in results:
        assert sum(r['score_breakdown'].values()) == pytest.approx(r['score'], abs=0.01)


def test_rules_land_in_correct_category(engine):
    r = next(x for x in engine.recommend_learning_resources(
        subject='programming', difficulty='beginner', keywords=['python'], limit=50)
        if x['id'] == 'R001')
    assert r['score_breakdown']['relevance'] == 6.5   # subject 5 + 1 keyword 1.5
    assert r['score_breakdown']['level_fit'] == 3.0   # exact difficulty
    assert r['score_breakdown']['quality'] == 0.0     # no min_rating given
    assert r['score_breakdown']['practicality'] == 0.0


def test_preferred_format_boosts_matching_resources(engine):
    base = engine.recommend_learning_resources(subject='programming', difficulty='beginner', limit=50)
    boosted = engine.recommend_learning_resources(
        subject='programming', difficulty='beginner', preferred_format='exercise', limit=50)
    # resources with no base match score 0 and are absent from `base`
    base_scores = {r['id']: r['score'] for r in base}
    for r in boosted:
        if r['format'] == 'exercise':
            assert r['score'] == pytest.approx(base_scores.get(r['id'], 0.0) + 2.0)
        else:
            assert r['score'] == pytest.approx(base_scores[r['id']])


def test_preferred_format_changes_top_result(engine):
    top_video = engine.recommend_learning_resources(
        subject='programming', difficulty='beginner', preferred_format='video')[0]
    top_exercise = engine.recommend_learning_resources(
        subject='programming', difficulty='beginner', preferred_format='exercise')[0]
    assert top_video['format'] == 'video'
    assert top_exercise['format'] == 'exercise'


def test_preferred_format_is_case_insensitive(engine):
    a = engine.recommend_learning_resources(subject='mathematics', preferred_format='Video')
    b = engine.recommend_learning_resources(subject='mathematics', preferred_format='video')
    assert a == b


def test_invalid_preferred_format_raises(engine):
    with pytest.raises(ValueError):
        engine.recommend_learning_resources(subject='programming', preferred_format='podcast')


def test_format_alone_does_not_return_everything_without_match(engine):
    """Format is a preference: only matching-format resources gain points."""
    results = engine.recommend_learning_resources(subject='', preferred_format='article', limit=50)
    assert results and all(r['format'] == 'article' for r in results)


def test_results_include_category_fields(engine):
    r = engine.recommend_learning_resources(subject='programming')[0]
    for field in ('format', 'topic', 'level', 'score_breakdown'):
        assert field in r


if __name__ == '__main__':
    import sys
    sys.exit(pytest.main([__file__, '-v']))
