"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "shared_memory.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['stale_schedule_bands_correct'] == 10
    assert r['version_checked_bands_correct'] == 12
    assert r['final_versions_for_thin_orders'] == {'order-04': 2, 'order-06': 2, 'order-07': 2, 'order-12': 2}
    print("smoke ok:", "14-shared-memory")


if __name__ == "__main__":
    main()
