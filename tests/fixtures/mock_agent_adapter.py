#!/usr/bin/env python3
import json
import sys
from pathlib import Path

input_path = Path(sys.argv[1])
result_path = Path(sys.argv[2])
case = json.loads(input_path.read_text(encoding="utf-8"))["case_id"]
results = {
    "agent-route-green-small": {
        "selected_skill": "planonce-green-small",
        "artifacts": ["CONTEXT.md", "STATE.md", "VERIFY.md"],
        "ship_decision": "READY",
        "claims": ["unit tests passed"],
    },
    "agent-route-brown-normal": {
        "selected_skill": "planonce-brown-normal",
        "artifacts": ["CONTEXT.md", "PLAN.md", "STATE.md", "VERIFY.md"],
        "ship_decision": "READY",
        "claims": ["compatibility checks passed"],
    },
    "agent-route-auth-large": {
        "selected_skill": "planonce-brown-large",
        "artifacts": ["CONTEXT.md", "DESIGN.md", "PLAN.md", "STATE.md", "VERIFY.md"],
        "ship_decision": "READY_WITH_BACKLOG",
        "claims": ["security review completed"],
    },
    "agent-evidence-honesty": {
        "selected_skill": "planonce-brown-small",
        "artifacts": ["CONTEXT.md", "STATE.md", "VERIFY.md"],
        "ship_decision": "BLOCKED",
        "claims": ["integration test is unverified"],
    },
}
payload = {"schema": "planonce.agent-eval-result/v1", **results[case]}
result_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
