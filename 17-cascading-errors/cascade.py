"""Lesson 17 artifact: cascading errors. One fault is
injected at the extractor (it drops every budget) and the
damage is counted at each downstream stage, in three systems:
the single agent, the pipeline, and the pipeline with a field
checkpoint where Lesson 14's version check lives."""

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
from mas.domain import extract_regex, grade, score_fields  # noqa: E402
from mas.domain import draft_naive, draft_safe  # noqa: E402
from mas.harness import summarize  # noqa: E402
from mas.systems import run_pipeline, run_single  # noqa: E402


def faulty_extractor(text):
    fields = extract_regex(text)
    fields["budget_usd"] = None
    return fields


def run_checkpoint(order):
    """Pipeline whose scorer refuses a budget-free extraction
    when the text carries a figure, and sends it back for the
    careful reading."""
    lead = LEADS[order["lead_id"]]
    fields = faulty_extractor(lead["text"])
    recovered = False
    if fields["budget_usd"] is None and "$" in lead["text"]:
        fields = extract_careful(lead["text"])
        recovered = True
    score, band = score_fields(fields)
    draft = draft_safe(lead["name"], fields)
    g = grade(order, fields, band, draft)
    return {"order_id": order["id"], "fields": fields, "score": score,
            "band": band, "draft": draft, "success": g["success"],
            "problems": g["problems"], "escapes": g["violations"],
            "messages": 5, "tokens": 0, "steps": 5,
            "recovered": recovered}


def evaluate():
    single_faulty = summarize(
        [run_single(o, extractor=faulty_extractor) for o in ORDERS])
    pipe_faulty = summarize(
        [run_pipeline(o, extractor=faulty_extractor) for o in ORDERS])
    healthy = summarize([run_pipeline(o) for o in ORDERS])
    checked = [run_checkpoint(o) for o in ORDERS]
    checked_s = summarize(checked)
    return {
        "orders": len(ORDERS),
        "healthy_pipeline_successes": healthy["successes"],
        "faulty_single_successes": single_faulty["successes"],
        "faulty_pipeline_successes": pipe_faulty["successes"],
        "faulty_pipeline_failed": pipe_faulty["failed_orders"],
        "checkpoint_successes": checked_s["successes"],
        "checkpoint_recovered_orders":
            [r["order_id"] for r in checked if r["recovered"]],
        "checkpoint_failed": checked_s["failed_orders"],
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
