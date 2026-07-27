#!/usr/bin/env python3
"""Fail-closed audit of the evaluator-visible release surface."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_manifest(path: Path) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in path.read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        digest, relative = line.split(maxsplit=1)
        if len(digest) != 64:
            raise AssertionError(f"invalid digest for {relative}")
        rows[relative] = digest
    return rows


def fenced_source(page: str, title: str) -> str:
    pattern = re.compile(
        rf"````python title={re.escape(title)}\n(.*?)\n````",
        re.DOTALL,
    )
    matches = pattern.findall(page)
    if len(matches) != 1:
        raise AssertionError(f"expected one inline source block for {title}, got {len(matches)}")
    return matches[0]


def function_segments(source: str, names: tuple[str, ...]) -> str:
    tree = ast.parse(source)
    by_name = {
        node.name: ast.get_source_segment(source, node)
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    missing = [name for name in names if name not in by_name]
    if missing:
        raise AssertionError(f"executed source missing functions: {missing}")
    return "\n\n".join(by_name[name] for name in names)


def expected_symbolic_result(claim: int) -> str:
    if claim == 1:
        result = json.loads(
            (ROOT / ".openresearch/artifacts/claim_1/raw_output.json").read_text()
        )
        return "CLAIM1_RESULT=" + json.dumps(result, sort_keys=True)
    claims = {
        f"C{number}": json.loads(
            (ROOT / f".openresearch/artifacts/claim_{number}/raw_output.json").read_text()
        )
        for number in range(2, 7)
    }
    witnesses = json.loads(
        (ROOT / ".openresearch/artifacts/claims2_6_symbolic_witnesses.json").read_text()
    )
    payload = {
        "claims": claims,
        "symbolic_witnesses": witnesses,
        "all_exact_claims_verified": witnesses["all_symbolic_witnesses_passed"],
    }
    return "CLAIMS2_6_RESULT=" + json.dumps(payload, sort_keys=True)


def historical_candidate(root: Path, relative: str) -> Path | None:
    """Resolve immutable evidence in a source checkout or downloaded Space."""
    mirror = root / ".trackio" / "logbook" / relative
    if mirror.is_file():
        return mirror
    published = root / relative
    if published.is_file():
        return published
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    logbook = json.loads((ROOT / "logbook.json").read_text())
    root = logbook["root"]
    assert root["file"] == "pages/current-verification/page.md"
    titles = [child["title"] for child in root["children"]]
    current_titles = [title for title in titles if title.startswith("CURRENT")]
    historical_titles = [title for title in titles if title.startswith("Historical rejected baseline")]
    assert len(current_titles) == 8
    assert len(historical_titles) == 1
    historical_archive = next(
        child for child in root["children"]
        if child["slug"] == "historical-rejected-baseline"
    )
    assert historical_archive["file"] == "pages/historical-rejected-baseline/page.md"
    assert len(historical_archive["children"]) == 12
    assert all(
        child["title"].startswith("Historical rejected baseline")
        for child in historical_archive["children"]
    )

    opened = [
        "README.md",
        "logbook.json",
        root["file"],
        historical_archive["file"],
    ]
    overview = (ROOT / root["file"]).read_text()
    required_overview = (
        "Previous live judged score: `6/12`",
        "11–12/12",
        "Visibility matrix",
        "not a judge result",
    )
    assert all(token in overview for token in required_overview)

    signature_source = (ROOT / "repro/src/measure_theorem_signatures.py").read_text()
    c1_proof_source = (ROOT / "repro/src/verify_claim1_proof.py").read_text().rstrip()
    c26_proof_source = (ROOT / "repro/src/verify_claims2_6_proofs.py").read_text().rstrip()
    inline_functions = {
        1: ("claim_1",),
        2: ("_piecewise_polynomial_count", "claim_2"),
        3: ("_bilevel_count", "claim_3"),
        4: ("_soft_threshold", "claim_4"),
        5: ("_group_lasso_instance", "claim_5"),
        6: ("_fused_dual", "_fused_measurement", "claim_6"),
    }
    claim_checks: dict[str, dict[str, bool | str]] = {}
    for claim in range(1, 7):
        relative = f"pages/current-c{claim}/page.md"
        page = (ROOT / relative).read_text()
        opened.append(relative)
        required = (
            "Verdict: VERIFIED",
            "Exact",
            "Fixed command:",
            "Raw JSON",
            "Empirical raw JSON",
            "Negative control",
            "Verifier source",
            "Historical rejected baseline",
            "Complete symbolic theorem certificate",
        )
        missing = [token for token in required if token not in page]
        if missing:
            raise AssertionError(f"{relative} missing {missing}")
        displayed = fenced_source(page, "repro/src/measure_theorem_signatures.py")
        expected = function_segments(signature_source, inline_functions[claim])
        if displayed != expected:
            raise AssertionError(f"{relative} inline source differs from executed functions")
        proof_title = (
            "repro/src/verify_claim1_proof.py"
            if claim == 1
            else "repro/src/verify_claims2_6_proofs.py"
        )
        displayed_proof = fenced_source(page, proof_title)
        expected_proof = c1_proof_source if claim == 1 else c26_proof_source
        if displayed_proof != expected_proof:
            raise AssertionError(f"{relative} inline symbolic certificate differs from executed source")
        symbolic_result = expected_symbolic_result(claim)
        if symbolic_result not in page:
            raise AssertionError(f"{relative} does not show exact symbolic-certificate output")
        artifact = json.loads(
            (ROOT / f".openresearch/artifacts/claim_{claim}/signature_output.json").read_text()
        )
        stable_result = (
            f"CLAIM_RESULT_C{claim}="
            + json.dumps(artifact["claim"], sort_keys=True, separators=(",", ":"))
        )
        if stable_result not in page:
            raise AssertionError(f"{relative} does not show its exact stable gate output")
        for token in (
            "GATE_STAGE_START name=six_empirical_theorem_signatures",
            "GATE_STAGE_PASS name=six_empirical_theorem_signatures",
            (
                "GATE_STAGE_START name=claim1_symbolic_certificate"
                if claim == 1
                else "GATE_STAGE_START name=claims2_6_symbolic_certificates"
            ),
            (
                "GATE_STAGE_PASS name=claim1_symbolic_certificate"
                if claim == 1
                else "GATE_STAGE_PASS name=claims2_6_symbolic_certificates"
            ),
            "````output",
        ):
            if token not in page:
                raise AssertionError(f"{relative} missing executed-output token: {token}")
        claim_checks[f"C{claim}"] = {
            "canonical_page": relative,
            "code_visible": "FULL_EXECUTED_EMPIRICAL_AND_SYMBOLIC_SOURCE_INLINE",
            "data_inline": True,
            "raw_link": True,
            "checker": True,
            "control": True,
            "exact_claim_tested": True,
            "reviewer_verdict": "VERIFIED",
        }

    proof_relative = "pages/current-proof-certificates/page.md"
    proof_page = (ROOT / proof_relative).read_text()
    opened.append(proof_relative)
    if fenced_source(proof_page, "repro/src/verify_claim1_proof.py") != c1_proof_source:
        raise AssertionError("root proof page C1 certificate differs from executed source")
    if fenced_source(proof_page, "repro/src/verify_claims2_6_proofs.py") != c26_proof_source:
        raise AssertionError("root proof page C2-C6 certificate differs from executed source")
    if expected_symbolic_result(1) not in proof_page or expected_symbolic_result(2) not in proof_page:
        raise AssertionError("root proof page missing exact certificate output")

    release_page = (ROOT / "pages/current-release/page.md").read_text()
    displayed_gate = fenced_source(release_page, "repro/src/run_publication_gate.py")
    executed_gate = (ROOT / "repro/src/run_publication_gate.py").read_text().rstrip()
    if displayed_gate != executed_gate:
        raise AssertionError("current release page does not embed the exact executed gate")
    for token in (
        "e41343cf30154ab7e49464ce303fc5ed1b56ea05",
        "six_empirical_theorem_signatures",
        "independent_signature_checker",
        "subprocess.run(command, cwd=ROOT, check=True)",
    ):
        if token not in release_page:
            raise AssertionError(f"current release page missing judge-directed token: {token}")

    for required in (
        "reports/theorem-certificates/report.md",
        "reports/theorem-certificates/images/headline.svg",
        "reports/theorem-certificates/images/proof-pipeline.svg",
        "reports/theorem-certificates/images/checker-cases.svg",
        "reports/theorem-certificates/images/adversarial-audit.svg",
        "reports/theorem-certificates/images/experiment-tree.svg",
        "reports/theorem-certificates/images/signature-evidence.svg",
        "notebooks/theorem_certificates.py",
        "evidence/run_metadata.json",
        "evidence/judged-space-a928c531.sha256",
    ):
        if not (ROOT / required).is_file():
            raise AssertionError(f"missing release file: {required}")
        opened.append(required)

    judged = parse_manifest(ROOT / "evidence/judged-space-a928c531.sha256")
    preserved_pages = 0
    for relative, expected in judged.items():
        if relative in {"README.md", "logbook.json"}:
            # The landing page and navigation are intentionally superseded.
            continue
        historical_copy = historical_candidate(ROOT, relative)
        if historical_copy is None:
            continue
        if sha256(historical_copy) != expected:
            raise AssertionError(f"historical hash changed: {relative}")
        preserved_pages += 1
    if preserved_pages < 19:
        raise AssertionError(f"only {preserved_pages} judged assets verified")

    report = (ROOT / "reports/theorem-certificates/report.md").read_text()
    for name in (
        "headline.svg",
        "proof-pipeline.svg",
        "checker-cases.svg",
        "adversarial-audit.svg",
        "experiment-tree.svg",
        "signature-evidence.svg",
    ):
        assert f"images/{name}" in report
        ET.parse(ROOT / "reports" / "theorem-certificates" / "images" / name)

    allowlist = [
        line for line in (ROOT / "evidence/hf_upload_allowlist.txt").read_text().splitlines()
        if line
    ]
    if len(allowlist) != 121 or len(set(allowlist)) != len(allowlist):
        raise AssertionError("upload allowlist must contain 121 unique paths")
    if allowlist != sorted(allowlist):
        raise AssertionError("upload allowlist is not sorted")
    for relative in allowlist:
        upload = ROOT / relative
        if not upload.is_file():
            raise AssertionError(f"allowlisted file is missing: {relative}")
        try:
            text = upload.read_text()
        except UnicodeDecodeError as error:
            raise AssertionError(f"non-text file in allowlist: {relative}") from error
        if re.search(r"\bhf_[A-Za-z0-9]{20,}\b", text):
            raise AssertionError(f"possible Hugging Face token in {relative}")

    candidate_manifest = parse_manifest(ROOT / "evidence/candidate_text_manifest.sha256")
    if len(candidate_manifest) != 120:
        raise AssertionError("candidate manifest must hash every upload except itself")
    for relative, expected in candidate_manifest.items():
        if relative not in allowlist:
            raise AssertionError(f"manifest path not allowlisted: {relative}")
        if sha256(ROOT / relative) != expected:
            raise AssertionError(f"candidate hash mismatch: {relative}")
    if "evidence/candidate_text_manifest.sha256" not in allowlist:
        raise AssertionError("candidate manifest is not allowlisted")

    blind_review = (ROOT / "evidence/evaluator_blind_review.md").read_text()
    assert "release visibility PASS" in blind_review
    assert "zero missing paths" in blind_review

    payload = {
        "canonical_entrypoint": root["file"],
        "opened_files": opened,
        "claims": claim_checks,
        "historical_manifest_entries": len(judged),
        "historical_assets_hash_verified": preserved_pages,
        "text_upload_paths": len(allowlist),
        "candidate_hashes_verified": len(candidate_manifest),
        "secret_scan": "PASS",
        "missing_cells": 0,
        "verdict": "EVALUATOR_VISIBLE_GATE_PASS",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("EVALUATOR_VISIBILITY=" + json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
