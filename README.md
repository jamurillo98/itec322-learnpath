# Data & Model — Rule-Based Learning Resource Recommendation Engine

Deterministic, rule-based recommender for learning resources. No ML —
every score is produced by explicit, explainable rules so results are
reproducible and easy to justify in the project report.

## Files in this folder

| File | Purpose |
|---|---|
| `rule_engine.py` | `RuleEngine` class — loads resources from CSV, scores and ranks them via `recommend_learning_resources()` |
| `sample_resources.csv` | Sample dataset of 30 learning resources across programming, mathematics, and data-science, covering every format (video/article/exercise) at every level |
| `evaluation_set.json`, `evaluate.py`, `baseline_results.json`, `tuned_results.json` | Sprint 3 evaluation: hand-judged cases, the scoring script, the before/after records (see `docs/SPRINT3_EVALUATION.md`) |
| `test_sprint3_regression.py` | Sprint 3 edge-case and regression tests, plus a guard that evaluation results never get worse |
| `test_rule_engine.py` | Unit tests covering determinism, hard filters, scoring rules, rule categories, format preference and fixture coverage |
| `EXAMPLE_INPUTS.md` | Five documented example requests with their real outputs and score breakdowns |
| `MODEL_CARD.md` | Final model summary: how it works, evaluation results, Sprint 4 fixes, limitations, future ML path |
| `DEMO_SCENARIOS.md` | Six prepared demo inputs with expected website/API results (Sprint 4 demo data) |

## For whoever wires this into the backend/frontend

This is the engine's only interface — `recommend_learning_resources()`.
Field names are explicit and self-descriptive (`subject`, `difficulty`,
`max_duration_minutes`, `min_rating`, `keywords`), matching the actual
domain of a learning resource recommender. No web framework dependency
— this can be called directly from a FastAPI route, a script, or tests.

```python
from rule_engine import RuleEngine

engine = RuleEngine()
results = engine.recommend_learning_resources(
    subject="programming",       # required
    difficulty="beginner",       # optional
    max_duration_minutes=60,     # optional, hard filter
    min_rating=4.0,              # optional, hard filter
    keywords=["hands-on"],       # optional
    limit=10,
    preferred_format="video",    # optional: video | article | exercise
)
```

Returns a list of dicts, each with `id`, `title`, `score`,
`score_breakdown` (points per rule category), `url`, `reason`
(human-readable explanation of the score), `format`, `topic`, `level`,
`duration_minutes`, `rating` and `keywords`, sorted by score descending
then id ascending.

## Rules implemented

- **Hard filters** (resources failing these are excluded entirely, not down-ranked):
  - `max_duration_minutes` — resources longer than this are excluded
  - `min_rating` — resources rated lower than this are excluded
- **Subject match** (+5): every word of `subject` must appear in the resource's topic, tags or title. Matching ignores case and treats hyphens as spaces (`data science` = `data-science`), and a few short forms are expanded (`maths`, `ml`, `js`, `stats`)
- **Relevance gate** (Sprint 3): if the learner gives a subject or keywords, a resource must match at least one of them to be returned. Difficulty, rating, duration and format only rank relevant resources, so an unknown subject such as `cooking` returns no results instead of arbitrary beginner resources
- **Difficulty match**: exact match (+3), one level off — e.g. beginner↔intermediate (+1), otherwise (+0)
- **Keyword match** (+1.5 per match): each keyword compared against the resource's tags; blank keywords are ignored
- **Rating bonus**: resources rated above `min_rating` score proportionally higher, capped at +1 so an empty rating box (sent as 0) cannot outweigh difficulty
- **Duration headroom**: resources well under `max_duration_minutes` score slightly higher
- **Format match** (+2): resource `format` equals the optional `preferred_format`

### Rule categories (Sprint 2)

Every scoring rule belongs to one category. Each result's
`score_breakdown` holds the points per category, and they always add up
to `score`.

| Category | Rules |
|---|---|
| `relevance` | subject match, keyword match |
| `level_fit` | difficulty match |
| `quality` | rating bonus |
| `practicality` | duration headroom, format match |

All weights are named constants at the top of `rule_engine.py`, easy to
tune and justify during evaluation.

## Data schema (`sample_resources.csv`)

| Column | Type | Required? | Description |
|---|---|---|---|
| `id` | string | yes | Unique resource ID |
| `title` | string | yes | Resource title |
| `topic` | string | yes | Subject area (e.g. `programming`, `mathematics`) |
| `tags` | string (semicolon-separated) | yes | Keywords (e.g. `python;hands-on`) |
| `level` | string | yes | Difficulty: `beginner`, `intermediate`, or `advanced` |
| `format` | string | yes | Resource category: `video`, `article`, or `exercise` |
| `url` | string | yes | Link to the resource |
| `duration_minutes` | number | optional | Length in minutes — enables the duration filter |
| `rating` | number | optional | Average rating — enables the rating filter |

## Documented example inputs and outputs

See [`EXAMPLE_INPUTS.md`](EXAMPLE_INPUTS.md) for five example requests
with their real outputs and score breakdowns.

## Running the tests

```bash
pip install pytest
pytest test_rule_engine.py test_sprint3_regression.py -v

# evaluation report and comparison with the recorded baseline
python evaluate.py --compare
```
