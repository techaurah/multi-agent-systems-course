# Lesson 16: History and loss: what survives a chain of summaries

Time: ~30 min | Difficulty: Intermediate | Prerequisites: Lesson 15

Long-running systems relay state through chains of agents, and each relay tends to re-summarize what it passes on. MAST (Cemri et al., 2025) names loss of conversation history as a system design failure mode; this lesson reproduces it with a ruler. Fields cross a chain of relays, and each relay drops the field it judges least important, in a fixed order: decision-maker status first, then timeline, then budget, then service. After each hop the scorer scores whatever is left, filling gaps with defaults. The question is not whether information is lost, but how fast the loss converts into wrong decisions.

## Run it

```bash
python3 history_loss.py
```

## What the code measures

Bands correct by hops survived: 10 of 12 at zero hops, 7 after one, 4 after two, 3 after three, 3 after four. The first dropped field, decision-maker status at 20 points, costs three bands on its own. The hop-zero row also carries a quieter fact: service and timeline survive extraction perfectly (12 and 12 of 12 match the truth), decision-maker status too (12), while budget already matches on only 10: the relay starts from a state that is itself lossy. Chains compound two different losses, extraction loss at the source and relay loss at every hop, and debugging them as one number hides which one to fix.

## Common failures

- Summarizing at every hop by default. Each relay should pass state verbatim unless a measured reason exists to compress it; summarization is a lossy operation pretending to be housekeeping.
- Dropping fields by gut feel. The drop order here is by rubric points ascending, and it still costs three bands in one hop; an unconsidered order costs more.
- Confusing source loss with relay loss. Budget is already wrong on two orders before the first relay; no relay discipline fixes an extraction problem.

## Recap checklist

- [ ] You can recite the decay curve: 10, 7, 4, 3, 3
- [ ] You know the first dropped field costs three bands
- [ ] You can separate extraction loss from relay loss in the hop-zero row

## Resources

- [README.md](../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
