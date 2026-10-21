# Model Card — LearnPath Recommendation Engine (Sprint 4)

## What it is

A **deterministic, rule-based recommender** (`data/rule_engine.py`). Given
a learner's request, it filters and scores the 30 resources in
`data/sample_resources.csv` and returns a ranked list with an explanation.
There is no training and no randomness: the same input always gives the
same output.

## How it works

```
 request
   │
   ▼
 1. hard filters     too long?  rating too low?  → dropped
   │
   ▼
 2. relevance gate   asked for a subject/keywords but matches neither? → dropped
   │
   ▼
 3. score rules      4 categories (table below)
   │
   ▼
 4. sort             score high → low, then id A → Z
```

| Category | Rule | Points |
|---|---|---|
| relevance | subject matches topic, tags or title (aliases: maths, ml, js, stats) | +5 |
| relevance | each keyword found in tags | +1.5 |
| level_fit | exact difficulty / one level off | +3 / +1 |
| quality | rating above `min_rating` (+1 per rating point) | max +1 |
| practicality | time headroom under `max_duration_minutes` | up to +1 |
| practicality | format matches `preferred_format` | +2 |

Every result includes `score_breakdown` (points per category, adding up to
`score`) and `reason` (plain-English explanation).

## Inputs and outputs

- **Inputs:** `subject`, `difficulty`, `max_duration_minutes`,
  `min_rating`, `keywords`, `preferred_format`, `limit`.
  (The API does not pass `preferred_format` to the engine yet.)
- **Output fields:** `id`, `title`, `score`, `score_breakdown`, `url`,
  `reason`, `format`, `topic`, `level`, `duration_minutes`, `rating`,
  `keywords`.

## Version history

| Sprint | Change |
|---|---|
| 1 | Baseline rules: subject, difficulty, keywords, rating, duration |
| 2 | Formats (video/article/exercise), rule categories, `score_breakdown`, 30 resources |
| 3 | Subject normalisation + aliases; relevance gate; evaluation set and guard (weights unchanged) |
| 4 | Fixes: blank keywords ignored; rating bonus capped at +1 |

## Evaluation (21 cases, see `docs/SPRINT3_EVALUATION.md`)

```
                    Baseline   Sprint 3   Sprint 4
 hit@1               1.000      1.000      1.000
 MRR                 1.000      1.000      1.000
 nDCG@5              0.953      0.993      0.993
 empty cases passed   2/4        4/4        4/4
 hard-filter breaks    0          0          0
```

Sprint 4 fixes do not change any evaluated case. They fix inputs the
evaluation set did not cover (see below).

## Sprint 4 fixes

1. **Blank keywords.** A keyword made only of spaces matched every
   resource, added +1.5 to each, and got past the relevance gate:
   `subject="cooking"` with keyword `"   "` returned 5 unrelated
   resources. Blank keywords are now removed before scoring.
2. **Empty rating box.** The website sends `min_rating: 0` when the box is
   left empty, which made the rating bonus as high as +4.9. That
   outweighed difficulty (+3), so an advanced maths learner got three
   beginner resources right behind the correct one. The bonus is now
   capped at +1 (`QUALITY_BONUS_CAP`). Requests with `min_rating` of 4 or
   more are unaffected, because their bonus was already under 1.

Tests: `data/test_sprint3_regression.py`, section "Sprint 4 release fixes".

## Why rules and not ML

- Rules already score nDCG@5 0.993 on the evaluation set.
- Every score can be explained to the user and the markers.
- 30 resources and no real user feedback are too little to train a
  reliable ML model.

## Limitations

- Small catalogue (30 resources, 3 subjects); URLs are placeholders.
- Aliases are a short fixed list ("coding" is not expanded).
- Evaluation cases were drafted by the team, so they show the engine
  behaves well on known cases, not on a large real catalogue.
- E04 still ranks a highly rated advanced video one place too high
  (nDCG 0.89).

## Future ML pathway

```
 now     rules (explainable, tested, guarded by evaluate.py)
  │
  ├─ 1. collect real clicks / ratings from users
  ├─ 2. grow the catalogue and alias list
  ├─ 3. train a ranking model; compare with  python evaluate.py --compare
  └─ 4. adopt only if it beats the rules, keeping rules as the fallback
```
