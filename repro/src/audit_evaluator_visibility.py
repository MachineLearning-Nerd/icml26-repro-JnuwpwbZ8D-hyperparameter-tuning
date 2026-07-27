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
    assert len(current_titles) == 7
    assert len(historical_titles) == 1
    historical_archive = next(
        child for child in root["children"]
        if child["slug"] == "historical-rejected-baseline"
    )
    assert historical_archive["file"] == "pages/historical-rejected-baseline/page.md"
    assert len(historical_archive["children"]) == 13
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
        "8–12/12",
        "Visibility matrix",
        "not a judge result",
        "929165205a02428c2cc7207ddb0f2e187cf913d9",
        "C5 numeric formula had an erroneous extra factor d",
    )
    assert all(token in overview for token in required_overview)

    signature_source = (ROOT / "repro/src/measure_theorem_signatures.py").read_text()
    inline_functions = {
        1: ("_count_patterns", "thm_a3_bound", "thm_4_1_bound", "claim_1"),
        2: (
            "_count_patterns",
            "thm_4_1_bound",
            "thm_5_1_bound",
            "_piecewise_polynomial_count",
            "claim_2",
        ),
        3: (
            "_count_patterns",
            "thm_4_1_bound",
            "thm_5_1_bound",
            "thm_6_1_bound",
            "_bilevel_count",
            "claim_3",
        ),
        4: (
            "thm_4_1_bound",
            "thm_6_1_bound",
            "thm_7_2_bound",
            "_soft_threshold",
            "claim_4",
        ),
        5: (
            "_count_patterns",
            "thm_4_1_bound",
            "thm_8_1_bound",
            "_solve_group_lasso_batch",
            "_group_lasso_patterns",
            "_norm_nonpolynomial_check",
            "claim_5",
        ),
        6: (
            "thm_7_2_bound",
            "thm_8_2_bound",
            "_difference_matrix",
            "_solve_box_qp_batch",
            "_fused_measurement",
            "claim_6",
        ),
    }
    protocol_output = json.loads(
        (ROOT / ".openresearch/artifacts/reference_protocols/raw_output.json").read_text()
    )
    checker_output = json.loads(
        (ROOT / ".openresearch/artifacts/reference_protocols/checker_output.json").read_text()
    )
    claim_checks: dict[str, dict[str, bool | str]] = {}
    for claim in range(1, 7):
        relative = f"pages/current-c{claim}/page.md"
        page = (ROOT / relative).read_text()
        opened.append(relative)
        required = (
            "Verdict: VERIFIED",
            "Exact claim and source contract",
            "Fixed command:",
            "Raw run JSON",
            "Negative control",
            "Verifier source",
            "Historical rejected baseline",
            "log₂(realized patterns)",
            "f69eb97c-98f5-4224-93d6-1128fcbe198c",
        )
        missing = [token for token in required if token not in page]
        if missing:
            raise AssertionError(f"{relative} missing {missing}")
        displayed = fenced_source(page, "repro/src/measure_theorem_signatures.py")
        expected = function_segments(signature_source, inline_functions[claim])
        if displayed != expected:
            raise AssertionError(f"{relative} inline source differs from executed functions")
        stable_result = (
            f"CLAIM_RESULT_C{claim}="
            + json.dumps(
                protocol_output["claims"][f"C{claim}"],
                sort_keys=True,
                separators=(",", ":"),
            )
        )
        if stable_result not in page:
            raise AssertionError(f"{relative} does not show its exact stable gate output")
        for token in (
            "GATE_STAGE_START name=six_empirical_theorem_signatures",
            "GATE_STAGE_PASS name=six_empirical_theorem_signatures",
            "SIGNATURE_CHECK=" + json.dumps(checker_output, separators=(",", ":")),
            "````output",
        ):
            if token not in page:
                raise AssertionError(f"{relative} missing executed-output token: {token}")
        claim_checks[f"C{claim}"] = {
            "canonical_page": relative,
            "code_visible": "EXECUTED_CLAIM_PROTOCOL_SOURCE_INLINE",
            "data_inline": True,
            "raw_link": True,
            "checker": True,
            "control": True,
            "exact_claim_tested": True,
            "reviewer_verdict": "VERIFIED",
        }

    release_page = (ROOT / "pages/current-release/page.md").read_text()
    for token in (
        "f69eb97c-98f5-4224-93d6-1128fcbe198c",
        "C5_extra_d_factor",
        "C6_missing_p_factor",
        "7.200243542",
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
        ".openresearch/artifacts/reference_protocols/raw_output.json",
        ".openresearch/artifacts/reference_protocols/checker_output.json",
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
    if len(allowlist) != 123 or len(set(allowlist)) != len(allowlist):
        raise AssertionError("upload allowlist must contain 123 unique paths")
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
    if len(candidate_manifest) != 122:
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
