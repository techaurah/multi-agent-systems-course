"""The systems under comparison, all built from mas/core.py and
mas/domain.py so their ledgers are comparable.

Every runner returns one result dict per order with the produced
fields, score, band, final draft, the violations left in that
draft (escapes), and the ledger stats for the run. Lessons race
these runners against each other; the capstone composes them.

Conventions: one agent invocation is one step. A message's token
cost is the approximation from mas/tokens.py over its serialized
form, headers included, because headers are part of what a
receiving agent reads.
"""

from .core import Ledger, Message
from .domain import (LEADS, check_draft, draft_naive, draft_safe,
                     extract_careful, extract_regex, grade,
                     score_fields)
from .tokens import approx_tokens


def _result(order, fields, draft, ledger, steps, extra=None):
    score, band = score_fields(fields)
    g = grade(order, fields, band, draft)
    out = {"order_id": order["id"], "fields": fields, "score": score,
           "band": band, "draft": draft, "success": g["success"],
           "problems": g["problems"], "escapes": g["violations"],
           "messages": ledger.message_count if ledger else 0,
           "tokens": ledger.token_count if ledger else 0,
           "steps": steps}
    if extra:
        out.update(extra)
    return out


def run_single(order, extractor=extract_regex, drafter=draft_naive):
    """The monolith: one agent does extract, score, and draft in
    a single pass, holding everything in its own context. No
    messages; its token count is the text it reads plus the text
    it writes, counted once."""
    lead = LEADS[order["lead_id"]]
    fields = extractor(lead["text"])
    draft = drafter(lead["name"], fields)
    tokens = approx_tokens(lead["text"]) + approx_tokens(draft)
    score, band = score_fields(fields)
    g = grade(order, fields, band, draft)
    return {"order_id": order["id"], "fields": fields, "score": score,
            "band": band, "draft": draft, "success": g["success"],
            "problems": g["problems"], "escapes": g["violations"],
            "messages": 0, "tokens": tokens, "steps": 3}


def run_pipeline(order, extractor=extract_regex, drafter=draft_naive,
                 reviewer=False):
    """The sequential pipeline: coordinator, extractor, scorer,
    drafter, and optionally a reviewer who can send a violating
    draft back for one safe redraft."""
    lead = LEADS[order["lead_id"]]
    led = Ledger()
    led.send(Message("coordinator", "extractor", "task",
                     {"lead_id": lead["id"], "text": lead["text"]}))
    led.step()
    fields = extractor(lead["text"])
    led.send(Message("extractor", "scorer", "fields", fields))
    led.step()
    score, band = score_fields(fields)
    led.send(Message("scorer", "drafter", "score",
                     {"score": score, "band": band, "fields": fields}))
    led.step()
    draft = drafter(lead["name"], fields)
    redrafts = 0
    if reviewer:
        led.send(Message("drafter", "reviewer", "draft",
                         {"draft": draft}))
        led.step()
        violations = check_draft(draft, fields)
        led.send(Message("reviewer", "drafter", "verdict",
                         {"ok": not violations,
                          "violations": violations}))
        led.step()
        if violations:
            redrafts = 1
            draft = draft_safe(lead["name"], fields)
            led.send(Message("drafter", "reviewer", "draft",
                             {"draft": draft}))
            led.step()
            violations = check_draft(draft, fields)
            led.send(Message("reviewer", "sender", "verdict",
                             {"ok": not violations,
                              "violations": violations}))
            led.step()
    return _result(order, fields, draft, led, led.steps,
                   {"redrafts": redrafts})


def run_parallel_batch(orders, workers=3, extractor=extract_regex):
    """Fan-out: orders are dealt round robin to a fixed pool of
    pipeline workers. Messages and tokens add up across workers;
    steps are the makespan, the busiest worker's step count,
    because workers run at the same time."""
    per_worker_steps = [0] * workers
    results = []
    for i, order in enumerate(orders):
        r = run_pipeline(order, extractor=extractor)
        per_worker_steps[i % workers] += r["steps"]
        results.append(r)
    return {"results": results,
            "messages": sum(r["messages"] for r in results),
            "tokens": sum(r["tokens"] for r in results),
            "steps": max(per_worker_steps) if per_worker_steps else 0,
            "successes": sum(1 for r in results if r["success"])}


def run_hierarchy(orders, extractor=extract_regex):
    """Two-level hierarchy: a manager deals orders to two team
    leads, who deal to workers. Every delegation is a message on
    top of the worker's own pipeline run, and steps are the
    busiest worker's step load plus the two delegation steps on
    its path."""
    results = []
    delegation_tokens = 0
    leaf_steps = [0, 0, 0, 0]
    for i, order in enumerate(orders):
        team = i % 2
        worker = i % 4
        delegation_tokens += Message(
            "manager", f"teamlead-{team}", "task",
            {"order_id": order["id"]}).tokens()
        delegation_tokens += Message(
            f"teamlead-{team}", f"worker-{worker}", "task",
            {"order_id": order["id"],
             "lead_id": order["lead_id"]}).tokens()
        r = run_pipeline(order, extractor=extractor)
        leaf_steps[worker] += r["steps"]
        results.append(r)
    return {"results": results,
            "messages": 2 * len(orders)
            + sum(r["messages"] for r in results),
            "tokens": delegation_tokens
            + sum(r["tokens"] for r in results),
            "steps": max(leaf_steps) + 2,
            "successes": sum(1 for r in results if r["success"])}



def run_debate(order):
    """Two scorers read the same lead with different extractors
    and argue in messages; a judge agent settles disagreements
    with the careful reading rule (a labelled total beats a phase
    price, words are numbers). The draft is written once, safely,
    from the settled fields."""
    lead = LEADS[order["lead_id"]]
    led = Ledger()
    led.send(Message("coordinator", "scorer-a", "task",
                     {"text": lead["text"]}))
    led.send(Message("coordinator", "scorer-b", "task",
                     {"text": lead["text"]}))
    led.step(2)
    fa = extract_regex(lead["text"])
    fb = extract_careful(lead["text"])
    sa, ba = score_fields(fa)
    sb, bb = score_fields(fb)
    led.send(Message("scorer-a", "judge", "score",
                     {"score": sa, "band": ba, "fields": fa}))
    led.send(Message("scorer-b", "judge", "score",
                     {"score": sb, "band": bb, "fields": fb}))
    led.step(2)
    agreed = fa == fb
    fields = fb if not agreed else fa
    led.send(Message("judge", "drafter", "fields", fields,
                     note="settled by the careful reading rule"
                     if not agreed else "scorers agreed"))
    led.step()
    draft = draft_safe(lead["name"], fields)
    return _result(order, fields, draft, led, led.steps,
                   {"agreed": agreed})


def run_blackboard(order):
    """Blackboard: agents post to a shared board and read what
    they subscribe to, instead of addressing each other. Board
    writes and reads are the messages."""
    lead = LEADS[order["lead_id"]]
    led = Ledger()
    board = {}
    led.send(Message("extractor", "board", "fields",
                     {"entry": "fields"}))
    board["fields"] = extract_regex(lead["text"])
    led.step()
    fields = board["fields"]
    score, band = score_fields(fields)
    led.send(Message("scorer", "board", "score",
                     {"entry": "score", "band": band}))
    led.step()
    led.send(Message("drafter", "board", "draft",
                     {"entry": "draft"}))
    draft = draft_safe(lead["name"], fields)
    led.step()
    return _result(order, fields, draft, led, led.steps,
                   {"board_entries": 3})


def run_orchestrated(order, extractor=extract_regex):
    """Orchestrator-worker: a router reads the lead first and
    chooses the route. Trap orders (a discount ask, or a missing
    budget) go through the reviewer; clean orders skip it. The
    routing decision itself is one message and one step."""
    lead = LEADS[order["lead_id"]]
    fields = extractor(lead["text"])
    needs_review = fields.get("discount_ask_pct") is not None \
        or fields.get("budget_usd") is None
    r = run_pipeline(order, extractor=extractor, reviewer=needs_review)
    r["routed_to_review"] = needs_review
    r["messages"] += 1
    r["steps"] += 1
    return r


def run_capstone(order, hardened=False):
    """The capstone system, built in Lesson 30: orchestrated
    routing, a reviewer on trap orders, and (in the hardened
    configuration from Lesson 31) a field check pass that
    re-reads the lead with the careful extractor whenever the
    quick extraction looks thin (no budget found, or a figure
    that might be a phase price)."""
    lead = LEADS[order["lead_id"]]
    extractor = extract_regex
    r = run_orchestrated(order, extractor=extractor)
    if hardened:
        fields = r["fields"]
        thin = fields.get("budget_usd") is None \
            or "total" in lead["text"].lower()
        if thin:
            fixed = extract_careful(lead["text"])
            r["messages"] += 2
            r["steps"] += 2
            r["tokens"] += Message(
                "fieldchecker", "extractor", "task",
                {"lead_id": lead["id"], "text": lead["text"]}).tokens()
            r["tokens"] += Message(
                "extractor", "fieldchecker", "fields", fixed).tokens()
            if fixed != fields:
                draft = draft_safe(lead["name"], fixed)
                score, band = score_fields(fixed)
                g = grade(order, fixed, band, draft)
                r.update({"fields": fixed, "score": score,
                          "band": band, "draft": draft,
                          "success": g["success"],
                          "problems": g["problems"],
                          "escapes": g["violations"],
                          "field_checked": True})
    return r
