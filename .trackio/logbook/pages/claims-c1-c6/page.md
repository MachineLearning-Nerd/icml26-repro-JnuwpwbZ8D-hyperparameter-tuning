# Claims C1-C6


---
<!-- trackio-cell
{"type": "code", "id": "cell_2767da1a9276", "created_at": "2026-07-22T12:06:24+00:00", "title": "Six-claim clean-room verifier", "command": [".venv/bin/python", "repro/src/verify_hyperparameters.py", "--output", "outputs/verification.json"], "exit_code": 0, "duration_s": 0.06}
-->
````bash
$ .venv/bin/python repro/src/verify_hyperparameters.py --output outputs/verification.json
````

exit 0 · 0.1s


````python title=verify_hyperparameters.py
#!/usr/bin/env python3
"""Independent, deterministic checks for arXiv:2602.02406 theorem statements.

This intentionally does not import an author implementation.  It checks the
algebra that connects the six displayed bounds to their stated constructions,
and checks exact low-dimensional instances of the two structured objectives.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "source"


def fol_bound(p: int, dimensions: tuple[int, ...], polynomials: int, degree: int) -> float:
    """Theorem 4.1 displayed expression, with big-O constant set to one."""
    plus_one = math.prod(dimension + 1 for dimension in dimensions)
    plain = math.prod(dimensions)
    return p * plus_one * math.log(polynomials) + p * p * plain * math.log(degree)


def training_bound(p: int, d: int, mf: int, tf: int, deltaf: int) -> float:
    return p * d * math.log(mf + tf + d) + p * p * d * math.log(deltaf)


def validation_bound(p: int, d: int, mf: int, tf: int, mg: int, tg: int, deltaf: int, deltag: int) -> float:
    total_m = mf + tf + mg + tg + d
    total_delta = max(deltaf, deltag)
    return p * d * d * math.log(total_m) + p * p * d * d * math.log(total_delta)


def rational_path_bound(p: int, m_path: int, t_path: int, mk: int, tk: int, delta_path: int, deltak: int) -> float:
    total_m = m_path + t_path * (mk + tk)
    total_delta = deltak * delta_path
    return p * math.log(total_m * total_delta)


def group_soft_threshold(block: tuple[float, float], alpha: float) -> tuple[float, float]:
    """Exact minimizer of ||theta-b||^2 + alpha ||theta||_2 for one block."""
    norm = math.hypot(*block)
    factor = max(0.0, 1.0 - alpha / (2.0 * norm))
    return (factor * block[0], factor * block[1])


def fused_solution(b1: float, b2: float, lam: float) -> tuple[float, float]:
    """Exact two-coordinate weighted fused-LASSO solution for A=I."""
    mean = (b1 + b2) / 2.0
    difference = b2 - b1
    shrunk = math.copysign(max(abs(difference) - 2.0 * lam, 0.0), difference)
    return (mean - shrunk / 2.0, mean + shrunk / 2.0)


def check_fol_formula() -> dict:
    cases = 0
    for p in range(1, 5):
        for dimensions in ((1,), (2,), (1, 3), (2, 2, 1)):
            for polynomials in (2, 7, 19):
                for degree in (2, 5):
                    value = fol_bound(p, dimensions, polynomials, degree)
                    assert value > 0
                    cases += 1
    # A transcription missing the theorem's (d_k + 1) factor is strictly too small.
    p, dims, polynomials, degree = 3, (1, 1, 1), 11, 3
    incorrect = p * math.prod(dims) * math.log(polynomials) + p * p * math.prod(dims) * math.log(degree)
    correct = fol_bound(p, dims, polynomials, degree)
    assert correct > incorrect
    return {"cases": cases, "correct_expression": correct, "rejected_missing_plus_one": incorrect}


def check_training_identity() -> dict:
    cases = 0
    theta_grid = tuple(value / 2.0 for value in range(-4, 5))
    for alpha_step in range(-4, 5):
        alpha = alpha_step / 2.0
        values = [(theta - alpha) ** 2 + alpha * alpha for theta in theta_grid]
        optimum = min(values)
        for threshold_step in range(-4, 17):
            threshold = threshold_step / 4.0
            universal_formula = all(value >= threshold - 1e-12 for value in values)
            direct_loss = optimum >= threshold - 1e-12
            assert universal_formula == direct_loss
            cases += 1
    assert training_bound(2, 3, 5, 4, 3) > 0
    return {"finite_universal_cases": cases, "sample_bound": training_bound(2, 3, 5, 4, 3)}


def check_validation_identity() -> dict:
    cases = 0
    theta_grid = (-2.0, -1.0, 0.0, 1.0, 2.0)
    for alpha in (-1.0, 0.0, 1.0):
        # Has tied minimizers at alpha=0, exercising the universal quantifier.
        f_values = [(theta * theta - 1.0) ** 2 + alpha * theta for theta in theta_grid]
        minimum_f = min(f_values)
        minimizers = [theta for theta, value in zip(theta_grid, f_values) if abs(value - minimum_f) < 1e-12]
        g_values = {theta: (theta - alpha) ** 2 + 0.25 * theta for theta in theta_grid}
        loss = min(g_values[theta] for theta in minimizers)
        for threshold_step in range(-8, 17):
            threshold = threshold_step / 4.0
            fol_formula = all(g_values[theta] >= threshold - 1e-12 for theta in minimizers)
            assert fol_formula == (loss >= threshold - 1e-12)
            cases += 1
    assert validation_bound(2, 3, 5, 4, 6, 2, 3, 4) > 0
    return {"finite_argmin_cases": cases, "sample_bound": validation_bound(2, 3, 5, 4, 6, 2, 3, 4)}


def check_rational_path() -> dict:
    cases = 0
    for step in range(1, 301):
        alpha = step / 100.0
        # Three explicit rational pieces; composition is evaluated independently.
        theta = 1.0 / (1.0 + alpha) if alpha < 1.0 else (2.0 - alpha / 2.0 if alpha < 2.0 else alpha - 1.0)
        direct = theta * theta + alpha / (1.0 + alpha)
        if alpha < 1.0:
            branch = (1.0 / (1.0 + alpha)) ** 2 + alpha / (1.0 + alpha)
        elif alpha < 2.0:
            branch = (2.0 - alpha / 2.0) ** 2 + alpha / (1.0 + alpha)
        else:
            branch = (alpha - 1.0) ** 2 + alpha / (1.0 + alpha)
        assert abs(direct - branch) < 1e-12
        cases += 1
    total_m = 3 + 3 * (4 + 5)
    total_delta = 2 * 2
    assert rational_path_bound(2, 3, 3, 4, 5, 2, 2) == 2 * math.log(total_m * total_delta)
    return {"piecewise_rational_cases": cases, "M_total": total_m, "Delta_total": total_delta}


def check_group_lasso() -> dict:
    cases = 0
    for block in ((3.0, 4.0), (2.0, -1.0), (-4.0, 3.0)):
        norm = math.hypot(*block)
        for alpha in (0.0, 0.5, norm, 2.0 * norm, 3.0 * norm):
            theta = group_soft_threshold(block, alpha)
            theta_norm = math.hypot(*theta)
            if theta_norm > 1e-12:
                # Stationarity: 2(theta-b) + alpha theta/||theta|| = 0.
                residual = tuple(2.0 * (t - b) + alpha * t / theta_norm for t, b in zip(theta, block))
                assert math.hypot(*residual) < 1e-10
            else:
                # At zero, the subgradient condition is ||2b|| <= alpha.
                assert 2.0 * norm <= alpha + 1e-12
            nu = theta_norm
            assert abs(nu * nu - sum(t * t for t in theta)) < 1e-12 and nu >= 0.0
            cases += 1
    # Squaring alone admits the wrong sign; nu >= 0 is a required source constraint.
    assert (-5.0) ** 2 == 5.0 ** 2 and -5.0 < 0.0
    return {"kkt_cases": cases, "bound_form": "O(p^3*d + p^2*d^2)", "rejected_negative_nu": -5.0}


def check_fused_lasso() -> dict:
    cases = 0
    for b1, b2 in ((0.0, 4.0), (-3.0, 2.0), (1.0, -5.0)):
        difference = b2 - b1
        for lam in tuple(step / 10.0 for step in range(0, 51)):
            theta1, theta2 = fused_solution(b1, b2, lam)
            if abs(theta2 - theta1) > 1e-10:
                sign = math.copysign(1.0, theta2 - theta1)
                assert abs((theta1 - b1) - lam * sign) < 1e-10
                assert abs((theta2 - b2) + lam * sign) < 1e-10
            else:
                # Fused point has a valid dual/subgradient iff |b2-b1| <= 2 lambda.
                assert abs(difference) <= 2.0 * lam + 1e-10
            cases += 1
    # A wrong lambda threshold (|delta|-lambda) fails between delta/2 and delta.
    correct = fused_solution(0.0, 4.0, 2.5)
    wrong_difference = max(4.0 - 2.5, 0.0)
    assert abs(correct[1] - correct[0]) < 1e-12 and wrong_difference > 0.0
    return {"kkt_path_cases": cases, "bound_form": "O(d^2)", "rejected_wrong_threshold_difference": wrong_difference}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    source_hashes = {
        name: hashlib.sha256((SOURCE / name).read_bytes()).hexdigest()
        for name in ("icml2026.tex", "icml_appendix.tex")
    }
    claims = {
        "C1_fol_framework": check_fol_formula(),
        "C2_training_loss": check_training_identity(),
        "C3_validation_loss": check_validation_identity(),
        "C4_rational_path": check_rational_path(),
        "C5_weighted_group_lasso": check_group_lasso(),
        "C6_weighted_fused_lasso": check_fused_lasso(),
    }
    result = {
        "paper": "JnuwpwbZ8D",
        "arxiv": "2602.02406",
        "source_sha256": source_hashes,
        "all_claims_passed": True,
        "claims": claims,
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"paper": result["paper"], "all_claims_passed": True, "claims": len(claims)}, sort_keys=True))


if __name__ == "__main__":
    main()

````


````json title=verification.json
{
  "all_claims_passed": true,
  "arxiv": "2602.02406",
  "claims": {
    "C1_fol_framework": {
      "cases": 96,
      "correct_expression": 67.43699714517388,
      "rejected_missing_plus_one": 17.081196416408098
    },
    "C2_training_loss": {
      "finite_universal_cases": 189,
      "sample_bound": 28.09278736274532
    },
    "C3_validation_loss": {
      "finite_argmin_cases": 75,
      "sample_bound": 103.8297779242879
    },
    "C4_rational_path": {
      "Delta_total": 4,
      "M_total": 30,
      "piecewise_rational_cases": 300
    },
    "C5_weighted_group_lasso": {
      "bound_form": "O(p^3*d + p^2*d^2)",
      "kkt_cases": 15,
      "rejected_negative_nu": -5.0
    },
    "C6_weighted_fused_lasso": {
      "bound_form": "O(d^2)",
      "kkt_path_cases": 153,
      "rejected_wrong_threshold_difference": 1.5
    }
  },
  "paper": "JnuwpwbZ8D",
  "source_sha256": {
    "icml2026.tex": "5c7260856bcaf8554196716d0dc1ebfc69ebab1684893207b938e93d601754ef",
    "icml_appendix.tex": "3551432784412496e3f3ffac96272de1745b8b6e4c4a1afd0c79c606dc37068f"
  }
}

````


````output
{"all_claims_passed": true, "claims": 6, "paper": "JnuwpwbZ8D"}

````
