"""Lesson 05 artifact: the race multi-agent loses. On chained
orders the pipeline does exactly the same work as the single
agent, in the same order, and gets exactly the same results.
The only differences are the coordination currencies, and
the pipeline spends more of all of them."""

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
from mas.systems import run_pipeline, run_single  # noqa: E402


def evaluate():
    chained = [o for o in ORDERS if o["family"] == "chained"]
    single = summarize([run_single(o) for o in chained])
    pipe = summarize([run_pipeline(o) for o in chained])
    return {
        "orders": [o["id"] for o in chained],
        "single_successes": single["successes"],
        "pipeline_successes": pipe["successes"],
        "same_failures": single["failed_orders"] == pipe["failed_orders"],
        "single_mean_tokens": single["mean_tokens"],
        "pipeline_mean_tokens": pipe["mean_tokens"],
        "token_ratio": round(
            pipe["mean_tokens"] / single["mean_tokens"], 2),
        "single_tokens_per_success": single["tokens_per_success"],
        "pipeline_tokens_per_success": pipe["tokens_per_success"],
        "single_messages_total": 0,
        "pipeline_mean_messages": pipe["mean_messages"],
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
