"""Lesson 14 artifact: shared memory and the stale read. A
shared store holds extracted fields. A verifier later writes
careful fields for the thin orders. A scorer that reads before
the verifier writes scores the old version, correctly, all the
way to a wrong band. Version checks are the fix."""

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

from mas.domain import LEADS, ORDERS, extract_careful  # noqa: E402
from mas.domain import extract_regex, score_fields  # noqa: E402

THIN = ("order-04", "order-06", "order-07", "order-12")


class Store:
    """A versioned shared store: every write bumps the version,
    and a read returns the version it saw."""

    def __init__(self):
        self.rows = {}

    def write(self, key, value):
        version = self.rows.get(key, (0, None))[0] + 1
        self.rows[key] = (version, value)

    def read(self, key):
        return self.rows[key]


def bands_correct(reads):
    return sum(1 for o, fields in reads
               if score_fields(fields)[1] == o["expected"]["band"])


def evaluate():
    store = Store()
    for o in ORDERS:
        store.write(o["id"], extract_regex(LEADS[o["lead_id"]]["text"]))

    # Stale schedule: the scorer's turn comes before the
    # verifier's writes for the thin orders.
    stale_reads = []
    for o in ORDERS:
        version, fields = store.read(o["id"])
        stale_reads.append((o, fields))
    stale_versions = {o["id"]: store.read(o["id"])[0]
                      for o in ORDERS if o["id"] in THIN}

    # The verifier upgrades the thin orders to version 2.
    for o in ORDERS:
        if o["id"] in THIN:
            store.write(o["id"],
                        extract_careful(LEADS[o["lead_id"]]["text"]))

    # Version-checked schedule: the scorer will not score a
    # thin order below version 2, so it reads the upgrade.
    fresh_reads = []
    for o in ORDERS:
        version, fields = store.read(o["id"])
        fresh_reads.append((o, fields))

    return {
        "orders": len(ORDERS),
        "thin_orders": list(THIN),
        "stale_schedule_bands_correct": bands_correct(stale_reads),
        "version_checked_bands_correct": bands_correct(fresh_reads),
        "versions_seen_by_stale_scorer": stale_versions,
        "final_versions_for_thin_orders":
            {o["id"]: store.read(o["id"])[0]
             for o in ORDERS if o["id"] in THIN},
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
