from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "planonce-init",
    "planonce-task",
    "planonce-green-small",
    "planonce-green-normal",
    "planonce-green-large",
    "planonce-brown-small",
    "planonce-brown-normal",
    "planonce-brown-large",
    "planonce-security",
    "planonce-security-fix",
    "planonce-review",
    "planonce-skill-audit",
}
REQUIRED_NPX_IDS = {
    "claude-code", "codex", "opencode", "cursor", "gemini-cli",
    "github-copilot", "cline", "kilo", "kiro-cli", "roo", "windsurf",
    "qwen-code", "goose", "openhands",
}
errors = []
found = {p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md")}
if found != EXPECTED:
    errors.append(f"skills mismatch: {sorted(found)}")

for p in (ROOT / "skills").glob("*/SKILL.md"):
    t = p.read_text(encoding="utf-8")
    lines = t.splitlines()
    if len(lines) < 4 or lines[0] != "---":
        errors.append(f"invalid frontmatter: {p}")
        continue
    try:
        end = lines[1:].index("---") + 1
    except ValueError:
        errors.append(f"invalid frontmatter: {p}")
        continue
    fm = {}
    for line in lines[1:end]:
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"')
    name = fm.get("name", "")
    desc = fm.get("description", "")
    if name != p.parent.name:
        errors.append(f"name mismatch: {p}")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        errors.append(f"bad name: {name}")
    if len(name) > 64:
        errors.append(f"name too long: {name}")
    if not desc or len(desc) > 1024:
        errors.append(f"bad description: {name}")
    if len(lines) > 500:
        errors.append(f"SKILL.md >500 lines: {p}")
    for required_ref in ["UPSTREAM_GUIDANCE.md", "PROVIDER_GUIDANCE.md"]:
        ref = p.parent / "references" / required_ref
        if not ref.exists():
            errors.append(f"missing {required_ref}: {p.parent.name}")
    if p.parent.name in {
        "planonce-green-small", "planonce-green-normal", "planonce-green-large",
        "planonce-brown-small", "planonce-brown-normal", "planonce-brown-large",
    } and not (p.parent / "references" / "UPSTREAM_RUNTIME.md").is_file():
        errors.append(f"missing UPSTREAM_RUNTIME.md: {p.parent.name}")

json.loads((ROOT / "evals" / "cases.json").read_text(encoding="utf-8"))
json.loads((ROOT / "upstream.lock.json").read_text(encoding="utf-8"))

registry_path = ROOT / "providers" / "registry.json"
if not registry_path.is_file():
    errors.append("missing provider registry")
else:
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    if registry.get("schema_version") != 1:
        errors.append("unexpected provider registry schema")
    items = registry.get("providers", [])
    ids = [item.get("npx_agent") for item in items]
    if len(ids) != len(set(ids)):
        errors.append("duplicate npx provider ids")
    missing = REQUIRED_NPX_IDS - set(ids)
    if missing:
        errors.append(f"missing npx provider ids: {sorted(missing)}")
    for item in items:
        pid = item.get("npx_agent", "")
        if not pid or not item.get("display_name") or not item.get("project_path"):
            errors.append(f"incomplete provider registry entry: {pid or '<missing>'}")
        adapter = item.get("adapter")
        if item.get("support_tier") == "first-class" and adapter and not (ROOT / "providers" / adapter).is_file():
            errors.append(f"missing first-class provider adapter: {adapter}")
    by_id = {item["npx_agent"]: item for item in items if item.get("npx_agent")}
    kilo = by_id.get("kilo", {})
    if kilo.get("preferred_project_path") != ".kilo/skills" or kilo.get("portable_project_path") != ".agents/skills":
        errors.append("kilo compatibility paths not pinned")
    kiro = by_id.get("kiro-cli", {})
    if kiro.get("project_path") != ".kiro/skills":
        errors.append("kiro-cli path mismatch")

for provider in [
    "claude-code", "codex", "opencode", "cursor", "gemini-cli", "github-copilot",
    "cline", "kilo-code", "kiro", "roo-code", "windsurf", "generic"
]:
    if not (ROOT / "providers" / f"{provider}.md").exists():
        errors.append(f"missing provider: {provider}")

version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
if version != "1.0.0":
    errors.append(f"unexpected version: {version}")
for rel in [
    ".claude-plugin/plugin.json", ".codex-plugin/plugin.json",
    "docs/INSTALLATION.md", "docs/PROVIDER_MATRIX.md", "docs/SECURITY_TOOLING.md",
    "docs/REVIEW_MODEL.md", "docs/RELEASE_GATE.md", "docs/RESEARCH_PROVENANCE.md",
    "docs/POLICY.md", "docs/TASKS_QUICKSTART.md", "docs/ARTIFACT_SCHEMA.md",
    "docs/WORKSPACE_SAFETY.md", "docs/EVAL_HARNESS.md", "scripts/install_matrix.py",
    "scripts/reliability.py", "scripts/route_task.py", "scripts/run_evals.py", "scripts/run_agent_evals.py",
]:
    path = ROOT / rel
    if not path.is_file():
        errors.append(f"missing release surface: {rel}")
for rel in [".claude-plugin/plugin.json", ".codex-plugin/plugin.json"]:
    path = ROOT / rel
    if path.exists():
        manifest = json.loads(path.read_text(encoding="utf-8"))
        if manifest.get("name") != "planonce" or manifest.get("version") != version:
            errors.append(f"plugin manifest mismatch: {rel}")


if (ROOT / ".claude").exists():
    errors.append("active root .claude runtime must not be distributed")
# Only enforce .git exclusion for release packaging (not repo/CI validation)
import subprocess, os
_in_repo = False
try:
    subprocess.run(["git", "rev-parse", "--git-dir"], cwd=str(ROOT), check=True, capture_output=True)
    _in_repo = True
except Exception:
    pass
if not _in_repo and (ROOT / ".git").exists():
    errors.append("release must not embed .git")
if not (ROOT / "upstream" / "agent-os" / "SOURCE" / "commands" / "agent-os" / "shape-spec.md").is_file():
    errors.append("missing exact Agent OS source export")
if not (ROOT / "upstream" / "gsd-core" / "runtime" / "VERSION").is_file():
    errors.append("missing GSD runtime VERSION")
elif (ROOT / "upstream" / "gsd-core" / "runtime" / "VERSION").read_text(encoding="utf-8").strip() != "1.12.0":
    errors.append("GSD runtime is not v1.12.0")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"OK: PlanOnce {version} — {len(found)} skills, {len(REQUIRED_NPX_IDS)} pinned npx provider targets, evals and upstream pins validated")
