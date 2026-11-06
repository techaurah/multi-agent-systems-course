# Lesson 28: Failure taxonomy in practice: the course profile against the field

Time: ~35 min | Difficulty: Advanced | Prerequisites: Lesson 27

MAST, the failure taxonomy built from 1,642 annotated traces (Cemri et al., 2025), sorts multi-agent failures into three categories: specification and system design, inter-agent misalignment, and task verification. This lesson turns the taxonomy inward. Every failure the course has reproduced, the failed orders of three reference systems, the band changes caused by summary handoffs, the clarification loop, and the deadlock, is classified into the same three categories, under a stated rule: a failure is classified by what reached the output, so a draft violation that shipped is a verification failure even when its root cause sat upstream. The course's profile is then set beside the field's, and the differences are explained rather than smoothed over.

## Run it

```bash
python3 taxonomy.py
```

## What the code measures

The course reproduces 20 classifiable failure instances: specification and system design 6 (share 0.3), inter-agent misalignment 6 (share 0.3), and task verification 8 (share 0.4). The field's profile from MAST, computed by summing the paper's per-mode figures as reported in RESEARCH.md, is roughly 44 percent specification, 32 percent misalignment, 24 percent verification. The course is verification-heavy by construction: its fixture set is trap-rich, with four of twelve orders carrying a policy trap, so exit failures are over-represented against field data drawn from coding and general agent tasks. The comparison still teaches two transferable things. Verification is the course's largest category and the field's most neglected one, the same conclusion from both directions. And the course's specification failures concentrate exactly where MAST's do: not in exotic reasoning, but in unread inputs, unwritten termination conditions, and steps repeated past their usefulness.

## Common failures

- Classifying by root cause and by symptom in the same table. Pick the rule (this lesson: what reached the output) and apply it to every row, or the shares are incomparable.
- Comparing shares without comparing populations. The course's fixtures are trap-rich by design; the field's traces are not, and the share difference is partly a sampling statement.
- Treating the taxonomy as a scoreboard. Its use is triage: the largest category is where the next engineering hour goes, and in both profiles that hour is rarely spent on the model.

## Recap checklist

- [ ] You can state the course profile: 6, 6, 8 across 20 instances
- [ ] You can explain why the course is verification-heavy against the field
- [ ] You know the classification rule and can defend it

## Resources

- [README.md](../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
