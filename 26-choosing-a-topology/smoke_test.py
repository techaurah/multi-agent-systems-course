"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "decision.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['picks'] == {'ambiguous': 'orchestrated', 'chained': 'orchestrated', 'independent': 'single'}
    assert r['overall_successes'] == {'orchestrated': 10, 'pipeline': 7, 'pipeline_reviewed': 10, 'single': 7}
    print("smoke ok:", "26-choosing-a-topology")


if __name__ == "__main__":
    main()
