"""Lesson 29 artifact: the capstone spec, executable. It
prints the gates fixed in capstone/gates.json and the
baseline numbers they were set against, so a reader can
check the gates were not reverse-engineered from the
capstone's results."""

import json
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
from mas.systems import run_single  # noqa: E402


def evaluate():
    with open(os.path.join(HERE, "capstone", "gates.json")) as f:
        spec = json.load(f)["capstone_system"]
    baseline = summarize([run_single(o) for o in ORDERS])
    return {
        "gates": spec["gates"],
        "fixed_before_build": spec["fixed_before_build"],
        "baseline_single_success_rate": baseline["success_rate"],
        "baseline_single_tokens_per_success":
            baseline["tokens_per_success"],
        "baseline_single_escapes": baseline["escapes"],
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
