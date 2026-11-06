"""Lesson 25 artifact: scaling the team. The same batch is
dealt to pools of one to twelve workers, and the makespan is
read against the pool size. The curve bends where the batch,
not the pool, becomes the limit, and tokens never move at
all: workers cost coordination, not parallelism."""

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
from mas.systems import run_parallel_batch  # noqa: E402


def evaluate():
    batch = [o for o in ORDERS if o["family"] == "independent"]
    sweep = {}
    for w in (1, 2, 3, 4, 6, 12):
        r = run_parallel_batch(batch, workers=w)
        sweep[w] = {"steps": r["steps"], "tokens": r["tokens"],
                    "messages": r["messages"],
                    "successes": r["successes"]}
    base = sweep[1]["steps"]
    gains = {w: round(base / sweep[w]["steps"], 2) for w in sweep}
    plateau = min(w for w in sweep
                  if sweep[w]["steps"] == sweep[max(sweep)]["steps"])
    return {"batch_orders": len(batch), "sweep": sweep,
            "speedup_by_workers": gains,
            "smallest_pool_at_best_makespan": plateau,
            "tokens_constant_across_pools":
                len({s["tokens"] for s in sweep.values()}) == 1}


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
