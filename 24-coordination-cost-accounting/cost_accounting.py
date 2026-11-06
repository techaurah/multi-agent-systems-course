"""Lesson 24 artifact: the full cost table. Six systems, one
order set, one accounting. Success alone is not the ranking;
cost per success is where coordination has to justify itself."""

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

from mas.domain import ORDERS  # noqa: E402
from mas.harness import summarize  # noqa: E402
from mas.systems import (run_blackboard, run_debate,  # noqa: E402
                         run_orchestrated, run_pipeline, run_single)

SYSTEMS = {
    "single": lambda o: run_single(o),
    "pipeline": lambda o: run_pipeline(o),
    "pipeline_reviewed": lambda o: run_pipeline(o, reviewer=True),
    "orchestrated": lambda o: run_orchestrated(o),
    "blackboard": lambda o: run_blackboard(o),
    "debate": lambda o: run_debate(o),
}


def evaluate():
    table = {}
    for name, fn in SYSTEMS.items():
        s = summarize([fn(o) for o in ORDERS])
        table[name] = {
            "successes": s["successes"],
            "success_rate": s["success_rate"],
            "mean_messages": s["mean_messages"],
            "mean_tokens": s["mean_tokens"],
            "tokens_per_success": s["tokens_per_success"],
            "escapes": s["escapes"],
        }
    best = min(table, key=lambda k: table[k]["tokens_per_success"])
    return {"orders": len(ORDERS), "table": table,
            "cheapest_per_success": best}


if __name__ == "__main__":
    r = evaluate()
    for name, row in r["table"].items():
        print(name, row)
    print("cheapest_per_success:", r["cheapest_per_success"])
