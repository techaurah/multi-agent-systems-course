# Lesson 08: Hierarchical teams: the manager tax, measured

Time: ~35 min | Difficulty: Intermediate | Prerequisites: Lesson 07

Hierarchy is the topology organisations reach for because it looks like an org chart: a manager deals work to team leads, who deal it to workers. Its genuine purpose is span of control: when there are more workers than one coordinator can brief, monitor, and merge, intermediate managers keep each brief small. The question is never whether hierarchy works, but whether the workload is big enough to need it. On twelve orders with four workers, it is not, and this lesson prices the difference.

The comparison is a two-level hierarchy (manager, two team leads, four workers) against a flat pool of the same four workers running the same pipeline stages.

## Run it

```bash
python3 hierarchy.py
```

## What the code measures

Both designs succeed on 7 of 12 orders; hierarchy changes no outcome. It changes the ledger. The hierarchy sends 60 messages against the flat pool's 36: 24 delegation messages that exist only to move orders down the tree. Tokens rise from 2802 to 3594, an overhead of 28.3 percent, and the makespan worsens from 9 to 11 steps because every path pays two delegation steps before work begins. The manager personally sends 12 messages and does no extraction, scoring, or drafting at all. None of this says hierarchy is wrong; it says hierarchy is a capacity technology bought with a per-order tax, and at four workers the tax purchases a span of control nobody was straining. Frameworks that default to a manager layer (CrewAI's hierarchical process is the well known example, checked 2026-11-06 in RESEARCH.md) are making this purchase on your behalf; this lesson teaches you to read its price tag.

## Common failures

- Adding a manager to fix a quality problem. The hierarchy's successes are identical to the flat pool's; management layers route work, they do not improve it.
- Counting only the manager's messages. The team leads' delegation messages are hierarchy's cost too; the full 24 are the tax.
- Removing hierarchy where it is needed. At hundreds of workers a flat coordinator becomes the bottleneck and the failure mode changes; the lesson's point is to size the tax to the workload, not to ban the pattern.

## Recap checklist

- [ ] You can price the manager tax on 12 orders: 24 messages, 28.3 percent more tokens, 2 extra steps
- [ ] You know hierarchy buys span of control, not quality
- [ ] You can name the condition under which the tax becomes worth paying

## Resources

- [README.md](../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
