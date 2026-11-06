"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "check_environment.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['python_ok']
    assert r['leads'] == 12
    assert r['orders'] == 12
    assert r['families'] == {'ambiguous': 3, 'chained': 3, 'independent': 6}
    assert r['max_discount_pct'] == 10
    print("smoke ok:", "00-course-setup")


if __name__ == "__main__":
    main()
