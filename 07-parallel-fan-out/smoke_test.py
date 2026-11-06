"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "parallel.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['serial_single_steps'] == 18
    assert r['sweep'][3]['steps'] == 6
    assert r['speedup_at_3_workers'] == 3.0
    assert r['sweep'][1]['tokens'] == r['sweep'][6]['tokens']
    print("smoke ok:", "07-parallel-fan-out")


if __name__ == "__main__":
    main()
