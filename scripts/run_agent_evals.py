#!/usr/bin/env python3
"""Run provider-neutral external coding-agent evaluations through an explicit adapter."""
from __future__ import annotations

import argparse
import json
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def score(expected: dict, result: dict) -> list[str]:
    errors: list[str] = []
    if "selected_skill" in expected and result.get("selected_skill") != expected["selected_skill"]:
        errors.append(f"selected_skill expected {expected['selected_skill']} got {result.get('selected_skill')}")
    required = set(expected.get("required_artifacts", []))
    actual = set(result.get("artifacts", []))
    missing = sorted(required - actual)
    if missing:
        errors.append(f"missing artifacts: {missing}")
    if "ship_decision" in expected and result.get("ship_decision") != expected["ship_decision"]:
        errors.append(f"ship_decision expected {expected['ship_decision']} got {result.get('ship_decision')}")
    claims = "\n".join(str(x) for x in result.get("claims", [])).lower()
    for forbidden in expected.get("forbidden_claims", []):
        if forbidden.lower() in claims:
            errors.append(f"forbidden claim present: {forbidden}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Run PlanOnce cases through an explicit coding-agent adapter")
    parser.add_argument("--adapter-command", required=True, help="Command prefix; input.json and result.json are appended")
    parser.add_argument("--cases", default=str(ROOT / "evals" / "agent_cases.json"))
    args = parser.parse_args()
    command = shlex.split(args.adapter_command)
    if not command:
        parser.error("adapter command is empty")
    cases_path = Path(args.cases).resolve()
    cases = json.loads(cases_path.read_text(encoding="utf-8"))
    failures: list[str] = []
    for case in cases:
        with tempfile.TemporaryDirectory(prefix="planonce-agent-eval-") as td:
            temp = Path(td)
            fixture_src = cases_path.parent / case.get("fixture", "")
            fixture_dst = temp / "repo"
            if fixture_src.is_dir():
                shutil.copytree(fixture_src, fixture_dst)
            else:
                fixture_dst.mkdir()
            input_path = temp / "input.json"
            result_path = temp / "result.json"
            input_payload = {
                "schema": "planonce.agent-eval-input/v1",
                "case_id": case["id"],
                "prompt": case["prompt"],
                "fixture_path": str(fixture_dst),
            }
            input_path.write_text(json.dumps(input_payload, indent=2) + "\n", encoding="utf-8")
            completed = subprocess.run([*command, str(input_path), str(result_path)], text=True, capture_output=True)
            if completed.returncode != 0:
                errors = [f"adapter exited {completed.returncode}: {(completed.stderr or completed.stdout).strip()}"]
            elif not result_path.is_file():
                errors = ["adapter did not write result.json"]
            else:
                try:
                    result = json.loads(result_path.read_text(encoding="utf-8"))
                except json.JSONDecodeError as exc:
                    errors = [f"invalid result JSON: {exc}"]
                else:
                    if result.get("schema") != "planonce.agent-eval-result/v1":
                        errors = ["unexpected/missing result schema"]
                    else:
                        errors = score(case["expected"], result)
            if errors:
                failures.append(case["id"])
                print(f"FAIL {case['id']}: {'; '.join(errors)}")
            else:
                print(f"PASS {case['id']}")
    if failures:
        print(f"Agent evals: FAIL ({len(failures)}/{len(cases)})", file=sys.stderr)
        return 1
    print(f"Agent evals: PASS ({len(cases)}/{len(cases)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
