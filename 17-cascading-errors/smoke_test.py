"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "cascade.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['healthy_pipeline_successes'] == 7
    assert r['faulty_pipeline_successes'] == 0
    assert r['checkpoint_successes'] == 11
    assert r['checkpoint_failed'] == ['order-04']
    print("smoke ok:", "17-cascading-errors")


if __name__ == "__main__":
    main()
