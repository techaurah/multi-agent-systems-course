# Lesson 15: Private vs shared context: exposure, and the contaminated draft

Time: ~35 min | Difficulty: Intermediate | Prerequisites: Lesson 14

What an agent can see is a design decision with two price tags. The first is exposure: every context is a copy of the data, and copies are where data leaks, confuses, and costs. This lesson counts lead-text exposure under broadcast and addressed designs in tokens of customer text placed in front of agents. The second price is contamination: an agent whose context holds other work's outputs can import their content. The lesson's stand-in for that failure is a drafter that writes with the run's earlier drafts in its context and repeats the strongest discount line it can see there, a small rule standing in for a large and well documented behaviour: agents anchor on what their context contains.

## Run it

```bash
python3 context_scope.py
```

## What the code measures

The 12 lead texts total 643 tokens. Under broadcast, all 5 agents read all of them: 3215 tokens of customer text exposure. Under the addressed pipeline only the extractor reads lead texts: 643 tokens, a ratio of 5.0 to 1. The contamination count is sharper. Drafting with no history produces 4 policy violations across the run, the naive drafter's own four. Drafting with the earlier drafts in context produces 11: once order-05's reply agrees to 25 percent off, every later drafter whose lead asked for nothing repeats the line anyway, and seven more drafts inherit a violation from a colleague's output. Nothing was communicated; the drafts were merely visible. Shared context is a communication channel whether you designed it as one or not.

## Common failures

- Giving every agent the full history 'for context'. The exposure ledger and the contamination count are the two halves of that decision's price.
- Treating contamination as a prompting problem. The repeating drafter follows its context faithfully; the fix is scoping what it can see, not exhorting it to ignore what it sees.
- Scoping by deletion after the fact. Context scope is decided when the message is composed; an agent that has read a discount line cannot unread it.

## Recap checklist

- [ ] You can state the exposure ratio: 5.0 to 1, broadcast against addressed
- [ ] You can trace the contamination: 4 violations clean, 11 with shared draft history
- [ ] You know shared context is a channel, designed or not

## Resources

- [README.md](../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
