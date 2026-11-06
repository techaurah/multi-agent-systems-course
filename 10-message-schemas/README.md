# Lesson 10: Message schemas: the handoff format is a correctness decision

Time: ~35 min | Difficulty: Intermediate | Prerequisites: Lesson 09

Agents in real systems rarely pass typed objects; they pass text, and the receiving agent reconstructs what it needs. This lesson isolates that reconstruction. The extractor's fields cross one handoff in two formats: as a typed payload, where every field has a name and a value, and as a prose summary written the way hurried summaries are actually written, leading with the service and the budget and dropping the qualifiers. A parser on the far side rebuilds the fields from each format, filling what is missing with defaults.

Nothing else changes: same fields, same scorer, same orders. Only the envelope differs, which makes the envelope's cost exactly measurable.

## Run it

```bash
python3 schemas.py
```

## What the code measures

The typed payload arrives intact: fields exact on 10 of 12 orders (the two misses are the extractor's own reading failures from Lesson 03, not handoff losses), and bands correct on 10. The prose summary arrives diminished: fields exact on 3 orders and bands correct on 4. The prose is much cheaper, 11.5 mean tokens against 52.8, and that is the whole trade in one table: prose saves about four fifths of the handoff tokens and loses the timeline and decision-maker status of nearly every order on the way. A summary does not announce what it dropped; the receiving agent scores defaults as if they were facts. This is MAST's inter-agent misalignment in its most ordinary costume (Cemri et al., 2025, in RESEARCH.md): not agents arguing, but a format silently deciding what the next agent is allowed to know.

## Common failures

- Blaming the receiving agent for defaults. The parser's defaults are reasonable; the information was never sent. Format bugs belong to the sender's schema, not the reader's intelligence.
- Summarizing by instinct. What a summary drops is a design decision with a failure table; 'the important parts' is not a schema.
- Assuming cheaper is better because the tokens are visible and the errors are not. Both numbers are in this lesson's output; quote them together or not at all.

## Recap checklist

- [ ] You can state the trade exactly: prose 11.5 tokens and 4 correct bands, typed 52.8 tokens and 10
- [ ] You know a summary's omissions arrive as confident defaults
- [ ] You can name which two fields the prose drops and why the scorer suffers

## Resources

- [README.md](../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
