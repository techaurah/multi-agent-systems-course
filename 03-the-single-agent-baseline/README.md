# Lesson 03: The single-agent baseline: the system every topology must beat

Time: ~35 min | Difficulty: Beginner | Prerequisites: Lesson 02

Every multi-agent design is an argument that coordination buys more than it costs. That argument is unanswerable without a baseline, so this course builds the strongest honest single agent first: one pass over each lead that extracts the fields with the quick regex extractor, scores them with the published rubric, and drafts the reply with the naive drafter. It holds everything in one context, sends no messages, and is very cheap. It is also, on this order set, wrong a lot, and the pattern of its wrongness is the syllabus for the rest of the course.

An order succeeds only when all three hold: the extracted fields match the lead's truth, the band matches the expected band, and the reply is policy clean (no discount above the 10 percent cap, no invented price, a callback promised). Partial credit is not given, because a customer experiences the whole reply, not its average.

## Run it

```bash
python3 single_agent.py
```

## What the code measures

The baseline succeeds on 7 of 12 orders (success rate 0.5833) at 99.0 mean tokens and 169.7 tokens per success, with 4 policy violations sitting in drafts it would have sent. By family the split is stark: independent orders 6 of 6, chained orders 1 of 3, ambiguous orders 0 of 3. The failures cluster into three kinds: fields wrong on 2 orders (the budget in words on order-04, the phase price taken as the budget on order-06), bands wrong on 2, and drafts violating policy on 4 (the discount agreement on order-05, invented starting prices on order-04, order-07, and order-12). Nothing here is a coordination failure; one agent, alone, makes all of them. The question the course asks of every topology is which of these failures coordination can remove, and at what price.

## Common failures

- Softening the baseline to make multi-agent look good. A straw baseline proves nothing; this one uses the same extractor, rubric, and drafter the pipelines use, so differences are coordination differences.
- Reporting the mean and hiding the families. The baseline is perfect on independent orders and hopeless on ambiguous ones; the average of those is a fiction.
- Counting a reply with one violation as mostly fine. The grading is all or nothing per order because the customer reads the reply that was sent, not the rubric.

## Recap checklist

- [ ] You can state the baseline exactly: 7 of 12, 169.7 tokens per success, 4 escapes
- [ ] You can name the three failure kinds and one order that shows each
- [ ] You know ambiguous orders are where the baseline scores zero

## Resources

- [README.md](../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
