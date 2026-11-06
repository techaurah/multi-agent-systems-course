"""Lesson 00 artifact: verify the environment and count the
instruments every later lesson uses."""

import os
import sys
from collections import Counter

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

from mas.domain import LEADS, ORDERS, POLICY  # noqa: E402


def evaluate():
    families = Counter(o["family"] for o in ORDERS)
    bands = Counter(o["expected"]["band"] for o in ORDERS)
    return {
        "python_ok": sys.version_info >= (3, 11),
        "leads": len(LEADS),
        "orders": len(ORDERS),
        "families": dict(sorted(families.items())),
        "expected_bands": dict(sorted(bands.items())),
        "services": len(POLICY["services"]),
        "max_discount_pct": POLICY["max_discount_pct"],
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
