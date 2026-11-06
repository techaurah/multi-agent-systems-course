# Lesson 26: Choosing a topology: the decision table, computed

Time: ~35 min | Difficulty: Advanced | Prerequisites: Lesson 25

Every lesson so far has been evidence; this one is the verdict form. Four systems (single agent, pipeline, reviewed pipeline, orchestrated) are scored per family, and the recommendation for each family is computed by a stated rule: best success rate first, then cheapest cost per success. The rule is printed because a decision table whose rule is hidden is an opinion with formatting. The families are the course's three workload shapes, and the point of the exercise is that they do not get the same answer, which is the entire thesis of the course compressed into three rows.

## Run it

```bash
python3 decision.py
```

## What the code measures

Independent orders: the single agent wins, 6 of 6 successes at 99.0 tokens per success, because nothing about these orders needs coordination and every coordinated system pays more for the same six successes. Chained orders: orchestrated wins, 2 of 3 at 555.0 tokens per success, beating the reviewed pipeline's identical successes at 602.5 by routing review only where traps live. Ambiguous orders: orchestrated again, 2 of 3, where the single agent and the plain pipeline both score zero (their failures, order-06, order-07, and order-12, are the fixture set's hardest). The table's honest footnotes: orchestrated still fails order-06 in both its families, because routing cannot fix a misread field, and the capstone will need the field check for that; and on independent orders the recommendation is genuinely to not build the multi-agent system, a result this course prints in the same typeface as all the others.

## Common failures

- Averaging the families into one recommendation. The overall winner (orchestrated, on successes) is the wrong choice for the independent majority of the workload; family mix is a design input.
- Hiding the decision rule. 'Best success, then cheapest' is one defensible rule; a shop that prices latency would write a different one and should say so.
- Treating the table as portable. It is computed on these fixtures with these workers; another workload re-runs the artifact, it does not inherit the answer.

## Recap checklist

- [ ] You can state the three picks: independent to single, chained and ambiguous to orchestrated
- [ ] You can defend each pick with its two numbers
- [ ] You know the table's rule and its two honest footnotes

## Resources

- [README.md](../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
