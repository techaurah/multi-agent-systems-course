# Lesson 09: Routing and orchestration: send each order the cheapest safe way

Time: ~40 min | Difficulty: Intermediate | Prerequisites: Lesson 08

An orchestrator is a pipeline whose shape is decided per order at run time. The orchestrator-worker pattern behind Anthropic's research system (June 2025, in RESEARCH.md) works because a lead agent decomposes each task and delegates; the humble version in this lesson does one decision well: it routes. Orders that carry a trap (a discount ask above the cap, or no stated budget) go through the reviewer; clean orders skip review entirely. The two lazy alternatives frame the value: review everything and pay for checks most orders do not need, or review nothing and let violations escape.

The router itself reads only the raw inquiry text, with two rules: a percent-off ask, or the absence of any dollar figure, routes to review.

## Run it

```bash
python3 routing.py
```

## What the code measures

The router is correct on 12 of 12 orders against the true routes, and only 4 orders genuinely need review. The orchestrated system matches the always-review pipeline's 10 successes at 302.4 mean tokens against 360.2, a saving of 16.1 percent, while the never-review pipeline lets 4 violations escape. Orchestration's win is not intelligence; it is selectivity. The check is worth its cost on a third of the orders and pure overhead on the rest, and a two-rule router is enough to tell them apart here. Note the honest limit: the router works because the traps are visible in the text. A trap that only appears after extraction would defeat a text router, which is why Lesson 29's capstone keeps the routing rules under the same gates as everything else.

## Common failures

- Routing on vibes. The router's rules are stated, tested against true routes, and counted; an orchestrator whose decisions cannot be scored is a random topology generator.
- Reviewing everything 'to be safe'. Safety has a price list: always-review spends the difference on eight orders that did not need it.
- Trusting the router past its evidence. Twelve of twelve on this fixture set means the rules fit these traps, not that routing is solved.

## Recap checklist

- [ ] You can state the router's score: 12 of 12, saving 16.1 percent against always-review at equal successes
- [ ] You know orchestration's value here is selectivity, not intelligence
- [ ] You can name the limit: traps must be visible to the router's inputs

## Resources

- [README.md](../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
