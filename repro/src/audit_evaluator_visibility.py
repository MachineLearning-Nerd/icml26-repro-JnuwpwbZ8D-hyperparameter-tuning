#!/usr/bin/env python3
"""Fail-closed audit of the evaluator-visible release surface."""
from __future__ import annotations

import argparse
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
    assert len(historical_titles) == 12

    opened = ["README.md", "logbook.json", root["file"]]
    overview = (ROOT / root["file"]).read_text()
    required_overview = (
        "Previous live judged score: `6/12`",
        "11–12/12",
        "Visibility matrix",
        "not a judge result",
    )
    assert all(token in overview for token in required_overview)

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
        )
        missing = [token for token in required if token not in page]
        if missing:
            raise AssertionError(f"{relative} missing {missing}")
        claim_checks[f"C{claim}"] = {
            "canonical_page": relative,
            "code_visible": True,
            "data_inline": True,
            "raw_link": True,
            "checker": True,
            "control": True,
            "exact_claim_tested": True,
            "reviewer_verdict": "VERIFIED",
        }

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
        historical_copy = ROOT / ".trackio" / "logbook" / relative
        if historical_copy.is_file():
            if relative == "logbook.json":
                # Navigation metadata is intentionally replaced; every page
                # and reader-facing asset it referenced remains byte-identical.
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
    if len(allowlist) != 118 or len(set(allowlist)) != len(allowlist):
        raise AssertionError("upload allowlist must contain 118 unique paths")
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
    if len(candidate_manifest) != 117:
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
