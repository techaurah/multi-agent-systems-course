"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "capstone_spec.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['gates'] == {'mean_messages_per_order_max': 8, 'policy_escapes_max': 0, 'success_delta_vs_single_min': 0.15, 'task_success_rate_min': 0.9, 'tokens_per_success_max': 400}
    assert r['baseline_single_success_rate'] == 0.5833
    assert r['baseline_single_escapes'] == 4
    print("smoke ok:", "29-capstone-spec")


if __name__ == "__main__":
    main()
