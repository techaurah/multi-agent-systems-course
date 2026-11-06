"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "hierarchy.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['hierarchy_successes'] == r['flat_successes'] == 7
    assert r['delegation_messages'] == 24
    assert r['token_overhead_pct'] == 28.3
    assert r['hierarchy_steps'] == 11
    print("smoke ok:", "08-hierarchical-teams")


if __name__ == "__main__":
    main()
