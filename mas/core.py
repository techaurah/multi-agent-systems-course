"""Core types for the course: messages and the coordination ledger.

Every system in this course is built from these two pieces. An
agent never calls another agent directly; it puts a Message on
the ledger, and the ledger is what makes coordination measurable:
messages, tokens, and steps are counted exactly once, here, so
every lesson's accounting agrees with every other lesson's.

The agents in this course are deterministic stand-ins: small
rule-based workers in the LeadPipe pattern, labelled as such
wherever their results are quoted. They stand in for LLM agents
so that coordination itself, not model behaviour, is what gets
measured.
"""

import json
from dataclasses import dataclass, field

from .tokens import approx_tokens

KINDS = ("task", "fields", "score", "draft", "verdict", "note",
         "question", "answer", "handoff", "error", "result")


@dataclass
class Message:
    sender: str
    recipient: str
    kind: str
    payload: dict = field(default_factory=dict)
    note: str = ""

    def text(self):
        """The serialized form: what a receiving agent would read."""
        head = f"[{self.kind}] {self.sender} -> {self.recipient}"
        body = json.dumps(self.payload, sort_keys=True)
        return head + "\n" + body + ("\n" + self.note if self.note else "")

    def tokens(self):
        return approx_tokens(self.text())


class Ledger:
    """Counts the three coordination currencies for one run."""

    def __init__(self):
        self.messages = []
        self.steps = 0

    def send(self, msg):
        self.messages.append(msg)
        return msg

    def step(self, n=1):
        self.steps += n

    @property
    def message_count(self):
        return len(self.messages)

    @property
    def token_count(self):
        return sum(m.tokens() for m in self.messages)

    def by_kind(self):
        out = {}
        for m in self.messages:
            out[m.kind] = out.get(m.kind, 0) + 1
        return out

    def tokens_by_hop(self):
        out = {}
        for m in self.messages:
            key = f"{m.sender}->{m.recipient}"
            out[key] = out.get(key, 0) + m.tokens()
        return out

    def stats(self):
        return {"messages": self.message_count,
                "tokens": self.token_count,
                "steps": self.steps}
