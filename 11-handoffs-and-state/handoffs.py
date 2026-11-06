"""Lesson 11 artifact: what state must travel. The full
field set crosses the handoff, or a two-field summary does,
and the scorer fills the gaps with defaults. Count what the
summary saves and what it costs."""

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

import json  # noqa: E402

from mas.domain import LEADS, ORDERS, extract_regex, score_fields  # noqa: E402
from mas.tokens import approx_tokens  # noqa: E402

DEFAULTS = {"timeline": "flexible", "decision_maker": False,
            "discount_ask_pct": None}


def summarize_fields(fields):
    return {"service": fields["service"],
            "budget_usd": fields["budget_usd"]}


def evaluate():
    full_bands = summary_bands = 0
    full_tokens = summary_tokens = 0
    changed = []
    for o in ORDERS:
        text = LEADS[o["lead_id"]]["text"]
        fields = extract_regex(text)
        full_tokens += approx_tokens(json.dumps(fields, sort_keys=True))
        if score_fields(fields)[1] == o["expected"]["band"]:
            full_bands += 1
        small = summarize_fields(fields)
        summary_tokens += approx_tokens(json.dumps(small, sort_keys=True))
        merged = dict(DEFAULTS)
        merged.update(small)
        band = score_fields(merged)[1]
        if band == o["expected"]["band"]:
            summary_bands += 1
        else:
            changed.append(o["id"])
    return {
        "orders": len(ORDERS),
        "full_handoff_bands": full_bands,
        "summary_handoff_bands": summary_bands,
        "bands_changed_by_summary": changed,
        "full_mean_tokens": round(full_tokens / len(ORDERS), 1),
        "summary_mean_tokens": round(summary_tokens / len(ORDERS), 1),
        "tokens_saved_pct": round(
            100 * (1 - summary_tokens / full_tokens), 1),
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
