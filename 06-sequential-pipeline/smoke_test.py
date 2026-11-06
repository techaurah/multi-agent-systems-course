"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "pipeline.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['successes'] == 7
    assert r['same_failures_as_single']
    assert r['stage_failures'] == {'drafter': 4, 'extractor': 2, 'scorer': 2}
    assert r['tokens_per_success'] == 400.3
    print("smoke ok:", "06-sequential-pipeline")


if __name__ == "__main__":
    main()
