"""Lesson 18 artifact: the clarification loop. A requester
that cannot add a case id meets a specialist that cannot work
without one. Neither agent is broken alone; the conversation
is. Three termination designs are raced against the loop."""

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


def run_loop(cap, fix=None):
    """Returns (messages, completed). The requester's request
    never gains a case id unless fix is 'include_id'. The
    specialist asks for the id whenever it is missing. With
    fix 'detect_repeat', a supervisor closes the conversation
    when the same payload arrives a third time."""
    led = Ledger()
    seen = {}
    has_id = fix == "include_id"
    completed = False
    while led.message_count < cap:
        payload = {"want": "fields"}
        if has_id:
            payload["case_id"] = "order-01"
        led.send(Message("requester", "specialist", "task", payload))
        if has_id:
            completed = True
            led.send(Message("specialist", "requester", "fields",
                             {"case_id": "order-01", "fields": 4}))
            break
        led.send(Message("specialist", "requester", "question",
                         {"need": "case_id"}))
        key = str(sorted(payload.items()))
        seen[key] = seen.get(key, 0) + 1
        if fix == "detect_repeat" and seen[key] >= 3:
            led.send(Message("supervisor", "requester", "handoff",
                             {"action": "escalate_to_human"}))
            break
    return led.message_count, completed


def evaluate():
    out = {}
    for cap in (4, 10, 50):
        msgs, done = run_loop(cap)
        out[f"cap_{cap}"] = {"messages": msgs, "completed": done}
    msgs, done = run_loop(50, fix="detect_repeat")
    out["repeat_detection"] = {"messages": msgs, "completed": done,
                               "escalated": True}
    msgs, done = run_loop(50, fix="include_id")
    out["fixed_spec"] = {"messages": msgs, "completed": done}
    return out


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
