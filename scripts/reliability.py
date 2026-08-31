#!/usr/bin/env python3
"""PlanOnce reliability primitives.

Standard-library only. These helpers make PlanOnce's human-readable Markdown
artifacts machine-verifiable without introducing a daemon or database.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import posixpath
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
    if plan_path.exists() and accepted and accepted not in {"PENDING", "NOT_APPROVED"}:
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
    return errors


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

    digest_p = sub.add_parser("plan-digest")
    digest_p.add_argument("plan")

    snapshot_p = sub.add_parser("snapshot")
    snapshot_p.add_argument("repo", nargs="?", default=".")

    validate_p = sub.add_parser("validate-work")
    validate_p.add_argument("workdir")
    validate_p.add_argument("--repo")

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

    args = parser.parse_args()
    if args.command == "plan-digest":
        print(plan_digest(Path(args.plan)))
    elif args.command == "snapshot":
        print(json.dumps(workspace_snapshot(args.repo), indent=2, sort_keys=True))
    elif args.command == "validate-work":
        errors = validate_work_artifacts(args.workdir, repo=args.repo)
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
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
