# Lesson 04: Decomposition: reading the shape of the work before choosing agents

Time: ~30 min | Difficulty: Beginner | Prerequisites: Lesson 03

Topologies do not fail in the abstract; they fail against the shape of a particular workload. Decomposition is the discipline of reading that shape first: what are the sub-jobs, what depends on what, and where are the edges? This lesson draws the dependency graph of the course's own work before any topology is chosen, because the graph, not preference, decides which topologies can possibly help.

Each order decomposes into four jobs: extract, score, draft, check. Inside an order the jobs form a chain, since each consumes the previous job's output. Between orders there are no edges at all: no order's output is another order's input.

## Run it

```bash
python3 decompose.py
```

## What the code measures

The counts: 4 jobs per order, 3 chain edges inside each order, 0 edges between orders, 48 jobs in the full batch, a chain depth of 4 and a parallel width of 12 (all 12 orders can sit at the extract stage simultaneously). Two consequences follow immediately. Parallelism lives between orders, never inside one: a single order cannot be hurried by adding agents, only a batch can. And the check job is load-bearing on exactly 4 orders, the ones with a discount ask or a missing budget, where drafting before checking produces a policy violation. A topology that parallelizes inside the chain, or checks everything uniformly, is fighting this graph; a topology that fans out across orders and routes the four trap orders to a check is reading it.

## Common failures

- Decomposing by agent persona instead of by dependency. 'Researcher, writer, editor' is a cast list; the graph is what decides whether they can work at the same time.
- Splitting a chain and calling the pieces parallel. Extract, score, and draft for one order are sequential by construction; running them 'in parallel' means running them on stale inputs.
- Ignoring the zero. Cross-order edges are exactly zero here, and that zero is the single most valuable fact in the graph: it is what makes fan-out safe.

## Recap checklist

- [ ] You can draw the order graph from memory: chains inside, nothing between
- [ ] You know parallelism lives between orders, not inside one
- [ ] You know the check job matters on exactly 4 of 12 orders

## Resources

- [README.md](../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
