# mas: the shared multi-agent library

Every lesson imports from this package, so the systems being compared across lessons are literally the same code.

- `tokens.py` is the course token approximation: a letter run costs ceil(length / 4), a digit run ceil(length / 3), and punctuation one token each. It is an approximation, stated as one wherever tokens are quoted.
- `core.py` holds the Message type (kind, sender, recipient, payload) with its serialized form and token cost, and the Ledger, which records messages, tokens, steps, and tokens by hop so coordination cost can be attributed, not just totalled.
- `domain.py` is the Fernhill lead domain: the two deterministic stand-in extractors (quick regex and careful), the two drafters (naive and policy-safe), the policy checker, the scoring rubric, and the grading rule.
- `systems.py` is the architectures: single agent, sequential pipeline (optionally reviewed), parallel batch with makespan accounting, hierarchy, debate, blackboard, orchestrated routing, and the capstone system with its optional hardening.
- `harness.py` summarizes runs: success rates, mean messages, tokens and steps, escapes, tokens per success, and family breakdowns.

The agents are deterministic stand-ins: rule-based workers whose behaviour is fully visible in these files. No lesson calls a live model, which is what makes every number in the course reproducible.
