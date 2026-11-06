# Lesson 11: Handoffs and state: what must travel, and what the gaps cost

Time: ~30 min | Difficulty: Intermediate | Prerequisites: Lesson 10

Lesson 10 varied the format; this lesson varies the contents. Suppose the handoff is typed and clean, but deliberately partial: only the service and the budget travel, because a designer judged the rest to be detail. The scorer receives the partial state and fills the gaps with the same defaults any real agent would assume: flexible timing, not the decision maker. The question is which orders can afford the omission and which cannot, and the answer is written in the rubric: timeline carries up to 30 points and decision-maker status 20, so a two-field handoff caps the score before the scorer starts.

## Run it

```bash
python3 handoffs.py
```

## What the code measures

The summary handoff saves 59.0 percent of the handoff tokens (21.7 against 52.8 mean) and changes the band on 8 of 12 orders: correct bands fall from 10 to 4. Read the changed list carefully: it is exactly the orders whose truth involves urgency, a near-term start, or a decision maker, which is to say the orders where the missing fields carried points. The independent, flexible, low-value orders sail through the summary untouched, which is how partial handoffs survive in production: they fail selectively, on the orders where the omitted state mattered, and averages conceal it until a specific customer is misjudged.

## Common failures

- Designing handoffs by payload size. The right question is which downstream decisions each field feeds; size is the last consideration, not the first.
- Letting defaults masquerade as data. The receiving scorer cannot distinguish 'flexible' the fact from 'flexible' the assumption; typed handoffs should mark assumed values as assumed.
- Testing handoffs on average orders. Partial state fails on the orders richest in the omitted fields; test those first.

## Recap checklist

- [ ] You can state the exchange: 59.0 percent of handoff tokens for 8 changed bands
- [ ] You can name the orders a summary handoff cannot hurt, and why
- [ ] You know defaults should be marked as assumptions in the schema

## Resources

- [README.md](../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
