"""Lesson 04 artifact: decomposition, measured. The four jobs
form a chain inside each order and no edges at all between
orders. That shape, not enthusiasm, decides which topologies
can possibly help."""

import os
import sys
from collections import Counter

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

from mas.domain import LEADS, ORDERS, extract_regex  # noqa: E402

JOBS = ("extract", "score", "draft", "check")


def evaluate():
    families = Counter(o["family"] for o in ORDERS)
    needs_check = 0
    for o in ORDERS:
        f = extract_regex(LEADS[o["lead_id"]]["text"])
        if f["discount_ask_pct"] is not None or f["budget_usd"] is None:
            needs_check += 1
    return {
        "jobs_per_order": len(JOBS),
        "chain_edges_per_order": len(JOBS) - 1,
        "orders": len(ORDERS),
        "total_jobs_batch": len(JOBS) * len(ORDERS),
        "cross_order_edges": 0,
        "families": dict(sorted(families.items())),
        "orders_where_draft_depends_on_check": needs_check,
        "parallel_width": len(ORDERS),
        "chain_depth": len(JOBS),
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
