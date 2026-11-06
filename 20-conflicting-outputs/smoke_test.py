"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "conflicts.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['disagreements'] == ['order-07', 'order-08']
    assert r['correct_on_disagreements'] == {'defer_rubric': 2, 'defer_strict': 0, 'escalate': 2, 'majority': 2}
    assert r['disagreement_count'] == 2
    print("smoke ok:", "20-conflicting-outputs")


if __name__ == "__main__":
    main()
