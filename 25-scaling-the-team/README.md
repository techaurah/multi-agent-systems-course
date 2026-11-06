# Lesson 25: Scaling the team: where the curve bends

Time: ~35 min | Difficulty: Advanced | Prerequisites: Lesson 24

If some workers are good, the scaling question asks whether more are better, and demands the curve instead of the slogan. The batch of six independent orders is dealt to pools of one to twelve workers, and three things are watched: the makespan, the tokens, and the successes. Google's scaling study found coordination gains plateauing beyond roughly four agents on its workloads (Kim et al., December 2025, in RESEARCH.md); this lesson finds the local version of that plateau and names its actual cause, which is not coordination overhead in the abstract but the arithmetic of the deal: somebody always holds the largest pile.

## Run it

```bash
python3 scaling.py
```

## What the code measures

Makespan by pool size: one worker 18 steps, two 9, three 6, four 6, six 3, twelve 3. Speedups against one worker: 2.0 times at two, 3.0 at three, still 3.0 at four, 6.0 at six, and 6.0 at twelve. The plateau between three and four workers is the deal from Lesson 07's exercise: with six orders, four workers still leave two workers holding two orders each. The second plateau, from six to twelve, is harder: six orders cannot occupy twelve workers, so half the pool is decoration. Tokens, meanwhile, do not move at all (true): 1434 at every pool size, because pool size changes who waits, never what is sent. Successes are 6 in every row. The whole economics of team size is in this table: time is bought in deal-shaped steps, cost is flat, quality is flat, and beyond the batch's natural width the only thing that scales is the roster.

## Common failures

- Reading the roster as the capacity. Twelve workers processed six orders; the capacity was six workers and the rest was payroll.
- Extrapolating the early slope. The 1 to 3 worker slope is perfect and meaningless; the curve's information lives in its plateaus.
- Expecting tokens to reward scale. Coordination cost here is per order, not per worker, so growth is free in tokens and expensive only in idle capacity; other designs invert that, and Lesson 12's broadcast is one.

## Recap checklist

- [ ] You can draw the curve: 18, 9, 6, 6, 3, 3 steps against pool size
- [ ] You can explain both plateaus from the deal
- [ ] You know tokens and successes are flat across the whole sweep

## Resources

- [README.md](../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
