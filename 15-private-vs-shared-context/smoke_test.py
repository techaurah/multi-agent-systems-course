"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "context_scope.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['exposure_ratio'] == 5.0
    assert r['violations_with_shared_draft_history'] == 11
    assert r['violations_without_history'] == 4
    assert r['broadcast_text_exposure_tokens'] == 3215
    print("smoke ok:", "15-private-vs-shared-context")


if __name__ == "__main__":
    main()
