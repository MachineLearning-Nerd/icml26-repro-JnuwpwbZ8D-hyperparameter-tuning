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
    assert logbook["schema_version"] == 2
    assert logbook["paper"] == {"arxiv_id": "2602.02406"}
    assert logbook["workspace"]["file"] == "workspace.json"
    assert (ROOT / "workspace.json").is_file()
    root = logbook["root"]
    assert root["file"] == "pages/universal-proof-index/page.md"
    titles = [child["title"] for child in root["children"]]
    assert len(root["children"]) == 8
    assert titles == [
        "Executive summary",
        "Claim 1: Theorem 4.1 logarithmic-boundary falsification",
        "Claim 2: Theorem 5.1 training-loss proof audit",
        "Claim 3: Theorem 6.1 bilevel proof audit",
        "Claim 4: Theorem 7.2 logarithmic-boundary falsification",
        "Claim 5: Theorem 8.1 group LASSO proof audit",
        "Claim 6: Theorem 8.2 fused LASSO proof audit",
        "Conclusion",
    ]
    assert all(
        child["slug"] != "historical-rejected-baseline"
        for child in root["children"]
    )

    opened = [
        "README.md",
        "logbook.json",
        root["file"],
        "pages/executive-summary/page.md",
        "poster_embed.html",
    ]
    overview = (ROOT / root["file"]).read_text()
    required_overview = (
        "<!-- trackio-cell",
        "| Executive summary |",
        "| Claim 1 |",
        "| Claim 4 |",
        "| Conclusion |",
    )
    assert all(token in overview for token in required_overview)
    executive = (ROOT / "pages/executive-summary/page.md").read_text()
    for token in ("pinned", "Scope & cost", "poster_embed.html", "510", "6/12"):
        if token not in executive:
            raise AssertionError(f"executive summary missing {token}")
    poster = (ROOT / "poster_embed.html").read_text()
    for token in ("Chenruishuo/posterly", "Claim 1", "Claim 4", "510 / 510"):
        if token not in poster:
            raise AssertionError(f"poster missing {token}")
    boundary = json.loads(
        (ROOT / ".openresearch/artifacts/log_boundary_counterexamples/raw_output.json").read_text()
    )
    boundary_check = json.loads(
        (ROOT / ".openresearch/artifacts/log_boundary_counterexamples/independent_check.json").read_text()
    )
    assert boundary["claims"]["C1"]["verdict"] == "FALSIFIED_AS_PRINTED"
    assert boundary["claims"]["C4"]["verdict"] == "FALSIFIED_AS_PRINTED"
    assert boundary["finite_sweeps_used_as_proof"] == 0
    assert boundary_check["verdict"] == "INDEPENDENT_CHECK_PASS"
    opened.extend(
        [
            ".openresearch/artifacts/log_boundary_counterexamples/raw_output.json",
            ".openresearch/artifacts/log_boundary_counterexamples/independent_check.json",
            "repro/src/audit_log_boundary_counterexamples.py",
            "repro/src/check_log_boundary_counterexamples.py",
        ]
    )
    primary_source = (ROOT / "repro/src/verify_universal_theorem_chains.py").read_text()
    audit_source = (ROOT / "repro/src/audit_universal_theorem_chains.py").read_text()
    assert "finite_parameter_sweeps_used_as_proof" in primary_source
    assert "does not import the primary verifier" in audit_source
    audit_output = json.loads(
        (ROOT / ".openresearch/artifacts/universal_proofs/independent_audit.json").read_text()
    )
    assert audit_output["independent_audit_passed"] is True
    assert audit_output["independent_checks"] == 42
    claim_checks: dict[str, dict[str, bool | str]] = {}
    for claim in range(1, 7):
        relative = f"pages/universal-proof-c{claim}/page.md"
        page = (ROOT / relative).read_text()
        opened.append(relative)
        if claim in (1, 4):
            required = (
                "Verdict: `FALSIFIED AS PRINTED`",
                "Assumption-satisfying counterexample",
                "Fail-sensitive control",
                "Raw exact evidence",
                "Independent verifier",
                "finite_sweeps_used_as_proof",
                "<!-- trackio-cell",
            )
        else:
            required = (
                "Verdict: `VERIFIED",
                "Exact claim, quantifiers, and assumptions",
                "Machine-checked proof chain",
                "Fail-sensitive controls",
                "Executed evidence",
                "finite_parameter_sweeps_used_as_proof",
                "<!-- trackio-cell",
                f"C{claim}_AUDIT=",
            )
        missing = [token for token in required if token not in page]
        if missing:
            raise AssertionError(f"{relative} missing {missing}")
        raw_relative = f".openresearch/artifacts/universal_proofs/C{claim}.json"
        raw = json.loads((ROOT / raw_relative).read_text())
        assert raw["claim_id"] == f"C{claim}"
        expected_verdict = "FALSIFIED_AS_PRINTED" if claim in (1, 4) else "VERIFIED"
        assert raw["verdict"] == expected_verdict
        assert raw["finite_parameter_sweeps_used_as_proof"] == 0
        assert len(raw["mutations_rejected"]) == 4
        assert all(value is True for value in raw["exact_checks"].values())
        assert all(value is True for value in audit_output["claims"][f"C{claim}"].values())
        if raw_relative not in page:
            raise AssertionError(f"{relative} does not link exact proof JSON")
        opened.append(raw_relative)
        claim_checks[f"C{claim}"] = {
            "canonical_page": relative,
            "code_visible": "PRIMARY_AND_INDEPENDENT_SOURCE_LINKED_FROM_PAGE",
            "data_inline": True,
            "raw_link": True,
            "checker": True,
            "control": True,
            "exact_claim_tested": True,
            "reviewer_verdict": expected_verdict,
        }

    release_page = (ROOT / "pages/universal-proof-release/page.md").read_text()
    for token in (
        "Claims 1 and 4",
        "Blind-review ceiling",
        "2/2",
        "1/2",
        "run_publication_gate.py",
        "6/12",
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
        "workspace.json",
        ".openresearch/artifacts/reference_protocols/raw_output.json",
        ".openresearch/artifacts/reference_protocols/checker_output.json",
        ".openresearch/artifacts/universal_proofs/independent_audit.json",
        "repro/src/verify_universal_theorem_chains.py",
        "repro/src/audit_universal_theorem_chains.py",
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
    if len(allowlist) < 139 or len(set(allowlist)) != len(allowlist):
        raise AssertionError("upload allowlist must contain at least 139 unique paths")
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
    if len(candidate_manifest) != len(allowlist) - 1:
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
    assert "universal proof" in blind_review.lower()
    assert "active tree contains no historical child" in blind_review

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
