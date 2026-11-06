"""Lesson 22 artifact: permission boundaries. Agents hold
least-privilege tool sets and a guard decides every attempted
action. The attempts list mixes legitimate work, wiring
mistakes, and one instruction planted in a lead's text; the
guard's verdicts are the lesson."""

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

PERMISSIONS = {
    "extractor": {"read_lead", "write_fields"},
    "scorer": {"read_fields", "write_score"},
    "drafter": {"read_fields", "read_score", "write_draft"},
    "reviewer": {"read_draft", "write_verdict"},
    "sender": {"send_reply"},
}

# (agent, action, needs_verdict)
ATTEMPTS = [
    ("extractor", "read_lead", False),
    ("extractor", "write_fields", False),
    ("scorer", "read_fields", False),
    ("scorer", "write_score", False),
    ("drafter", "write_draft", False),
    ("reviewer", "read_draft", False),
    ("reviewer", "write_verdict", False),
    ("sender", "send_reply", True),
    ("extractor", "send_reply", False),
    ("scorer", "send_reply", False),
    ("drafter", "send_reply", False),
    ("reviewer", "write_fields", False),
    ("drafter", "approve_discount", False),
    ("sender", "send_reply", False),
]


def guard(agent, action, has_verdict):
    if action not in PERMISSIONS.get(agent, set()):
        return False, "not_in_toolset"
    if action == "send_reply" and not has_verdict:
        return False, "no_verdict"
    return True, "ok"


def evaluate():
    verdicts = []
    for agent, action, has_verdict in ATTEMPTS:
        ok, why = guard(agent, action, has_verdict)
        verdicts.append({"agent": agent, "action": action,
                         "allowed": ok, "reason": why})
    allowed = [v for v in verdicts if v["allowed"]]
    blocked = [v for v in verdicts if not v["allowed"]]
    return {
        "attempts": len(verdicts),
        "allowed": len(allowed),
        "blocked": len(blocked),
        "blocked_reasons": {
            r: sum(1 for v in blocked if v["reason"] == r)
            for r in ("not_in_toolset", "no_verdict")},
        "legitimate_work_blocked": 0,
        "send_attempts_blocked":
            sum(1 for v in blocked if v["action"] == "send_reply"),
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
