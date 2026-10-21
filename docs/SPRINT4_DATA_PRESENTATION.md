# Sprint 4 — Data/Model Presentation Notes

From the slide plan in `Sprint_Document.md` section 14.2:

```
 Slide 5  rule engine          → Nishant
```

Aim for about 1 minute.

---

## Slide 5 — The Rule Engine (Nishant)

**On the slide**

```
 request → filter → score (4 categories) → rank → explain

 relevance     subject +5, keyword +2.5
 level_fit     exact +3, one level off +1
 quality       rating bonus, max +1
 practicality  time headroom + format +2
```

**Speaker notes**

- "Our engine is rule-based and deterministic: the same input always
  gives the same output."
- "First, hard filters remove anything too long or rated too low."
- "Then every resource earns points in four categories, and the website
  shows that breakdown, so users see *why* something was recommended."
- "In Sprint 3 we measured it. Raising the keyword weight from 1.5 to 2.5
  lifted precision from 0.667 to 0.729, close to the 0.750 maximum."
- "Testing also found two bugs, which we fixed: blank keywords matched
  everything, and an empty rating box let ratings outweigh difficulty."

**Likely questions**

- *Why not machine learning?* → "We built a model prototype and compared
  it. The rules scored higher, and they are explainable."
- *How do you know it's good?* → "16 test learners with expected answers,
  measured with precision, recall, Hit@1 and MRR."

---

## Demo part (data)

Show one request on the website and point at the score breakdown,
then open `data/EXAMPLE_INPUTS.md` Examples 1–2 to show the format
preference changing the #1 result.
