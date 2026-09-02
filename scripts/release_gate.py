#!/usr/bin/env python3
"""Run the deterministic PlanOnce release gates from one command."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMANDS = [
    [sys.executable, "scripts/validate.py"],
    [sys.executable, "scripts/verify_upstreams.py"],
    [sys.executable, "scripts/verify_runtime_profile.py"],
    [sys.executable, "scripts/verify_release_manifest.py"],
    [sys.executable, "scripts/audit_skill_pack.py"],
    [sys.executable, "scripts/run_evals.py"],
    [sys.executable, "scripts/verify_consumer_install.py"],
    [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py", "-v"],
]


def main() -> int:
    for command in COMMANDS:
        print("\n==>", " ".join(command), flush=True)
        result = subprocess.run(command, cwd=ROOT)
        if result.returncode != 0:
            print(f"Release gate failed: {' '.join(command)}", file=sys.stderr)
            return result.returncode
    print("\nPlanOnce release gate: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
