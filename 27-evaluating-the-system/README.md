# Lesson 27: Evaluating the system: per-agent metrics and fault attribution

Time: ~40 min | Difficulty: Advanced | Prerequisites: Lesson 26

A multi-agent system that fails as a whole still needs its failures assigned, or every postmortem ends at 'the system was wrong'. This lesson builds the assignment instrument: three faults are injected one at a time (an extractor that drops budgets, a scorer with shifted thresholds, a drafter that adds a discount line to every reply), each run is compared against the healthy reference run stage by stage, and a trace-inspection rule blames the first stage whose output deviates. The rule's accuracy is measured on the new failures each fault causes, the failures that were not already there.

## Run it

```bash
python3 evaluation.py
```

## What the code measures

The extractor fault causes 7 new failures, the drafter fault 7, the scorer fault 2: 16 in all. The first-deviation rule attributes 16 of them correctly, an accuracy of 1.0. That perfect score deserves immediate suspicion, and the lesson supplies it: attribution is easy here precisely because stage outputs are typed, logged, and separable, so the first deviation really is the fault. The rule's known weakness is shared causes, as the exercise demonstrates, and its known precondition is Lesson 10's discipline: with prose handoffs and unlogged intermediate state there is nothing clean to compare, and attribution collapses into opinion. Per-agent evaluation is therefore not a reporting feature to bolt on; it is a property bought by the schema and ledger decisions made ten lessons earlier.

## Common failures

- Blaming the stage that surfaced the error. Drafts surface most failures; the first deviation, not the loudest symptom, is where the fault lives.
- Attributing pre-existing failures to the new fault. The accuracy here is measured only on failures the fault actually caused; everything else is noise dressed as signal.
- Trusting a perfect score. 1.0 on separable stand-ins means the instrument works on separable systems, not that production attribution is solved.

## Recap checklist

- [ ] You can state the attribution result: 16 of 16 new failures blamed correctly
- [ ] You know the first-deviation rule and its preconditions
- [ ] You can name the precondition this course bought in Lesson 10

## Resources

- [README.md](../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
