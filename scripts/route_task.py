#!/usr/bin/env python3
"""Deterministic helper for PlanOnce route-only classification."""
from __future__ import annotations

import argparse
import json

LARGE_TRIGGERS = {
    "one_way_door": "one-way/costly decision",
    "destructive_migration": "destructive migration or data-loss risk",
    "public_contract_break": "public API/compatibility contract break",
    "cross_service_consistency": "cross-service consistency risk",
    "payment_correctness": "payment/financial correctness",
    "auth_model_change": "authorization model change",
    "tenant_isolation_change": "tenant isolation/boundary change",
    "credential_architecture_change": "credential/key storage architecture change",
    "token_claims_change": "token claims/validation contract change",
    "cross_service_auth_change": "cross-service authentication semantics change",
}

# Security-sensitive does not automatically mean Large. These require security review
# but only LARGE_TRIGGERS force Large. Kept for backward compat + explicit security signal.
SECURITY_SENSITIVE_FLAGS = {
    "security_boundary": "security/authz/trust boundary (legacy flag — triggers security review, not auto-Large)",
    "security_sensitive": "security-sensitive change (bounded scope — Normal can remain appropriate)",
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

    # Security review is required for any security-sensitive flag or any security Large trigger
    needs_security_review = bool(
        flags.get("security_boundary")
        or flags.get("security_sensitive")
        or any(flags.get(k) for k in ["auth_model_change", "tenant_isolation_change", "credential_architecture_change", "token_claims_change", "cross_service_auth_change"])
    )
    security_triggers: list[str] = []
    for key, label in {**LARGE_TRIGGERS, **SECURITY_SENSITIVE_FLAGS}.items():
        if flags.get(key, False):
            # Only include security-relevant labels in security_triggers
            if key in SECURITY_SENSITIVE_FLAGS or key in {"auth_model_change", "tenant_isolation_change", "credential_architecture_change", "token_claims_change", "cross_service_auth_change"}:
                security_triggers.append(label)

    if needs_security_review and not triggered:
        rationale.append("security-sensitive: requires planonce-security review (Normal remains appropriate when architecture/API/auth model/tenant/credential contracts unchanged, blast radius bounded, rollback straightforward)")
    elif needs_security_review and triggered:
        rationale.append("security-sensitive Large: mandatory planonce-security + planonce-review before ship")

    return {
        "selected_skill": selected_skill,
        "family": "brownfield" if existing else "greenfield",
        "size": selected_size,
        "mandatory_large": bool(triggered),
        "large_triggers": triggered,
        "needs_security_review": needs_security_review,
        "security_triggers": security_triggers,
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
    # Security-sensitive flags are not Large triggers but still affect routing rationale + security gate
    for flag in SECURITY_SENSITIVE_FLAGS:
        parser.add_argument("--" + flag.replace("_", "-"), action="store_true", help=SECURITY_SENSITIVE_FLAGS[flag])
    args = parser.parse_args()
    flags = {}
    for key in list(LARGE_TRIGGERS.keys()) + list(SECURITY_SENSITIVE_FLAGS.keys()):
        flags[key] = getattr(args, key, False)
    print(json.dumps(route_task(existing=args.existing, size=args.size, **flags), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
