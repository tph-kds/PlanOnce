#!/usr/bin/env python3
"""Verify the inert upstream runtime/profile contract used by PlanOnce."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []
agent = ROOT / "upstream" / "agent-os" / "SOURCE"
gsd = ROOT / "upstream" / "gsd-core"
profile_dir = gsd / "profiles" / "claude-core-audit"

for rel in [
    "commands/agent-os/discover-standards.md",
    "commands/agent-os/index-standards.md",
    "commands/agent-os/inject-standards.md",
    "commands/agent-os/plan-product.md",
    "commands/agent-os/shape-spec.md",
]:
    if not (agent / rel).is_file():
        errors.append(f"missing Agent OS capability source: {rel}")

if (gsd / "runtime" / "VERSION").read_text(encoding="utf-8").strip() != "1.12.0":
    errors.append("unexpected GSD runtime version")

profile = json.loads((profile_dir / "PROFILE.json").read_text(encoding="utf-8"))
if profile.get("profile") != "core,audit":
    errors.append("unexpected GSD profile marker")

required_commands = {
    "gsd-new-project.md", "gsd-discuss-phase.md", "gsd-plan-phase.md",
    "gsd-execute-phase.md", "gsd-verify-work.md", "gsd-review.md",
    "gsd-code-review.md", "gsd-surface.md",
}
commands = {p.name for p in (profile_dir / "commands").glob("*.md")}
missing = required_commands - commands
if missing:
    errors.append(f"missing preserved core/audit commands: {sorted(missing)}")

if (ROOT / ".claude").exists():
    errors.append("root .claude runtime is active; upstream profile must remain inert")

for marker in ["H:/" + "SideProjects/PlanOnce", "D:/" + "Downloads/Program Files/nodejs"]:
    for base in [gsd / "runtime", profile_dir]:
        for path in base.rglob("*"):
            if not path.is_file():
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if marker in text:
                errors.append(f"machine-local marker remains in {path.relative_to(ROOT)}")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"OK: Agent OS v3 source + GSD v1.12.0 core,audit profile verified ({len(commands)} surfaced commands)")
