"""Lesson 01 artifact: the same order, done by one agent and by
many. The work is identical; what changes is the coordination
surface, and the ledger makes the change visible."""

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
from mas.systems import run_pipeline, run_single  # noqa: E402


def evaluate():
    order = ORDERS[0]
    one = run_single(order)
    many = run_pipeline(order)
    agents = {"extractor", "scorer", "drafter", "coordinator"}
    return {
        "order_id": order["id"],
        "single_success": one["success"],
        "pipeline_success": many["success"],
        "single_messages": one["messages"],
        "pipeline_messages": many["messages"],
        "single_tokens": one["tokens"],
        "pipeline_tokens": many["tokens"],
        "single_agents": 1,
        "pipeline_agents": len(agents),
        "same_band": one["band"] == many["band"],
        "same_draft": one["draft"] == many["draft"],
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
