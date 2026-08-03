#!/usr/bin/env python3
"""Fail-closed publication gate for the deterministic theorem verifier."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def run_stage(name: str, command: list[str]) -> None:
    displayed = ["python", *command[1:]] if command and command[0] == sys.executable else command
    rendered = " ".join(displayed)
    print(f"GATE_STAGE_START name={name} command={rendered}", flush=True)
    subprocess.run(command, cwd=ROOT, check=True)
    print(f"GATE_STAGE_PASS name={name}", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "outputs" / "publication_gate.json")
    args = parser.parse_args()
    verifier_output = ROOT / "outputs" / "verification.json"
    boundary_output = ROOT / "outputs" / "log_boundary_counterexamples.json"
    boundary_check_output = ROOT / "outputs" / "log_boundary_counterexamples_check.json"
    visibility_output = ROOT / "outputs" / "evaluator_visibility.json"
    universal_proof_output = ROOT / "outputs" / "universal_theorem_proofs.json"
    universal_audit_output = ROOT / "outputs" / "universal_theorem_proofs_audit.json"
    run_stage(
        "historical_regression",
        [sys.executable, "repro/src/verify_hyperparameters.py", "--output", str(verifier_output)],
    )
    run_stage(
        "claims_1_and_4_log_boundary_counterexamples",
        [
            sys.executable,
            "repro/src/audit_log_boundary_counterexamples.py",
            "--output",
            str(boundary_output),
            "--max-p",
            "8",
        ],
    )
    run_stage(
        "independent_log_boundary_checker",
        [
            sys.executable,
            "repro/src/check_log_boundary_counterexamples.py",
            "--input",
            str(boundary_output),
            "--output",
            str(boundary_check_output),
        ],
    )
    run_stage(
        "six_source_exact_theorem_chain_audits",
        [
            sys.executable,
            "repro/src/verify_universal_theorem_chains.py",
            "--output",
            str(universal_proof_output),
        ],
    )
    run_stage(
        "independent_theorem_chain_audit",
        [
            sys.executable,
            "repro/src/audit_universal_theorem_chains.py",
            "--input",
            str(universal_proof_output),
            "--output",
            str(universal_audit_output),
        ],
    )
    run_stage(
        "evaluator_visibility_audit",
        [sys.executable, "repro/src/audit_evaluator_visibility.py", "--output", str(visibility_output)],
    )
    run_stage(
        "marimo_notebook_check",
        [sys.executable, "-m", "marimo", "check", "notebooks/theorem_certificates.py"],
    )
    run_stage(
        "unit_tests",
        [sys.executable, "-m", "unittest", "discover", "-s", "repro/tests", "-v"],
    )
    verification = json.loads(verifier_output.read_text())
    boundary = json.loads(boundary_output.read_text())
    boundary_check = json.loads(boundary_check_output.read_text())
    visibility = json.loads(visibility_output.read_text())
    universal_proofs = json.loads(universal_proof_output.read_text())
    universal_audit = json.loads(universal_audit_output.read_text())
    passed = (
        verification["all_claims_passed"]
        and len(verification["claims"]) == 6
        and boundary["classification"] == "LITERAL_FALSIFICATION_AS_PRINTED"
        and boundary["claims"]["C1"]["verdict"] == "FALSIFIED_AS_PRINTED"
        and boundary["claims"]["C4"]["verdict"] == "FALSIFIED_AS_PRINTED"
        and boundary["finite_sweeps_used_as_proof"] == 0
        and boundary_check["verdict"] == "INDEPENDENT_CHECK_PASS"
        and universal_proofs["all_universal_proof_chains_passed"]
        and universal_proofs["finite_parameter_sweeps_used_as_proof"] == 0
        and universal_audit["independent_audit_passed"]
        and universal_audit["independent_checks"] == 42
        and visibility["verdict"] == "EVALUATOR_VISIBLE_GATE_PASS"
        and visibility["missing_cells"] == 0
    )
    payload = {
        "paper": "JnuwpwbZ8D",
        "tests_passed": True,
        "claims_passed": len(verification["claims"]),
        "current_exact_claims": {
            claim: result["verdict"]
            for claim, result in universal_proofs["claims"].items()
        },
        "log_boundary_counterexamples": {
            "claims": ["C1", "C4"],
            "checker": boundary_check["verdict"],
            "labelings_recomputed": boundary_check["labelings_recomputed"],
            "finite_sweeps_used_as_proof": 0,
        },
        "universal_theorem_proofs": {
            "claims": universal_proofs["claim_count"],
            "mutations_rejected": universal_proofs["total_mutations_rejected"],
            "independent_checks": universal_audit["independent_checks"],
            "finite_sweeps_used_as_proof": 0,
            "audit_passed": universal_audit["independent_audit_passed"],
        },
        "publication_gate_passed": passed,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, sort_keys=True))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
