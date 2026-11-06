# Lesson 23: Termination and budgets: finish lines that are not finish lines

Time: ~35 min | Difficulty: Intermediate | Prerequisites: Lesson 22

Budgets are how systems promise not to run forever, and they fail in two opposite ways, both measured here. A reviewed pipeline order needs five steps when its draft is clean and seven when the reviewer sends it back. Run the fleet under a step budget below the need and orders die unfinished. Run it with a sender who treats the budget as the finish line, sending whatever exists when the steps run out, and orders ship unchecked. MAST counts premature termination at 6.2 percent of failures; this lesson shows the mechanism, and why 'the run ended' is not evidence that 'the work completed'.

## Run it

```bash
python3 budgets.py
```

## What the code measures

Steps needed across the fleet run from 5 to 7: eight orders need five, and the four redraft orders (order-04, order-05, order-07, order-12) need seven. A budget of 4 finishes 0 of the twelve orders; a budget of 5 finishes 8, stranding exactly the four orders that needed the reviewer most; a budget of 7 finishes 12. The other failure style is worse: a sender who ships at step 3, before any verdict, sends drafts carrying 4 policy violations, the full unreviewed escape count from Lesson 21. So the budget question is never just 'how many steps may a run take'. It is 'what state may an order be in when the steps run out', and the only defensible answers are 'finished and checked' or 'stopped and flagged'. 'Shipped anyway' is the third answer, and it is the one that reaches customers.

## Common failures

- Sizing the budget to the average order. The mean need here is under six steps and a budget of five still strands a third of the fleet, because budgets bind at the tail, not the mean.
- Letting the budget decide what ships. Exhaustion is a stop signal for the system, never a send signal for the order.
- Forgetting that redrafts are variable cost. The orders that need the most steps are the ones with violations; a tight budget selectively amputates the safety process.

## Recap checklist

- [ ] You can state the step needs: 5 clean, 7 with a redraft, and the budget table 4, 5, 7 against them
- [ ] You know a budget of 5 strands exactly the trap orders
- [ ] You can name the three legal states at budget exhaustion

## Resources

- [README.md](../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
