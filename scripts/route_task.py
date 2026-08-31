#!/usr/bin/env python3
"""Deterministic helper for PlanOnce route-only classification."""
from __future__ import annotations

import argparse
import json

LARGE_TRIGGERS = {
    "one_way_door": "one-way/costly decision",
    "security_boundary": "security/authz/trust boundary",
    "destructive_migration": "destructive migration or data-loss risk",
    "public_contract_break": "public compatibility/contract break",
    "cross_service_consistency": "cross-service consistency risk",
    "payment_correctness": "payment/financial correctness",
}


def route_task(*, existing: bool, size: str = "normal", **flags: bool) -> dict[str, object]:
    if size not in {"small", "normal", "large"}:
        raise ValueError("size must be small, normal, or large")
    triggered = [label for key, label in LARGE_TRIGGERS.items() if flags.get(key, False)]
    selected_size = "large" if triggered else size
    family = "brown" if existing else "green"
    selected_skill = f"planonce-{family}-{selected_size}"
    rationale = ["existing implementation detected" if existing else "primarily new implementation"]
    if triggered:
        rationale.append("mandatory Large trigger: " + "; ".join(triggered))
    else:
        rationale.append(f"requested/observed change size: {size}")
    return {
        "selected_skill": selected_skill,
        "family": "brownfield" if existing else "greenfield",
        "size": selected_size,
        "mandatory_large": bool(triggered),
        "large_triggers": triggered,
        "rationale": rationale,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Route a change to the smallest safe PlanOnce implementation workflow")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--existing", action="store_true", help="Change modifies an existing implementation")
    group.add_argument("--new", action="store_true", help="Change is primarily greenfield")
    parser.add_argument("--size", choices=["small", "normal", "large"], default="normal")
    for flag in LARGE_TRIGGERS:
        parser.add_argument("--" + flag.replace("_", "-"), action="store_true")
    args = parser.parse_args()
    flags = {key: getattr(args, key) for key in LARGE_TRIGGERS}
    print(json.dumps(route_task(existing=args.existing, size=args.size, **flags), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
