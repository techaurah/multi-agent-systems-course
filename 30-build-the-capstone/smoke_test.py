"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "capstone_pipeline.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['successes'] == 10
    assert r['failed_orders'] == ['order-04', 'order-06']
    assert r['escapes'] == 0
    assert r['routed_to_review'] == 4
    print("smoke ok:", "30-build-the-capstone")


if __name__ == "__main__":
    main()
