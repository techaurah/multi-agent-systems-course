"""Lesson 27 artifact: attribution. Three faults are injected
one at a time into the pipeline (extractor, scorer, drafter),
and a trace-inspection rule blames the first stage whose
output deviates from the healthy reference run. Its accuracy
is measured on the new failures each fault causes."""

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

from mas.domain import LEADS, ORDERS, check_draft, draft_naive  # noqa: E402
from mas.domain import extract_regex, grade, score_fields  # noqa: E402


def run_with(order, extractor=extract_regex, band_fn=None,
             drafter=draft_naive):
    lead = LEADS[order["lead_id"]]
    fields = extractor(lead["text"])
    score, band = score_fields(fields)
    if band_fn:
        band = band_fn(score)
    draft = drafter(lead["name"], fields)
    g = grade(order, fields, band, draft)
    return {"fields": fields, "band": band, "draft": draft,
            "success": g["success"],
            "violations": check_draft(draft, fields)}


def faulty_extractor(text):
    f = extract_regex(text)
    f["budget_usd"] = None
    return f


def strict_band(score):
    return "hot" if score >= 90 else "warm" if score >= 70 \
        else "nurture"


def sloppy_drafter(name, fields):
    return draft_naive(name, fields) + " We can do 15% off this month."


FAULTS = {
    "extractor": {"extractor": faulty_extractor},
    "scorer": {"band_fn": strict_band},
    "drafter": {"drafter": sloppy_drafter},
}


def attribute(ref, got):
    if got["fields"] != ref["fields"]:
        return "extractor"
    if got["band"] != ref["band"]:
        return "scorer"
    return "drafter"


def evaluate():
    reference = {o["id"]: run_with(o) for o in ORDERS}
    per_fault = {}
    total_new = total_correct = 0
    for stage, kwargs in FAULTS.items():
        new_failures = 0
        correct = 0
        for o in ORDERS:
            got = run_with(o, **kwargs)
            if not got["success"] and reference[o["id"]]["success"]:
                new_failures += 1
                if attribute(reference[o["id"]], got) == stage:
                    correct += 1
        per_fault[stage] = {"new_failures": new_failures,
                            "attributed_correctly": correct}
        total_new += new_failures
        total_correct += correct
    return {"per_fault": per_fault,
            "new_failures_total": total_new,
            "attributed_correctly_total": total_correct,
            "attribution_accuracy": round(total_correct / total_new, 4)
            if total_new else 0.0}


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
