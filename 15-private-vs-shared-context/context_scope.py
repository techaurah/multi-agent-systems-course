"""Lesson 15 artifact: who sees what. Counted two ways: the
exposure ledger (how many lead texts each design puts in front
of each agent) and a contamination case, where a drafter whose
context holds earlier drafts repeats a discount line it saw
in one of them."""

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

import re  # noqa: E402

from mas.domain import LEADS, ORDERS, check_draft, draft_naive  # noqa: E402
from mas.domain import extract_regex  # noqa: E402
from mas.tokens import approx_tokens  # noqa: E402

AGENTS = ("coordinator", "extractor", "scorer", "drafter", "sender")


def contaminated_draft(name, fields, context_drafts):
    """A stand-in for a real failure: a drafter whose context
    holds earlier replies copies the strongest discount line
    it can see there, whether or not this lead asked for it."""
    draft = draft_naive(name, fields)
    seen = [int(m.group(1)) for d in context_drafts
            for m in [re.search(r"(\d+)%\s*off", d)] if m]
    if seen and fields.get("discount_ask_pct") is None:
        draft += f" And we can do {max(seen)}% off."
    return draft


def evaluate():
    texts = [LEADS[o["lead_id"]]["text"] for o in ORDERS]
    total_text_tokens = sum(approx_tokens(t) for t in texts)
    # Broadcast: every agent reads every lead text.
    broadcast_exposure = total_text_tokens * len(AGENTS)
    # Addressed pipeline: only the extractor reads lead texts.
    addressed_exposure = total_text_tokens
    # Contamination: drafts are written in order-05's shadow.
    history = []
    contaminated_violations = 0
    clean_violations = 0
    for o in ORDERS:
        lead = LEADS[o["lead_id"]]
        fields = extract_regex(lead["text"])
        d = contaminated_draft(lead["name"], fields, history)
        contaminated_violations += len(check_draft(d, fields))
        clean_violations += len(check_draft(
            draft_naive(lead["name"], fields), fields))
        history.append(d)
    return {
        "orders": len(ORDERS),
        "agents": len(AGENTS),
        "lead_text_tokens_total": total_text_tokens,
        "broadcast_text_exposure_tokens": broadcast_exposure,
        "addressed_text_exposure_tokens": addressed_exposure,
        "exposure_ratio": round(broadcast_exposure
                                / addressed_exposure, 1),
        "violations_with_shared_draft_history": contaminated_violations,
        "violations_without_history": clean_violations,
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
