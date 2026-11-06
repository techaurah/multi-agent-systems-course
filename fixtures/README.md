# Fixtures: the Fernhill lead set

Two files carry the whole course's measurements.

- `leads.json` holds twelve inquiries to the fictional Fernhill Garden Centres, each with a `truth` record (service, budget_usd, timeline, decision_maker) that grading uses. The twelve leads are built to contain the traps the course studies: a budget written out in words, a 25 percent discount ask, a budget split into a phase price and a total, timeline and decision-maker signals spread across a long message, an order with no budget at all, and one junk lead.
- `policy.json` holds the reply policy: the five services, which are premium, the maximum discount of 10 percent, and the callback promise of within one working day.
- `orders.json` holds the twelve orders over those leads, each with a `family` (independent, chained, or ambiguous), a note about which trap or property makes it interesting, and the `expected` score and band. Expected values are not asserted by hand: `tools/validate_course.py` recomputes them from the truth records with the rubric in `mas/domain.py` and fails if they drift.

Every number in every lesson is produced by running the lesson's code on these fixtures. If a number in the prose cannot be reproduced from these files and the `mas` package, that is a bug in the course, and it is worth an issue.
