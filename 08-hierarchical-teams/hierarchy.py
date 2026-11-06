"""Lesson 08 artifact: a two-level hierarchy against a flat
worker pool, on all 12 orders. The hierarchy adds a manager
and two team leads, and with them delegation messages, token
overhead, and two extra steps on every path, in exchange for
a span of control nobody needed at this size."""

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
from mas.systems import run_hierarchy, run_parallel_batch  # noqa: E402


def evaluate():
    flat = run_parallel_batch(ORDERS, workers=4)
    hier = run_hierarchy(ORDERS)
    return {
        "orders": len(ORDERS),
        "flat_successes": flat["successes"],
        "hierarchy_successes": hier["successes"],
        "flat_messages": flat["messages"],
        "hierarchy_messages": hier["messages"],
        "delegation_messages": hier["messages"] - flat["messages"],
        "flat_tokens": flat["tokens"],
        "hierarchy_tokens": hier["tokens"],
        "token_overhead_pct": round(
            100 * (hier["tokens"] - flat["tokens"]) / flat["tokens"], 1),
        "flat_steps": flat["steps"],
        "hierarchy_steps": hier["steps"],
        "manager_messages_sent": len(ORDERS),
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
