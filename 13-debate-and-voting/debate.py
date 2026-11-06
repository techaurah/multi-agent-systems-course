"""Lesson 13 artifact: debate. Two scorers read the same lead
with different extractors; where they disagree, a judge
settles it with a stated rule. The gain is real and so is
the bill: both are printed."""

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
from mas.systems import run_debate, run_pipeline, run_single  # noqa: E402


def evaluate():
    debate = [run_debate(o) for o in ORDERS]
    d = summarize(debate)
    s = summarize([run_single(o) for o in ORDERS])
    p = summarize([run_pipeline(o, reviewer=True) for o in ORDERS])
    return {
        "orders": len(ORDERS),
        "scorers_agreed": sum(1 for r in debate if r["agreed"]),
        "scorers_disagreed": sum(1 for r in debate if not r["agreed"]),
        "debate_successes": d["successes"],
        "single_successes": s["successes"],
        "reviewed_pipeline_successes": p["successes"],
        "debate_mean_tokens": d["mean_tokens"],
        "single_mean_tokens": s["mean_tokens"],
        "debate_tokens_per_success": d["tokens_per_success"],
        "reviewed_pipeline_tokens_per_success":
            p["tokens_per_success"],
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
