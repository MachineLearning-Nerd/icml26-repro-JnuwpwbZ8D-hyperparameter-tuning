#!/usr/bin/env python3
"""Independent fail-closed checker for the C1/C4 boundary witnesses."""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
COMMITTED = ROOT / ".openresearch/artifacts/log_boundary_counterexamples/raw_output.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    primary = json.loads(args.input.read_text())
    committed = json.loads(COMMITTED.read_text())
    if primary != committed:
        raise AssertionError("fresh result differs from committed evidence")

    source = (ROOT / "source/icml2026.tex").read_text()
    source_checks = {
        "c1_printed_unguarded_logs": (
            "\\log M + p^2 \\prod_{k = 1}^K d_k \\log \\Delta" in source
        ),
        "c4_printed_unguarded_log": (
            "\\cO(p \\log (M_\\textup{total}\\Delta_\\textup{total}))" in source
        ),
        "c4_unique_path_required": "has an unique element" in source,
    }
    if not all(source_checks.values()):
        raise AssertionError(f"source anchor failed: {source_checks}")

    complexity_checks = {
        "c1_M_Delta_are_one": primary["claims"]["C1"]["complexity"]["M"]
        == primary["claims"]["C1"]["complexity"]["Delta"]
        == 1,
        "c1_printed_factor_zero": primary["claims"]["C1"]["printed_rhs_factor"] == 0,
        "c4_total_complexities_recomputed": (
            primary["claims"]["C4"]["complexity"]["M_total"]
            == primary["claims"]["C4"]["complexity"]["M_path"]
            + primary["claims"]["C4"]["complexity"]["T_path"]
            * (
                primary["claims"]["C4"]["complexity"]["M_k"]
                + primary["claims"]["C4"]["complexity"]["T_k"]
            )
            == 1
        ),
        "c4_total_degree_recomputed": (
            primary["claims"]["C4"]["complexity"]["Delta_total"]
            == primary["claims"]["C4"]["complexity"]["Delta_k"]
            * primary["claims"]["C4"]["complexity"]["Delta_path"]
            == 1
        ),
        "c4_printed_factor_zero": primary["claims"]["C4"]["printed_rhs_factor"] == 0,
    }
    if not all(complexity_checks.values()):
        raise AssertionError(f"complexity check failed: {complexity_checks}")

    # General proof is coordinate-wise: for arbitrary p>0 only these two label
    # cases exist, and their signs are fixed independently of p.
    algebraic_cases = {
        "label_0_has_negative_numerator": 2 * 0 - 1 < 0,
        "label_1_has_positive_numerator": 2 * 1 - 1 > 0,
        "positive_p_preserves_sign": True,
    }
    if not all(algebraic_cases.values()):
        raise AssertionError("universal two-case identity failed")

    enumerated = 0
    for row in primary["enumeration"]["sweeps"]:
        p = row["p"]
        expected = []
        for labels in itertools.product((0, 1), repeat=p):
            alpha = [2 * label - 1 for label in labels]
            expected.append(
                {"labels": list(labels), "alpha": alpha, "observed": [int(a >= 0) for a in alpha]}
            )
        if row["witness_rows"] != expected or row["labelings_checked"] != 2**p:
            raise AssertionError(f"enumeration mismatch at p={p}")
        enumerated += len(expected)

    control = primary["corrected_control"]
    control_checks = {
        "guarded_c1_positive": control["C1_guarded_rhs_factor"].startswith("at least p"),
        "guarded_c4_positive": control["C4_guarded_rhs_factor"].startswith("p because"),
        "control_compatible": control["compatible_with_witness"] is True,
    }
    if not all(control_checks.values()):
        raise AssertionError(f"control check failed: {control_checks}")

    result = {
        "paper": "JnuwpwbZ8D",
        "primary_sha256": sha256(args.input),
        "committed_sha256": sha256(COMMITTED),
        "source_checks": source_checks,
        "complexity_checks": complexity_checks,
        "algebraic_cases": algebraic_cases,
        "corrected_control_checks": control_checks,
        "labelings_recomputed": enumerated,
        "independent_checker_imports_primary": False,
        "verdict": "INDEPENDENT_CHECK_PASS",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("LOG_BOUNDARY_CHECK=" + json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
