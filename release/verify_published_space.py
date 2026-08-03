#!/usr/bin/env python3
"""Byte-verify an exact published Space revision and its no-regression subset."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO_ID = "DineshAI/JnuwpwbZ8D"
BASELINE = ROOT / ".campaign/baseline/judged"
ALLOWLIST = ROOT / "evidence/hf_upload_allowlist.txt"


def slugs(node: dict) -> set[str]:
    result = {node["slug"]}
    for child in node.get("children", []):
        result |= slugs(child)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--revision", required=True)
    args = parser.parse_args()

    from huggingface_hub import HfApi, get_token, hf_hub_download

    token = get_token()
    if not token:
        raise SystemExit("no cached Hugging Face token")
    api = HfApi(token=token)
    head = api.repo_info(REPO_ID, repo_type="space").sha
    if head != args.revision:
        raise SystemExit(f"Space HEAD changed: expected {args.revision}, found {head}")
    remote_files = set(api.list_repo_files(REPO_ID, repo_type="space", revision=head))
    baseline_files = {
        path.relative_to(BASELINE).as_posix()
        for path in BASELINE.rglob("*")
        if path.is_file() and ".cache" not in path.relative_to(BASELINE).parts
    }
    missing = sorted(baseline_files - remote_files)
    if missing:
        raise SystemExit(f"published revision removed baseline paths: {missing}")

    cache = ROOT / ".campaign/published" / head
    allowlist = [line for line in ALLOWLIST.read_text().splitlines() if line]
    aggregate = hashlib.sha256()
    for relative in allowlist:
        downloaded = Path(
            hf_hub_download(
                REPO_ID,
                relative,
                repo_type="space",
                revision=head,
                local_dir=cache,
                token=token,
            )
        )
        local_bytes = (ROOT / relative).read_bytes()
        if downloaded.read_bytes() != local_bytes:
            raise SystemExit(f"published byte mismatch: {relative}")
        aggregate.update(relative.encode())
        aggregate.update(b"\0")
        aggregate.update(local_bytes)

    old_logbook = json.loads((BASELINE / "logbook.json").read_text())
    new_logbook = json.loads((cache / "logbook.json").read_text())
    old_slugs = slugs(old_logbook["root"])
    new_slugs = slugs(new_logbook["root"])
    if not old_slugs <= new_slugs:
        raise SystemExit("published page tree removed judged routes")
    result = {
        "aggregate_sha256": aggregate.hexdigest(),
        "baseline_files_preserved": len(baseline_files),
        "baseline_routes_preserved": len(old_slugs),
        "byte_identical_uploads": len(allowlist),
        "head": head,
        "passed": True,
        "published_files": len(remote_files),
    }
    print("PUBLISHED_SPACE_VERIFIED " + json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
