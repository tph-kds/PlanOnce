#!/usr/bin/env python3
"""PlanOnce reliability primitives.

Standard-library only. These helpers make PlanOnce's human-readable Markdown
artifacts machine-verifiable without introducing a daemon or database.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import posixpath
import re
import subprocess
import time
from pathlib import Path
from typing import Iterable

SCHEMAS = {
    "CONTEXT.md": "planonce.context/v1",
    "DESIGN.md": "planonce.design/v1",
    "PLAN.md": "planonce.plan/v1",
    "STATE.md": "planonce.state/v1",
    "VERIFY.md": "planonce.verify/v1",
}

# Formal state machine (recommended improvement)
STATES = [
    "NOT_STARTED",
    "IN_PROGRESS",
    "DISCOVERY",
    "PLANNED",
    "AWAITING_APPROVAL",
    "APPROVED",
    "EXECUTING",
    "VERIFYING",
    "REVIEWING",
    "IMPLEMENTED_NOT_VERIFIED",
    "VERIFIED",
    "READY",
    "BLOCKED",
    "COMPLETE",
]

# Allowed transitions; any not listed is invalid. Agents may not invent transitions.
VALID_TRANSITIONS: dict[str, set[str]] = {
    "NOT_STARTED": {"DISCOVERY", "PLANNED", "AWAITING_APPROVAL", "IN_PROGRESS", "BLOCKED"},
    "IN_PROGRESS": {"IMPLEMENTED_NOT_VERIFIED", "VERIFYING", "VERIFIED", "BLOCKED", "EXECUTING"},
    "DISCOVERY": {"PLANNED", "AWAITING_APPROVAL", "BLOCKED"},
    "PLANNED": {"AWAITING_APPROVAL", "APPROVED", "BLOCKED"},
    "AWAITING_APPROVAL": {"APPROVED", "BLOCKED"},
    "APPROVED": {"EXECUTING", "IN_PROGRESS", "BLOCKED"},
    "EXECUTING": {"VERIFYING", "IMPLEMENTED_NOT_VERIFIED", "BLOCKED"},
    "IMPLEMENTED_NOT_VERIFIED": {"VERIFYING", "BLOCKED"},
    "VERIFYING": {"VERIFIED", "REVIEWING", "BLOCKED", "EXECUTING"},
    "VERIFIED": {"REVIEWING", "READY", "BLOCKED"},
    "REVIEWING": {"READY", "BLOCKED", "EXECUTING"},
    "READY": {"COMPLETE", "BLOCKED"},
    "BLOCKED": {"DISCOVERY", "PLANNED", "AWAITING_APPROVAL", "APPROVED", "EXECUTING", "VERIFYING", "REVIEWING", "IN_PROGRESS"},
    "COMPLETE": set(),
}


class ReliabilityError(RuntimeError):
    pass


class LockConflict(ReliabilityError):
    pass


def parse_frontmatter(text: str) -> dict[str, str]:
    """Parse the deliberately simple scalar YAML frontmatter PlanOnce emits."""
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = normalized.split("\n")
    if not lines or lines[0] != "---":
        return {}
    try:
        end = lines.index("---", 1)
    except ValueError:
        return {}
    result: dict[str, str] = {}
    for raw in lines[1:end]:
        line = raw.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip('"').strip("'")
    return result


def _update_frontmatter(text: str, updates: dict[str, str]) -> str:
    """Update frontmatter keys, preserving body. Adds keys if missing."""
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = normalized.split("\n")
    if not lines or lines[0] != "---":
        # No frontmatter, create one
        fm_lines = ["---"]
        for k, v in updates.items():
            fm_lines.append(f"{k}: {v}")
        fm_lines.append("---")
        fm_lines.append("")
        fm_lines.append(text)
        return "\n".join(fm_lines)
    try:
        end = lines.index("---", 1)
    except ValueError:
        return text
    fm = lines[1:end]
    # Build dict of existing keys to line index
    idx_by_key: dict[str, int] = {}
    for i, raw in enumerate(fm):
        if ":" in raw and not raw.strip().startswith("#"):
            k = raw.split(":", 1)[0].strip()
            idx_by_key[k] = i
    for k, v in updates.items():
        if k in idx_by_key:
            fm[idx_by_key[k]] = f"{k}: {v}"
        else:
            fm.append(f"{k}: {v}")
    return "\n".join(["---"] + fm + ["---"] + lines[end + 1 :])


def normalized_markdown(text: str) -> str:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in normalized.split("\n")]
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines) + "\n"


def plan_digest(text_or_path: str | Path) -> str:
    if isinstance(text_or_path, Path):
        text = text_or_path.read_text(encoding="utf-8")
    else:
        text = text_or_path
    digest = hashlib.sha256(normalized_markdown(text).encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=repo, text=True, capture_output=True, check=False
    )


def working_tree_digest(repo: str | Path) -> str:
    """Hash code/worktree changes while excluding PlanOnce's own state directory."""
    repo = Path(repo).resolve()
    probe = _git(repo, "rev-parse", "--is-inside-work-tree")
    if probe.returncode != 0 or probe.stdout.strip() != "true":
        return "unavailable"

    digest = hashlib.sha256()
    diff = _git(repo, "diff", "--binary", "HEAD", "--", ".", ":(exclude).planonce/**")
    digest.update(diff.stdout.encode("utf-8", errors="surrogateescape"))

    untracked = _git(repo, "ls-files", "--others", "--exclude-standard", "-z")
    for raw in sorted(filter(None, untracked.stdout.split("\0"))):
        rel = raw.replace("\\", "/")
        if rel == ".planonce" or rel.startswith(".planonce/"):
            continue
        path = repo / raw
        digest.update(rel.encode("utf-8"))
        digest.update(b"\0")
        if path.is_file():
            digest.update(path.read_bytes())
        digest.update(b"\0")
    return f"sha256:{digest.hexdigest()}"


def workspace_snapshot(repo: str | Path) -> dict[str, object]:
    repo = Path(repo).resolve()
    inside = _git(repo, "rev-parse", "--is-inside-work-tree")
    if inside.returncode != 0 or inside.stdout.strip() != "true":
        return {
            "git_available": False,
            "revision": "unavailable",
            "branch": "unavailable",
            "dirty": None,
            "working_tree_digest": "unavailable",
        }
    revision = _git(repo, "rev-parse", "HEAD").stdout.strip()
    branch = _git(repo, "branch", "--show-current").stdout.strip() or "DETACHED"
    status = _git(repo, "status", "--porcelain=v1", "--untracked-files=all").stdout.splitlines()
    code_dirty = any(
        len(line) >= 4 and not line[3:].replace("\\", "/").startswith(".planonce/")
        for line in status
    )
    return {
        "git_available": True,
        "revision": revision,
        "branch": branch,
        "dirty": code_dirty,
        "working_tree_digest": working_tree_digest(repo),
    }


def failure_route(*, plan_invalid: bool, implementation_defect: bool) -> str:
    if plan_invalid:
        return "BLOCKED_AMEND"
    if implementation_defect:
        return "FIX_REVERIFY"
    return "DIAGNOSE"


def validate_work_artifacts(workdir: str | Path, repo: str | Path | None = None) -> list[str]:
    workdir = Path(workdir)
    errors: list[str] = []
    metadata: dict[str, dict[str, str]] = {}
    for filename, schema in SCHEMAS.items():
        path = workdir / filename
        if not path.exists():
            continue
        fm = parse_frontmatter(path.read_text(encoding="utf-8"))
        metadata[filename] = fm
        if fm.get("schema") != schema:
            errors.append(f"{filename}: expected schema {schema}")

    state_path = workdir / "STATE.md"
    if not state_path.exists():
        errors.append("STATE.md: missing resumable state artifact")
        return errors

    state = metadata.get("STATE.md", {})
    plan_path = workdir / "PLAN.md"
    current_plan_digest = plan_digest(plan_path) if plan_path.exists() else ""
    accepted = state.get("approved_plan_digest", "")
    if plan_path.exists() and accepted and accepted not in {"PENDING", "NOT_APPROVED", "NOT_APPLICABLE"}:
        if accepted != current_plan_digest:
            errors.append("PLAN.md: approved plan digest no longer matches accepted PLAN.md")

    verify = metadata.get("VERIFY.md", {})
    if verify.get("evidence_status") == "FRESH":
        if plan_path.exists() and verify.get("plan_digest") != current_plan_digest:
            errors.append("VERIFY.md: stale evidence because plan digest changed")
        if repo is not None:
            snap = workspace_snapshot(repo)
            if snap["git_available"]:
                if verify.get("revision") != snap["revision"]:
                    errors.append("VERIFY.md: stale evidence because Git revision changed")
                if verify.get("working_tree_digest") != snap["working_tree_digest"]:
                    errors.append("VERIFY.md: stale evidence because working tree changed")
    # Validate state machine transition if status present
    status = state.get("status", "")
    if status and status not in STATES:
        errors.append(f"STATE.md: unknown status {status!r}")
    return errors


def is_valid_transition(from_status: str, to_status: str) -> bool:
    if from_status not in VALID_TRANSITIONS:
        return False
    return to_status in VALID_TRANSITIONS[from_status]


def approve_plan(workdir: str | Path, *, approved_by: str = "human") -> dict[str, str]:
    """Machine-enforce human approval: compute digest and record in STATE.md."""
    workdir = Path(workdir)
    plan_path = workdir / "PLAN.md"
    state_path = workdir / "STATE.md"
    if not plan_path.exists():
        # Small workflow: no PLAN.md, set NOT_APPLICABLE
        if not state_path.exists():
            raise ReliabilityError("STATE.md missing; cannot approve")
        digest = "NOT_APPLICABLE"
    else:
        digest = plan_digest(plan_path)
    if not state_path.exists():
        raise ReliabilityError("STATE.md missing; cannot approve")
    text = state_path.read_text(encoding="utf-8")
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    updates = {
        "approved_plan_digest": digest,
        "approval_status": "approved",
        "approved_by": approved_by,
        "approved_at": now,
        "status": "APPROVED",
    }
    # Keep legacy approved_plan_digest key for compat, add structured approval
    new_text = _update_frontmatter(text, updates)
    state_path.write_text(new_text, encoding="utf-8")
    return {"approved_plan_digest": digest, "approved_by": approved_by, "approved_at": now}


def gate_execution(workdir: str | Path, repo: str | Path | None = None) -> dict[str, object]:
    """Check if execution may proceed. Returns PASS or BLOCKED with reason."""
    workdir = Path(workdir)
    state_path = workdir / "STATE.md"
    plan_path = workdir / "PLAN.md"
    if not state_path.exists():
        return {"result": "BLOCKED", "reason": "STATE.md missing", "required_transition": "BLOCKED_AMEND"}
    fm = parse_frontmatter(state_path.read_text(encoding="utf-8"))
    approved = fm.get("approved_plan_digest", "")
    approval_status = fm.get("approval_status", fm.get("status", ""))
    # Check approval presence
    if not approved or approved in {"PENDING", "NOT_APPROVED", ""}:
        return {"result": "BLOCKED", "reason": "Human approval missing or pending (approved_plan_digest not set)", "required_transition": "BLOCKED_AMEND"}
    if plan_path.exists():
        current = plan_digest(plan_path)
        if approved != current and approved != "NOT_APPLICABLE":
            return {
                "result": "BLOCKED",
                "reason": "PLAN.md no longer matches approved_plan_digest. Expected approval digest does not match current plan.",
                "expected": approved,
                "actual": current,
                "required_transition": "BLOCKED_AMEND",
            }
    # Also run stale evidence check
    errors = validate_work_artifacts(workdir, repo=repo)
    if errors:
        return {"result": "BLOCKED", "reason": "; ".join(errors), "required_transition": "BLOCKED_AMEND" if any("approved plan" in e.lower() for e in errors) else "FIX_REVERIFY"}
    return {"result": "PASS"}


def readiness_check(workdir: str | Path, repo: str | Path | None = None) -> dict[str, object]:
    """Check if work is READY/COMPLETE. Verifies evidence freshness, plan digest, gates."""
    workdir = Path(workdir)
    errors = validate_work_artifacts(workdir, repo=repo)
    state_path = workdir / "STATE.md"
    fm = parse_frontmatter(state_path.read_text(encoding="utf-8")) if state_path.exists() else {}
    status = fm.get("status", "")
    verify_path = workdir / "VERIFY.md"
    verify_fm = parse_frontmatter(verify_path.read_text(encoding="utf-8")) if verify_path.exists() else {}
    evidence_status = verify_fm.get("evidence_status", "NOT_RUN")
    checks: list[str] = []
    if errors:
        checks.extend(errors)
    if evidence_status != "FRESH":
        checks.append(f"VERIFY.md evidence_status is {evidence_status!r}, not FRESH")
    if status not in {"VERIFIED", "READY", "COMPLETE"}:
        checks.append(f"STATE status is {status!r}, expected VERIFIED/READY/COMPLETE")
    # Check approval digest if PLAN exists
    if (workdir / "PLAN.md").exists() and fm.get("approved_plan_digest", "") in {"", "PENDING", "NOT_APPROVED"}:
        checks.append("approved_plan_digest missing; human approval required")
    if checks:
        return {"result": "NOT_READY", "reasons": checks}
    return {"result": "READY" if status in {"READY", "VERIFIED"} else "COMPLETE", "evidence": "FRESH bound to revision/working_tree/plan_digest"}


def doctor_check(repo: str | Path = ".") -> dict[str, object]:
    """Run planonce doctor checks."""
    repo_path = Path(repo).resolve()
    results: list[dict[str, str]] = []

    def check(label: str, ok: bool, hint: str = "") -> None:
        results.append({"check": label, "status": "PASS" if ok else "WARN", "hint": hint})

    planonce_dir = repo_path / ".planonce"
    check(".planonce exists", planonce_dir.exists(), "Run planonce-init first" if not planonce_dir.exists() else "")
    check("PROJECT.md exists", (planonce_dir / "PROJECT.md").exists())
    check("POLICY.yml exists", (planonce_dir / "POLICY.yml").exists())
    check("standards index exists", (planonce_dir / "standards" / "index.yml").exists())
    # Check workdirs
    work_root = planonce_dir / "work"
    if work_root.exists():
        for workdir in work_root.iterdir():
            if workdir.is_dir():
                errs = validate_work_artifacts(workdir, repo=repo_path)
                check(f"work/{workdir.name} artifacts", len(errs) == 0, "; ".join(errs) if errs else "")
    else:
        check("work directory", False, "No .planonce/work found")
    # Git check
    snap = workspace_snapshot(repo_path)
    check("git available", bool(snap["git_available"]), "Git not available; using unavailable digests" if not snap["git_available"] else "")
    overall = "PASS" if all(r["status"] == "PASS" for r in results) else "WARN"
    return {"overall": overall, "checks": results, "snapshot": snap}


def _normalize_scope(scope: str) -> str:
    value = scope.strip().replace("\\", "/")
    while value.startswith("./"):
        value = value[2:]
    value = posixpath.normpath(value)
    if value in {"", "."} or value.startswith("../") or value == ".." or value.startswith("/"):
        raise ReliabilityError(f"invalid repository-relative lock scope: {scope!r}")
    return value


def _lock_path(repo: Path, scope: str) -> Path:
    key = hashlib.sha256(scope.encode("utf-8")).hexdigest()
    return repo / ".planonce" / "locks" / f"{key}.json"


def acquire_scope_locks(
    repo: str | Path,
    *,
    owner: str,
    scopes: Iterable[str],
    ttl_seconds: int = 3600,
    now: float | None = None,
) -> list[Path]:
    repo = Path(repo).resolve()
    if not owner.strip():
        raise ReliabilityError("lock owner is required")
    if ttl_seconds <= 0:
        raise ReliabilityError("ttl_seconds must be positive")
    timestamp = time.time() if now is None else float(now)
    normalized = sorted({_normalize_scope(scope) for scope in scopes})
    if not normalized:
        raise ReliabilityError("at least one lock scope is required")
    lock_dir = repo / ".planonce" / "locks"
    lock_dir.mkdir(parents=True, exist_ok=True)
    acquired: list[Path] = []
    try:
        for scope in normalized:
            path = _lock_path(repo, scope)
            if path.exists():
                try:
                    existing = json.loads(path.read_text(encoding="utf-8"))
                except (json.JSONDecodeError, OSError):
                    existing = {}
                expires_at = float(existing.get("expires_at", 0))
                if expires_at > timestamp and existing.get("owner") != owner:
                    raise LockConflict(
                        f"scope {scope!r} is locked by {existing.get('owner', 'unknown')} until {expires_at:g}"
                    )
                if expires_at <= timestamp or existing.get("owner") == owner:
                    path.unlink(missing_ok=True)
            payload = {
                "schema": "planonce.lock/v1",
                "owner": owner,
                "scope": scope,
                "acquired_at": timestamp,
                "expires_at": timestamp + ttl_seconds,
            }
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(payload, handle, indent=2, sort_keys=True)
                handle.write("\n")
            acquired.append(path)
    except Exception:
        for path in acquired:
            path.unlink(missing_ok=True)
        raise
    return acquired


def release_scope_locks(repo: str | Path, *, owner: str, scopes: Iterable[str]) -> None:
    repo = Path(repo).resolve()
    for scope in sorted({_normalize_scope(scope) for scope in scopes}):
        path = _lock_path(repo, scope)
        if not path.exists():
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if payload.get("owner") == owner:
            path.unlink(missing_ok=True)


def _main() -> int:
    parser = argparse.ArgumentParser(description="PlanOnce workflow reliability helper")
    sub = parser.add_subparsers(dest="command", required=True)

    digest_p = sub.add_parser("plan-digest", help="Compute normalized SHA-256 of PLAN.md")
    digest_p.add_argument("plan")
    # Alias per roadmap
    hash_p = sub.add_parser("hash-plan", help="Alias for plan-digest (roadmap: planonce hash-plan)")
    hash_p.add_argument("plan")

    snapshot_p = sub.add_parser("snapshot")
    snapshot_p.add_argument("repo", nargs="?", default=".")

    validate_p = sub.add_parser("validate-work")
    validate_p.add_argument("workdir")
    validate_p.add_argument("--repo")

    # New: evidence check alias
    evidence_p = sub.add_parser("evidence", help="Check evidence freshness (alias for validate-work)")
    evidence_p.add_argument("workdir")
    evidence_p.add_argument("--repo")
    evidence_p.add_argument("--check", action="store_true", help="Run evidence check")

    failure_p = sub.add_parser("failure-route")
    failure_p.add_argument("--plan-invalid", action="store_true")
    failure_p.add_argument("--implementation-defect", action="store_true")

    acquire_p = sub.add_parser("lock-acquire")
    acquire_p.add_argument("--repo", default=".")
    acquire_p.add_argument("--owner", required=True)
    acquire_p.add_argument("--scope", action="append", required=True)
    acquire_p.add_argument("--ttl", type=int, default=3600)

    release_p = sub.add_parser("lock-release")
    release_p.add_argument("--repo", default=".")
    release_p.add_argument("--owner", required=True)
    release_p.add_argument("--scope", action="append", required=True)

    approve_p = sub.add_parser("approve", help="Machine-enforce human approval: record plan digest in STATE.md")
    approve_p.add_argument("workdir", help=".planonce/work/<change> directory")
    approve_p.add_argument("--by", dest="approved_by", default="human")

    gate_p = sub.add_parser("gate", help="Execution gate: verify approval and freshness before proceeding")
    gate_p.add_argument("workdir", nargs="?", default=None, help=".planonce/work/<change> or change id")
    gate_p.add_argument("--repo", default=".")
    gate_p.add_argument("--target", default="execution", help="gate target (execution, readiness, etc.)")

    readiness_p = sub.add_parser("readiness", help="Check if work is READY/COMPLETE with fresh evidence")
    readiness_p.add_argument("workdir")
    readiness_p.add_argument("--repo")

    verify_state_p = sub.add_parser("verify-state", help="Validate state machine transition")
    verify_state_p.add_argument("--from", dest="from_state", required=True)
    verify_state_p.add_argument("--to", dest="to_state", required=True)

    doctor_p = sub.add_parser("doctor", help="Run planonce doctor checks")
    doctor_p.add_argument("--repo", default=".")

    args = parser.parse_args()
    if args.command in ("plan-digest", "hash-plan"):
        print(plan_digest(Path(args.plan)))
    elif args.command == "snapshot":
        print(json.dumps(workspace_snapshot(args.repo), indent=2, sort_keys=True))
    elif args.command in ("validate-work", "evidence"):
        workdir = args.workdir if hasattr(args, "workdir") else args.workdir
        errors = validate_work_artifacts(workdir, repo=args.repo if hasattr(args, "repo") else None)
        if errors:
            print("\n".join(errors))
            return 1
        print("PlanOnce work artifacts: PASS")
    elif args.command == "failure-route":
        print(failure_route(plan_invalid=args.plan_invalid, implementation_defect=args.implementation_defect))
    elif args.command == "lock-acquire":
        for path in acquire_scope_locks(args.repo, owner=args.owner, scopes=args.scope, ttl_seconds=args.ttl):
            print(path)
    elif args.command == "lock-release":
        release_scope_locks(args.repo, owner=args.owner, scopes=args.scope)
    elif args.command == "approve":
        result = approve_plan(args.workdir, approved_by=args.approved_by)
        print(json.dumps(result, indent=2))
        print(f"Approved {args.workdir}: {result['approved_plan_digest']}")
    elif args.command == "gate":
        # Resolve workdir: if change id given, look under .planonce/work/<id>
        workdir = args.workdir
        if workdir and not Path(workdir).exists():
            candidate = Path(args.repo) / ".planonce" / "work" / workdir
            if candidate.exists():
                workdir = str(candidate)
        if not workdir:
            print("gate requires workdir or change id", file=os.sys.stderr)
            return 2
        result = gate_execution(workdir, repo=args.repo)
        if result["result"] == "PASS":
            print("PASS")
            return 0
        else:
            print("BLOCKED")
            print("")
            print(f"Reason: {result['reason']}")
            if "expected" in result:
                print(f"Expected: {result['expected']}")
                print(f"Actual: {result['actual']}")
            print(f"Required transition: {result.get('required_transition','BLOCKED_AMEND')}")
            return 1
    elif args.command == "readiness":
        result = readiness_check(args.workdir, repo=args.repo)
        print(json.dumps(result, indent=2))
        return 0 if result["result"] in {"READY", "COMPLETE"} else 1
    elif args.command == "verify-state":
        ok = is_valid_transition(args.from_state, args.to_state)
        print(f"{args.from_state} -> {args.to_state}: {'PASS' if ok else 'BLOCKED'}")
        if not ok:
            print(f"Invalid transition. Allowed from {args.from_state}: {sorted(VALID_TRANSITIONS.get(args.from_state, set()))}")
            return 1
        return 0
    elif args.command == "doctor":
        result = doctor_check(args.repo)
        print(json.dumps(result, indent=2))
        return 0 if result["overall"] == "PASS" else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
