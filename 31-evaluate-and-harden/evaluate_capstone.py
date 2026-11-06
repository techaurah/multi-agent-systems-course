"""Lesson 31 artifact: the verdict. The as-built capstone is
checked against the gates fixed in Lesson 29; it fails the
success gate. The hardening (a field check pass, Lesson 14's
lesson applied at the extractor boundary) is then measured
against the same gates, with the as-built run kept in the
output and the costs stated plainly."""

import importlib.util
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
from mas.systems import run_capstone, run_single  # noqa: E402

GATES = os.path.join(ROOT, "29-capstone-spec", "capstone",
                     "gates.json")


def load_gates():
    with open(GATES) as f:
        return json.load(f)["capstone_system"]["gates"]


def check(metrics, baseline, gates):
    return {
        "task_success_rate_min":
            metrics["success_rate"] >= gates["task_success_rate_min"],
        "policy_escapes_max":
            metrics["escapes"] <= gates["policy_escapes_max"],
        "mean_messages_per_order_max":
            metrics["mean_messages"]
            <= gates["mean_messages_per_order_max"],
        "tokens_per_success_max":
            metrics["tokens_per_success"]
            <= gates["tokens_per_success_max"],
        "success_delta_vs_single_min":
            round(metrics["success_rate"]
                  - baseline["success_rate"], 4)
            >= gates["success_delta_vs_single_min"],
    }


def evaluate():
    gates = load_gates()
    baseline = summarize([run_single(o) for o in ORDERS])
    as_built = summarize([run_capstone(o) for o in ORDERS])
    hardened = summarize(
        [run_capstone(o, hardened=True) for o in ORDERS])
    as_checks = check(as_built, baseline, gates)
    hard_checks = check(hardened, baseline, gates)
    return {
        "gates": gates,
        "baseline_single": baseline,
        "as_built": as_built,
        "as_built_checks": as_checks,
        "as_built_gates_passed": sum(as_checks.values()),
        "hardened": hardened,
        "hardened_checks": hard_checks,
        "hardened_gates_passed": sum(hard_checks.values()),
        "ship": all(hard_checks.values()),
    }


if __name__ == "__main__":
    r = evaluate()
    print("as built:", r["as_built"])
    print("as-built gates passed:", r["as_built_gates_passed"], "of 5")
    for k, v in r["as_built_checks"].items():
        print(("PASS " if v else "FAIL ") + k)
    print("hardened:", r["hardened"])
    print("hardened gates passed:", r["hardened_gates_passed"], "of 5")
    for k, v in r["hardened_checks"].items():
        print(("PASS " if v else "FAIL ") + k)
    print("ship:", r["ship"])
