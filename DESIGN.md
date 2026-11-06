# Course Design: Multi-Agent Systems

This document records the design as specified before the lessons were written, including the capstone gates policy. The measured outcomes live in the lessons and the root README's scorecard.

## Audience and promise

For builders who have shipped a single agent (or finished Agentic AI for Beginners) and are deciding whether, where, and how to split work across several. The promise: coordination treated as an engineering quantity with a price, not a vibe. Every design claim in the course is either measured by the lesson's own code on the bundled fixtures or cited to a dated source in RESEARCH.md.

## Principles

1. **Single agent first.** The baseline is built and measured (Lesson 03) before any topology, and one full lesson (05) is devoted to where multi-agent measures worse. A course that cannot show its subject losing cannot be trusted when it wins.
2. **Deterministic stand-ins, labelled as such.** Agents are small rule-based workers (extractors, scorers, drafters, reviewers) in the pattern of earlier TechAurah courses. They exhibit the coordination phenomena the course studies (cost, cascades, loops, deadlock, amplification) with full reproducibility and no API keys.
3. **One fixture set, every architecture.** All systems run the same twelve Fernhill lead inquiries with graded truth records, so prices and success rates are comparable across lessons and the final cost table (Lesson 24) is honest arithmetic.
4. **Failures are curriculum.** The fixture set deliberately contains the traps the field's literature names: word-form budgets, phase pricing, planted instructions in lead text, missing budgets, junk leads. Lessons 17 to 20 reproduce the multi-agent failure modes as mechanisms, not anecdotes.
5. **Gates before code.** The capstone's five gates were fixed in `29-capstone-spec/capstone/gates.json`, dated 2026-11-06, from the baseline's measured numbers, before any capstone code existed. The as-built verdict and the hardening are both reported against those unchanged numbers.

## Structure

32 lessons in 10 modules:

- Module 0, Foundations (00-02): setup, the boundary of multi-agent, the coordination ledger.
- Module 1, One agent first (03-05): baseline, decomposition, the losing lesson.
- Module 2, Topologies (06-09): sequential, parallel, hierarchical, routing.
- Module 3, Communication (10-13): schemas, handoffs, blackboard, debate.
- Module 4, State and memory (14-16): shared memory, private vs shared context, history loss.
- Module 5, Failure modes (17-20): cascades, loops, deadlock, conflicts.
- Module 6, Verification and safety (21-23): reviewer, permissions, termination.
- Module 7, Cost and scaling (24-26): the cost table, scaling sweep, decision table.
- Module 8, Evaluation (27-28): fault attribution, taxonomy profiling.
- Module 9, Capstone (29-31): spec and gates, build, evaluate and harden.

## The fixture domain

Fernhill Garden Centres (the fictional company carried across TechAurah courses) receives twelve service inquiries. Each has a graded truth record (service, budget, timeline, decision-maker) and each order an expected score and band computed by a printed rubric. The workers are deterministic: a quick regex extractor and a careful one, a naive drafter (which produces the policy violations the course studies) and a policy-safe one, a rule reviewer, and routers with stated rules. The `mas` package holds all of it, shared by every lesson, so cross-lesson comparisons compare designs rather than reimplementations.

## The capstone

A lead-processing system composed only of parts measured in earlier lessons: the Lesson 09 router, the Lesson 06 pipeline, the Lesson 21 reviewer. Gates (success at least 0.9, escapes at most 0, mean messages at most 8, tokens per success at most 400, success delta over the single agent at least 0.15) were set from the Lesson 03 baseline (0.5833 success, 4 escapes, 169.7 tokens per success). The design expectation, recorded in advance, was that routing plus review would pass the draft-level gates and that extraction quality would decide the success gate; the spec deliberately did not pre-authorise a field check, so that if one proved necessary it would arrive as a measured hardening in Lesson 31, with its cost printed.

## What the course deliberately does not do

- No framework tutorials: LangGraph, CrewAI, and AutoGen each teach themselves better than a framework-free course can. The course teaches the decisions those frameworks leave to the builder.
- No live model calls, no prompt engineering for specific hosted models, no benchmark claims beyond the fixture set and the cited literature.
- No sales material, no certificate, no invented statistics. Where the course's fixtures and the field's numbers disagree in shape (Lesson 28's taxonomy profile), the disagreement is explained as a sampling difference, not smoothed over.
