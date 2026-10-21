# Model Card — LearnPath Recommendation Engine (final, Sprint 4)

## What it is

A **deterministic, rule-based recommender** (`data/rule_engine.py`). Given
a learner's request, it filters and scores the resources in
`data/sample_resources.csv` and returns a ranked, explained list. There is
no training and no randomness: the same input always gives the same output.

## How it works

```
 request ──► 1. hard filters ──► 2. score rules ──► 3. sort ──► top N
             too long? drop       4 categories        score ↓
             rating too low? drop                     then id ↑
```

| Category | Rule | Points |
|---|---|---|
| relevance | subject matches topic | +5 |
| relevance | each keyword found in tags | +2.5 |
| level_fit | exact difficulty / one level off | +3 / +1 |
| quality | rating above `min_rating` (+1 per rating point) | max +1 |
| practicality | time headroom under `max_duration_minutes` | up to +1 |
| practicality | format matches `preferred_format` | +2 |

Each result includes `score_breakdown` (points per category, adding up to
`score`) and `reason` (plain-English explanation).

## Inputs and outputs

- **Inputs:** `subject` (required), `difficulty`, `max_duration_minutes`,
  `min_rating`, `keywords`, `preferred_format`, `limit`.
- **Output fields (frozen in Sprint 4):** `id`, `title`, `score`,
  `score_breakdown`, `url`, `reason`, `format`, `topic`, `level`,
  `duration_minutes`, `rating`, `keywords`.

## Version history

| Sprint | Change |
|---|---|
| 1 | Baseline rules: subject, difficulty, keywords (+1.5), rating, duration |
| 2 | Formats (video/article/exercise), rule categories, `score_breakdown`, 30 resources |
| 3 | Keyword weight 1.5 → 2.5; rating bonus capped at +1; blank-keyword bug fixed |
| 4 | Final version frozen; contract test added |

## Evaluation (16 test learners, Sprint 3)

```
                   P@3    R@3   Hit@1   MRR
 Sprint 2 rules   0.667  0.906  1.000  1.000
 FINAL rules      0.729  0.979  1.000  1.000
 TF-IDF model     0.667  0.906  0.938  0.969   (not adopted)
 best possible    0.750
```

## Why rules and not ML (yet)

- Rules scored higher than the model prototype on this data.
- Every score can be explained to the user and the markers.
- 30 resources and no real user feedback are too little to train a
  reliable ML model.

## Limitations

- Small dataset (30 resources, 3 subjects); URLs are placeholders.
- Matching is by exact words: "ML" does not match "machine-learning".
- Subject must match the topic name (`programming`, `mathematics`,
  `data-science`).
- Relevance labels for evaluation come from the team's judgement.

## Future ML pathway

```
 now     rules (explainable, tested)
  │
  ├─ 1. collect real clicks / ratings from users
  ├─ 2. grow dataset + add synonyms ("ML" → machine-learning)
  ├─ 3. train a ranking model; compare on the evaluation set
  └─ 4. adopt only if it beats the rules, keeping rules as the fallback
```
