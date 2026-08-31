from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []

for name in ["agent-os", "gsd-core"]:
    base = ROOT / "upstream" / name
    manifest_path = base / "manifest.json"
    if not manifest_path.is_file():
        errors.append(f"missing {manifest_path}")
        continue
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for item in manifest.get("files", []):
        path = base / item["path"]
        if not path.is_file():
            errors.append(f"missing {path}")
            continue
        got = hashlib.sha256(path.read_bytes()).hexdigest()
        if got != item["sha256"]:
            errors.append(f"hash mismatch {path}: {got}")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print("OK: vendored Agent OS/GSD upstream manifests and recursive SHA-256 hashes verified")
