# Demo Scenarios (Sprint 4 — demo data)

Prepared inputs for the live demo. Each scenario lists what to type into
the website form, the result to expect, and one line to say. All results
were captured from `POST /api/recommend` on the current `main`
(30 resources). If the dataset or rules change, re-run them before the
demo.

```
 S1  Beginner Python          → normal happy path + score breakdown
 S2  "data science" (spaces)  → free-text subject still matches
 S3  "maths", 30 min          → alias + time limit + empty rating box
 S4  "cooking"                → unknown subject returns nothing
 S5  1-minute limit           → empty state, no crash
 S6  difficulty "expert"      → validation error (HTTP 422)
```

Suggested order for a 2-minute demo: **S1 → S3 → S4**. Keep S2, S5 and
S6 as backups or for questions.

## S1 — beginner Python (happy path)

| Subject | Difficulty | Max duration | Min rating | Keywords | Limit |
|---|---|---|---|---|---|
| `programming` | beginner | `60` | `4` | `python` | `3` |

| Rank | ID | Title | Format | Score |
|---|---|---|---|---|
| 1 | R009 | Python Loops and Functions Practice | exercise | 10.5 |
| 2 | R001 | Intro to Python Programming | video | 10.45 |
| 3 | R010 | Understanding Variables and Data Types | article | 10.25 |

> **Say:** "Three beginner Python resources under an hour, in three
> different formats. The breakdown shows why each one ranked where it did."

## S2 — free-text subject "data science"

| Subject | Difficulty | Max duration | Min rating | Keywords | Limit |
|---|---|---|---|---|---|
| `data science` | intermediate | `90` | `4` | `machine-learning` | `3` |

| Rank | ID | Title | Level | Score |
|---|---|---|---|---|
| 1 | R028 | Decision Trees and Random Forests | intermediate | 10.267 |
| 2 | R027 | Regression Models in Scikit-Learn | intermediate | 10.011 |
| 3 | R026 | Exploratory Data Analysis Walkthrough | intermediate | 8.833 |

> **Say:** "The catalogue stores `data-science` with a hyphen, but the
> learner typed it with a space. Subject matching handles that."

## S3 — "maths", 30-minute slot, rating box empty

| Subject | Difficulty | Max duration | Min rating | Keywords | Limit |
|---|---|---|---|---|---|
| `maths` | advanced | `30` | *(leave empty)* | `theory` | `3` |

| Rank | ID | Title | Level | Score |
|---|---|---|---|---|
| 1 | R022 | Eigenvalues Explained Visually | advanced | 10.667 |
| 2 | R023 | Graph Theory Introduction | beginner | 7.833 |
| 3 | R003 | Linear Algebra Fundamentals | beginner | 7.667 |

> **Say:** "'maths' is expanded to mathematics. Only one advanced resource
> fits in 30 minutes, so it leads by a clear margin. Before our Sprint 4
> fix, leaving the rating empty let ratings outweigh difficulty."

## S4 — unknown subject

| Subject | Difficulty | Max duration | Min rating | Keywords | Limit |
|---|---|---|---|---|---|
| `cooking` | beginner | `60` | *(empty)* | *(empty)* | `3` |

Expected: **"No matching resources found"** with a hint to broaden the
search.

> **Say:** "We have no cooking resources, so the engine returns nothing
> instead of five random beginner resources, which is what it did before
> Sprint 3."

## S5 — impossible time limit

| Subject | Difficulty | Max duration | Min rating | Keywords | Limit |
|---|---|---|---|---|---|
| `programming` | beginner | `1` | *(empty)* | *(empty)* | `3` |

Expected: **"No matching resources found"**.

> **Say:** "Nothing fits in one minute. The hard filter removes everything
> and the website explains what to change."

## S6 — invalid input (validation)

Open `http://127.0.0.1:8000/docs` → **POST /api/recommend** → **Try it
out**, set `"difficulty": "expert"`, then **Execute**.

Expected: **HTTP 422**, `Input should be 'beginner', 'intermediate' or 'advanced'`.

> **Say:** "Bad input is rejected by the API before it reaches the rules."

## Before the demo

```
 Terminal 1:  uvicorn backend.main:app --reload
 Terminal 2:  cd frontend → npm run dev → open the localhost link
 Check:       run S1 once to warm up
```

## If the live demo fails

- Show this file's tables as the expected results.
- Run `cd data && python evaluate.py` to show the evaluation table live.
