"""Lesson 28 artifact: the course's own failures, classified.
Every failed order from three reference systems, the band
changes caused by summary handoffs, and the two termination
failures from Module 5 are sorted into the three MAST
categories (Cemri et al., 2025, cited in RESEARCH.md), so the
course's failure profile can be compared with the field's."""

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

from mas.domain import LEADS, ORDERS, extract_regex, score_fields  # noqa: E402
from mas.systems import run_orchestrated, run_pipeline, run_single  # noqa: E402

SPEC = "specification and system design"
MISALIGN = "inter-agent misalignment"
VERIFY = "task verification"

DEFAULTS = {"timeline": "flexible", "decision_maker": False,
            "discount_ask_pct": None}


def classify(result):
    for p in result["problems"]:
        if p.startswith("draft"):
            return VERIFY
    return SPEC


def evaluate():
    counts = {SPEC: 0, MISALIGN: 0, VERIFY: 0}
    detail = {SPEC: [], MISALIGN: [], VERIFY: []}
    for name, fn in (("single", run_single),
                     ("pipeline", lambda o: run_pipeline(o)),
                     ("orchestrated", run_orchestrated)):
        for o in ORDERS:
            r = fn(o)
            if not r["success"]:
                cat = classify(r)
                counts[cat] += 1
                detail[cat].append(f"{name}:{o['id']}")
    # Misalignment: bands the summary handoff loses between
    # the extractor and the scorer (Lesson 11's mechanism).
    for o in ORDERS:
        fields = extract_regex(LEADS[o["lead_id"]]["text"])
        merged = dict(DEFAULTS)
        merged.update({"service": fields["service"],
                       "budget_usd": fields["budget_usd"]})
        if score_fields(fields)[1] == o["expected"]["band"] and \
                score_fields(merged)[1] != o["expected"]["band"]:
            counts[MISALIGN] += 1
            detail[MISALIGN].append(f"summary-handoff:{o['id']}")
    # Termination failures reproduced in Module 5: the
    # clarification loop and the deadlock both live in MAST's
    # specification category (step repetition; unaware of
    # termination conditions).
    counts[SPEC] += 2
    detail[SPEC] += ["loop:clarification", "deadlock:cyclic-wait"]
    total = sum(counts.values())
    return {
        "instances": total,
        "counts": counts,
        "shares": {k: round(v / total, 4) for k, v in counts.items()},
        "detail": detail,
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
