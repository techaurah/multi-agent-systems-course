# Lesson 12: The blackboard: shared state instead of addressed messages

Time: ~35 min | Difficulty: Intermediate | Prerequisites: Lesson 11

The blackboard is the oldest multi-agent architecture in this course: agents do not write to each other at all, they write to a shared board, and each agent reads the entries it subscribes to. MetaGPT's shared message pool and AutoGen's group chat are its modern relatives (checked 2026-11-06 in RESEARCH.md). Its promise is decoupling: no agent needs to know who else exists. Its price is that the board becomes a piece of shared state, with all the hazards Module 4 is about.

This lesson counts deliveries under three disciplines: addressed messages, where each message arrives once; a broadcast bus, where every message arrives in every other agent's inbox; and the blackboard, where writes and subscribed reads are the deliveries. One accounting caveat is stated now and applied in Lesson 24: the blackboard's messages carry entry names, not content, so its token count prices the pointers while the board's content sits in shared memory, unpriced. Compare its deliveries freely; compare its tokens with that caveat attached.

## Run it

```bash
python3 blackboard.py
```

## What the code measures

Per order: addressed messages cause 3.0 deliveries, broadcast causes 12.0 (three messages into four other inboxes each), and the blackboard causes 7.0 (three writes and four subscribed reads). The blackboard's measured successes are 10 of 12 against the plain pipeline's 7, but be careful about why: the blackboard build in `mas/systems.py` drafts safely, so its gain is the drafter's policy discipline, not the board. Its mean message tokens are 72.2 against the pipeline's 233.5, with the pointer caveat above doing most of that work. The topology's honest wins are the delivery count against broadcast and the decoupling; its honest cost is that correctness now depends on what the board holds and who may write to it, which is a governance question addressed messages never ask.

## Common failures

- Crediting the board for the drafter's discipline. Two variables changed between these builds (topology and drafting policy); the lesson names which one produced the successes.
- Pricing pointers as if they were content. A blackboard that looks 3 times cheaper on tokens has moved its content into shared state, not eliminated it.
- Letting every agent write every entry. The board's convenience becomes a correctness hazard the moment two agents can overwrite the same entry; Lesson 14 shows the versioned version of that problem.

## Recap checklist

- [ ] You can rank the disciplines by deliveries: addressed 3.0, blackboard 7.0, broadcast 12.0
- [ ] You can explain the blackboard's token caveat without being prompted
- [ ] You know decoupling is the board's real product

## Resources

- [README.md](../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
