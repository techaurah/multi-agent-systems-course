# Lesson 07: Parallel fan-out: buying time with workers

Time: ~35 min | Difficulty: Intermediate | Prerequisites: Lesson 06

Lesson 04's graph said the only parallelism in this workload lives between orders. Fan-out collects it: orders are dealt round robin to a pool of pipeline workers, each worker running the full extract, score, draft chain for its own orders. Success cannot change, since each order gets the same processing as before. Tokens cannot change either: the same messages are sent, just from more desks. The one currency that moves is steps, read as the makespan, the busiest worker's step load, which is the deterministic stand-in for elapsed time.

The batch is the six independent orders, the family where fan-out is safe by construction, because no order's output feeds another's input.

## Run it

```bash
python3 parallel.py
```

## What the code measures

Run serially by the single agent, the batch takes 18 steps and 594 tokens. Dealt to three pipeline workers, the makespan is 6 steps, a speedup of 3.0 times, with all 6 orders still succeeding. The price is in the other ledger: the batch's tokens rise to 1434, 2.41 times the single agent's serial tokens, because each order now pays pipeline serialization. The sweep is the honest shape of parallelism: one worker 18 steps, two workers 9, three workers 6, six workers 3, while tokens and messages are identical in every row. Parallelism buys time at a fixed token premium; it never buys accuracy, and it never gets cheaper as the pool grows.

## Common failures

- Reporting speedup without the token premium. The 3.0 times makespan improvement and the 2.41 times token increase are one result, not two.
- Fanning out inside a chain. Dealing extract, score, and draft of one order to three workers does not parallelize the order; it runs the stages on stale inputs or serializes them anyway.
- Assuming the pool is free. Every worker here is a full pipeline with its own context; the course counts steps honestly but flags that real pools also pay in capacity, which Lesson 25 prices.

## Recap checklist

- [ ] You can state the fan-out trade: makespan 18 to 6 steps, tokens 594 to 1434
- [ ] You know tokens and messages are invariant across pool sizes
- [ ] You know fan-out is safe here because cross-order edges are zero

## Resources

- [README.md](../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
