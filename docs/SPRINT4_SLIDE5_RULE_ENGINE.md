# Sprint 4 — Slide 5: The Rule Engine (Nishant)

From the slide plan in `Sprint_Document.md` section 14.2. About 1 minute.

## On the slide

```
 request → filter → relevance gate → score (4 categories) → rank → explain

 relevance     subject +5, keyword +1.5
 level_fit     exact +3, one level off +1
 quality       rating bonus, max +1
 practicality  time headroom + format +2

 nDCG@5  0.953 → 0.993    empty-result cases  2/4 → 4/4
```

## Speaker notes

- "Our engine is rule-based and deterministic: the same input always gives
  the same output, and every score can be explained."
- "First, hard filters remove anything too long or rated too low. Then a
  relevance gate removes anything unrelated to the subject or keywords."
- "Each remaining resource earns points in four categories. The website
  shows that breakdown, so users see *why* something was recommended."
- "In Sprint 3 we built an evaluation set of 21 cases. Ranking quality went
  from 0.953 to 0.993 nDCG, and unknown subjects now correctly return
  nothing."
- "In Sprint 4 testing we found and fixed two bugs: blank keywords matched
  everything, and an empty rating box let ratings outweigh difficulty."

## Likely questions

- *Why not machine learning?* → "With 30 resources and no real user data,
  a trained model wouldn't be reliable. Rules already score 0.993, and we
  can explain every result."
- *How do you know it's good?* → "21 hand-judged cases, measured with
  hit@1, MRR and nDCG. A test fails CI if any case gets worse."
- *What would you do next?* → "Collect real user feedback, then compare a
  trained model against the rules using the same evaluation."

## Demo moment

Enter `mathematics` / `advanced` / 30 minutes / keyword `theory`, leaving
the rating box empty. Point at the score breakdown on the #1 result,
"Eigenvalues Explained Visually".
