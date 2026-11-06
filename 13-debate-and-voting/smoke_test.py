"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "debate.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['debate_successes'] == 12
    assert r['scorers_disagreed'] == 2
    assert r['debate_tokens_per_success'] == 389.2
    print("smoke ok:", "13-debate-and-voting")


if __name__ == "__main__":
    main()
