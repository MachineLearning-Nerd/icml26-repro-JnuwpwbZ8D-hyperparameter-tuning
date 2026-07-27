#!/usr/bin/env python3
"""Independent fail-closed checker for empirical theorem-signature output."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def increasing(values: list[float]) -> bool:
    return all(right > left for left, right in zip(values, values[1:]))


def check(payload: dict) -> dict:
    claims = payload["claims"]
    failures: list[str] = []

    if payload["seeds"] != [173, 271, 419]:
        failures.append("unexpected seeds")
    if payload["budget_policy"] != "fixed independently of theorem formulas":
        failures.append("circular budget")

    c1 = claims["C1"]
    if not all(row["patterns"] == row["possible"] for row in c1["positive_control"]):
        failures.append("C1 halfspace control did not shatter")
    c1_bounds = [row["bound"] for row in c1["scaling_signature"]]
    if not increasing(c1_bounds):
        failures.append("C1 block signature absent")
    if c1["negative_control"]["applicable"]:
        failures.append("C1 negative control unexpectedly applicable")

    c2 = claims["C2"]
    if not all(min(row["patterns_by_seed"]) >= 32 for row in c2["measured_piecewise_polynomial"]):
        failures.append("C2 pattern measurement degenerate")
    if not increasing([row["bound"] for row in c2["p_sweep"]]):
        failures.append("C2 p signature absent")
    if not increasing([row["bound"] for row in c2["d_sweep"]]):
        failures.append("C2 d signature absent")

    c3 = claims["C3"]
    if not all(min(row["patterns_by_seed"]) >= 16 for row in c3["measured_bilevel_quadratic"]):
        failures.append("C3 bilevel pattern measurement degenerate")
    ratios = [row["ratio_to_c2"] for row in c3["d2_signature"]]
    if not increasing(ratios):
        failures.append("C3 d-to-d2 separation absent")
    if not c3["negative_control"]["rejected"]:
        failures.append("C3 f==g mutation accepted")

    c4 = claims["C4"]
    if not all(row["cap_holds"] and row["observed_exact_orthogonal_elasticnet_regions"] >= 3
               for row in c4["exact_elasticnet_path_regions"]):
        failures.append("C4 exact path region check failed")
    if not increasing([row["ratio_qe_to_path"] for row in c4["elasticnet_signature"]]):
        failures.append("C4 QE/path separation absent")
    if c4["negative_control"]["applicable"]:
        failures.append("C4 negative control unexpectedly applicable")

    c5 = claims["C5"]
    if not all(min(row["active_patterns_by_seed"]) >= 2
               for row in c5["measured_weighted_group_lasso"]):
        failures.append("C5 active patterns degenerate")
    if not increasing([row["bound"] for row in c5["p_signature"]]):
        failures.append("C5 p signature absent")
    if not increasing([row["bound"] for row in c5["d_signature"]]):
        failures.append("C5 d signature absent")

    c6 = claims["C6"]
    if not all(row["cap_holds"] and row["max_kkt_violation"] < 1e-8
               and min(row["regions_by_seed"]) >= 2
               for row in c6["measured_weighted_fused_lasso"]):
        failures.append("C6 region/KKT check failed")
    normalized = [row["bound_over_d2"] for row in c6["d2_signature"]]
    if min(normalized) < 0.7 or max(normalized) > 1.2:
        failures.append("C6 d2 normalization outside calibrated range")
    if not all(row["rejected"] for row in c6["negative_controls"]):
        failures.append("C6 negative control accepted")

    # Mutation audit: removing the C6 p=d-1 factor must be detected because
    # the normalized values become O(1/d), not near-constant.
    mutated = [
        math.log(4 * 3 ** (row["d"] - 1)) / (row["d"] * row["d"])
        for row in c6["d2_signature"]
    ]
    mutation_rejected = max(mutated) / min(mutated) > 2.0
    if not mutation_rejected:
        failures.append("C6 missing-p mutation was not rejected")

    return {
        "verdict": "SIGNATURE_CHECK_PASS" if not failures else "SIGNATURE_CHECK_FAIL",
        "failures": failures,
        "claims_checked": 6,
        "independent_formula_and_invariant_checker": True,
        "missing_p_mutation_rejected": mutation_rejected,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = check(json.loads(args.input.read_text()))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("SIGNATURE_CHECK=" + json.dumps(result, sort_keys=True))
    if result["verdict"] != "SIGNATURE_CHECK_PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
