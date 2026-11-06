"""The shared work domain: Fernhill lead processing.

One fictional business (Fernhill Garden Centres, invented for
this course) receives leads; every system in the course does the
same four jobs on each lead:

1. extract: pull service, budget, timeline, and decision-maker
   status out of the free text inquiry;
2. score: apply the published rubric to the extracted fields;
3. draft: compose the first reply;
4. check: hold the draft against the reply policy.

The workers here are deterministic stand-ins: rule-based agents
in the LeadPipe pattern. Two extractor variants exist on purpose.
extract_regex is the quick one a team ships first; it misses a
budget written in words and takes the first figure in a message
that names two. extract_careful reads number words and prefers a
figure labelled as a total. Most of the course's failure lessons
live in the gap between those two functions.
"""

import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(name):
    with open(os.path.join(ROOT, "fixtures", name)) as f:
        return json.load(f)


LEADS = {lead["id"]: lead for lead in load("leads.json")}
ORDERS = load("orders.json")
POLICY = load("policy.json")
SERVICES = POLICY["services"]
PREMIUM = set(POLICY["premium_services"])
MAX_DISCOUNT = POLICY["max_discount_pct"]

_WORD_NUMBERS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "fifteen": 15, "twenty": 20,
}

_URGENT = ("this week", "urgent", "asap", "abruptly")
_SOON = ("next month",)
_DM_YES = ("i own", "my house, my", "my decision", "my call",
          "i run", "i can approve", "i decide", "he pays and he decides",
          "my money, my decision", "i will sign off", "send the quote to me",
          "come back to me directly")


def _service(text):
    low = text.lower()
    for s in SERVICES:
        if s in low:
            return s
    if "lawn" in low:
        return "lawn care"
    if "tree" in low:
        return "tree surgery"
    return None


def _timeline(text):
    low = text.lower()
    if any(k in low for k in _URGENT):
        return "urgent"
    if any(k in low for k in _SOON):
        return "soon"
    return "flexible"


def _decision_maker(text):
    low = text.lower()
    if "on behalf of my manager" in low or "for my parents" in low \
            or "asking for my landlord" in low:
        return False
    return any(k in low for k in _DM_YES)


def _discount_ask(text):
    m = re.search(r"(\d+)%\s*off", text)
    return int(m.group(1)) if m else None


def extract_regex(text):
    """The quick extractor: first dollar figure wins, digits only."""
    m = re.search(r"\$([\d,]+)", text)
    budget = int(m.group(1).replace(",", "")) if m else None
    return {"service": _service(text), "budget_usd": budget,
            "timeline": _timeline(text),
            "decision_maker": _decision_maker(text),
            "discount_ask_pct": _discount_ask(text)}


def extract_careful(text):
    """The careful extractor: totals beat phase prices, and a
    budget written in words still counts."""
    fields = extract_regex(text)
    low = text.lower()
    m = re.search(r"total[^$]*\$([\d,]+)", low)
    if m:
        fields["budget_usd"] = int(m.group(1).replace(",", ""))
    if fields["budget_usd"] is None:
        m = re.search(r"(" + "|".join(_WORD_NUMBERS) + r")\s+thousand", low)
        if m:
            fields["budget_usd"] = _WORD_NUMBERS[m.group(1)] * 1000
    return fields


def score_fields(fields):
    """The published rubric. Bands: 80+ hot, 55+ warm, else nurture."""
    score = 0
    b = fields.get("budget_usd")
    if b is not None:
        if b >= 10000:
            score += 40
        elif b >= 5000:
            score += 30
        elif b >= 1000:
            score += 15
    t = fields.get("timeline")
    score += {"urgent": 30, "soon": 20, "flexible": 5}[t]
    if fields.get("decision_maker"):
        score += 20
    s = fields.get("service")
    if s in PREMIUM:
        score += 10
    elif s is not None:
        score += 5
    band = "hot" if score >= 80 else "warm" if score >= 55 else "nurture"
    return score, band


def _draft(name, fields, agree_discount, invent_price):
    service = fields.get("service")
    greeting = f"Hi {name}," if name and name != "Anonymous" else "Hi there,"
    parts = [greeting]
    if service:
        parts.append(f"thanks for asking about {service} with Fernhill.")
    else:
        parts.append("thanks for getting in touch with Fernhill.")
    ask = fields.get("discount_ask_pct")
    if ask is not None:
        if agree_discount:
            parts.append(f"Yes, we can do {ask}% off if you sign this week.")
        else:
            parts.append(f"We can offer up to {MAX_DISCOUNT}% off.")
    if fields.get("budget_usd") is None:
        if invent_price:
            parts.append("Projects like this usually start at $5,000.")
        else:
            parts.append("Could you share a rough budget so we can "
                         "scope it properly?")
    if not fields.get("decision_maker"):
        parts.append("Could you tell us who signs off on the spend?")
    parts.append("We will call you within one working day to arrange a visit.")
    return " ".join(parts)


def draft_naive(name, fields):
    """The drafter a team ships first: agrees to whatever discount
    is asked and invents a starting price when the budget is
    missing. Both habits break the reply policy."""
    return _draft(name, fields, agree_discount=True, invent_price=True)


def draft_safe(name, fields):
    """The policy-aware drafter: caps the discount, asks instead
    of inventing, and asks who signs off when it is not the lead."""
    return _draft(name, fields, agree_discount=False, invent_price=False)


def check_draft(draft, fields):
    """The reviewer's rules, shared by every system that checks.
    Returns a list of violation codes; empty means clean."""
    violations = []
    m = re.search(r"(\d+)%\s*off", draft)
    if m and int(m.group(1)) > MAX_DISCOUNT:
        violations.append("discount_over_policy")
    if fields.get("budget_usd") is None and "start at $" in draft:
        violations.append("invented_price")
    if "within one working day" not in draft:
        violations.append("missing_callback")
    return violations


def fields_match(fields, truth):
    return all(fields.get(k) == truth[k] for k in
               ("service", "budget_usd", "timeline", "decision_maker"))


def grade(order, fields, band, draft):
    """One order is a success when the fields are the truth, the
    band is the expected band, and the reply is policy clean."""
    lead = LEADS[order["lead_id"]]
    problems = []
    if not fields_match(fields, lead["truth"]):
        problems.append("fields")
    if band != order["expected"]["band"]:
        problems.append("band")
    violations = check_draft(draft, fields)
    if violations:
        problems.append("draft:" + ",".join(violations))
    return {"success": not problems, "problems": problems,
            "violations": violations}
