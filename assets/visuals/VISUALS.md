# Visuals

Branded SVG diagrams for the course README and lessons. Regenerate them with:

```bash
python3 generate_visuals.py
```

| File | What it shows | Source of its numbers |
|---|---|---|
| `course-map.svg` | The 10 modules and 32 lessons | Course structure |
| `topology-family.svg` | The five topologies and the single-agent baseline | Lessons 03, 06 to 13 |
| `coordination-ledger.svg` | Tokens per success for all six compared systems | Lesson 24 |
| `cascade.svg` | Healthy, faulted, and checkpoint-fixed pipeline successes | Lesson 17 |
| `scaling-curve.svg` | Makespan against pool size for a six-order batch | Lesson 25 |
| `failure-taxonomy.svg` | The course failure profile against the MAST field profile | Lesson 28, RESEARCH.md |
| `capstone-pipeline.svg` | The capstone composition and its gate verdicts | Lessons 29 to 31 |

Style: white canvas, navy `#0B1F4A`, light blue `#E0F2FE`, cyan `#0891B2`, amber `#F59E0B`. Every number in a visual is produced by the course's own code on the bundled fixtures, and each subtitle names the lesson it comes from.
