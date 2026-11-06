# Lesson 13: Debate and voting: two readings, one judge, a stated rule

Time: ~40 min | Difficulty: Advanced | Prerequisites: Lesson 12

Debate is the topology that sounds most like intelligence and is easiest to oversell: several agents argue, and the argument supposedly converges on truth. The measurable version is narrower and more useful. Two scorers read the same lead with different extractors, the quick one and the careful one. Where they agree, nobody pays for a judge. Where they disagree, a judge agent settles the fields with a stated rule: a figure labelled as a total beats a phase price, and words are numbers. The draft is then written once, safely, from the settled fields.

This is the first topology in the course that can beat the single agent on accuracy, and the lesson's job is to price exactly how, and exactly where its power comes from: not from argument, but from a second, different reading plus an arbitration rule.

## Run it

```bash
python3 debate.py
```

## What the code measures

The scorers agree on 10 of 12 orders and disagree on 2: order-04 and order-06, the two known extraction traps. With the judge's rule applied, debate succeeds on 12 of 12 orders, the first perfect score in the course, against the single agent's 7 and the reviewed pipeline's 10. Its cost per success is 389.2 tokens, which is cheaper per success than the reviewed pipeline's 432.3 despite a higher mean cost per order (389.2 against the single agent's 99.0), because it wastes nothing on failures. Two honest qualifications belong in the same breath: the judge's rule is doing the work, and the rule was written by someone who knew the traps; and the second reading is a different algorithm, not a second opinion from the same one. Debate between identical readers would settle nothing, as the exercise shows.

## Common failures

- Calling it debate when it is redundancy. The gain comes from diverse readings plus arbitration; identical agents voting is a coin weighted by repetition.
- Letting the judge improvise. An arbitration rule that is not stated cannot be tested, and the disagreements are too rare and too valuable to spend on improvisation.
- Debating everything. The judge is only invoked on disagreement; a design that argues every order pays the argument tax on the ten orders that never needed it.

## Recap checklist

- [ ] You can state debate's table: 12 of 12 successes, 389.2 tokens per success, 2 disagreements
- [ ] You know the judge's stated rule is the mechanism, not the argument
- [ ] You know diversity of reading, not headcount, is the active ingredient

## Resources

- [README.md](../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
