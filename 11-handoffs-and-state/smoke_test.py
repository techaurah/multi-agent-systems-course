"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "handoffs.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['full_handoff_bands'] == 10
    assert r['summary_handoff_bands'] == 4
    assert len(r['bands_changed_by_summary']) == 8
    assert r['tokens_saved_pct'] == 59.0
    print("smoke ok:", "11-handoffs-and-state")


if __name__ == "__main__":
    main()
