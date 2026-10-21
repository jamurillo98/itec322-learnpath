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
    w = engine.weights
    assert r['score_breakdown']['relevance'] == w['SUBJECT_MATCH_WEIGHT'] + w['KEYWORD_MATCH_WEIGHT']
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


# --- Sprint 3: edge cases ------------------------------------------------

def test_empty_and_blank_keywords_do_not_crash(engine):
    a = engine.recommend_learning_resources(subject='programming', keywords=[])
    b = engine.recommend_learning_resources(subject='programming', keywords=['', '   '])
    assert a == b


def test_zero_duration_returns_empty(engine):
    assert engine.recommend_learning_resources(subject='programming', max_duration_minutes=0) == []


def test_max_rating_filter_returns_only_perfect_scores(engine):
    # no resource is rated 5.0, so nothing should survive the hard filter
    assert engine.recommend_learning_resources(subject='programming', min_rating=5) == []


def test_matching_is_case_and_space_insensitive(engine):
    a = engine.recommend_learning_resources(subject='programming', keywords=['python'])
    b = engine.recommend_learning_resources(subject='  PROGRAMMING ', keywords=['PyThOn'])
    assert [r['id'] for r in a] == [r['id'] for r in b]


def test_unknown_difficulty_gives_no_level_points(engine):
    results = engine.recommend_learning_resources(subject='programming', difficulty='expert')
    assert results and all(r['score_breakdown']['level_fit'] == 0 for r in results)


def test_ties_are_broken_by_id(engine):
    results = engine.recommend_learning_resources(subject='programming', limit=50)
    for a, b in zip(results, results[1:]):
        if a['score'] == b['score']:
            assert a['id'] < b['id']


def test_missing_csv_returns_empty_not_crash(tmp_path):
    engine = RuleEngine(str(tmp_path / 'does_not_exist.csv'))
    assert engine.recommend_learning_resources(subject='programming') == []


def test_rows_with_missing_rating_or_duration_are_kept(tmp_path):
    csv_path = tmp_path / 'r.csv'
    csv_path.write_text(
        'id,title,topic,tags,level,format,url,duration_minutes,rating,cost\n'
        'X1,No rating,programming,python,beginner,video,https://e.com,30,,0\n'
        'X2,No duration,programming,python,beginner,video,https://e.com,,4.0,0\n',
        encoding='utf-8')
    results = RuleEngine(str(csv_path)).recommend_learning_resources(
        subject='programming', max_duration_minutes=60, min_rating=4.0)
    assert {r['id'] for r in results} == {'X1', 'X2'}


def test_custom_weights_change_scores():
    default = RuleEngine().recommend_learning_resources(subject='programming', keywords=['python'], limit=50)
    heavier = RuleEngine(weights={'KEYWORD_MATCH_WEIGHT': 10}).recommend_learning_resources(
        subject='programming', keywords=['python'], limit=50)
    assert heavier[0]['score'] > default[0]['score']


def test_unknown_weight_name_raises():
    with pytest.raises(ValueError):
        RuleEngine(weights={'NOT_A_WEIGHT': 1})


def test_zero_min_rating_does_not_outweigh_difficulty(engine):
    """The website sends min_rating=0 when the box is empty; level must still matter."""
    results = engine.recommend_learning_resources(
        subject='mathematics', difficulty='advanced', max_duration_minutes=30,
        min_rating=0, keywords=['theory'])
    assert results[0]['level'] == 'advanced'
    assert all(r['score_breakdown']['quality'] <= engine.weights['QUALITY_BONUS_CAP'] for r in results)


# --- Sprint 3: model prototype -------------------------------------------

from model_prototype import SimilarityModel


def test_model_prototype_respects_hard_filters(engine):
    results = SimilarityModel().recommend_learning_resources(
        subject='programming', max_duration_minutes=40, min_rating=4.5, limit=50)
    by_id = {r['id']: r for r in engine.resources}
    for r in results:
        assert float(by_id[r['id']]['duration_minutes']) <= 40
        assert float(by_id[r['id']]['rating']) >= 4.5


# --- Sprint 4: frozen recommendation contract ----------------------------

FROZEN_FIELDS = {
    'id', 'title', 'score', 'score_breakdown', 'url', 'reason', 'format',
    'topic', 'level', 'duration_minutes', 'rating', 'keywords',
}


def test_recommendation_fields_are_frozen(engine):
    """Sprint 4 contract freeze: the frontend relies on exactly these fields."""
    for r in engine.recommend_learning_resources(subject='programming', limit=50):
        assert set(r) == FROZEN_FIELDS
        assert isinstance(r['score'], float)
        assert isinstance(r['score_breakdown'], dict)
        assert isinstance(r['keywords'], list)


if __name__ == '__main__':
    import sys
    sys.exit(pytest.main([__file__, '-v']))
