# Lesson 06: The sequential pipeline: same failures, better addresses

Time: ~35 min | Difficulty: Intermediate | Prerequisites: Lesson 05

The sequential pipeline is the topology most teams build first: a coordinator hands each order to an extractor, whose fields go to a scorer, whose score goes to a drafter. It is also the topology Lesson 05 just watched lose on chained orders. This lesson runs it on the full order set and asks the fair question: across all three families, what does the pipeline actually change?

The answer is unfashionable and important. The pipeline changes where failures live, not how many there are. That relocation turns out to be worth something, but not what the sales version of multi-agent claims, and pricing it honestly is the point of running the numbers.

## Run it

```bash
python3 pipeline.py
```

## What the code measures

The pipeline succeeds on 7 of 12 orders, exactly the single agent's count, with exactly the same failed orders (true). It spends 233.5 mean tokens per order, 2.36 times the single agent's 99.0, and its cost per success is 400.3 tokens against the baseline's 169.7. What the pipeline adds is attribution: every failure can be assigned to the stage that produced it. The extractor owns 2 failures (order-04 and order-06, wrong fields), the scorer owns 2 (the bands those fields produce), and the drafter owns 4 (the policy violations). In the single agent those attributions exist only in principle; in the pipeline each stage's output crosses a boundary as a message, so it can be inspected, replayed, and, later in the course, checked. The pipeline is not an accuracy technology. It is an observability and intervention technology, and it should be bought as one.

## Common failures

- Expecting decomposition to create competence. Splitting one agent's work among four agents with the same rules yields the same answers; the rules are the competence.
- Counting stage failures as independent. The scorer's two failures are the extractor's two failures arriving downstream; Lesson 17 measures that inheritance directly.
- Judging the pipeline only on this lesson's table. Its payoff appears when a later lesson inserts a check at a boundary that the monolith does not have.

## Recap checklist

- [ ] You can state the pipeline's table: same successes, 2.36 times the tokens, full attribution
- [ ] You can assign each failed order to its stage
- [ ] You know the pipeline's real product is intervention points, not accuracy

## Resources

- [README.md](../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
