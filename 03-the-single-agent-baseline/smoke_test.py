"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "single_agent.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['successes'] == 7
    assert r['success_rate'] == 0.5833
    assert r['tokens_per_success'] == 169.7
    assert r['failed_orders'] == ['order-04', 'order-05', 'order-06', 'order-07', 'order-12']
    assert r['by_family']['ambiguous']['successes'] == 0
    print("smoke ok:", "03-the-single-agent-baseline")


if __name__ == "__main__":
    main()
