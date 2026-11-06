"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "history_loss.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['bands_correct_by_hops'] == {0: 10, 1: 7, 2: 4, 3: 3, 4: 3}
    assert r['fields_matching_truth_at_hop_0']['budget_usd'] == 10
    assert r['drop_order'][0] == 'decision_maker'
    print("smoke ok:", "16-history-and-loss")


if __name__ == "__main__":
    main()
