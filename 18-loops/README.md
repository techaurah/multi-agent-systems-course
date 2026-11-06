# Lesson 18: Loops: the conversation that never finishes

Time: ~30 min | Difficulty: Intermediate | Prerequisites: Lesson 17

Step repetition is the single most frequent failure mode in MAST's 1,642 traces, at 15.7 percent of failures (Cemri et al., 2025). Its minimal form needs two agents and one missing field. A requester asks a specialist for an order's fields; the specialist cannot work without a case id and asks for one; the requester's specification has no way to add the id, so it repeats its original request. Neither agent is malfunctioning. The conversation is.

This lesson runs that loop under three termination designs: a bare message cap, a supervisor that detects the repeated payload and escalates, and the specification fix, giving the requester the ability to include the id.

## Run it

```bash
python3 loops.py
```

## What the code measures

Under bare caps the loop consumes the entire budget without completing: 4 messages at a cap of 4, 10 at 10, 50 at 50, completion false in every row. A cap is not a termination condition; it is a decision to fail later at a higher price. Repeat detection does better on cost: the supervisor sees the same payload a third time and escalates at 7 messages, still without completing the work, because detection can stop a loop but cannot supply the missing field. Only the specification fix completes: 2 messages, task done, because the requester can finally say what the specialist needs. The three rows are the course's termination doctrine in miniature: caps bound the damage, detection names it, and only fixing the interface ends it.

## Common failures

- Raising the cap to give the loop 'more room'. The loop's appetite is unbounded by construction; room is what it eats.
- Retrying with backoff as a loop strategy. Backoff changes the loop's period, not its logic; the fiftieth retry carries the same missing field as the first.
- Counting escalation as success. The escalated conversation still delivered no fields; report completion and escalation as different outcomes, because they are.

## Recap checklist

- [ ] You can price the three designs: cap 50 messages and no completion, detection 7 and escalation, fix 2 and done
- [ ] You know a cap is a budget, not a termination condition
- [ ] You can connect step repetition to its MAST frequency from RESEARCH.md

## Resources

- [README.md](../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
