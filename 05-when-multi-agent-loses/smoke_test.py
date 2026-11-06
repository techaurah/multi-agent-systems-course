"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "sequential_race.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['single_successes'] == 1
    assert r['pipeline_successes'] == 1
    assert r['same_failures']
    assert r['token_ratio'] == 2.24
    assert r['pipeline_tokens_per_success'] == 709.0
    print("smoke ok:", "05-when-multi-agent-loses")


if __name__ == "__main__":
    main()
