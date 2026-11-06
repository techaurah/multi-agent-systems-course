# Lesson 14: Shared memory: the stale read and the version check

Time: ~35 min | Difficulty: Intermediate | Prerequisites: Lesson 13

Shared memory promises that agents coordinate by reading the same facts. Its characteristic failure is quieter: an agent reads the right row at the wrong time. This lesson builds a versioned store of extracted fields. The extractor writes version 1 for every order. A verifier then upgrades the four thin orders (the traps from Lesson 09's routing table) to version 2 with careful fields. Two scorer schedules are raced: one that reads the thin orders before the upgrade lands, and one that refuses to score a thin order below version 2.

No agent in this lesson makes an error. The stale scorer applies the rubric perfectly to the fields it read. The failure is purely temporal, which is exactly why it survives code review and reaches production.

## Run it

```bash
python3 shared_memory.py
```

## What the code measures

The stale schedule scores 10 of 12 bands correctly; the version-checked schedule scores 12. The stale scorer read version 1 for every thin order (order-04, order-06, order-07, order-12), and two of those reads cost bands: order-04 and order-06 again, the same pair that has now failed through a format (Lesson 10), a summary (Lesson 11), and a schedule. The other two thin orders survive their stale reads because their version 1 fields happen to carry the same band as version 2, a reminder that stale reads are probabilistic damage: the mechanism is broken even on the days it does not fire. The fix costs one integer per row and one comparison per read, which is the cheapest correctness in the course so far.

## Common failures

- Treating shared memory as coordination. A store is state, not agreement; without versions or ordering, readers cannot know which truth they hold.
- Blaming the stale reader. It read a real version of the row and scored it correctly; the system's schedule was the bug.
- Upgrading silently. The verifier's write is a coordination event other agents depend on; if it is not visible in versions or messages, it did not happen.

## Recap checklist

- [ ] You can state the two schedules: 10 against 12 correct bands
- [ ] You know the failure is temporal, not computational
- [ ] You can explain why version 1 reads on order-07 and order-12 did no damage

## Resources

- [README.md](../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
