# Lesson 22: Permission boundaries: least privilege between agents

Time: ~35 min | Difficulty: Intermediate | Prerequisites: Lesson 21

Every agent in the course so far could, in principle, do anything: the pipeline's discipline was conventional, not enforced. This lesson replaces convention with a guard. Each agent holds a least-privilege tool set (the extractor may read leads and write fields, the sender may only send, and sending additionally requires a reviewer verdict), and every attempted action is decided by the guard, with the reason recorded. The attempts list is deliberately mixed: the eight actions the work actually needs, three agents attempting to send replies themselves, a reviewer attempting to write fields, a drafter attempting to approve a discount (the instruction planted in order-05's lead text, arriving as an action), and a sender attempting to send with no verdict on record.

## Run it

```bash
python3 permissions.py
```

## What the code measures

Of 14 attempts, 8 are allowed and 6 blocked: 5 because the action is not in the agent's tool set, and 1 because a send lacked its verdict. Send attempts blocked: 4 of the five sends attempted, with the single legitimate send (sender, with verdict) allowed through. Legitimate work blocked: 0. That zero is the design target and the honest caveat in one number: least privilege is only free when the permission matrix was drawn from the real workflow, as this one was. A matrix drawn from imagination either blocks the work (and gets bypassed by frustrated builders) or allows everything (and guards nothing). The planted instruction deserves a final word: it never reached the guard as an argument at all, because the only agent who reads raw lead text, the extractor, holds no send or approve action. Architecture decided that fight before policy was consulted.

## Common failures

- Granting tools by seniority. The coordinator's seniority does not need a send tool; need is per action, not per rank.
- Writing the matrix from the org chart instead of the trace. The eight allowed actions here are exactly the actions the measured runs perform; anything else is speculation with a blast radius.
- Letting the verdict be implied. The sender's no-verdict attempt is the most realistic row in the table: under time pressure, 'the reviewer basically approved it' is how unreviewed output ships.

## Recap checklist

- [ ] You can state the guard's table: 14 attempts, 8 allowed, 6 blocked, 0 legitimate blocked
- [ ] You know sending is a two-key action: tool set plus verdict
- [ ] You can explain how the planted instruction died of architecture, not policy

## Resources

- [README.md](../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
