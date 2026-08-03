#!/usr/bin/env python3
"""Publish the exact UTF-8 allowlist additively to the existing ID Space."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
REPO_ID = "DineshAI/JnuwpwbZ8D"
ALLOWLIST = ROOT / "evidence/hf_upload_allowlist.txt"
MANIFEST = ROOT / "evidence/candidate_text_manifest.sha256"
TEXT_SUFFIXES = {".css", ".csv", ".html", ".js", ".json", ".lock", ".md", ".py", ".sha256", ".svg", ".tex", ".toml", ".txt"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_allowlist() -> list[str]:
    entries = [line for line in ALLOWLIST.read_text().splitlines() if line]
    if entries != sorted(set(entries)):
        raise SystemExit("allowlist must be sorted and duplicate-free")
    for entry in entries:
        parsed = PurePosixPath(entry)
        if parsed.is_absolute() or ".." in parsed.parts:
            raise SystemExit(f"unsafe allowlist path: {entry}")
        path = ROOT / entry
        if not path.is_file() or (
            path.suffix.lower() not in TEXT_SUFFIXES and path.name != ".python-version"
        ):
            raise SystemExit(f"missing or non-text allowlist path: {entry}")
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as error:
            raise SystemExit(f"non-UTF-8 allowlist path: {entry}") from error
        if path.suffix == ".json":
            json.loads(text)
    return entries


def verify_manifest(allowlist: list[str]) -> None:
    rows = {}
    for line in MANIFEST.read_text().splitlines():
        digest, relative = line.split(maxsplit=1)
        rows[relative] = digest
    expected = set(allowlist) - {"evidence/candidate_text_manifest.sha256"}
    if set(rows) != expected:
        raise SystemExit("candidate manifest paths differ from the allowlist")
    for relative, expected_digest in rows.items():
        if sha256(ROOT / relative) != expected_digest:
            raise SystemExit(f"candidate manifest mismatch: {relative}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--message", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    allowlist = read_allowlist()
    verify_manifest(allowlist)
    print(f"release gates passed: {len(allowlist)} exact UTF-8 text paths")
    if args.dry_run:
        return

    os.environ["HF_HUB_DISABLE_XET"] = "1"
    from huggingface_hub import CommitOperationAdd, HfApi, get_token

    token = get_token()
    if not token:
        raise SystemExit("no cached Hugging Face token")
    api = HfApi(token=token)
    live_head = api.repo_info(REPO_ID, repo_type="space").sha
    if live_head != args.expected_head:
        raise SystemExit(f"Space HEAD changed: expected {args.expected_head}, found {live_head}")
    operations = [
        CommitOperationAdd(path_in_repo=relative, path_or_fileobj=str(ROOT / relative))
        for relative in allowlist
    ]
    commit = api.create_commit(
        repo_id=REPO_ID,
        repo_type="space",
        operations=operations,
        commit_message=args.message,
        parent_commit=live_head,
        token=token,
    )
    print(f"published revision: {commit.oid}")
    print(f"retained judged baseline: {live_head}")
    print("status: awaiting judge")


if __name__ == "__main__":
    main()
