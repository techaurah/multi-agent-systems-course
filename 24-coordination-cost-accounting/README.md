# Lesson 24: Coordination cost accounting: the full table, read properly

Time: ~40 min | Difficulty: Advanced | Prerequisites: Lesson 23

This lesson is Module 7's ledger closed: six systems, all twelve orders, one accounting, ranked by cost per success rather than by applause. Cost per success is the only honest denominator in this course, because it refuses to let a system look cheap by failing cheaply or look good by succeeding expensively without saying so. The blackboard's row carries Lesson 12's caveat into the table: its messages price pointers, not board content, so its token row flatters it and the lesson says so in the same breath as the number.

## Run it

```bash
python3 cost_accounting.py
```

## What the code measures

The table, successes first: debate 12 of 12 at 389.2 tokens per success; blackboard 10 at 86.7 (pointer-priced, caveat attached); orchestrated 10 at 362.9; reviewed pipeline 10 at 432.3; single agent 7 at 169.7; plain pipeline 7 at 400.3, the worst row in the book, since it pays coordination prices for the baseline's exact results. Three readings matter. First, the cheapest system per success (the single agent) and the most successful system (debate) are different systems, and choosing between them is a business decision about what a success is worth, not a technical ranking. Second, the reviewed pipeline is dominated by its own routed child: orchestration delivers the same successes for fewer tokens, purely by not reviewing clean orders. Third, escapes split the table as cleanly as cost does: every system with a check at the exit has 0, and every system without one has 4.

## Common failures

- Ranking by mean tokens per order. That ranking crowns systems that fail cheap; cost per success is the ranking that survives contact with a budget review.
- Quoting the blackboard's row without its caveat. Pointer pricing is an accounting choice, and hiding it converts a modelling decision into a false result.
- Reading the table as a league. These systems differ in what they guarantee (escapes, attribution, routing) as well as what they cost; the table informs the choice, it does not make it.

## Recap checklist

- [ ] You can reproduce the six-row table from the artifact
- [ ] You know the plain pipeline is the worst row and why
- [ ] You can state the two business questions the table cannot answer for you

## Resources

- [README.md](../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
