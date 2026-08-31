#!/usr/bin/env python3
"""Verify RELEASE_MANIFEST.json describes the exact distributable source tree."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "RELEASE_MANIFEST.json"
EXCLUDED_DIRS = {"__pycache__", ".pytest_cache"}
EXCLUDED_FILES = {"RELEASE_MANIFEST.json"}


def release_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if rel.as_posix() in EXCLUDED_FILES:
            continue
        if any(part in EXCLUDED_DIRS for part in rel.parts):
            continue
        files.append(path)
    return sorted(files, key=lambda path: path.relative_to(ROOT).as_posix())


def source_tree_hash(files: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in files:
        rel = path.relative_to(ROOT).as_posix().encode("utf-8")
        digest.update(rel)
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    files = release_files()
    actual_hash = source_tree_hash(files)
    expected_count = manifest.get("source_files_count")
    expected_hash = manifest.get("source_tree_sha256")
    if expected_count != len(files):
        raise SystemExit(
            f"Release manifest file-count mismatch: expected {expected_count}, actual {len(files)}"
        )
    if expected_hash != actual_hash:
        raise SystemExit(
            "Release manifest source-tree hash mismatch: "
            f"expected {expected_hash}, actual {actual_hash}"
        )
    print(
        f"OK: RELEASE_MANIFEST source tree verified — {len(files)} files, sha256 {actual_hash}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
