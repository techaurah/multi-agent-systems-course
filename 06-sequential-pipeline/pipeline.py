"""Lesson 06 artifact: the sequential pipeline on the full
order set, with failures attributed to the stage that produced
them. Compare Lesson 03: the failure list is the same list.
What the pipeline bought is not accuracy; it is places to
stand: a stage boundary where a check can be inserted later."""

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

STAGE_OF = {"fields": "extractor", "band": "scorer", "draft": "drafter"}


def evaluate():
    results = [run_pipeline(o) for o in ORDERS]
    out = summarize(results)
    single = summarize([run_single(o) for o in ORDERS])
    stage_failures = {}
    for r in results:
        for p in r["problems"]:
            stage = STAGE_OF[p.split(":")[0]]
            stage_failures[stage] = stage_failures.get(stage, 0) + 1
    out["stage_failures"] = stage_failures
    out["same_failures_as_single"] = \
        out["failed_orders"] == single["failed_orders"]
    out["single_mean_tokens"] = single["mean_tokens"]
    out["token_ratio_vs_single"] = round(
        out["mean_tokens"] / single["mean_tokens"], 2)
    return out


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
