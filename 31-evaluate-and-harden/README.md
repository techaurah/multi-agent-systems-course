# Lesson 31: Evaluate and harden: the verdict, the failed gate, and the fix

Time: ~60 min | Difficulty: Advanced | Prerequisites: Lesson 30

The verdict comes first, and it is a failure. The as-built capstone passes four of its five gates and fails the one that matters most: task success. This lesson reports that verdict without softening it, diagnoses the failure to the component level, and applies the hardening the diagnosis dictates: a field check pass at the extractor boundary, Lesson 14's and Lesson 17's lesson composed, which re-reads an order with the careful extractor whenever the quick extraction looks thin (no budget found, or a figure that might be a phase price). The hardened system is then measured against the same unchanged gates, and the costs of the fix are printed next to its benefits.

## Run it

```bash
python3 evaluate_capstone.py
```

## What the code measures

As built: success rate 0.8333 against a gate of 0.9 (fail), escapes 0 (pass), mean messages 5.33 (pass), tokens per success 362.9 (pass), success delta over the baseline 0.25 (pass). Gates passed: 4 of 5. Hardened: success rate 1.0, 12 of 12 orders, escapes 0, gates passed 5 of 5. The fix is not free and the invoice is in the same output: mean messages rise from 5.33 to 6.0, mean tokens from 302.4 to 349.3, and the hardened system's tokens per success (349.3) remain about twice the single agent's (169.7). Two honest residues stay on the record. On independent orders the single agent is still the cheapest way to succeed, exactly as Lesson 26's table said. And the field check's thin test is itself a trigger with a blind spot, of the kind Lesson 17 named: a budget misread to a plausible wrong figure with no 'total' in the text would pass it silently.

## Common failures

- Moving the gate. The success gate was 0.90 before the build and is 0.90 now; the system moved, which is the only direction hardening is allowed to travel.
- Hiding the failed run. The as-built numbers are printed in this lesson's output and in the root README's scorecard, because the failure is the evidence that the gates mean something.
- Declaring the hardened system strictly better. It is better on success and worse on messages and tokens; both halves ship in the report or the report is marketing.

## Recap checklist

- [ ] You can state the verdict precisely: as built 4 of 5, hardened 5 of 5
- [ ] You can name the hardening, the trigger that drives it, and its known blind spot
- [ ] You can quote the fix's invoice alongside its benefit

## Resources

- [README.md](../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
