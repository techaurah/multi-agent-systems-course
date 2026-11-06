"""Lesson 23 artifact: termination and budgets. A pipeline
that needs five steps to reach its reviewer is run under
step budgets, and the two failure styles are counted
separately: orders that never finish, and orders that are
sent early, unchecked, when a sender treats the budget as
the finish line."""

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

from mas.domain import LEADS, ORDERS, check_draft, draft_naive  # noqa: E402
from mas.domain import extract_regex  # noqa: E402
from mas.systems import run_pipeline  # noqa: E402

# Steps one reviewed order needs: task, fields, score, draft,
# verdict, and two more when the verdict sends it back.
NEEDS = {}


def steps_needed(order):
    r = run_pipeline(order, reviewer=True)
    return r["steps"]


def evaluate():
    needed = {o["id"]: steps_needed(o) for o in ORDERS}
    out = {"steps_needed": needed}
    for budget in (4, 5, 7):
        finished = sum(1 for v in needed.values() if v <= budget)
        out[f"budget_{budget}"] = {
            "finished": finished,
            "unfinished": len(needed) - finished}
    early_escapes = 0
    for o in ORDERS:
        lead = LEADS[o["lead_id"]]
        fields = extract_regex(lead["text"])
        early_escapes += len(check_draft(
            draft_naive(lead["name"], fields), fields))
    out["escapes_if_sent_at_step_3"] = early_escapes
    out["max_steps_needed"] = max(needed.values())
    out["min_steps_needed"] = min(needed.values())
    return out


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
