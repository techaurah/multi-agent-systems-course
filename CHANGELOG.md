# Changelog

## v1.0.0, 2026-11-06

First release.

- 32 lessons across 10 modules: foundations, the single-agent baseline, topologies, communication, state and memory, failure modes, verification and safety, cost and scaling, evaluation, and the capstone.
- The `mas` package: a shared deterministic multi-agent library (messages, ledger, domain workers, eight system architectures, run harness), standard library only.
- The Fernhill fixture set: 12 leads with graded truth records and 12 orders whose expected scores and bands are recomputed by the validator.
- Every lesson ships a runnable artifact, an exercise with a worked solution whose numbers come from running code variants, and a smoke test.
- The capstone: gates fixed in `29-capstone-spec/capstone/gates.json` before the build; the as-built system passes 4 of 5 gates (success 0.8333 against a 0.9 gate) and the hardened system, with a field check at the extractor boundary, passes 5 of 5 at 12 of 12 orders, 0 escapes, and 349.3 tokens per success.
- Honest negatives kept in print: multi-agent ties the single agent on chained work at 2.24x the tokens; hierarchy pays a delegation tax and amplifies cost per success; blackboard messages price pointers, not board content; the hardened capstone still costs about 2.06x the single agent's tokens per success.
- Branded SVG visuals with a generator script; structure validator and link checker wired into CI with all lesson smoke tests.
