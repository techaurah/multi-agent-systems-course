"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "one_vs_many.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['single_success'] and r['pipeline_success']
    assert r['same_band'] and r['same_draft']
    assert r['single_messages'] == 0 and r['pipeline_messages'] == 3
    assert r['single_tokens'] == 106
    assert r['pipeline_tokens'] == 251
    print("smoke ok:", "01-what-makes-it-multi-agent")


if __name__ == "__main__":
    main()
