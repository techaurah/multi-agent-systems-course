# Notes for agents and contributors working in this repo

- Every number in a lesson README, exercise, or solution must be reproducible by running that lesson's code on the bundled fixtures. If you change a fixture, the rubric, or the `mas` package, re-run every affected lesson and update every quoted number.
- The capstone gates live in `29-capstone-spec/capstone/gates.json` and do not move. If a change makes the capstone fail a gate, report the failure; never edit the gate to fit.
- Honest negatives stay in print: Lesson 05 (multi-agent loses on chained work), the blackboard pointer-accounting caveat (Lessons 12 and 24), the reviewer's blind spots (Lesson 21), the checkpoint blind spot (Lesson 17), and the capstone's failed as-built verdict and residual cost (Lesson 31).
- No em dashes in any file. Write around them with commas, colons, or separate sentences.
- Runnable code is Python standard library only. No API keys, no live model calls, no new dependencies. Agents are deterministic stand-ins and must be labelled as such wherever they are introduced.
- Keep the validators green: `python3 tools/validate_course.py`, `python3 tools/check_links.py`, `python -m compileall .`, and every lesson's `smoke_test.py` run from its own folder.
- External claims need a source and a check date in RESEARCH.md. Framework version claims in particular must be re-checked before being repeated.
- Fixtures are shared by all lessons. The orders' expected scores and bands must always recompute from the leads' truth records via `mas.domain.score_fields`; the validator enforces this.
