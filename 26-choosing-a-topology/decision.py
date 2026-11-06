"""Lesson 26 artifact: choosing a topology, from the course's
own measurements. Each task family is scored for four systems,
and the recommendation row is computed, not asserted: best
success first, then cheapest cost per success."""

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
from mas.systems import (run_orchestrated, run_pipeline,  # noqa: E402
                         run_single)

SYSTEMS = {
    "single": run_single,
    "pipeline": lambda o: run_pipeline(o),
    "pipeline_reviewed": lambda o: run_pipeline(o, reviewer=True),
    "orchestrated": run_orchestrated,
}


def evaluate():
    fams = {}
    picks = {}
    for name, fn in SYSTEMS.items():
        fams[name] = by_family([fn(o) for o in ORDERS], ORDERS)
    for fam in ("independent", "chained", "ambiguous"):
        best = None
        for name in SYSTEMS:
            row = fams[name][fam]
            key = (row["success_rate"], -(row["tokens_per_success"]
                                          or 10 ** 9))
            if best is None or key > best[0]:
                best = (key, name)
        picks[fam] = best[1]
    overall = {name: summarize([fn(o) for o in ORDERS])
               for name, fn in SYSTEMS.items()}
    return {"by_family": fams, "picks": picks,
            "overall_successes":
                {k: v["successes"] for k, v in overall.items()}}


if __name__ == "__main__":
    r = evaluate()
    for fam, pick in r["picks"].items():
        print(fam, "->", pick)
    for name, fams in r["by_family"].items():
        print(name, {f: (row["successes"], row["tokens_per_success"])
                     for f, row in fams.items()})
