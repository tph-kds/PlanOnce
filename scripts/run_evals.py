#!/usr/bin/env python3
"""Run deterministic PlanOnce runtime/effectiveness contract evals."""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from reliability import LockConflict, acquire_scope_locks, failure_route, plan_digest  # noqa: E402
from route_task import route_task  # noqa: E402


def evaluate(case: dict) -> tuple[bool, str]:
    kind = case["type"]
    if kind == "route":
        actual = route_task(**case["input"])["selected_skill"]
    elif kind == "failure":
        actual = failure_route(**case["input"])
    elif kind == "digest_mutation":
        actual = plan_digest(case["input"]["before"]) != plan_digest(case["input"]["after"])
    elif kind == "lock_conflict":
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            acquire_scope_locks(repo, owner="a", scopes=[case["input"]["scope"]], ttl_seconds=60, now=100)
            try:
                acquire_scope_locks(repo, owner="b", scopes=[case["input"]["scope"]], ttl_seconds=60, now=101)
                actual = False
            except LockConflict:
                actual = True
    else:
        return False, f"unknown eval type {kind!r}"
    return actual == case["expected"], f"expected={case['expected']!r} actual={actual!r}"


def main() -> int:
    cases = json.loads((ROOT / "evals" / "runtime_cases.json").read_text(encoding="utf-8"))
    failures = []
    for case in cases:
        ok, detail = evaluate(case)
        print(f"{'PASS' if ok else 'FAIL'} {case['id']}: {detail}")
        if not ok:
            failures.append(case["id"])
    if failures:
        print(f"Runtime evals: FAIL ({len(failures)}/{len(cases)})", file=sys.stderr)
        return 1
    print(f"Runtime evals: PASS ({len(cases)}/{len(cases)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
