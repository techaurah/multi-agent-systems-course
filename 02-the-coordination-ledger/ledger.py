"""Lesson 02 artifact: read one run like a ledger. A pipeline
run with a reviewer, rebuilt by hand on the ledger so every
message, its kind, and its token cost is visible; then the same
accounting across all 12 orders."""

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

from mas.core import Ledger, Message  # noqa: E402
from mas.domain import LEADS, ORDERS, check_draft, draft_naive  # noqa: E402
from mas.domain import draft_safe, extract_regex, score_fields  # noqa: E402
from mas.harness import summarize  # noqa: E402
from mas.systems import run_pipeline, run_single  # noqa: E402


def traced_run(order):
    """Lesson 06's pipeline with a reviewer, rebuilt message by
    message so the ledger itself is the lesson."""
    lead = LEADS[order["lead_id"]]
    led = Ledger()
    led.send(Message("coordinator", "extractor", "task",
                     {"lead_id": lead["id"], "text": lead["text"]}))
    led.step()
    fields = extract_regex(lead["text"])
    led.send(Message("extractor", "scorer", "fields", fields))
    led.step()
    score, band = score_fields(fields)
    led.send(Message("scorer", "drafter", "score",
                     {"score": score, "band": band, "fields": fields}))
    led.step()
    draft = draft_naive(lead["name"], fields)
    led.send(Message("drafter", "reviewer", "draft", {"draft": draft}))
    led.step()
    violations = check_draft(draft, fields)
    led.send(Message("reviewer", "drafter", "verdict",
                     {"ok": not violations, "violations": violations}))
    led.step()
    if violations:
        draft = draft_safe(lead["name"], fields)
        led.send(Message("drafter", "reviewer", "draft",
                         {"draft": draft}))
        led.step()
        led.send(Message("reviewer", "sender", "verdict",
                         {"ok": True, "violations": []}))
        led.step()
    return led


def evaluate():
    trap = next(o for o in ORDERS if o["id"] == "order-05")
    led = traced_run(trap)
    pipe = summarize([run_pipeline(o, reviewer=True) for o in ORDERS])
    single = summarize([run_single(o) for o in ORDERS])
    return {
        "traced_order": trap["id"],
        "traced_messages": led.message_count,
        "traced_tokens": led.token_count,
        "traced_steps": led.steps,
        "by_kind": led.by_kind(),
        "tokens_by_hop": led.tokens_by_hop(),
        "fleet_pipeline_messages": pipe["mean_messages"],
        "fleet_pipeline_tokens": pipe["mean_tokens"],
        "fleet_single_tokens": single["mean_tokens"],
        "overhead_share": round(
            1 - single["mean_tokens"] / pipe["mean_tokens"], 4),
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
