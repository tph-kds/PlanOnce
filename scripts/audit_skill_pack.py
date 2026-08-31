#!/usr/bin/env python3
"""Static, no-execution self-audit for the PlanOnce Agent Skill pack."""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"

SECRET_PATTERNS = {
    "private-key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "openai-like-key": re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{24,}\b"),
    "github-token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    "aws-access-key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
}
DANGEROUS_INSTRUCTION_PATTERNS = {
    "curl-pipe-shell": re.compile(r"curl[^\n|]{0,500}\|\s*(?:sh|bash)\b", re.I),
    "wget-pipe-shell": re.compile(r"wget[^\n|]{0,500}\|\s*(?:sh|bash)\b", re.I),
    "powershell-download-exec": re.compile(r"(?:Invoke-WebRequest|iwr)[^\n]{0,500}\|\s*(?:iex|Invoke-Expression)", re.I),
    "root-delete": re.compile(r"\brm\s+-rf\s+/(?:\s|$)"),
    "chmod-777": re.compile(r"\bchmod\s+777\b"),
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def main() -> int:
    errors: list[str] = []
    names: set[str] = set()
    audited = 0

    for skill_md in sorted(SKILLS.glob("*/SKILL.md")):
        audited += 1
        text = skill_md.read_text(encoding="utf-8")
        name_match = re.search(r"^name:\s*([^\n]+)$", text, re.M)
        if not name_match:
            errors.append(f"missing name: {skill_md}")
            continue
        name = name_match.group(1).strip().strip('"')
        if name in names:
            errors.append(f"duplicate skill name: {name}")
        names.add(name)

        # Scan the complete installed skill surface, not just SKILL.md. References/assets can
        # influence an agent after activation and therefore belong to the supply-chain boundary.
        text_suffixes = {".md", ".txt", ".yml", ".yaml", ".json", ".py", ".sh", ".ps1"}
        for candidate_file in sorted(
            f for f in skill_md.parent.rglob("*") if f.is_file() and f.suffix.lower() in text_suffixes
        ):
            candidate_text = candidate_file.read_text(encoding="utf-8", errors="replace")
            for label, pattern in SECRET_PATTERNS.items():
                if pattern.search(candidate_text):
                    errors.append(f"possible {label} in {candidate_file}")
            # Validate only actual executable instruction shapes, not prose that merely names a risk.
            for label, pattern in DANGEROUS_INSTRUCTION_PATTERNS.items():
                if pattern.search(candidate_text):
                    errors.append(f"dangerous instruction pattern {label} in {candidate_file}")

        for rel in re.findall(r"`((?:references|assets)/[^`]+)`", text):
            # Ignore user-created output artifacts; only bundled references/assets are checked.
            candidate = skill_md.parent / rel
            if not candidate.exists():
                errors.append(f"broken bundled reference {rel} in {skill_md}")

        # A self-contained installed skill should have a provider fallback reference.
        if not (skill_md.parent / "references" / "PROVIDER_GUIDANCE.md").exists():
            errors.append(f"missing provider guidance: {skill_md.parent.name}")

    for script in sorted((ROOT / "scripts").glob("*.py")):
        text = script.read_text(encoding="utf-8")
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"possible {label} in executable {script}")

    if errors:
        print("PlanOnce static skill-pack audit: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    manifest = hashlib.sha256()
    for path in sorted(p for p in SKILLS.rglob("*") if p.is_file()):
        manifest.update(path.relative_to(ROOT).as_posix().encode())
        manifest.update(bytes.fromhex(sha256(path)))
    print(f"PlanOnce static skill-pack audit: PASS — {audited} skills")
    print(f"Skill-tree fingerprint: {manifest.hexdigest()}")
    print("No candidate code was executed by this audit.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
