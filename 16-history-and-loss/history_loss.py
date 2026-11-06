"""Lesson 16 artifact: the relay. Fields cross a chain of
relay agents, and each relay re-summarizes what it passes on,
dropping the field it judges least important. After each hop
the scorer scores what is left. This is MAST's loss of
conversation history, reproduced with a ruler."""

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

from mas.domain import LEADS, ORDERS, extract_regex, score_fields  # noqa: E402

DROP_ORDER = ("decision_maker", "timeline", "budget_usd", "service")
DEFAULTS = {"service": None, "budget_usd": None,
            "timeline": "flexible", "decision_maker": False,
            "discount_ask_pct": None}


def relay(fields, hops):
    out = dict(fields)
    for key in DROP_ORDER[:hops]:
        out[key] = DEFAULTS[key]
    return out


def evaluate():
    per_hop = {}
    survival = {k: 0 for k in DROP_ORDER}
    for hops in range(0, 5):
        bands = 0
        for o in ORDERS:
            fields = extract_regex(LEADS[o["lead_id"]]["text"])
            left = relay(fields, hops)
            if score_fields(left)[1] == o["expected"]["band"]:
                bands += 1
            if hops == 4:
                pass
        per_hop[hops] = bands
    for o in ORDERS:
        truth = LEADS[o["lead_id"]]["truth"]
        fields = extract_regex(LEADS[o["lead_id"]]["text"])
        for key in DROP_ORDER:
            if fields.get(key) == truth[key]:
                survival[key] += 1
    return {
        "orders": len(ORDERS),
        "bands_correct_by_hops": per_hop,
        "drop_order": list(DROP_ORDER),
        "fields_matching_truth_at_hop_0": survival,
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
