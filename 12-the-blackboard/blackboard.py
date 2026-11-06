"""Lesson 12 artifact: three ways to move the same work.
Addressed messages, a broadcast bus, and a blackboard with
subscriptions, counted in deliveries: how many agent-inbox
arrivals one order causes under each discipline."""

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
from mas.systems import run_blackboard, run_pipeline  # noqa: E402

AGENTS = 5  # coordinator, extractor, scorer, drafter, sender


def broadcast_deliveries(order):
    """Every pipeline message is delivered to every other
    agent's inbox: the group-chat discipline."""
    msgs = run_pipeline(order)["messages"]
    return msgs * (AGENTS - 1)


def evaluate():
    board = [run_blackboard(o) for o in ORDERS]
    pipe = [run_pipeline(o) for o in ORDERS]
    board_s = summarize(board)
    pipe_s = summarize(pipe)
    return {
        "orders": len(ORDERS),
        "addressed_deliveries_per_order": pipe_s["mean_messages"],
        "broadcast_deliveries_per_order": round(
            sum(broadcast_deliveries(o) for o in ORDERS) / len(ORDERS), 2),
        "blackboard_deliveries_per_order": board_s["mean_messages"] + 4,
        "blackboard_successes": board_s["successes"],
        "pipeline_successes": pipe_s["successes"],
        "blackboard_mean_tokens": board_s["mean_tokens"],
        "pipeline_mean_tokens": pipe_s["mean_tokens"],
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
