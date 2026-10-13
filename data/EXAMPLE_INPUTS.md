# Example Inputs and Outputs (Sprint 2)

Every output below was produced by running `data/rule_engine.py` against
`data/sample_resources.csv` (30 resources). Re-run them any time with:

```bash
cd data
python -c "from rule_engine import RuleEngine; print(RuleEngine().recommend_learning_resources(subject='programming', difficulty='beginner', preferred_format='video', limit=3))"
```

## How to read the score

```
 total score = relevance + level_fit + quality + practicality

 relevance    subject match (+5) + each matching keyword (+1.5)
 level_fit    exact difficulty (+3) / one level off (+1)
 quality      rating above min_rating (+1 per rating point)
 practicality time headroom (up to +1) + preferred format match (+2)
```

## Example 1 — beginner who prefers short Python **videos**

```json
{"subject": "programming", "difficulty": "beginner", "max_duration_minutes": 60,
 "min_rating": 4.0, "keywords": ["python"], "preferred_format": "video", "limit": 3}
```

| Rank | ID | Title | Format | Score | relevance | level_fit | quality | practicality |
|---|---|---|---|---|---|---|---|---|
| 1 | R001 | Intro to Python Programming | video | 12.45 | 6.5 | 3.0 | 0.7 | 2.25 |
| 2 | R012 | Git and GitHub Essentials | video | 11.033 | 5.0 | 3.0 | 0.7 | 2.333 |
| 3 | R009 | Python Loops and Functions Practice | exercise | 10.5 | 6.5 | 3.0 | 0.5 | 0.5 |

## Example 2 — same learner, but prefers **exercises**

Only `preferred_format` changes, and the top result changes with it.

```json
{"subject": "programming", "difficulty": "beginner", "max_duration_minutes": 60,
 "min_rating": 4.0, "keywords": ["python"], "preferred_format": "exercise", "limit": 3}
```

| Rank | ID | Title | Format | Score | relevance | level_fit | quality | practicality |
|---|---|---|---|---|---|---|---|---|
| 1 | R009 | Python Loops and Functions Practice | exercise | 12.5 | 6.5 | 3.0 | 0.5 | 2.5 |
| 2 | R001 | Intro to Python Programming | video | 10.45 | 6.5 | 3.0 | 0.7 | 0.25 |
| 3 | R005 | SQL for Beginners | exercise | 10.4 | 5.0 | 3.0 | 0.4 | 2.0 |

## Example 3 — intermediate data-science learner who prefers **articles**

```json
{"subject": "data-science", "difficulty": "intermediate", "min_rating": 4.0,
 "keywords": ["machine-learning"], "preferred_format": "article", "limit": 3}
```

| Rank | ID | Title | Format | Score | relevance | level_fit | quality | practicality |
|---|---|---|---|---|---|---|---|---|
| 1 | R028 | Decision Trees and Random Forests | article | 11.6 | 6.5 | 3.0 | 0.1 | 2.0 |
| 2 | R006 | Statistics for Data Analysis | article | 10.3 | 5.0 | 3.0 | 0.3 | 2.0 |
| 3 | R027 | Regression Models in Scikit-Learn | exercise | 9.9 | 6.5 | 3.0 | 0.4 | 0.0 |

## Example 4 — advanced maths in a 30-minute slot (no format preference)

The 30-minute hard filter removes every longer resource before scoring.

```json
{"subject": "mathematics", "difficulty": "advanced", "max_duration_minutes": 30,
 "keywords": ["theory"], "limit": 3}
```

| Rank | ID | Title | Format | Score | relevance | level_fit | quality | practicality |
|---|---|---|---|---|---|---|---|---|
| 1 | R022 | Eigenvalues Explained Visually | video | 9.667 | 6.5 | 3.0 | 0.0 | 0.167 |
| 2 | R023 | Graph Theory Introduction | article | 6.833 | 6.5 | 0.0 | 0.0 | 0.333 |
| 3 | R003 | Linear Algebra Fundamentals | article | 6.667 | 6.5 | 0.0 | 0.0 | 0.167 |

## Example 5 — nothing to match

```json
{"subject": "", "limit": 3}
```

Returns `[]`. The engine never returns arbitrary results when nothing matches.

## Invalid format

`preferred_format` must be `video`, `article` or `exercise` (case-insensitive).
Anything else, e.g. `"podcast"`, raises `ValueError`.
