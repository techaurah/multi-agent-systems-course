"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "cost_accounting.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['table']['debate']['successes'] == 12
    assert r['table']['pipeline']['tokens_per_success'] == 400.3
    assert r['cheapest_per_success'] == 'blackboard'
    assert r['table']['single']['escapes'] == 4
    print("smoke ok:", "24-coordination-cost-accounting")


if __name__ == "__main__":
    main()
