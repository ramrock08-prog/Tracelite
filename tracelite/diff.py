"""LLM regression testing -- the thing most small tools don't do.

Save today's answers as a baseline; later, rerun the same prompts and see
exactly which answers changed. This is how teams catch a prompt change that
quietly breaks other cases.

Usage (from the project folder):

    python -m tracelite.diff --save     # save current answers as the baseline
    python -m tracelite.diff            # rerun and show what changed

It uses the prompts in testcases.json and runs them at temperature 0 so the
answers are as repeatable as possible.
"""

import argparse
import difflib
import json
import os
import urllib.error

from . import ollama

TESTCASES = "testcases.json"
BASELINE = "golden.json"
MODEL = "llama3.2"


def load_cases():
    with open(TESTCASES, encoding="utf-8") as f:
        return json.load(f)


def run_all(cases):
    """Run every test case and return {prompt: answer}."""
    results = {}
    for case in cases:
        results[case] = ollama.ask(case, MODEL)["response"].strip()
    return results


def similarity(a, b):
    """How alike two answers are, from 0.0 (nothing in common) to 1.0 (same)."""
    return difflib.SequenceMatcher(None, a, b).ratio()


def main():
    parser = argparse.ArgumentParser(description="TraceLite LLM regression check")
    parser.add_argument(
        "--save", action="store_true", help="save current answers as the baseline"
    )
    args = parser.parse_args()

    cases = load_cases()
    print(f"Running {len(cases)} test cases through {MODEL} ...\n")

    try:
        current = run_all(cases)
    except urllib.error.URLError:
        print("Could not reach Ollama. Is it running?  (try: ollama serve)")
        return

    # First run (or --save): store the baseline and stop.
    if args.save or not os.path.exists(BASELINE):
        with open(BASELINE, "w", encoding="utf-8") as f:
            json.dump(current, f, indent=2, ensure_ascii=False)
        print(f"Saved baseline to {BASELINE} ({len(current)} answers).")
        return

    with open(BASELINE, encoding="utf-8") as f:
        baseline = json.load(f)

    changed = 0
    print(f"{'status':<9}{'match':>7}  prompt")
    print("-" * 64)
    for case in cases:
        old = baseline.get(case, "")
        new = current[case]
        ratio = similarity(old, new)
        status = "SAME" if old == new else "CHANGED"
        if status == "CHANGED":
            changed += 1
        print(f"{status:<9}{ratio * 100:6.0f}%  {case[:42]}")
        if status == "CHANGED":
            print(f"          old: {old[:60]!r}")
            print(f"          new: {new[:60]!r}")

    print()
    if changed == 0:
        print("No regressions: every answer is identical to the baseline.")
    else:
        print(f"{changed} of {len(cases)} answers changed vs the baseline.")


if __name__ == "__main__":
    main()
