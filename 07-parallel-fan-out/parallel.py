"""Lesson 07 artifact: fan-out on the independent orders.
Dealing whole orders to a worker pool changes exactly one
currency: steps, the simulated makespan. Success and tokens
are what they were; time is what parallelism buys."""

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
from mas.systems import run_parallel_batch, run_single  # noqa: E402


def evaluate():
    batch = [o for o in ORDERS if o["family"] == "independent"]
    serial_steps = sum(run_single(o)["steps"] for o in batch)
    serial_tokens = sum(run_single(o)["tokens"] for o in batch)
    sweep = {}
    for w in (1, 2, 3, 6):
        r = run_parallel_batch(batch, workers=w)
        sweep[w] = {"steps": r["steps"], "tokens": r["tokens"],
                    "messages": r["messages"],
                    "successes": r["successes"]}
    return {
        "batch_orders": len(batch),
        "serial_single_steps": serial_steps,
        "serial_single_tokens": serial_tokens,
        "sweep": sweep,
        "speedup_at_3_workers": round(
            serial_steps / sweep[3]["steps"], 2),
        "token_ratio_at_3_workers": round(
            sweep[3]["tokens"] / serial_tokens, 2),
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
