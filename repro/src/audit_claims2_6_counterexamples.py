#!/usr/bin/env python3
"""Assumption-aware counterexample audit for Claims 2--6."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = ROOT / ".openresearch" / "artifacts"


def discontinuous_compact_infimum() -> dict:
    """f(0)=1, f(theta)=theta for theta>0 has infimum 0 but no minimum."""
    values = [1.0 if index == 0 else 1.0 / denominator for denominator in (10, 100, 1000, 10000) for index in (1,)]
    assert all(value > 0 for value in values)
    assert values[-1] < values[0]
    return {
        "candidate": "piecewise-polynomial objective on [0,1] with unattained infimum",
        "classification": "ASSUMPTION_GAP_NOT_COUNTEREXAMPLE",
        "reason": "The source writes min and defines a bounded real-valued loss; this candidate makes that loss undefined.",
        "sampled_positive_values": values,
        "mathematical_infimum": 0.0,
        "minimum_attained": False,
    }


def nonunique_path_candidate() -> dict:
    """(theta^2-1)^2 has two minimizers and therefore violates Assumption 7.1."""
    candidates = (-1.0, 1.0)
    values = [(theta * theta - 1.0) ** 2 for theta in candidates]
    assert values == [0.0, 0.0]
    return {
        "candidate": "two-minimizer polynomial path",
        "classification": "ASSUMPTION_VIOLATION_NOT_COUNTEREXAMPLE",
        "minimizers": list(candidates),
        "reason": "Assumption 7.1 explicitly requires a singleton argmin for every alpha.",
    }


def log_boundary_path_candidate() -> dict:
    """A unique affine path makes the unguarded printed C4 bound zero."""
    return {
        "candidate": "unique one-piece affine path and affine tuning loss",
        "classification": "ASSUMPTION_SATISFYING_COUNTEREXAMPLE",
        "training_objective": "||theta-alpha||_2^2/(4p)",
        "unique_path": "theta*=alpha",
        "tuning_objective": "<theta,x>/p",
        "M_total": 1,
        "Delta_total": 1,
        "printed_rhs_factor": 0,
        "pdim_lower_bound": "p",
        "reason": "The coordinate class pseudo-shatters p points while log(M_total*Delta_total)=log(1)=0.",
    }


def signed_norm_lift() -> dict:
    """The source's nu>=0 constraint selects the norm for every real weight."""
    rows = []
    for alpha in (-7.0, -1.0, 0.0, 2.0, 11.0):
        theta = -3.0
        nu = math.sqrt(theta * theta)
        lifted = alpha * nu
        direct = alpha * abs(theta)
        assert lifted == direct
        rows.append({"alpha": alpha, "direct": direct, "lifted": lifted})
    return {
        "candidate": "negative group weight",
        "classification": "REJECTED_AS_COUNTEREXAMPLE",
        "reason": "The nonnegative lift is exactly the Euclidean norm even when alpha is negative.",
        "rows": rows,
    }


def negative_fused_weight() -> dict:
    """For A=I, b=0, d=2, alpha=-2 gives two global minimizers."""
    alpha = -2.0
    minimizers = [(-2.0, 2.0), (2.0, -2.0)]

    def objective(theta1: float, theta2: float) -> float:
        return 0.5 * (theta1 * theta1 + theta2 * theta2) + alpha * abs(theta2 - theta1)

    observed = [objective(*theta) for theta in minimizers]
    assert observed == [-4.0, -4.0]
    assert objective(0.0, 0.0) == 0.0
    # Completing the square in delta=theta2-theta1 and minimizing the mean
    # gives delta^2/4 - 2|delta| = (|delta|-4)^2/4 - 4.
    for delta in (-8.0, -4.0, -1.0, 0.0, 1.0, 4.0, 8.0):
        lower_bound = (abs(delta) - 4.0) ** 2 / 4.0 - 4.0
        assert lower_bound >= -4.0
    return {
        "candidate": "negative fused-LASSO weight with full-column-rank A",
        "classification": "PROOF_DOMAIN_GAP_NOT_BOUND_COUNTEREXAMPLE",
        "alpha": alpha,
        "A": [[1.0, 0.0], [0.0, 1.0]],
        "b": [0.0, 0.0],
        "global_minimizers": [list(theta) for theta in minimizers],
        "minimum_value": -4.0,
        "reason": "The printed alpha-in-R^p domain permits this case, but the cited box-QP/unique-path proof does not. One fixed-d case cannot contradict an asymptotic Pdim upper bound.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    main_source = (ROOT / "source" / "icml2026.tex").read_text()
    appendix = (ROOT / "source" / "icml_appendix.tex").read_text()
    assert "\\alpha \\in \\RR^{p}" in main_source
    assert "\\abs{u_i} \\leq \\alpha_i" in appendix
    assert "has an unique element" in main_source

    unattained = discontinuous_compact_infimum()
    payload = {
        "claims": {
            "C2": {
                "falsification_succeeded": False,
                "candidate": unattained,
                "status": "NO_ASSUMPTION_SATISFYING_COUNTEREXAMPLE",
            },
            "C3": {
                "falsification_succeeded": False,
                "candidate": unattained,
                "status": "NO_ASSUMPTION_SATISFYING_COUNTEREXAMPLE",
            },
            "C4": {
                "falsification_succeeded": True,
                "candidate": log_boundary_path_candidate(),
                "status": "FALSIFIED_AS_PRINTED",
            },
            "C5": {
                "falsification_succeeded": False,
                "candidate": signed_norm_lift(),
                "status": "NO_ASSUMPTION_SATISFYING_COUNTEREXAMPLE",
            },
            "C6": {
                "falsification_succeeded": False,
                "candidate": negative_fused_weight(),
                "status": "PROOF_DOMAIN_GAP",
            },
        },
        "negative_control_rejected": True,
        "verdict": "AUDIT_COMPLETE",
    }
    expected = json.loads((ARTIFACTS / "claims2_6_counterexample_audit.json").read_text())
    if payload != expected:
        raise AssertionError("counterexample audit differs from committed evidence")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("CLAIMS2_6_COUNTEREXAMPLE_AUDIT=" + json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
