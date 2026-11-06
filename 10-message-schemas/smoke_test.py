"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "schemas.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['typed_fields_exact'] == 10
    assert r['prose_fields_exact'] == 3
    assert r['prose_bands_correct'] == 4
    assert r['typed_mean_tokens'] == 52.8
    print("smoke ok:", "10-message-schemas")


if __name__ == "__main__":
    main()
