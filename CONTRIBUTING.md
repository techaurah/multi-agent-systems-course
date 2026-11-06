# Contributing

Contributions are welcome: corrections, clearer explanations, additional exercises, and translations.

## Ground rules

- **Numbers must reproduce.** Any figure in prose must come from running the lesson's code on the bundled fixtures. Pull requests that change a fixture, the rubric, or the `mas` package must include the re-run outputs for every affected lesson and update every quoted number.
- **The capstone gates do not move.** `29-capstone-spec/capstone/gates.json` is fixed. A change that makes the capstone fail a gate is reported as a failure, not fixed by editing the gate.
- **Honest negatives stay.** Do not soften Lesson 05, the blackboard accounting caveat, the reviewer's blind spots, or the capstone's as-built verdict in the name of polish.
- **Standard library only.** Runnable code uses the Python standard library. No API keys, no live model calls, no new dependencies.
- **No em dashes** in any file, and no certificate promises or sales copy anywhere in the course.
- **External claims need sources.** Add the source and the date you checked it to RESEARCH.md.

## Before you open a pull request

Run the same checks CI runs:

```bash
python -m compileall .
python3 tools/validate_course.py
python3 tools/check_links.py
for d in [0-9][0-9]-*/; do (cd "$d" && python3 smoke_test.py); done
```

## Style

Lesson READMEs follow the house structure: title and metadata line, introduction, Run it, What the code measures, Common failures, Recap checklist, Resources. Exercises must be answerable by running a variant of the lesson's code, and solutions must quote only numbers those variants produce.
