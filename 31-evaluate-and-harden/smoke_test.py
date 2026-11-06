"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "evaluate_capstone.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['as_built_gates_passed'] == 4
    assert r['hardened_gates_passed'] == 5
    assert r['ship']
    assert r['hardened']['successes'] == 12
    assert r['as_built']['success_rate'] == 0.8333
    print("smoke ok:", "31-evaluate-and-harden")


if __name__ == "__main__":
    main()
