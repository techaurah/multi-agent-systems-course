"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "budgets.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['budget_4']['finished'] == 0
    assert r['budget_5']['finished'] == 8
    assert r['budget_7']['finished'] == 12
    assert r['escapes_if_sent_at_step_3'] == 4
    print("smoke ok:", "23-termination-and-budgets")


if __name__ == "__main__":
    main()
