"""Lesson 21 artifact: the reviewer, priced. A verification
bottleneck at the exit catches every policy violation in the
drafts, and its cost and its blind spot are both measured:
it reads drafts, not facts, so wrong fields walk past it."""

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
from mas.systems import run_pipeline  # noqa: E402


def evaluate():
    bare = [run_pipeline(o) for o in ORDERS]
    reviewed = [run_pipeline(o, reviewer=True) for o in ORDERS]
    b = summarize(bare)
    r = summarize(reviewed)
    wrong_bands_past_review = [
        x["order_id"] for x in reviewed
        if not x["success"] and "band" in x["problems"]]
    return {
        "orders": len(ORDERS),
        "escapes_without_reviewer": b["escapes"],
        "escapes_with_reviewer": r["escapes"],
        "successes_without_reviewer": b["successes"],
        "successes_with_reviewer": r["successes"],
        "extra_mean_tokens": round(
            r["mean_tokens"] - b["mean_tokens"], 1),
        "extra_mean_messages": round(
            r["mean_messages"] - b["mean_messages"], 2),
        "redrafts_triggered": sum(x["redrafts"] for x in reviewed),
        "wrong_bands_past_the_reviewer": wrong_bands_past_review,
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
