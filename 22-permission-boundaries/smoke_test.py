"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "permissions.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['attempts'] == 14
    assert r['allowed'] == 8 and r['blocked'] == 6
    assert r['blocked_reasons'] == {'no_verdict': 1, 'not_in_toolset': 5}
    assert r['legitimate_work_blocked'] == 0
    print("smoke ok:", "22-permission-boundaries")


if __name__ == "__main__":
    main()
