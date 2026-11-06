"""Lesson 20 artifact: conflicting outputs. Two scorers with
different thresholds read the same fields and disagree on
the edge orders. Four arbitration rules are raced on the
disagreements: the rule you pick is a design decision with
a measurable price and a measurable error count."""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def find_root():
    cur = HERE
    while True:
        if os.path.isfile(os.path.join(cur, "mas", "systems.py")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            raise FileNotFoundError("repo root (mas/) not found above " + HERE)
        cur = parent


ROOT = find_root()
sys.path.insert(0, ROOT)

from mas.domain import LEADS, ORDERS, extract_careful  # noqa: E402
from mas.domain import extract_regex, score_fields  # noqa: E402


def strict_band(score):
    return "hot" if score >= 85 else "warm" if score >= 60 else "nurture"


def evaluate():
    disagreements = []
    rows = {}
    for o in ORDERS:
        text = LEADS[o["lead_id"]]["text"]
        score, rubric = score_fields(extract_regex(text))
        strict = strict_band(score)
        if rubric != strict:
            disagreements.append(o["id"])
        rows[o["id"]] = (rubric, strict)
    correct = {"defer_rubric": 0, "defer_strict": 0,
               "majority": 0, "escalate": 0}
    for oid in disagreements:
        o = next(x for x in ORDERS if x["id"] == oid)
        rubric, strict = rows[oid]
        if rubric == o["expected"]["band"]:
            correct["defer_rubric"] += 1
        if strict == o["expected"]["band"]:
            correct["defer_strict"] += 1
        # majority: a third scorer with careful fields joins
        c_score, c_band = score_fields(
            extract_careful(LEADS[o["lead_id"]]["text"]))
        votes = [rubric, strict, c_band]
        winner = max(set(votes), key=votes.count)
        if winner == o["expected"]["band"]:
            correct["majority"] += 1
        # escalate: careful fields plus the rubric decide
        if c_band == o["expected"]["band"]:
            correct["escalate"] += 1
    return {
        "orders": len(ORDERS),
        "disagreements": disagreements,
        "disagreement_count": len(disagreements),
        "correct_on_disagreements": correct,
        "extra_messages_per_disagreement": {
            "defer_rubric": 0, "defer_strict": 0,
            "majority": 2, "escalate": 3},
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
