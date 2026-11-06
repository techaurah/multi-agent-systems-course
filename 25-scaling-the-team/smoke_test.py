"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "scaling.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['sweep'][4]['steps'] == 6
    assert r['sweep'][12]['steps'] == 3
    assert r['tokens_constant_across_pools']
    assert r['smallest_pool_at_best_makespan'] == 6
    print("smoke ok:", "25-scaling-the-team")


if __name__ == "__main__":
    main()
