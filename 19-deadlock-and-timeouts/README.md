# Lesson 19: Deadlock and timeouts: the standstill nobody declares

Time: ~30 min | Difficulty: Intermediate | Prerequisites: Lesson 18

A loop at least announces itself in the message count. A deadlock is silent: two agents each waiting for the other's output, forever, with no messages at all. This lesson wires one on purpose: the scorer is configured to wait for the draft before scoring (a plausible misreading of 'score the reply'), and the drafter waits for the score before drafting. A round-based scheduler gives each agent its turn; an agent acts only when its input is ready. A watchdog that declares deadlock after a stated number of progress-free rounds is then raced against the same wiring with no watchdog at all, and a timeout fallback is priced: proceed with the partial information that does exist.

## Run it

```bash
python3 deadlock.py
```

## What the code measures

With a watchdog, the standstill is declared at exactly the watchdog's threshold: 3 rounds for a threshold of 3, 5 for 5, 10 for 10. Without a watchdog nothing ever declares it: the scheduler burns its entire 100 round budget and stops undiagnosed, completion false and deadlock never named (false). The timeout fallback, scoring from the fields alone when the wait expires, completes order-01 with the correct band (true), because the score never actually needed the draft; the dependency was a wiring fiction. Deadlock detection therefore has two separate products: a diagnosis (which cycle, which waits) and an escape (which dependency can be dropped without changing the answer), and a watchdog that only kills the run delivers neither.

## Common failures

- Treating silence as health. A deadlocked system produces no errors, no messages, and no output; monitoring that only watches for activity will call it idle.
- Setting the watchdog by feel. The threshold is the price of certainty about the standstill; state it in rounds and pay it knowingly.
- Killing without diagnosing. A restarted deadlock deadlocks again; the watchdog's report (who waits on whom) is the fixable artifact.

## Recap checklist

- [ ] You can state the watchdog arithmetic: declaration at exactly the threshold
- [ ] You know the unwatched run burns 100 rounds and names nothing
- [ ] You can separate diagnosis from escape in a deadlock response

## Resources

- [README.md](../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
