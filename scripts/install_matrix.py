#!/usr/bin/env python3
"""Generate precise `npx skills add` commands from the pinned provider registry.

This script does not install anything. It keeps documentation/examples tied to the
same provider IDs that PlanOnce validates in providers/registry.json.
"""
from __future__ import annotations

import argparse
import json
import sys
import shlex
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "providers" / "registry.json"


def load_registry() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def provider_map(data: dict) -> dict[str, dict]:
    return {item["npx_agent"]: item for item in data["providers"]}


def main() -> int:
    parser = argparse.ArgumentParser(description="Print a PlanOnce npx installation command for selected coding agents.")
    parser.add_argument("--repo", default="tph-kds/PlanOnce", help="GitHub owner/repo, URL, or local path")
    parser.add_argument("--providers", help="Comma-separated exact npx agent IDs")
    parser.add_argument("--global", dest="global_install", action="store_true", help="Add -g for a global installation")
    parser.add_argument("--copy", action="store_true", help="Add --copy instead of the default symlink/canonical install")
    parser.add_argument("--list", action="store_true", help="List PlanOnce's validated provider IDs")
    args = parser.parse_args()

    data = load_registry()
    providers = provider_map(data)

    if args.list or not args.providers:
        for item in data["providers"]:
            print(f"{item['npx_agent']:<16} {item['display_name']:<18} {item['support_tier']:<11} {item['project_path']}")
        if not args.providers:
            return 0

    selected = [p.strip() for p in args.providers.split(",") if p.strip()]
    unknown = [p for p in selected if p not in providers]
    if unknown:
        print(f"Unknown provider ID(s): {', '.join(unknown)}", file=sys.stderr)
        print("Run with --list to see validated IDs.", file=sys.stderr)
        return 2
    if not selected:
        print("No provider IDs supplied.", file=sys.stderr)
        return 2

    cmd = ["npx", "skills", "add", args.repo, "--skill", "*"]
    for provider in selected:
        cmd.extend(["-a", provider])
    if args.global_install:
        cmd.append("-g")
    if args.copy:
        cmd.append("--copy")
    cmd.append("-y")
    print(" ".join(shlex.quote(part) for part in cmd))

    if "kilo" in selected:
        print(
            "NOTE: Kilo's current native docs prefer .kilo/skills and accept .agents/skills; "
            "the current Skills CLI source still carries a legacy .kilocode/skills agent mapping. "
            "Verify PlanOnce discovery in Kilo after install.",
            file=sys.stderr,
        )
    if "kiro-cli" in selected:
        print(
            "NOTE: Kiro default agents auto-discover .kiro/skills. Custom agents must include "
            "skill://.kiro/skills/*/SKILL.md in resources.",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
