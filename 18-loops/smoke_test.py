"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "loops.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['cap_50'] == {'completed': False, 'messages': 50}
    assert r['repeat_detection']['messages'] == 7
    assert r['fixed_spec'] == {'completed': True, 'messages': 2}
    print("smoke ok:", "18-loops")


if __name__ == "__main__":
    main()
