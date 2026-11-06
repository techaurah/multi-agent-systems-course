"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "routing.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['router_correct'] == 12
    assert r['orders_needing_review'] == 4
    assert r['token_saving_pct'] == 16.1
    assert r['never_review_escapes'] == 4
    print("smoke ok:", "09-routing-and-orchestration")


if __name__ == "__main__":
    main()
