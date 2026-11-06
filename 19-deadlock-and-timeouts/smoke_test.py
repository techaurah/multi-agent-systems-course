"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "deadlock.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['watchdog_3'] == {'completed': False, 'deadlocked': True, 'rounds': 3}
    assert r['no_watchdog']['rounds'] == 100
    assert r['fallback_matches_expected']
    print("smoke ok:", "19-deadlock-and-timeouts")


if __name__ == "__main__":
    main()
