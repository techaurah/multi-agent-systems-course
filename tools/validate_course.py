#!/usr/bin/env python3
"""Validate the multi-agent systems course structure.

Checks:
- the 32 numbered lesson folders exist, each with README.md,
  exercise.md, smoke_test.py, solution/SOLUTION.md and at least one
  runnable Python artifact
- every lesson README has the standard sections and no em dash
- no em dash characters anywhere in the course markdown
- fixtures/leads.json and fixtures/orders.json parse; every lead has
  a truth record with service, budget_usd, timeline, decision_maker
- fixtures/orders.json expected scores and bands recompute from the
  truth records with the course rubric (mas/domain.py)
- the capstone gates file exists and carries the five gate keys
- root documents (README, RESEARCH, DESIGN, PROGRESS, llms.txt)
  exist and are non-trivial

Run from the repo root: python3 tools/validate_course.py
Exit code 0 means the structure is valid.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from mas.domain import score_fields  # noqa: E402

LESSON_DIRS = [
    "00-course-setup", "01-what-makes-it-multi-agent",
    "02-the-coordination-ledger", "03-the-single-agent-baseline",
    "04-decomposition", "05-when-multi-agent-loses",
    "06-sequential-pipeline", "07-parallel-fan-out",
    "08-hierarchical-teams", "09-routing-and-orchestration",
    "10-message-schemas", "11-handoffs-and-state",
    "12-the-blackboard", "13-debate-and-voting",
    "14-shared-memory", "15-private-vs-shared-context",
    "16-history-and-loss", "17-cascading-errors",
    "18-loops", "19-deadlock-and-timeouts",
    "20-conflicting-outputs", "21-the-reviewer",
    "22-permission-boundaries", "23-termination-and-budgets",
    "24-coordination-cost-accounting", "25-scaling-the-team",
    "26-choosing-a-topology", "27-evaluating-the-system",
    "28-failure-taxonomy", "29-capstone-spec",
    "30-build-the-capstone", "31-evaluate-and-harden",
]

REQUIRED_LESSON_FILES = ["README.md", "exercise.md", "smoke_test.py"]
REQUIRED_SECTIONS = ["## Run it", "## What the code measures",
                     "## Common failures", "## Recap checklist",
                     "## Resources"]
GATE_KEYS = ["task_success_rate_min", "policy_escapes_max",
             "mean_messages_per_order_max", "tokens_per_success_max",
             "success_delta_vs_single_min"]
EM_DASH = "\u2014"

problems = []


def check(cond, message):
    if not cond:
        problems.append(message)


for name in LESSON_DIRS:
    folder = ROOT / name
    check(folder.is_dir(), f"missing lesson folder: {name}")
    if not folder.is_dir():
        continue
    for required in REQUIRED_LESSON_FILES:
        check((folder / required).is_file(), f"{name}: missing {required}")
    check((folder / "solution" / "SOLUTION.md").is_file(),
          f"{name}: missing solution/SOLUTION.md")
    artifacts = [p for p in folder.glob("*.py") if p.name != "smoke_test.py"]
    check(len(artifacts) >= 1, f"{name}: no runnable artifact")
    readme = folder / "README.md"
    if readme.is_file():
        text = readme.read_text(encoding="utf-8")
        for section in REQUIRED_SECTIONS:
            check(section in text, f"{name}: README missing '{section}'")
        check(len(text) > 800, f"{name}: README suspiciously short")

for md in ROOT.rglob("*.md"):
    if ".git" in md.parts:
        continue
    check(EM_DASH not in md.read_text(encoding="utf-8"),
          f"em dash found in {md.relative_to(ROOT)}")

# Fixtures ---------------------------------------------------------------
leads_path = ROOT / "fixtures" / "leads.json"
policy_path = ROOT / "fixtures" / "policy.json"
check(leads_path.is_file(), "fixtures/leads.json missing")
check(policy_path.is_file(), "fixtures/policy.json missing")
leads = {}
policy = None
if leads_path.is_file() and policy_path.is_file():
    raw_leads = json.loads(leads_path.read_text(encoding="utf-8"))
    leads = {lead["id"]: lead for lead in raw_leads}
    policy = json.loads(policy_path.read_text(encoding="utf-8"))
    check(len(leads) == 12, "fixtures: expected 12 leads")
    for lead in raw_leads:
        for key in ("service", "budget_usd", "timeline", "decision_maker"):
            check(key in lead["truth"], f"lead {lead['id']}: truth missing {key}")

orders_path = ROOT / "fixtures" / "orders.json"
if orders_path.is_file() and policy is not None:
    orders = json.loads(orders_path.read_text(encoding="utf-8"))
    check(len(orders) == 12, "fixtures: expected 12 orders")
    for order in orders:
        check(order["lead_id"] in leads,
              f"{order['id']}: unknown lead {order['lead_id']}")
        lead = leads[order["lead_id"]]
        score, band = score_fields(lead["truth"])
        check(score == order["expected"]["score"],
              f"{order['id']}: expected score {order['expected']['score']} "
              f"but rubric gives {score}")
        check(band == order["expected"]["band"],
              f"{order['id']}: expected band {order['expected']['band']} "
              f"but rubric gives {band}")

# Capstone gates -----------------------------------------------------------
gates_path = (ROOT / "29-capstone-spec" / "capstone" / "gates.json")
check(gates_path.is_file(), "capstone gates file missing")
if gates_path.is_file():
    gates = json.loads(gates_path.read_text(encoding="utf-8"))
    check("capstone_system" in gates, "gates: missing capstone_system key")
    gate_values = gates.get("capstone_system", {}).get("gates", {})
    for key in GATE_KEYS:
        check(isinstance(gate_values.get(key), (int, float)),
              f"gates: {key} missing or not numeric")

for doc in ("README.md", "RESEARCH.md", "DESIGN.md", "PROGRESS.md",
            "llms.txt", "AGENTS.md", "CHANGELOG.md"):
    path = ROOT / doc
    check(path.is_file() and len(path.read_text(encoding="utf-8")) > 200
          if path.is_file() else False, f"root doc missing or too short: {doc}")

if problems:
    print("VALIDATION FAILED")
    for problem in problems:
        print(" -", problem)
    sys.exit(1)
print(f"course structure OK: {len(LESSON_DIRS)} lessons, fixtures and "
      "gates verified")
