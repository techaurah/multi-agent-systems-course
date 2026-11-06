# Lesson 20: Conflicting outputs: arbitration is a design decision

Time: ~35 min | Difficulty: Intermediate | Prerequisites: Lesson 19

The moment two agents can produce the same output, they will eventually produce different ones, and the system needs a law for that day. This lesson creates the conflict cleanly: two scorers read the same extracted fields, the rubric scorer with its published thresholds (80 and 55) and a strict scorer with tighter ones (85 and 60). They disagree only where a score falls between the two threshold sets, which is to say on the edge orders, which is to say on exactly the orders a business argues about.

Four arbitration rules are raced on the disagreements: defer to the rubric, defer to the strict scorer, a majority vote with a third scorer who reads carefully, and escalation to the careful reading with the rubric applied.

## Run it

```bash
python3 conflicts.py
```

## What the code measures

The scorers disagree on 2 of 12 orders: order-07, order-08, both scoring exactly 55, the rubric's warm threshold and below the strict warm line. On those disagreements deferring to the rubric is right 2 of 2 times, deferring to strict is right 0, and both majority and escalation are right 2 and 2. The prices differ: the defer rules cost no extra messages, majority costs 2 per disagreement, escalation 3. Two qualifications keep this honest. First, the rubric is right here partly because the expected bands were defined by the rubric; arbitration cannot be fairer than the standard it defers to. Second, with only two disagreements, every rule's score is a small-sample story; the durable lesson is that the rule must be chosen in advance, priced, and owned, because the day it fires is the worst day to invent it.

## Common failures

- Letting the loudest agent win. Recency, confidence formatting, and message length are arbitration rules too, just unchosen ones.
- Averaging the disagreement away. A hot and a nurture do not average into a warm that anyone decided; they average into an output no rule produced.
- Inventing the rule during the incident. Arbitration designed mid-conflict is politics; arbitration designed in advance is engineering.

## Recap checklist

- [ ] You can name the disagreement set: order-07, order-08, both at score 55
- [ ] You can price the four rules in correctness and messages
- [ ] You know arbitration fairness is bounded by the standard it defers to

## Resources

- [README.md](../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
