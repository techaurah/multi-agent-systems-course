# Tools

Two small, dependency-free maintenance scripts. Run both from the repo root.

- `validate_course.py` checks the structure: all 32 lesson folders with their required files and README sections, no em dash characters in any markdown, the fixtures (12 leads with complete truth records; 12 orders whose expected scores and bands recompute from the truth records with the course rubric in `mas/domain.py`), and the capstone gates file in `29-capstone-spec/capstone/gates.json` with its five numeric gate keys.
- `check_links.py` verifies that every relative Markdown link in the repo resolves to a file or folder on disk.

Both run in CI on every push, alongside a compile pass over all Python files and every lesson's smoke test.
