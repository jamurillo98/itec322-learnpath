# Sprint 4 — Slide 6: Data and Future ML (Aarjan)

From the presentation slide plan: Slide 5 rule engine (Nishant), Slide 6
data and future ML (Aarjan). About 1 minute.

## On the slide

```
 CATALOGUE      30 resources
                programming 13 · data-science 9 · mathematics 8
                exercise 11 · video 10 · article 9
                beginner 11 · intermediate 11 · advanced 8

 EVALUATION     21 hand-judged cases (17 ranked + 4 "should be empty")
                nDCG@5  0.953 → 0.993    empty cases 2/4 → 4/4

 FUTURE ML      real feedback → bigger catalogue → train → compare → adopt only if better
```

## Speaker notes

- "Our catalogue has 30 learning resources across three subjects, in three
  formats and three levels, so every type of learner gets options."
- "To measure quality, we wrote 21 test cases with the answers a reviewer
  would expect, before running the engine. That way the test doesn't just
  copy the engine."
- "`evaluate.py` scores the engine on these cases. Sprint 3 changes
  improved nDCG from 0.953 to 0.993, and a test fails CI if any case ever
  gets worse."
- "We are not using machine learning yet. With 30 resources and no real
  user data, a trained model wouldn't be reliable, and the rules are
  already explainable."
- "The path to ML: collect real clicks and ratings, grow the catalogue,
  train a ranking model, and compare it with the same evaluation. We would
  adopt it only if it beats the rules, and keep the rules as a fallback."

## Likely questions

- *Is the data real?* → "The resources are realistic examples, but the
  links are placeholders. Real links and a bigger catalogue are the next
  data step."
- *Who decided the correct answers?* → "The team, from each learner's
  stated need. That's a limitation: an independent review would make the
  evaluation stronger."
- *What is nDCG?* → "A score from 0 to 1 for how close our ranking is to
  the ideal order. 1.0 means a perfect order."
- *What's still imperfect?* → "One case, E04, ranks a highly rated
  advanced video one place too high. We left it, because the fixes we
  tried made other cases worse."

## Demo moment

Use **S4** from `data/DEMO_SCENARIOS.md`: subject `cooking` returns
"No matching resources found". That is one of the "should be empty"
evaluation cases working live.
