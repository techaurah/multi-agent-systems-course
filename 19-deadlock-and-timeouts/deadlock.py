"""Lesson 19 artifact: deadlock. A wiring bug makes the
scorer wait for the draft before scoring, and the drafter
wait for the score before drafting. A round-based scheduler
shows the standstill, a watchdog names it, and a timeout
fallback finishes the order with partial information."""

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

from mas.domain import ORDERS, extract_regex, score_fields  # noqa: E402
from mas.domain import LEADS  # noqa: E402


def run_scheduler(watchdog_rounds, step_budget=100):
    """Each round, every agent whose input is ready acts. In
    the buggy wiring neither input is ever ready. Returns
    (rounds_run, progressed, deadlocked)."""
    ready = {"fields": True, "score": False, "draft": False}
    wants = {"scorer": "draft", "drafter": "score"}
    rounds = 0
    while rounds < step_budget:
        rounds += 1
        progressed = False
        for agent, need in wants.items():
            if ready[need] and not ready[
                    "score" if agent == "scorer" else "draft"]:
                ready["score" if agent == "scorer" else "draft"] = True
                progressed = True
        if ready["score"] and ready["draft"]:
            return rounds, True, False
        if not progressed and rounds >= watchdog_rounds:
            return rounds, False, True
    return rounds, False, False


def evaluate():
    out = {}
    for w in (3, 5, 10):
        rounds, done, dead = run_scheduler(w)
        out[f"watchdog_{w}"] = {"rounds": rounds, "deadlocked": dead,
                                "completed": done}
    rounds, done, dead = run_scheduler(10 ** 9)
    out["no_watchdog"] = {"rounds": rounds, "deadlocked": dead,
                          "completed": done}
    order = ORDERS[0]
    fields = extract_regex(LEADS[order["lead_id"]]["text"])
    score, band = score_fields(fields)
    out["fallback_band"] = band
    out["fallback_matches_expected"] = band == order["expected"]["band"]
    return out


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
