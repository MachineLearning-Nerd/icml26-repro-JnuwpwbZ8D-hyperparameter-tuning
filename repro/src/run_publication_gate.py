#!/usr/bin/env python3
"""Fail-closed publication gate for the deterministic theorem verifier."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "outputs" / "publication_gate.json")
    args = parser.parse_args()
    verifier_output = ROOT / "outputs" / "verification.json"
    claim1_output = ROOT / "outputs" / "claim1_proof.json"
    claim1_falsification_output = ROOT / "outputs" / "claim1_falsification.json"
    claims2_6_audit_output = ROOT / "outputs" / "claims2_6_counterexample_audit.json"
    subprocess.run([sys.executable, "repro/src/verify_hyperparameters.py", "--output", str(verifier_output)], cwd=ROOT, check=True)
    subprocess.run([sys.executable, "repro/src/verify_claim1_proof.py", "--output", str(claim1_output)], cwd=ROOT, check=True)
    subprocess.run(
        [sys.executable, "repro/src/audit_claim1_falsification.py", "--output", str(claim1_falsification_output)],
        cwd=ROOT,
        check=True,
    )
    subprocess.run(
        [sys.executable, "repro/src/audit_claims2_6_counterexamples.py", "--output", str(claims2_6_audit_output)],
        cwd=ROOT,
        check=True,
    )
    subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "repro/tests", "-v"], cwd=ROOT, check=True)
    verification = json.loads(verifier_output.read_text())
    claim1 = json.loads(claim1_output.read_text())
    claim1_falsification = json.loads(claim1_falsification_output.read_text())
    claims2_6_audit = json.loads(claims2_6_audit_output.read_text())
    passed = (
        verification["all_claims_passed"]
        and len(verification["claims"]) == 6
        and claim1["verdict"] == "VERIFIED"
        and len(claim1["mutations_rejected"]) == 3
        and claim1_falsification["falsification_succeeded"] is False
        and claim1_falsification["main_claim_status"] == "VERIFIED_BY_SYMBOLIC_CERTIFICATE"
        and claims2_6_audit["verdict"] == "AUDIT_COMPLETE"
        and all(not row["falsification_succeeded"] for row in claims2_6_audit["claims"].values())
        and claims2_6_audit["claims"]["C6"]["status"] == "PROOF_DOMAIN_GAP"
    )
    payload = {
        "paper": "JnuwpwbZ8D",
        "tests_passed": True,
        "claims_passed": len(verification["claims"]),
        "current_exact_claims": {"C1": claim1["verdict"]},
        "publication_gate_passed": passed,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, sort_keys=True))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
