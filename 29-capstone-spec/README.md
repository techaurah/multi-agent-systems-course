# Lesson 29: Capstone spec: the system and its gates, fixed in advance

Time: ~40 min | Difficulty: Advanced | Prerequisites: Lesson 28

The capstone is a Fernhill lead-processing system built from the course's own parts: the orchestrator's router (Lesson 09), the sequential pipeline (Lesson 06), the reviewer at the exit (Lesson 21), and the ledger accounting of Lesson 02, graded against the reply policy and the expected answers in the fixtures. Before any capstone code is written, this lesson fixes the gates in `capstone/gates.json`, and this artifact prints them beside the baseline numbers they were set from, so any reader can audit that the gates were not reverse-engineered from the capstone's own results.

The gates are set from the evidence of the earlier lessons: the single agent's success rate and escape count (Lesson 03), and the cost table's range (Lesson 24). A gate the baseline already passes would be theatre; a gate no measured system approaches would be fantasy. These five are neither.

## Run it

```bash
python3 capstone_spec.py
```

## What the code measures

The gates: task success rate at least 0.9 (the baseline manages 0.5833); policy escapes at most 0 (the baseline ships 4); mean messages per order at most 8; tokens per success at most 400 (the baseline's 169.7 is cheaper, and the gate deliberately allows coordination to cost more per success than the monolith, but not without limit); and a success delta over the single agent of at least 0.15, so the system must actually beat the baseline it replaces, not merely exist beside it. The spec was fixed on the date recorded in the gates file, before Lesson 30's code. Lesson 31 will report the as-built verdict and the hardening against these exact numbers, unchanged.

## Common failures

- Setting gates after seeing results. A gate fitted to the outcome is a description wearing a gate's clothes; the fix is procedural (write it first, in a file, with a date), and this lesson is the procedure.
- Gating on means alone. The success gate and the escape gate are both fleet-level; the per-family breakdown is reported in Lesson 30 precisely so a strong family cannot carry a broken one through the gate.
- Allowing unlimited cost per success. The tokens-per-success gate is the course's thesis as a number: coordination must justify its price, in writing, in advance.

## Recap checklist

- [ ] You can recite the five gates and the baseline figure each was set against
- [ ] You know the gates file predates the capstone code, and how a reader verifies that
- [ ] You can explain the delta gate: the system must beat the baseline, not merely differ from it

## Resources

- [README.md](../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
