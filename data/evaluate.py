"""
evaluate.py - repeatable evaluation of the LearnPath rule engine (Sprint 3).

Runs every case in evaluation_set.json through RuleEngine and scores the
ranked output against the hand-judged relevance labels.

Usage (from the data/ folder):
    python evaluate.py                    # print a report
    python evaluate.py --output FILE      # also write the results as JSON
    python evaluate.py --compare          # compare with baseline_results.json, exit 1 on regression
    python evaluate.py --compare --against tuned_results.json   # compare with another recorded run
    python evaluate.py --set SUBJECT_MATCH_WEIGHT=6   # try a weight change without editing code

Metrics (per case with relevant items):
    hit@1     1 if the top result is relevant
    MRR       1 / rank of the first relevant result (0 if none in top k)
    nDCG@k    graded ranking quality (grade 2 = ideal, 1 = acceptable)
    ideal@k   share of the grade-2 resources found in the top k
Cases with expect_empty=true pass only if nothing is returned.
Every case is also checked for hard-filter violations (must always be 0).
"""

import argparse
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import rule_engine  # noqa: E402
from rule_engine import RuleEngine  # noqa: E402

EVAL_PATH = os.path.join(HERE, "evaluation_set.json")
BASELINE_PATH = os.path.join(HERE, "baseline_results.json")
TOLERANCE = 1e-9


def apply_overrides(pairs):
    """Override module-level weights for an experiment, e.g. SUBJECT_MATCH_WEIGHT=6."""
    for pair in pairs or []:
        name, _, value = pair.partition("=")
        if not hasattr(rule_engine, name):
            raise SystemExit(f"Unknown rule constant: {name}")
        setattr(rule_engine, name, float(value))


def ndcg(ranked_ids, grades, k):
    gains = [grades.get(i, 0) for i in ranked_ids[:k]]
    dcg = sum(g / math.log2(pos + 2) for pos, g in enumerate(gains))
    ideal = sorted(grades.values(), reverse=True)[:k]
    idcg = sum(g / math.log2(pos + 2) for pos, g in enumerate(ideal))
    return dcg / idcg if idcg else 0.0


def violations(engine, request, ranked_ids):
    """Count returned resources that break the request's own hard filters."""
    by_id = {r["id"]: r for r in engine.resources}
    bad = 0
    for rid in ranked_ids:
        row = by_id[rid]
        if request.get("max_duration_minutes") is not None and float(row["duration_minutes"]) > float(request["max_duration_minutes"]):
            bad += 1
        elif request.get("min_rating") is not None and float(row["rating"]) < float(request["min_rating"]):
            bad += 1
    return bad


def run_case(engine, case, k):
    results = engine.recommend_learning_resources(limit=k, **case["request"])
    ranked = [r["id"] for r in results]
    out = {"id": case["id"], "top": ranked,
           "violations": violations(engine, case["request"], ranked)}
    if case.get("expect_empty"):
        out["kind"] = "empty"
        out["pass"] = ranked == []
        return out
    grades = case["relevant"]
    first = next((pos for pos, i in enumerate(ranked) if grades.get(i, 0) > 0), None)
    ideal_ids = [i for i, g in grades.items() if g == 2]
    out.update({
        "kind": "ranked",
        "hit_at_1": 1.0 if ranked and grades.get(ranked[0], 0) > 0 else 0.0,
        "mrr": 1.0 / (first + 1) if first is not None else 0.0,
        "ndcg": round(ndcg(ranked, grades, k), 4),
        "ideal_at_k": round(len([i for i in ideal_ids if i in ranked]) / len(ideal_ids), 4) if ideal_ids else 1.0,
    })
    return out


def evaluate(overrides=None):
    apply_overrides(overrides)
    with open(EVAL_PATH, encoding="utf-8") as fh:
        spec = json.load(fh)
    engine = RuleEngine()
    k = spec["k"]
    cases = [run_case(engine, c, k) for c in spec["cases"]]
    ranked = [c for c in cases if c["kind"] == "ranked"]
    empty = [c for c in cases if c["kind"] == "empty"]
    mean = lambda key: round(sum(c[key] for c in ranked) / len(ranked), 4)
    summary = {
        "hit_at_1": mean("hit_at_1"),
        "mrr": mean("mrr"),
        "ndcg": mean("ndcg"),
        "ideal_at_k": mean("ideal_at_k"),
        "empty_cases_passed": f"{sum(c['pass'] for c in empty)}/{len(empty)}",
        "empty_pass_rate": round(sum(c["pass"] for c in empty) / len(empty), 4) if empty else 1.0,
        "hard_filter_violations": sum(c["violations"] for c in cases),
        "ranked_cases": len(ranked),
        "empty_cases": len(empty),
    }
    return {"k": k, "resources": len(engine.resources), "summary": summary, "cases": cases}


METRICS = ["hit_at_1", "mrr", "ndcg", "ideal_at_k", "empty_pass_rate"]


def print_report(result):
    s = result["summary"]
    print(f"LearnPath evaluation  (k={result['k']}, {result['resources']} resources, "
          f"{s['ranked_cases']} ranked cases, {s['empty_cases']} expect-empty cases)\n")
    print(f"{'case':<5} {'hit@1':>5} {'MRR':>6} {'nDCG':>6} {'ideal@k':>8}  top results")
    for c in result["cases"]:
        if c["kind"] == "ranked":
            print(f"{c['id']:<5} {c['hit_at_1']:>5.0f} {c['mrr']:>6.2f} {c['ndcg']:>6.2f} {c['ideal_at_k']:>8.2f}  {', '.join(c['top'])}")
        else:
            print(f"{c['id']:<5} {'PASS' if c['pass'] else 'FAIL':>5}   (expected no results)       {', '.join(c['top']) or '-'}")
    print("\nSUMMARY")
    print(f"  hit@1 {s['hit_at_1']:.3f} | MRR {s['mrr']:.3f} | nDCG@{result['k']} {s['ndcg']:.3f} | "
          f"ideal@{result['k']} {s['ideal_at_k']:.3f}")
    print(f"  expect-empty cases passed: {s['empty_cases_passed']} | hard-filter violations: {s['hard_filter_violations']}")


def compare(current, baseline):
    """Return (lines, regressed). A regression is any metric drop or any case that got worse."""
    lines, regressed = [], False
    lines.append(f"{'metric':<18}{'baseline':>10}{'current':>10}{'change':>10}")
    for m in METRICS:
        b, c = baseline["summary"][m], current["summary"][m]
        flag = ""
        if c < b - TOLERANCE:
            flag, regressed = "  WORSE", True
        elif c > b + TOLERANCE:
            flag = "  better"
        lines.append(f"{m:<18}{b:>10.3f}{c:>10.3f}{c - b:>+10.3f}{flag}")
    bv, cv = baseline["summary"]["hard_filter_violations"], current["summary"]["hard_filter_violations"]
    if cv > bv:
        regressed = True
    lines.append(f"{'hard violations':<18}{bv:>10}{cv:>10}")
    base_cases = {c["id"]: c for c in baseline["cases"]}
    worse, better = [], []
    for c in current["cases"]:
        b = base_cases.get(c["id"])
        if not b:
            continue
        key = "pass" if c["kind"] == "empty" else "ndcg"
        cv_, bv_ = float(c[key]), float(b[key])
        if cv_ < bv_ - TOLERANCE:
            worse.append(f"{c['id']} ({bv_:.2f} -> {cv_:.2f})")
        elif cv_ > bv_ + TOLERANCE:
            better.append(f"{c['id']} ({bv_:.2f} -> {cv_:.2f})")
    lines.append(f"cases improved: {', '.join(better) or 'none'}")
    lines.append(f"cases worse:    {', '.join(worse) or 'none'}")
    if worse:
        regressed = True
    return lines, regressed


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--output", metavar="FILE", help="write the results to this JSON file")
    p.add_argument("--compare", action="store_true")
    p.add_argument("--against", metavar="FILE", default=BASELINE_PATH,
                   help="recorded results to compare with (default: baseline_results.json)")
    p.add_argument("--set", action="append", metavar="CONSTANT=VALUE")
    a = p.parse_args()
    result = evaluate(a.set)
    print_report(result)
    if a.output:
        with open(a.output, "w", encoding="utf-8") as fh:
            json.dump(result, fh, indent=2)
            fh.write("\n")
        print(f"\nResults saved to {a.output}")
    if a.compare:
        with open(a.against, encoding="utf-8") as fh:
            baseline = json.load(fh)
        lines, regressed = compare(result, baseline)
        print("\nCOMPARISON WITH BASELINE")
        print("\n".join(lines))
        sys.exit(1 if regressed else 0)


if __name__ == "__main__":
    main()
