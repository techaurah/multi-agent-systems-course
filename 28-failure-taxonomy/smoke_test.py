"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "taxonomy.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['instances'] == 20
    assert r['counts'] == {'inter-agent misalignment': 6, 'specification and system design': 6, 'task verification': 8}
    assert r['shares']['task verification'] == 0.4
    print("smoke ok:", "28-failure-taxonomy")


if __name__ == "__main__":
    main()
