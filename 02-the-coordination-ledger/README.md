# Lesson 02: The coordination ledger: messages, tokens, and steps

Time: ~30 min | Difficulty: Beginner | Prerequisites: Lesson 01

Coordination cannot be designed until it can be counted. This course counts it in three currencies. Messages are the discrete handoffs: each one is a place where information can be lost, delayed, or checked. Tokens are what the messages cost, counted with the labelled approximation in `mas/tokens.py` over the serialized message, headers included, because headers are part of what a receiving agent reads. Steps are agent invocations, the course's deterministic stand-in for time: when agents run in parallel, the step count of a batch is the busiest agent's load, not the sum.

This lesson rebuilds one reviewed pipeline run by hand on the ledger in `mas/core.py`, so every message, its kind, and its token cost is visible, then applies the same accounting to all 12 orders.

## Run it

```bash
python3 ledger.py
```

## What the code measures

The traced run is order-05, the discount trap: 7 messages and 433 tokens in 7 steps. The message kinds tell the story of the trap: one task, one fields, one score, then two drafts and two verdicts, because the first draft agreed to a 25 percent discount and the reviewer sent it back. The token heavy hop is drafter to reviewer at 134 tokens (the full draft travels), while the verdicts cost 36 and 26 tokens: judgement is cheap to send, evidence is expensive. Across all 12 orders the reviewed pipeline averages 5.67 messages and 360.2 tokens per order against the single agent's 99.0; 72.5 percent of the reviewed pipeline's tokens are coordination overhead relative to the single agent doing the same work.

## Common failures

- Counting only the messages you designed. Retries, verdicts, and redrafts are messages too; the ledger counts what was sent, not what the diagram showed.
- Pricing tokens by payload alone. A message's header and structure are read by the receiving agent as surely as its body; the course counts the serialized whole.
- Adding steps across parallel agents. Steps measure elapsed work on the critical path; summing them double counts time that ran concurrently.

## Recap checklist

- [ ] You can name the three currencies and what each one is a stand-in for
- [ ] You can read order-05's ledger: 7 messages, the redraft loop visible in the kinds
- [ ] You know verdicts are cheap and evidence is expensive, from the hop table

## Resources

- [README.md](../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
