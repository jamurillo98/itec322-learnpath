# Sprint 3 — Data/Model Evaluation Report

Status: **evaluation complete, rule change measured.** This covers the Data/Model
deliverables in `SPRINT3_RELEASE.md`. Backend, frontend and deployment checks are
reported separately by their owners.

## 1. Method

- **Evaluation set** — `data/evaluation_set.json`: 21 learner requests (17 with an
  expected ranking, 4 where the correct answer is "no results"). Each lists the
  resources a reasonable reviewer would call *ideal* (grade 2) or *acceptable*
  (grade 1). Judgments were written from the CSV and the learner's stated need
  **before** the engine was run, so they do not simply copy engine output. A
  resource that breaks the request's own duration or rating limit is never
  relevant.
- **Runner** — `data/evaluate.py` runs every case through `RuleEngine`
  (top 5) and reports:
  - **hit@1**: is the top result relevant?
  - **MRR**: 1 / rank of the first relevant result
  - **nDCG@5**: ranking quality using the 2/1 grades (1.0 = ideal order)
  - **ideal@5**: share of the grade-2 resources found in the top 5
  - **expect-empty pass rate**: cases that should return nothing, and do
  - **hard-filter violations**: results breaking the request's own limits (must be 0)
- **Repeatable comparison** — `python evaluate.py --compare` re-runs everything and
  compares with `baseline_results.json`. It exits with an error if any metric or
  any individual case gets worse. Weight experiments need no code edits:
  `python evaluate.py --compare --set KEYWORD_MATCH_WEIGHT=3`.

Run from the `data/` folder:

```bash
python evaluate.py                 # report
python evaluate.py --compare       # compare with the baseline recorded before tuning
```

## 2. Baseline (engine as merged at the start of Sprint 3)

`data/baseline_results.json`

| Metric | Baseline |
|---|---|
| hit@1 | 1.000 |
| MRR | 1.000 |
| nDCG@5 | 0.953 |
| ideal@5 | 1.000 |
| Expect-empty cases passed | 2 / 4 |
| Hard-filter violations | 0 |

The engine already ranked the right resource first for every case with an
expected ranking, and never broke a hard filter. The weaknesses were:

1. **Unknown subjects still returned results (E18, E19).** The difficulty rule
   awards +3 regardless of subject, so `cooking` + `beginner` returned five
   unrelated beginner resources.
2. **Subject text had to equal the topic text (E03, E13, E17).** The CSV stores
   `data-science`, but a learner types `data science`, `maths` or `calculus`.
   These scored no subject points, so unrelated beginner resources outranked
   relevant ones (E03 nDCG 0.64, E13 0.76, E17 0.92).

## 3. Tuning

Weight changes were tried first, one constant at a time:

| Experiment | nDCG@5 | Result |
|---|---|---|
| `SUBJECT_MATCH_WEIGHT` 3 or 8 | 0.953 | no change |
| `DIFFICULTY_EXACT_MATCH_WEIGHT` = 2 | 0.944 | worse (E04, E11) |
| `DIFFICULTY_EXACT_MATCH_WEIGHT` = 4 | 0.954 | tiny gain |
| `KEYWORD_MATCH_WEIGHT` = 3 | 0.979 | better, but two cases only |
| `KEYWORD_MATCH_WEIGHT` = 1 | 0.953 | no change |
| `RATING_BONUS_WEIGHT` = 2 | 0.951 | worse (E04, E11) |
| `DURATION_HEADROOM_WEIGHT` = 2 | 0.933 | worse (E02, E17) |

No weight change fixed the empty-result problem, and the one weight that helped
(`KEYWORD_MATCH_WEIGHT`) was only compensating for the subject-matching problem,
so **no weights were changed**. The two causes above were fixed as rules instead
(`data/rule_engine.py`):

1. **Subject matching**: ignores case, treats hyphens as spaces, expands a small
   alias list (`maths`, `ml`, `js`, `stats`), and requires every word of the subject
   to appear in the resource's topic, tags or title.
2. **Relevance gate**: when a subject or keywords are supplied, a resource must
   match at least one of them to be returned. Difficulty, rating, duration and
   format now only rank relevant resources. With no subject and no keywords the
   old behaviour is unchanged.

## 4. Result (`data/tuned_results.json`)

| Metric | Baseline | After | Change |
|---|---|---|---|
| hit@1 | 1.000 | 1.000 | 0 |
| MRR | 1.000 | 1.000 | 0 |
| nDCG@5 | 0.953 | 0.993 | +0.040 |
| ideal@5 | 1.000 | 1.000 | 0 |
| Expect-empty cases passed | 2 / 4 | 4 / 4 | +2 |
| Hard-filter violations | 0 | 0 | 0 |

Cases improved: E03, E13, E17, E18, E19. **No case got worse.** The five example
inputs in `data/EXAMPLE_INPUTS.md` still reproduce exactly.

## 5. Tests added

`data/test_sprint3_regression.py` (19 tests): the evaluation guard (fails if any
metric or case drops below `tuned_results.json`), subject normalisation and
aliases, the relevance gate, inclusive duration and rating boundaries, zero and
impossible limits, `limit=1`, tie-breaking by id, ordering that does not depend on
catalogue order, repeatable output, and result fields. CI now runs this file.

## 6. Known limitations

- **Small catalogue and judgments.** 30 resources and 21 cases, drafted by
  one person with an AI assistant. The 0.993 nDCG shows the engine behaves well on this set; it is not a
  claim about a large real catalogue. The team should review `evaluation_set.json`.
- **The set was extended after seeing the baseline.** E18–E19 and the free-text
  subject cases were written to probe likely weaknesses, and the fix then targeted
  them. Judgments were fixed before the engine ran, but a reviewer should still
  treat the improvement as "fixes the known failures", not as a general guarantee.
- **Aliases are a short fixed list.** Synonyms outside it (e.g. `coding`) still
  rely on the learner's keywords.
- **Remaining imperfection:** E04 (nDCG 0.89) ranks an advanced maths video
  (R022, one level off, rated 4.9) above two acceptable resources (R018, R019)
  because its high-rating bonus outweighs their small advantages. Left unchanged:
  the weight changes tried did not fix it without hurting other cases.
- **Substring matching** can match inside longer words. It has not caused a wrong
  result on this set.
