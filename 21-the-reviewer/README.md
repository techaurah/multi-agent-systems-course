# Lesson 21: The reviewer: a verification bottleneck, priced, with its blind spot

Time: ~40 min | Difficulty: Advanced | Prerequisites: Lesson 20

MAST's most actionable finding is that verification is the neglected category: roughly a quarter of annotated multi-agent failures are verification failures, and adding a verification step was the strongest single intervention the study measured (Cemri et al., 2025, in RESEARCH.md). Google's scaling study lands in the same place from the other direction: centralized coordination contains error amplification largely through validation bottlenecks. This lesson builds the bottleneck: a reviewer agent at the exit who reads every draft, checks it against the reply policy, and sends violations back for one safe redraft. Its catches, its cost, and the class of error it structurally cannot see are all measured.

## Run it

```bash
python3 reviewer.py
```

## What the code measures

Without the reviewer, 4 policy violations sit in drafts that would be sent. With it, 0: every violation is caught, 4 redrafts are triggered, and successes rise from 7 to 10 of 12. The price is 2.67 extra messages and 126.7 extra mean tokens per order, paid on all twelve orders to protect the four that needed it (Lesson 09's router exists to stop paying it on the other eight). The blind spot is stated in the same output: the orders still failing with the reviewer are order-04, order-06, wrong bands built on wrong fields, and the reviewer waves them through because it reads drafts, not facts. A verification layer verifies what it reads. Exit checking is necessary and insufficient, and the capstone will need a second kind of check, aimed at the fields, for exactly this reason.

## Common failures

- Reviewing outputs against vibes. The reviewer's rules are the policy file's rules, checkable and counted; a reviewer that 'looks for problems' catches what it happens to notice.
- Assuming the exit check covers the system. It covers the exit. Field errors with clean drafts are invisible to it, by construction.
- Paying for review uniformly without measuring the catch rate per route. Four of twelve orders used the reviewer here; the other eight bought insurance they did not claim on.

## Recap checklist

- [ ] You can state the reviewer's ledger: escapes 4 to 0, successes 7 to 10, cost 126.7 mean tokens
- [ ] You can name the blind spot and the two orders that prove it
- [ ] You can connect the bottleneck to the MAST and scaling-study findings in RESEARCH.md

## Resources

- [README.md](../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
