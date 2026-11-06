"""Lesson 30 artifact: the capstone system, as built.
Composition, not invention: the orchestrator's router
(Lesson 09) sends trap orders through the reviewer
(Lesson 21) and clean orders past it, over the sequential
pipeline (Lesson 06), with the ledger accounting of
Lesson 02 throughout."""

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
from mas.harness import by_family, summarize  # noqa: E402
from mas.systems import run_capstone  # noqa: E402


def evaluate():
    results = [run_capstone(o) for o in ORDERS]
    out = summarize(results)
    out["by_family"] = by_family(results, ORDERS)
    out["routed_to_review"] = sum(
        1 for r in results if r.get("routed_to_review"))
    return out


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
