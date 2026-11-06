"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "reviewer.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['escapes_without_reviewer'] == 4
    assert r['escapes_with_reviewer'] == 0
    assert r['successes_with_reviewer'] == 10
    assert r['redrafts_triggered'] == 4
    print("smoke ok:", "21-the-reviewer")


if __name__ == "__main__":
    main()
