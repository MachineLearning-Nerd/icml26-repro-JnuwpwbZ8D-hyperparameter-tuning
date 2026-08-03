#!/usr/bin/env python3
"""Construct exact boundary counterexamples to the printed C1 and C4 bounds."""
from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def shattered_labelings(p: int) -> list[dict[str, list[int]]]:
    """Enumerate the universal witness alpha_i=2*y_i-1 on x_i=e_i."""
    rows = []
    for labels in itertools.product((0, 1), repeat=p):
        alpha = [2 * label - 1 for label in labels]
        observed = [int(value >= 0) for value in alpha]
        if observed != list(labels):
            raise AssertionError("shattering witness failed")
        rows.append({"labels": list(labels), "alpha": alpha, "observed": observed})
    return rows


def build_payload(max_p: int) -> dict:
    if max_p < 1:
        raise ValueError("max_p must be positive")
    sweeps = []
    for p in range(1, max_p + 1):
        rows = shattered_labelings(p)
        sweeps.append(
            {
                "p": p,
                "labelings_checked": len(rows),
                "all_labelings_realized": len(rows) == 2**p,
                "pdim_lower_bound": p,
                "witness_rows": rows,
            }
        )

    common = {
        "parameter_domain": "alpha in [-1,1]^p",
        "instances": "x_i=e_i for i=1,...,p",
        "thresholds": "t_i=0",
        "loss": "ell_alpha(x)=<alpha,x>/p",
        "universal_witness": "for y in {0,1}^p choose alpha_i=2*y_i-1",
        "universal_identity": "I[ell_alpha(e_i)>=0]=I[(2*y_i-1)/p>=0]=y_i for every p>=1",
        "consequence": "the p coordinate instances are pseudo-shattered, so Pdim(L)>=p",
    }
    return {
        "paper": "JnuwpwbZ8D",
        "source": "arXiv:2602.02406",
        "classification": "LITERAL_FALSIFICATION_AS_PRINTED",
        "finite_sweeps_used_as_proof": 0,
        "algebraic_certificate": common,
        "claims": {
            "C1": {
                "verdict": "FALSIFIED_AS_PRINTED",
                "source_anchor": "source/icml2026.tex:390-400",
                "fol": "(exists theta in R) [<alpha,x>/p-t >= 0]",
                "vacuous_quantifier_validity": "Definition 3.1 imposes no requirement that a quantified variable occur in an atom",
                "complexity": {"K": 1, "dimensions": [1], "M": 1, "Delta": 1},
                "printed_rhs_factor": 0,
                "printed_rhs_reason": "log(M)=log(Delta)=log(1)=0",
                "contradiction_family": "Pdim(L)>=p>0 for every p>=1 while the printed asymptotic expression is identically zero",
            },
            "C4": {
                "verdict": "FALSIFIED_AS_PRINTED",
                "source_anchor": "source/icml2026.tex:536-555",
                "training_objective": "f_x(alpha,theta)=||theta-alpha||_2^2/(4p)",
                "unique_path": "theta*(x,alpha)=alpha",
                "tuning_objective": "k_x(alpha,theta)=<theta,x>/p",
                "complexity": {
                    "M_path": 0,
                    "T_path": 1,
                    "Delta_path": 1,
                    "M_k": 0,
                    "T_k": 1,
                    "Delta_k": 1,
                    "M_total": 1,
                    "Delta_total": 1,
                },
                "printed_rhs_factor": 0,
                "printed_rhs_reason": "log(M_total*Delta_total)=log(1)=0",
                "assumption_checks": {
                    "bounded_training_objective_on_boxes": True,
                    "bounded_tuning_loss": True,
                    "unique_minimizer_for_every_alpha": True,
                    "one_affine_path_piece": True,
                    "one_affine_tuning_piece": True,
                },
                "contradiction_family": "Pdim(L)>=p>0 for every p>=1 while the printed asymptotic expression is identically zero",
            },
        },
        "corrected_control": {
            "mutation": "replace each unguarded log(z) at the complexity boundary by log_2(1+z)",
            "C1_guarded_rhs_factor": "at least p because log_2(1+M)=1",
            "C4_guarded_rhs_factor": "p because log_2(1+M_total*Delta_total)=1",
            "compatible_with_witness": True,
            "purpose": "shows the contradiction is specifically caused by the missing positive log guard",
        },
        "enumeration": {
            "scope": f"diagnostic only, p=1,...,{max_p}; the two-case algebraic identity is the proof",
            "total_labelings_checked": sum(row["labelings_checked"] for row in sweeps),
            "sweeps": sweeps,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-p", type=int, default=8)
    args = parser.parse_args()
    payload = build_payload(args.max_p)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    summary = {
        "claims": {claim: row["verdict"] for claim, row in payload["claims"].items()},
        "finite_sweeps_used_as_proof": 0,
        "labelings_checked": payload["enumeration"]["total_labelings_checked"],
        "verdict": payload["classification"],
    }
    print("LOG_BOUNDARY_COUNTEREXAMPLES=" + json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
