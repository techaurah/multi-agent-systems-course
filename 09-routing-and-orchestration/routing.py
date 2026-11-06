"""Lesson 09 artifact: the router. An orchestrator earns its
keep by sending each order down the cheapest route that is
still safe. Measured here: a small text router against the
two lazy strategies, always review everything and always
review nothing."""

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

from mas.domain import LEADS, ORDERS, extract_regex  # noqa: E402
from mas.systems import run_orchestrated, run_pipeline  # noqa: E402


def text_route(text):
    """The router's rules, reading the raw inquiry only."""
    if "% off" in text or "$" not in text:
        return "review"
    return "standard"


def true_route(order):
    f = extract_regex(LEADS[order["lead_id"]]["text"])
    if f["discount_ask_pct"] is not None or f["budget_usd"] is None:
        return "review"
    return "standard"


def evaluate():
    correct = 0
    review_orders = 0
    for o in ORDERS:
        if text_route(LEADS[o["lead_id"]]["text"]) == true_route(o):
            correct += 1
        if true_route(o) == "review":
            review_orders += 1
    orch = [run_orchestrated(o) for o in ORDERS]
    always = [run_pipeline(o, reviewer=True) for o in ORDERS]
    never = [run_pipeline(o, reviewer=False) for o in ORDERS]
    return {
        "router_correct": correct,
        "orders": len(ORDERS),
        "orders_needing_review": review_orders,
        "orchestrated_successes": sum(r["success"] for r in orch),
        "always_review_successes": sum(r["success"] for r in always),
        "never_review_escapes": sum(len(r["escapes"]) for r in never),
        "orchestrated_mean_tokens": round(
            sum(r["tokens"] for r in orch) / len(orch), 1),
        "always_review_mean_tokens": round(
            sum(r["tokens"] for r in always) / len(always), 1),
        "token_saving_pct": round(100 * (1 - sum(
            r["tokens"] for r in orch)
            / sum(r["tokens"] for r in always)), 1),
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
