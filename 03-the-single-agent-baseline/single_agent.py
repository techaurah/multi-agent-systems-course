"""Lesson 03 artifact: the single-agent baseline. One agent,
one pass, all four jobs. Every multi-agent system in this
course is raced against this file's numbers, so they are
printed in full, failures included."""

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
from mas.systems import run_single  # noqa: E402


def evaluate():
    results = [run_single(o) for o in ORDERS]
    out = summarize(results)
    out["by_family"] = by_family(results, ORDERS)
    out["failure_kinds"] = {}
    for r in results:
        for p in r["problems"]:
            kind = p.split(":")[0]
            out["failure_kinds"][kind] = \
                out["failure_kinds"].get(kind, 0) + 1
    return out


if __name__ == "__main__":
    r = evaluate()
    for k, v in r.items():
        print(f"{k}: {v}")
