#!/usr/bin/env python3
"""Maintainer-only upstream refresh helper.

This script is never used by PlanOnce at runtime. It prints the exact release
commands maintainers should use when deliberately refreshing vendored upstreams.
The current release already contains its pinned sources; updates must be reviewed
as PlanOnce release changes rather than fetched automatically for end users.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK = json.loads((ROOT / "upstream.lock.json").read_text(encoding="utf-8"))

agent = LOCK["agent_os"]
gsd = LOCK["gsd_core"]

print("PlanOnce upstream refresh is maintainer-only.\n")
print("Agent OS exact release export:")
print(f"  git clone --depth 1 --branch {agent['tag']} {agent['repo']} /tmp/planonce-agent-os")
print("  git -C /tmp/planonce-agent-os archive HEAD | tar -x -C upstream/agent-os/SOURCE")
print()
print("GSD Core release/package inspection:")
print(f"  npm pack @opengsd/gsd-core@{gsd['tag'].lstrip('v')} --ignore-scripts")
print("  inspect the package/runtime transformations before replacing upstream/gsd-core/runtime")
print()
print("After a reviewed refresh, regenerate manifest.json hashes and run:")
print("  python scripts/verify_upstreams.py")
print("  python scripts/release_gate.py")
