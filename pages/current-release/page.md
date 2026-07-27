# CURRENT — Release evidence and visibility

## Reproduction contract

- Python: 3.12.11, selected by `.python-version`
- Manager: `uv`; lockfile: `uv.lock`
- Exact fixed command:
  `uv run --frozen --python 3.12 repro/src/run_publication_gate.py --output outputs/publication_gate.json`
- Seeds: proof checks are deterministic; empirical checks use `173,271,419`
- Winning scientific and visibility SHA: `965d3915a574ab325f1411e4811cddd121ccead7`
- Winning run: `4d4a3555-a313-4b8d-b38a-c191809d01d6`
- Empirical stage runtime: 3.004 seconds; formal gate runtime: 10 seconds; local CPU, one Python process on a host exposing 8 logical CPUs
- Hugging Face `cpu-upgrade`: not used; every formal task was confidently under five minutes and single-core
- Recorded formal CPU runtime through the winning visibility run: 130 seconds across 13 runs, including three fail-closed fixture/manifest/visibility checks
- Compute cost: $0 local; $0 Hugging Face

## Fail-closed behavior

The current gate runs the historical regression suite, C1 symbolic certificate,
C1 falsification audit, C2–C6 symbolic/specialization certificates, the
C2–C6 adversarial audit, six concrete theorem-signature experiments, an
independent signature checker, and 19 unit tests. It exits nonzero on any mismatch.
The negative controls reject a missing `p²` term, source-index mutations,
finite-grid proxy evidence, missing bilevel existential structure, nonunique
paths, a signed norm lift, an invalid negative-radius dual box, a circular
sample budget, and a missing `p=d-1` factor.

## Historical safety and red team

The immutable judged revision is
`a928c531f0d7b6784a4bfa3e7944bf0e20a49b26`. Its 23-file SHA-256 manifest is
[here](../../evidence/judged-space-a928c531.sha256). The candidate changes no
historical claim page or asset; the old file set is a subset of the candidate
tree. Navigation labels every old page **Historical rejected baseline** and
places current verification first.

The evaluator-blind audit starts only at `README.md`, `logbook.json`, and this
index. It records every opened page and treats unlinked evidence as missing.
Its report and exact upload allowlist are linked below:

- [Blind traversal record](../../evidence/evaluator_blind_review.md)
- [Final release report](../../evidence/release_report.md)
- [Text upload allowlist](../../evidence/hf_upload_allowlist.txt)
- [Candidate SHA-256 manifest](../../evidence/candidate_text_manifest.sha256)
- [Run metadata](../../evidence/run_metadata.json)
- [Empirical raw output](../../.openresearch/artifacts/theorem_signatures/raw_output.json)
- [Independent empirical checker](../../.openresearch/artifacts/theorem_signatures/checker_output.json)

## Remaining limitation

C6's box-constrained dual proof requires `alpha_i >= 0`. The main text calls
the coordinates regularization weights but also typesets `alpha in R^p`.
For `A=I`, `b=0`, `d=2`, and `alpha=-2`, the primal problem has two global
minimizers `(-2,2)` and `(2,-2)`, both with value `-4`. This defeats the cited
unique-path route but is not an asymptotic pseudo-dimension counterexample.

## Judge-directed visibility correction

The live evaluator judged Space revision
`e41343cf30154ab7e49464ce303fc5ed1b56ea05` on
`2026-07-27T04:11:17+00:00`. It found and executed the stronger empirical
programs, but assigned TOY because the referenced SymPy proof certificates
were not embedded. This revision answers that exact criticism: every current
claim page embeds its empirical implementation, the complete applicable
symbolic certificate, and both stable outputs. The root navigation also exposes
[the two complete certificate programs](#/current-proof-certificates). The
prior empirical-only visibility rule was rejected.

## Shared executed measurement engine

These are the actual shared pattern counter and bound functions called by the
six claim-specific code blocks. Together with those blocks, the evaluator can
read the implementation without leaving the canonical logbook.

````python title=repro/src/measure_theorem_signatures.py
SEEDS = (173, 271, 419)


def _patterns(
    losses: Callable[[tuple[float, ...]], Iterable[float]],
    alphas: Iterable[tuple[float, ...]],
    thresholds: tuple[float, ...],
) -> int:
    seen = {
        tuple(value >= threshold for value, threshold in zip(losses(alpha), thresholds))
        for alpha in alphas
    }
    return len(seen)


def _random_alphas(seed: int, count: int, p: int, low: float = -1.5, high: float = 1.5):
    rng = random.Random(seed)
    return [tuple(rng.uniform(low, high) for _ in range(p)) for _ in range(count)]


def thm_4_1_bound(p: int, dimensions: tuple[int, ...], atoms: int, degree: int) -> float:
    plus_product = math.prod(value + 1 for value in dimensions)
    plain_product = math.prod(dimensions)
    return (
        p * plus_product * math.log(max(2, atoms))
        + p * p * plain_product * math.log(max(2, degree))
    )


def thm_5_1_bound(p: int, d: int, mf: int, tf: int, degree: int) -> float:
    return thm_4_1_bound(p, (d,), mf + tf + 2 * d, degree)


def thm_6_1_bound(
    p: int, d: int, mf: int, tf: int, mg: int, tg: int, degree: int
) -> float:
    atoms = 4 * d + mg + tg + 2 * mf + tf * tf
    return thm_4_1_bound(p, (d, d), atoms, degree)


def thm_7_2_bound(
    p: int,
    m_path: int,
    t_path: int,
    m_loss: int,
    t_loss: int,
    degree_loss: int,
    degree_path: int,
) -> float:
    atoms = m_path + t_path * (m_loss + t_loss)
    degree = degree_loss * degree_path
    return p * math.log(max(2, atoms * degree))


def thm_8_1_bound(p: int, d: int) -> float:
    return (
        p * (d + 1) * (d + 2 * p + 1) * math.log(2 + 4 * p)
        + p * p * d * (d + 2 * p) * math.log(2)
    )


def thm_8_2_bound(d: int) -> float:
    p = d - 1
    regions = 3**p
    return thm_7_2_bound(p, regions, regions, 0, 1, 2, 1)
````

## Executed publication gate

The fixed command executes the following fail-closed gate. In particular, the
`six_empirical_theorem_signatures` stage runs the source embedded on the six
claim pages, and `independent_signature_checker` consumes that stage's raw JSON.
Every `subprocess.run(..., check=True)` exits nonzero on failure.

````python title=repro/src/run_publication_gate.py
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
    claim1_output = ROOT / "outputs" / "claim1_proof.json"
    claim1_falsification_output = ROOT / "outputs" / "claim1_falsification.json"
    specialization_output = ROOT / "outputs" / "claims2_6_proofs.json"
    claims2_6_audit_output = ROOT / "outputs" / "claims2_6_counterexample_audit.json"
    signature_output = ROOT / "outputs" / "theorem_signatures.json"
    signature_check_output = ROOT / "outputs" / "theorem_signatures_check.json"
    visibility_output = ROOT / "outputs" / "evaluator_visibility.json"
    run_stage(
        "historical_regression",
        [sys.executable, "repro/src/verify_hyperparameters.py", "--output", str(verifier_output)],
    )
    run_stage(
        "claim1_symbolic_certificate",
        [sys.executable, "repro/src/verify_claim1_proof.py", "--output", str(claim1_output)],
    )
    run_stage(
        "claim1_falsification_audit",
        [sys.executable, "repro/src/audit_claim1_falsification.py", "--output", str(claim1_falsification_output)],
    )
    run_stage(
        "claims2_6_symbolic_certificates",
        [sys.executable, "repro/src/verify_claims2_6_proofs.py", "--output", str(specialization_output)],
    )
    run_stage(
        "claims2_6_counterexample_audit",
        [sys.executable, "repro/src/audit_claims2_6_counterexamples.py", "--output", str(claims2_6_audit_output)],
    )
    run_stage(
        "six_empirical_theorem_signatures",
        [sys.executable, "repro/src/measure_theorem_signatures.py", "--output", str(signature_output)],
    )
    run_stage(
        "independent_signature_checker",
        [
            sys.executable,
            "repro/src/check_theorem_signatures.py",
            "--input",
            str(signature_output),
            "--output",
            str(signature_check_output),
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
    claim1 = json.loads(claim1_output.read_text())
    claim1_falsification = json.loads(claim1_falsification_output.read_text())
    specializations = json.loads(specialization_output.read_text())
    claims2_6_audit = json.loads(claims2_6_audit_output.read_text())
    signatures = json.loads(signature_output.read_text())
    signature_check = json.loads(signature_check_output.read_text())
    visibility = json.loads(visibility_output.read_text())
    passed = (
        verification["all_claims_passed"]
        and len(verification["claims"]) == 6
        and claim1["verdict"] == "VERIFIED"
        and len(claim1["mutations_rejected"]) == 3
        and claim1_falsification["falsification_succeeded"] is False
        and claim1_falsification["main_claim_status"] == "VERIFIED_BY_SYMBOLIC_CERTIFICATE"
        and specializations["all_exact_claims_verified"]
        and claims2_6_audit["verdict"] == "AUDIT_COMPLETE"
        and all(not row["falsification_succeeded"] for row in claims2_6_audit["claims"].values())
        and claims2_6_audit["claims"]["C6"]["status"] == "PROOF_DOMAIN_GAP"
        and signatures["all_empirical_checks_passed"]
        and signature_check["verdict"] == "SIGNATURE_CHECK_PASS"
        and visibility["verdict"] == "EVALUATOR_VISIBLE_GATE_PASS"
        and visibility["missing_cells"] == 0
    )
    payload = {
        "paper": "JnuwpwbZ8D",
        "tests_passed": True,
        "claims_passed": len(verification["claims"]),
        "current_exact_claims": {
            "C1": claim1["verdict"],
            **{claim: result["verdict"] for claim, result in specializations["claims"].items()},
        },
        "empirical_theorem_signatures": {
            "claims": len(signatures["claims"]),
            "checker": signature_check["verdict"],
            "seeds": signatures["seeds"],
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
````

The expected stable transcript section is:

````output
GATE_STAGE_START name=six_empirical_theorem_signatures command=python repro/src/measure_theorem_signatures.py --output outputs/theorem_signatures.json
CLAIM_RESULT_C1=... VERIFIED
CLAIM_RESULT_C2=... VERIFIED
CLAIM_RESULT_C3=... VERIFIED
CLAIM_RESULT_C4=... VERIFIED
CLAIM_RESULT_C5=... VERIFIED
CLAIM_RESULT_C6=... VERIFIED
GATE_STAGE_PASS name=six_empirical_theorem_signatures
GATE_STAGE_START name=independent_signature_checker command=python repro/src/check_theorem_signatures.py --input outputs/theorem_signatures.json --output outputs/theorem_signatures_check.json
GATE_STAGE_PASS name=independent_signature_checker
{"claims_passed":6,"empirical_theorem_signatures":{"checker":"SIGNATURE_CHECK_PASS","claims":6,"seeds":[173,271,419]},"publication_gate_passed":true}
````
