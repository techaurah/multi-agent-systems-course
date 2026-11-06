# Lesson 05: When multi-agent loses: the sequential race, run honestly

Time: ~30 min | Difficulty: Intermediate | Prerequisites: Lesson 04

This is the lesson the course is obliged to include and vendors are obliged to skip. On chained orders, where each job consumes the previous job's output and there is nothing to parallelize, the sequential pipeline does exactly the same work as the single agent, in the same order, with the same rules. Coordination cannot add information to a chain; it can only carry the same information at a higher price, across boundaries where it can be dropped. The published evidence points the same way: in Google's controlled scaling study (Kim et al., December 2025, cited in RESEARCH.md), every multi-agent variant degraded performance on sequential reasoning tasks by 39 to 70 percent. This lesson reproduces the small, honest version of that result on the course's own fixtures.

## Run it

```bash
python3 sequential_race.py
```

## What the code measures

On the chained family (order-04, order-05, order-09), the single agent and the pipeline succeed on exactly 1 of 3 orders each, and the failure sets are identical (true): order-04 defeats both, order-09 passes both, order-05's draft violates policy in both. The price is not identical. The single agent averages 105.7 tokens per order; the pipeline averages 236.3, 2.24 times as much, plus 3.0 messages per order the single agent never sends. Cost per success: 317.0 tokens against 709.0. On chained work the pipeline is the single agent with a coordination surcharge, and the surcharge buys nothing measurable. Any honest case for multi-agent has to be made on the other families, and it will be, in Lessons 07 and 21; but it cannot be made here.

## Common failures

- Averaging this result away. Reporting the pipeline's score across all 12 orders hides the fact that on this family it is strictly dominated: same successes, more cost.
- Blaming the pipeline's implementation. The loss is structural: serialization and re-reading at boundaries cost tokens whether or not the code is elegant.
- Concluding multi-agent never helps. The chained family is the worst case by construction; the error is generalizing from it in either direction.

## Recap checklist

- [ ] You can state the chained result without flinching: equal successes, 2.24 times the tokens
- [ ] You know the loss is structural, not an implementation bug
- [ ] You can connect it to the published sequential-task penalty in RESEARCH.md

## Resources

- [README.md](../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
