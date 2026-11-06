# Lesson 00: Course setup: what you need, and how this course works

Time: ~20 min | Difficulty: Beginner | Prerequisites: None

This course teaches multi-agent systems by measuring them. Every claim it makes about topologies, handoffs, reviewers, or cost is the output of code in the lesson, run on the fixtures bundled in this repository, with small deterministic rule-based workers standing in for LLM agents. The workers are stand-ins, labelled as such wherever their results are quoted: what is being measured is coordination itself, the messages, the tokens, the failure paths, not model behaviour. If a fashionable topology measures badly here, the lesson prints the bad number and explains it. There are no borrowed benchmarks presented as the course's own, and no certificate at the end.

Everything runs offline on the Python standard library. The shared instruments live in `mas/` (a message and ledger core, the work domain, the systems under comparison, and the measurement harness) and the data lives in `fixtures/` (12 leads to a fictional garden services business, 12 work orders over them, and the reply policy they are graded against). This lesson verifies your environment and counts the instruments, so later surprises are about ideas, not setup.

## Run it

```bash
python3 check_environment.py
```

## What the code measures

The check confirms Python 3.11 or newer and counts the fixtures: 12 leads, 12 orders, 5 services in the policy, and a maximum permitted discount of 10 percent. The orders split by shape into 6 independent, 3 chained, and 3 ambiguous, and by expected band into 5 hot, 4 warm, and 3 nurture. Those three shapes are the course's test track: nearly every system you build will be raced over all three.

## Common failures

- Running a lesson's code from the repository root instead of its own folder. Each artifact finds the repo root by walking up from its own file, so it works from anywhere, but the smoke tests expect to run from the lesson folder.
- Expecting to install something. There is nothing to install; if you reach for pip, you have taken a wrong turn.
- Treating the stand-in workers as models. They are deterministic rules (see `mas/README.md`); lessons compare coordination designs with them, never model behaviour.

## Recap checklist

- [ ] `python3 check_environment.py` runs and prints leads: 12 and orders: 12
- [ ] You can name the three order families and what makes each one different
- [ ] You know the course rule: every number comes from running the code

## Resources

- [README.md](../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
