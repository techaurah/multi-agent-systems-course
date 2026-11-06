"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "ledger.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['traced_messages'] == 7
    assert r['traced_tokens'] == 433
    assert r['by_kind'] == {'draft': 2, 'fields': 1, 'score': 1, 'task': 1, 'verdict': 2}
    assert r['fleet_pipeline_tokens'] == 360.2
    print("smoke ok:", "02-the-coordination-ledger")


if __name__ == "__main__":
    main()
