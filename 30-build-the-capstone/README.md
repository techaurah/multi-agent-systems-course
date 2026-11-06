# Lesson 30: Build the capstone system

Time: ~60 min | Difficulty: Advanced | Prerequisites: Lesson 29

The capstone system is a composition, not an invention. A router reads each inquiry and sends the four trap orders (discount asks, missing budgets) through the reviewer, and the eight clean orders past it. Reviewed orders run the sequential pipeline with a verdict and one safe redraft; clean orders run it bare. The extractor is the quick regex reader, the drafter is the naive one, and every message crosses the ledger. Each of those choices was made and measured in an earlier lesson; the capstone's claim is only that they compose.

Run the artifact and read the per-family table before Lesson 31 delivers the gate verdict. Note where the remaining failures sit: they are not randomly distributed, and their address is the hardening's address.

## Run it

```bash
python3 capstone_pipeline.py
```

## What the code measures

As built, the capstone succeeds on 10 of 12 orders (success rate 0.8333), with 0 escapes, 5.33 mean messages, 302.4 mean tokens, and 362.9 tokens per success. The router sent 4 orders to review. By family: independent 6 of 6, chained 2 of 3, ambiguous 2 of 3. The two failures are order-04 and order-06, the extraction traps, untouched by every component in the composition, because no component in it re-reads the source. The system's draft discipline is complete and its reading discipline is inherited, unexamined, from Lesson 03's quickest extractor. That asymmetry is the capstone's real output, and Lesson 31 grades it.

## Common failures

- Adding a new component at capstone time. Anything not measured in its own lesson is a hypothesis, not a building block; the composition rule is what keeps the capstone's failures attributable.
- Reading the fleet rate and skipping the families. The two failures hide in different families (one chained, one ambiguous); the fleet's 0.8333 is the least informative number on the page.
- Tuning the router to the failures. The router's rules were fixed in Lesson 09 against routing truth, not against these outcomes; refitting them now would be gate-shopping.

## Recap checklist

- [ ] You can state the as-built headline: 10 of 12, 0 escapes, 362.9 tokens per success
- [ ] You can name the two failing orders and the component-shaped hole they share
- [ ] You know the routed-to-review count and why it is four

## Resources

- [README.md](../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
