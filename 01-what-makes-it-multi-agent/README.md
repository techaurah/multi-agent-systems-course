# Lesson 01: What makes it multi-agent: one agent, or many, doing the same work

Time: ~25 min | Difficulty: Beginner | Prerequisites: Lesson 00

A multi-agent system is not a bigger prompt or a longer chain of thought. It is a system where more than one agent, each with its own context, does part of the work, and something has to move information between them. That movement is the whole subject of this course: it costs tokens, it loses information, it creates places where errors can be caught or amplified, and sometimes it buys parallelism or specialisation worth paying for.

This lesson runs one order twice: once through the single agent of `mas/systems.py`, which extracts, scores, and drafts in one pass inside one context, and once through a four-agent pipeline (coordinator, extractor, scorer, drafter) doing exactly the same jobs with exactly the same rules. The outputs are compared field by field, and the ledgers are compared currency by currency.

## Run it

```bash
python3 one_vs_many.py
```

## What the code measures

On order-01 both systems succeed, produce the same band, and produce the same draft, word for word. The difference is entirely in the coordination ledger: the single agent sends 0 messages and spends 106 tokens (the lead text it reads plus the reply it writes), while the pipeline sends 3 messages and spends 251 tokens for the identical result. Nothing went wrong; the extra 145 tokens are the price of serialization, headers, and re-reading at every boundary. Keep that number in mind: it is the baseline tax every topology in this course has to earn its way out of.

## Common failures

- Defining multi-agent by counting model calls. One agent calling itself in a loop is still one context; the defining feature is separate contexts plus a coordination mechanism between them.
- Assuming different outputs mean different systems. Here the outputs are identical; the systems differ in cost, failure surface, and where a check could be inserted, and those differences are the design space.
- Forgetting the coordinator. The pipeline has four agents, not three: someone owns the order, and that ownership is itself a design decision later lessons price.

## Recap checklist

- [ ] You can define a multi-agent system by contexts and coordination, not by model calls
- [ ] You can state the coordination tax on order-01: 145 extra tokens for an identical result
- [ ] You know the three coordination currencies this course counts: messages, tokens, steps

## Resources

- [README.md](../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
