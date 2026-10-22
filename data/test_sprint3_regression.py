"""
test_sprint3_regression.py
---------------------------
Sprint 3 regression and edge-case tests for the rule engine, plus a guard
that the evaluation set never scores worse than the recorded tuned run.

Run with:  pytest data/test_sprint3_regression.py -v
"""

import json
import os

import pytest

import evaluate
from rule_engine import RuleEngine

HERE = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture
def engine():
    return RuleEngine()


def ids(results):
    return [r['id'] for r in results]


# --- Evaluation guard ----------------------------------------------------------

def test_evaluation_has_no_regression_against_tuned_results():
    """If a rule change makes any metric or case worse, this fails."""
    current = evaluate.evaluate()
    with open(os.path.join(HERE, 'tuned_results.json'), encoding='utf-8') as fh:
        recorded = json.load(fh)
    lines, regressed = evaluate.compare(current, recorded)
    assert not regressed, "\n".join(lines)


def test_evaluation_never_violates_hard_filters():
    assert evaluate.evaluate()['summary']['hard_filter_violations'] == 0


# --- Subject matching (Sprint 3 tuning) ------------------------------------------

def test_subject_with_space_matches_hyphenated_topic(engine):
    spaced = engine.recommend_learning_resources(subject='data science', limit=50)
    hyphen = engine.recommend_learning_resources(subject='data-science', limit=50)
    assert ids(spaced) == ids(hyphen) and spaced


def test_subject_alias_maths_matches_mathematics(engine):
    maths = engine.recommend_learning_resources(subject='maths', limit=50)
    full = engine.recommend_learning_resources(subject='mathematics', limit=50)
    assert ids(maths) == ids(full) and maths


def test_subject_matches_tags_such_as_python(engine):
    results = engine.recommend_learning_resources(subject='python', limit=50)
    assert {'R001', 'R011', 'R024'} <= set(ids(results))


def test_subject_matching_ignores_case_and_outer_whitespace(engine):
    a = engine.recommend_learning_resources(subject='  PROGRAMMING ', difficulty='Beginner', keywords=['PYTHON'])
    b = engine.recommend_learning_resources(subject='programming', difficulty='beginner', keywords=['python'])
    # reasons echo the learner's own text, so compare ranking and scores
    assert [(r['id'], r['score']) for r in a] == [(r['id'], r['score']) for r in b] and a


# --- Relevance gate --------------------------------------------------------------

def test_unknown_subject_returns_nothing_even_with_difficulty(engine):
    assert engine.recommend_learning_resources(subject='cooking', difficulty='beginner',
                                               max_duration_minutes=60, min_rating=4.0) == []


def test_keyword_only_request_still_works(engine):
    results = engine.recommend_learning_resources(subject='', keywords=['python'], limit=50)
    assert results and all('python' in r['keywords'] for r in results)


def test_difficulty_only_request_still_works(engine):
    """With no subject and no keywords there is no content criterion, so difficulty ranks everything."""
    results = engine.recommend_learning_resources(subject='', difficulty='beginner', limit=50)
    assert results


def test_filters_only_cannot_surface_unrelated_resources(engine):
    results = engine.recommend_learning_resources(subject='history', max_duration_minutes=1000, min_rating=0)
    assert results == []


# --- Boundaries ----------------------------------------------------------------------

def test_duration_limit_is_inclusive(engine):
    # R009 is exactly 30 minutes
    assert 'R009' in ids(engine.recommend_learning_resources(subject='python', max_duration_minutes=30, limit=50))
    assert 'R009' not in ids(engine.recommend_learning_resources(subject='python', max_duration_minutes=29.9, limit=50))


def test_rating_floor_is_inclusive(engine):
    # R010 is rated exactly 4.0
    assert 'R010' in ids(engine.recommend_learning_resources(subject='python', min_rating=4.0, limit=50))
    assert 'R010' not in ids(engine.recommend_learning_resources(subject='python', min_rating=4.01, limit=50))


def test_zero_duration_returns_nothing(engine):
    assert engine.recommend_learning_resources(subject='programming', max_duration_minutes=0) == []


def test_rating_floor_above_every_resource_returns_nothing(engine):
    assert engine.recommend_learning_resources(subject='programming', min_rating=5.0) == []


def test_limit_one_returns_the_top_result(engine):
    full = engine.recommend_learning_resources(subject='programming', difficulty='beginner', limit=50)
    one = engine.recommend_learning_resources(subject='programming', difficulty='beginner', limit=1)
    assert ids(one) == ids(full)[:1]


# --- Stable ordering -------------------------------------------------------------------

def test_ties_are_broken_by_id(engine):
    results = engine.recommend_learning_resources(subject='programming', limit=50)
    keys = [(-r['score'], r['id']) for r in results]
    assert keys == sorted(keys)


def test_order_is_stable_when_catalogue_order_changes(engine):
    request = dict(subject='data science', difficulty='intermediate', keywords=['python'], limit=50)
    before = engine.recommend_learning_resources(**request)
    engine.resources = list(reversed(engine.resources))
    assert engine.recommend_learning_resources(**request) == before


def test_repeated_calls_give_identical_output(engine):
    request = dict(subject='programming', difficulty='beginner', max_duration_minutes=60,
                   min_rating=4.0, keywords=['python'], preferred_format='video')
    assert engine.recommend_learning_resources(**request) == engine.recommend_learning_resources(**request)


# --- Result shape ----------------------------------------------------------------------------

def test_every_result_has_the_fields_the_api_exposes(engine):
    for r in engine.recommend_learning_resources(subject='programming', limit=50):
        for field in ('id', 'title', 'score', 'url', 'reason', 'score_breakdown'):
            assert field in r
        assert r['score'] > 0 and r['reason']


# --- Sprint 4 release fixes ------------------------------------------------------

def test_blank_keywords_are_ignored(engine):
    """A whitespace-only keyword used to match every resource and inflate scores."""
    plain = engine.recommend_learning_resources(subject='programming', keywords=[])
    blank = engine.recommend_learning_resources(subject='programming', keywords=['', '   '])
    assert plain == blank


def test_blank_keyword_does_not_bypass_relevance_gate(engine):
    """An unknown subject plus a blank keyword must still return nothing."""
    assert engine.recommend_learning_resources(subject='cooking', difficulty='beginner', keywords=['   ']) == []


def test_empty_rating_box_does_not_outweigh_difficulty(engine):
    """The website sends min_rating=0 when the box is empty; level must still decide."""
    results = engine.recommend_learning_resources(subject='mathematics', difficulty='advanced',
                                                  max_duration_minutes=30, min_rating=0, keywords=['theory'])
    assert results[0]['level'] == 'advanced'
    assert all(r['score_breakdown']['quality'] <= 1.0 for r in results)
    assert results[0]['score'] - results[1]['score'] >= 2.0


if __name__ == '__main__':
    import sys
    sys.exit(pytest.main([__file__, '-v']))
