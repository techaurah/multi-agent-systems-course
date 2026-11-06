"""Lesson 10 artifact: the handoff format is a correctness
decision. The same extracted fields travel two ways: as a
typed payload, and as a prose summary written the way a
hurried agent writes one. Downstream, the scorer can only
score what survived."""

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

from mas.domain import LEADS, ORDERS, extract_regex  # noqa: E402
from mas.domain import fields_match, score_fields  # noqa: E402
from mas.tokens import approx_tokens  # noqa: E402


def to_prose(fields):
    """A summary-style handoff: it leads with the service and
    the budget, and drops timing and decision-maker status,
    the way real summaries drop qualifiers."""
    parts = []
    if fields["service"]:
        parts.append(f"wants {fields['service']}")
    if fields["budget_usd"] is not None:
        parts.append(f"budget ${fields['budget_usd']:,}")
    else:
        parts.append("budget not stated")
    return "; ".join(parts)


def from_prose(text):
    """The receiving agent's parser: what the prose does not
    carry comes back as a default, not as an error."""
    import re
    fields = {"service": None, "budget_usd": None,
              "timeline": "flexible", "decision_maker": False,
              "discount_ask_pct": None}
    for s in ("garden design", "lawn care", "tree surgery",
              "irrigation", "patio build"):
        if s in text:
            fields["service"] = s
    m = re.search(r"\$([\d,]+)", text)
    if m:
        fields["budget_usd"] = int(m.group(1).replace(",", ""))
    return fields


def evaluate():
    typed_exact = prose_exact = 0
    typed_bands = prose_bands = 0
    typed_tokens = prose_tokens = 0
    for o in ORDERS:
        truth = LEADS[o["lead_id"]]["truth"]
        fields = extract_regex(LEADS[o["lead_id"]]["text"])
        import json
        typed_tokens += approx_tokens(json.dumps(fields, sort_keys=True))
        prose = to_prose(fields)
        prose_tokens += approx_tokens(prose)
        back = from_prose(prose)
        if fields_match(fields, truth):
            typed_exact += 1
        if fields_match(back, truth):
            prose_exact += 1
        if score_fields(fields)[1] == o["expected"]["band"]:
            typed_bands += 1
        if score_fields(back)[1] == o["expected"]["band"]:
            prose_bands += 1
    return {
        "orders": len(ORDERS),
        "typed_fields_exact": typed_exact,
        "prose_fields_exact": prose_exact,
        "typed_bands_correct": typed_bands,
        "prose_bands_correct": prose_bands,
        "typed_mean_tokens": round(typed_tokens / len(ORDERS), 1),
        "prose_mean_tokens": round(prose_tokens / len(ORDERS), 1),
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
