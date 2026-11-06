"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "blackboard.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['addressed_deliveries_per_order'] == 3.0
    assert r['broadcast_deliveries_per_order'] == 12.0
    assert r['blackboard_deliveries_per_order'] == 7.0
    assert r['blackboard_successes'] == 10
    print("smoke ok:", "12-the-blackboard")


if __name__ == "__main__":
    main()
