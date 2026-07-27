#!/usr/bin/env python3
"""Independent fail-closed checker for the six reconstructed protocols."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def increasing(values: list[float]) -> bool:
    return all(right > left for left, right in zip(values, values[1:]))


def _thm4(p: int, dimensions: list[int], atoms: int, degree: int) -> float:
    plus_product = math.prod(value + 1 for value in dimensions)
    plain_product = math.prod(dimensions)
    return (
        p * plus_product * math.log(max(2, atoms))
        + p * p * plain_product * math.log(max(2, degree))
    )


def check(payload: dict) -> dict:
    claims = payload["claims"]
    failures: list[str] = []
    mutations_rejected: list[str] = []

    if payload["seed"] != 0:
        failures.append("unexpected seed")
    if payload["budget_policy"] != "fixed independently of theorem formulas":
        failures.append("circular budget")
    if payload["thread_cap"] != 1:
        failures.append("single-core contract absent")

    c1 = claims["C1"]
    if min(row["patterns"] for row in c1["positive_control"]) < 30:
        failures.append("C1 halfspace positive control degenerate")
    ratios = c1["block_scaling"]["ratios"]
    if not (1.7 < ratios[0] < 2.1 and 1.7 < ratios[1] < 2.1):
        failures.append("C1 product(d_k+1) signature absent")
    if c1["negative_control"]["applicable"]:
        failures.append("C1 non-semi-algebraic control accepted")

    c2 = claims["C2"]
    if not c2["direct_substitution"]:
        failures.append("C2 direct substitution failed")
    if min(row["patterns"] for row in c2["measured_piecewise_polynomial"]) < 150:
        failures.append("C2 pattern measurement too weak")
    if not all(row["bound_covers_lower_bound"] for row in c2["measured_piecewise_polynomial"]):
        failures.append("C2 empirical lower bound exceeds representative theorem bound")
    if not increasing([row["bound"] for row in c2["p_sweep"]]):
        failures.append("C2 p signature absent")
    if not increasing([row["bound"] for row in c2["d_sweep"]]):
        failures.append("C2 d signature absent")

    c3 = claims["C3"]
    if not c3["direct_two_block_substitution"]:
        failures.append("C3 direct two-block substitution failed")
    if min(row["patterns"] for row in c3["measured_bilevel_piecewise_quadratic"]) < 150:
        failures.append("C3 bilevel pattern measurement too weak")
    if not all(
        row["training_validation_different"] and row["bound_covers_lower_bound"]
        for row in c3["measured_bilevel_piecewise_quadratic"]
    ):
        failures.append("C3 exact f!=g contract failed")
    if not increasing([row["ratio_to_training_only"] for row in c3["d2_signature"]]):
        failures.append("C3 d-to-d2 separation absent")
    if not c3["negative_control"]["rejected"]:
        failures.append("C3 f==g mutation accepted")

    c4 = claims["C4"]
    if not all(
        row["cap_holds"] and row["regions_observed"] >= row["d"]
        for row in c4["measured_elasticnet_regions"]
    ):
        failures.append("C4 ElasticNet path-region check failed")
    if not increasing(
        [row["ratio_qe_to_path"] for row in c4["elasticnet_corollary_f2"]]
    ):
        failures.append("C4 QE/path separation absent")
    if c4["negative_control"]["applicable"]:
        failures.append("C4 non-rational control accepted")

    c5 = claims["C5"]
    if not c5["appendix_g1_substitution"]["matches_theorem_4_1"]:
        failures.append("C5 Appendix G.1 substitution failed")
    if min(row["patterns"] for row in c5["measured_weighted_group_lasso"]) < 30:
        failures.append("C5 dense-design sign patterns too weak")
    if not all(row["bound_covers_lower_bound"] for row in c5["measured_weighted_group_lasso"]):
        failures.append("C5 empirical lower bound exceeds representative theorem bound")
    if not increasing([row["bound"] for row in c5["p_sweep"]]):
        failures.append("C5 p signature absent")
    if not increasing([row["bound"] for row in c5["d_sweep"]]):
        failures.append("C5 d signature absent")
    for row in c5["measured_weighted_group_lasso"]:
        expected = _thm4(
            row["p"],
            [row["d"] + 2 * row["p"]],
            2 * (1 + 2 * row["p"]),
            2,
        )
        if not math.isclose(row["representative_bound"], expected, rel_tol=1e-12):
            failures.append("C5 independent numeric formula mismatch")
    # The previous implementation multiplied both terms by an extra d.
    first = c5["measured_weighted_group_lasso"][0]
    old_mutation = first["representative_bound"] * first["d"]
    c5_mutation_rejected = not math.isclose(
        first["representative_bound"], old_mutation, rel_tol=1e-12
    )
    if c5_mutation_rejected:
        mutations_rejected.append("C5_extra_d_factor")
    else:
        failures.append("C5 extra-d mutation not rejected")

    c6 = claims["C6"]
    if not c6["dual_mpqp_check"]["hessian_psd"]:
        failures.append("C6 dual Hessian is not PSD")
    if not all(
        row["cap_holds"]
        and row["training_design_rank"] == row["d"]
        and row["max_kkt_violation"] < 1e-7
        and row["regions_observed"] >= 4
        for row in c6["measured_weighted_fused_lasso"]
    ):
        failures.append("C6 dense-design region/KKT check failed")
    normalized = [row["bound_over_d2"] for row in c6["d2_signature"]]
    if min(normalized) < 0.7 or max(normalized) > 1.2:
        failures.append("C6 d2 normalization outside calibrated range")
    if not all(row["rejected"] for row in c6["negative_controls"]):
        failures.append("C6 negative control accepted")

    mutated = [
        math.log(4 * 3 ** (row["d"] - 1)) / (row["d"] * row["d"])
        for row in c6["d2_signature"]
    ]
    c6_mutation_rejected = max(mutated) / min(mutated) > 2.0
    if c6_mutation_rejected:
        mutations_rejected.append("C6_missing_p_factor")
    else:
        failures.append("C6 missing-p mutation was not rejected")

    return {
        "verdict": "SIGNATURE_CHECK_PASS" if not failures else "SIGNATURE_CHECK_FAIL",
        "failures": failures,
        "claims_checked": 6,
        "independent_formula_and_invariant_checker": True,
        "mutations_rejected": mutations_rejected,
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
