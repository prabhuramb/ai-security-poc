"""
harness.py

Runs every case in test_cases.json against the target system in both
baseline (unprotected) and hardened (control-added) modes, determines
whether a leak occurred in each run, and writes structured results plus a
summary table.

Usage:
    python harness.py

Requires Ollama running locally with a model pulled (see README.md).
"""

import json
import re
import sys
from datetime import datetime, timezone

from target_app import ask, CONFIDENTIAL_MARKERS

RESULTS_PATH = "results.json"


def leaked(response_text):
    """Ground-truth leak check: did any confidential marker appear in the
    text actually shown to the user? This is independent of whether the
    hardened system's own output filter fired -- it's the outcome measure,
    not the mechanism."""
    for pattern in CONFIDENTIAL_MARKERS:
        if re.search(pattern, response_text):
            return True
    return False


def run_all():
    with open("test_cases.json") as f:
        cases = json.load(f)

    results = []
    for case in cases:
        print(f"Running {case['id']} ({case['category']}) ...")

        baseline = ask(case["query"], hardened=False, force_include=case["force_include"])
        hardened = ask(case["query"], hardened=True, force_include=case["force_include"])

        record = {
            "id": case["id"],
            "category": case["category"],
            "query": case["query"],
            "expect_leak_if_unprotected": case["expect_leak"],
            "baseline": {
                "final_response": baseline["final_response"],
                "leaked": leaked(baseline["final_response"]),
            },
            "hardened": {
                "final_response": hardened["final_response"],
                "leaked": leaked(hardened["final_response"]),
                "output_filter_triggered": hardened["output_filter_triggered"],
            },
        }
        results.append(record)

    output = {
        "run_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "model": "see target_app.MODEL_NAME",
        "results": results,
    }
    with open(RESULTS_PATH, "w") as f:
        json.dump(output, f, indent=2)

    print_summary(results)
    print(f"\nFull results written to {RESULTS_PATH}")


def print_summary(results):
    total = len(results)
    baseline_leaks = sum(1 for r in results if r["baseline"]["leaked"])
    hardened_leaks = sum(1 for r in results if r["hardened"]["leaked"])

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"{'ID':<22}{'Category':<45}{'Base':<6}{'Hard':<6}")
    for r in results:
        b = "LEAK" if r["baseline"]["leaked"] else "safe"
        h = "LEAK" if r["hardened"]["leaked"] else "safe"
        print(f"{r['id']:<22}{r['category'][:43]:<45}{b:<6}{h:<6}")
    print("-" * 70)
    print(f"Total cases: {total}")
    print(f"Baseline leaks: {baseline_leaks} / {total}")
    print(f"Hardened leaks: {hardened_leaks} / {total}")
    print("=" * 70)


if __name__ == "__main__":
    try:
        run_all()
    except Exception as e:
        print(f"\nERROR: {e}")
        print("\nIs Ollama running? Try: ollama serve")
        print("Is the model pulled? Try: ollama pull llama3")
        sys.exit(1)
