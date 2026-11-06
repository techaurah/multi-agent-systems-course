"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "decompose.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['jobs_per_order'] == 4
    assert r['cross_order_edges'] == 0
    assert r['total_jobs_batch'] == 48
    assert r['orders_where_draft_depends_on_check'] == 4
    print("smoke ok:", "04-decomposition")


if __name__ == "__main__":
    main()
