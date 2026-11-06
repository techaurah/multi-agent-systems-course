# Lesson 17: Cascading errors: one fault, every stage, and the checkpoint

Time: ~40 min | Difficulty: Advanced | Prerequisites: Lesson 16

Error amplification is the multi-agent failure with a published multiplier: in Google's scaling study (Kim et al., December 2025), independent agents amplified errors 17.2 times over a single agent through unchecked propagation, while centralized coordination with validation checkpoints contained the same effect to 4.4 times. This lesson reproduces the mechanism at bench scale. One fault is injected at the extractor: it drops every budget it reads. The fault is then counted at each downstream stage, in the single agent, in the pipeline, and in a pipeline whose scorer refuses a budget-free extraction when the text visibly carries a figure, sending it back for the careful reading: a checkpoint.

## Run it

```bash
python3 cascade.py
```

## What the code measures

The healthy pipeline succeeds on 7 of 12. With the fault injected, the single agent succeeds on 0 and the pipeline on 0: total collapse in both. The mechanism is worth tracing once. Drop the budget and the fields are wrong on every order that had one; the bands computed from those fields are wrong; and the naive drafter, seeing no budget, invents a starting price on every draft, so a single upstream fault manufactures a second, unrelated violation type downstream. That is amplification, not mere propagation. The checkpoint recovers 9 orders and lifts successes to 11. Its one failure is instructive: order-04, whose budget is written in words, carries no dollar sign, so the checkpoint's trigger never fires. A checkpoint only catches the failures its trigger can see.

## Common failures

- Counting a cascade as many independent errors. The dashboard shows fields, bands, and drafts all failing; the fault count is one, and fixing it fixes all three rows.
- Placing checkpoints by intuition. The checkpoint sits where the fault becomes visible (a missing budget beside a visible figure), which is an observable contradiction, not a hunch.
- Trusting the trigger. The checkpoint's blind spot is a whole representation (words instead of digits); every trigger has one, and naming it is part of placing the check.

## Recap checklist

- [ ] You can state the collapse: healthy 7, faulty 0, checkpoint 11
- [ ] You can explain how one fault manufactured a second violation type downstream
- [ ] You can name the checkpoint's blind spot and the order that proves it

## Resources

- [README.md](../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
