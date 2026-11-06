"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "evaluation.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['new_failures_total'] == 16
    assert r['attribution_accuracy'] == 1.0
    assert r['per_fault']['scorer']['new_failures'] == 2
    print("smoke ok:", "27-evaluating-the-system")


if __name__ == "__main__":
    main()
