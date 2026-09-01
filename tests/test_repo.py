import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
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
IMPLEMENTATION_WORKFLOWS = {
    "planonce-green-small",
    "planonce-green-normal",
    "planonce-green-large",
    "planonce-brown-small",
    "planonce-brown-normal",
    "planonce-brown-large",
}

PROVIDERS = {
    "claude-code.md",
    "codex.md",
    "opencode.md",
    "cursor.md",
    "gemini-cli.md",
    "github-copilot.md",
    "cline.md",
    "kilo-code.md",
    "kiro.md",
    "roo-code.md",
    "windsurf.md",
    "generic.md",
}

CORE_NPX_PROVIDER_IDS = {
    "claude-code",
    "codex",
    "opencode",
    "cursor",
    "gemini-cli",
    "github-copilot",
    "cline",
    "kilo",
    "kiro-cli",
    "roo",
    "windsurf",
    "qwen-code",
    "goose",
    "openhands",
}


def frontmatter(text: str) -> dict[str, str]:
    self_match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not self_match:
        return {}
    result = {}
    for line in self_match.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip().strip('"')
    return result


class RepoContractTests(unittest.TestCase):
    def test_exact_user_facing_skills(self):
        found = {p.parent.name for p in SKILLS.glob("*/SKILL.md")}
        self.assertEqual(found, EXPECTED)

    def test_agent_skills_frontmatter(self):
        for skill in SKILLS.glob("*/SKILL.md"):
            fm = frontmatter(skill.read_text(encoding="utf-8"))
            self.assertEqual(fm.get("name"), skill.parent.name)
            self.assertRegex(fm["name"], r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
            self.assertLessEqual(len(fm["name"]), 64)
            self.assertTrue(fm.get("description"))
            self.assertLessEqual(len(fm["description"]), 1024)
            self.assertLessEqual(len(skill.read_text(encoding="utf-8").splitlines()), 500)

    def test_version_and_upstream_lock_exist(self):
        self.assertEqual((ROOT / "VERSION").read_text().strip(), "1.0.0")
        lock = json.loads((ROOT / "upstream.lock.json").read_text(encoding="utf-8"))
        self.assertEqual(lock["agent_os"]["tag"], "v3.0.0")
        self.assertTrue(lock["agent_os"]["commit"].startswith("809fb4e"))
        self.assertEqual(lock["gsd_core"]["tag"], "v1.12.0")
        self.assertTrue(lock["gsd_core"]["commit"].startswith("ceed559"))
        self.assertEqual(lock["update_policy"], "release-pinned-no-runtime-auto-update")

    def test_upstream_resources_present_with_licenses_and_provenance(self):
        for upstream in ["agent-os", "gsd-core"]:
            base = ROOT / "upstream" / upstream
            self.assertTrue((base / "LICENSE").is_file())
            self.assertTrue((base / "PROVENANCE.md").is_file())
            self.assertTrue((base / "manifest.json").is_file())
            manifest = json.loads((base / "manifest.json").read_text(encoding="utf-8"))
            self.assertTrue(manifest["upstream"].startswith("https://github.com/"))
            self.assertGreaterEqual(len(manifest["files"]), 10)
            for item in manifest["files"]:
                path = base / item["path"]
                self.assertTrue(path.is_file(), path)
                self.assertRegex(item["sha256"], r"^[0-9a-f]{64}$")

    def test_provider_adapters_are_present_and_capability_based(self):
        provider_dir = ROOT / "providers"
        self.assertEqual({p.name for p in provider_dir.glob("*.md")}, PROVIDERS)
        for p in provider_dir.glob("*.md"):
            text = p.read_text(encoding="utf-8").lower()
            self.assertIn("ask human", text)
            self.assertIn("run command", text)
            self.assertIn("read/write", text)
            self.assertIn("fallback", text)

    def test_skills_do_not_require_installing_upstreams(self):
        forbidden = ["install agent os", "install gsd core", "npx @opengsd/gsd-core"]
        for p in SKILLS.glob("*/SKILL.md"):
            text = p.read_text(encoding="utf-8").lower()
            for token in forbidden:
                self.assertNotIn(token, text, f"{token} leaked into {p}")

    def test_all_workflows_have_core_production_contracts(self):
        for name in IMPLEMENTATION_WORKFLOWS:
            text = (SKILLS / name / "SKILL.md").read_text(encoding="utf-8").lower()
            for phrase in [
                "plan once",
                "human gate",
                "evidence",
                "blocked",
                "plan amendment",
                "fresh context",
                "provider fallback",
                ".planonce/",
            ]:
                self.assertIn(phrase, text, f"{name} missing {phrase}")

    def test_small_workflows_are_lightweight(self):
        for name in ["planonce-green-small", "planonce-brown-small"]:
            text = (SKILLS / name / "SKILL.md").read_text(encoding="utf-8").lower()
            self.assertIn("micro-plan", text)
            self.assertIn("interactive", text)
            self.assertIn("do not create", text)
            self.assertIn("upgrade to normal", text)

    def test_normal_workflows_use_one_plan_and_bounded_waves(self):
        for name in ["planonce-green-normal", "planonce-brown-normal"]:
            text = (SKILLS / name / "SKILL.md").read_text(encoding="utf-8").lower()
            self.assertIn("exactly one", text)
            self.assertIn("plan.md", text)
            self.assertIn("wave", text)
            self.assertIn("requirement", text)

    def test_large_workflows_include_architecture_risk_rollback_and_phase_gates(self):
        for name in ["planonce-green-large", "planonce-brown-large"]:
            text = (SKILLS / name / "SKILL.md").read_text(encoding="utf-8").lower()
            for phrase in ["design.md", "risk", "rollback", "phase gate", "one-way"]:
                self.assertIn(phrase, text, f"{name} missing {phrase}")

    def test_brownfield_requires_existing_evidence_and_no_drive_by_refactor(self):
        for name in [n for n in EXPECTED if "brown" in n]:
            text = (SKILLS / name / "SKILL.md").read_text(encoding="utf-8").lower()
            self.assertRegex(text, r"(inspect|map|read).*(existing|current).*(code|implementation|repository)")
            self.assertIn("no drive-by", text)
            self.assertIn("analogous", text)

    def test_init_discovers_only_non_obvious_durable_standards(self):
        text = (SKILLS / "planonce-init" / "SKILL.md").read_text(encoding="utf-8").lower()
        self.assertIn("representative", text)
        self.assertIn("non-obvious", text)
        self.assertIn("human", text)
        self.assertIn("index", text)
        self.assertIn("verification commands", text)

    def test_security_and_one_way_door_escalation_is_documented(self):
        matrix = (ROOT / "docs" / "WORKFLOW_MATRIX.md").read_text(encoding="utf-8").lower()
        self.assertIn("one-way door", matrix)
        self.assertIn("authorization", matrix)
        self.assertIn("destructive migration", matrix)
        self.assertIn("upgrade", matrix)

    def test_state_and_evidence_contracts_support_resume(self):
        state = (ROOT / "docs" / "STATE_CONTRACT.md").read_text(encoding="utf-8").lower()
        for phrase in ["resume", "not_started", "implemented_not_verified", "blocked", "verified", "complete"]:
            self.assertIn(phrase, state)
        evidence = (ROOT / "docs" / "EVIDENCE_CONTRACT.md").read_text(encoding="utf-8").lower()
        for phrase in ["command", "exit code", "scope", "fresh", "requirement coverage", "unverified"]:
            self.assertIn(phrase, evidence)

    def test_eval_suite_covers_routing_and_failure_modes(self):
        cases = json.loads((ROOT / "evals" / "cases.json").read_text(encoding="utf-8"))
        ids = {case["id"] for case in cases}
        required = {
            "route-green-small", "route-brown-normal", "route-brown-large",
            "escalate-one-way-door", "no-duplicate-planning", "brownfield-no-drive-by",
            "provider-no-subagents", "plan-amendment-on-conflict", "evidence-before-complete",
            "resume-after-interruption", "security-boundary-escalation", "small-no-overplanning",
        }
        self.assertTrue(required.issubset(ids), required - ids)

    def test_validation_workflow_and_scripts_exist(self):
        for path in [
            ROOT / "scripts" / "validate.py",
            ROOT / "scripts" / "verify_upstreams.py",
            ROOT / "scripts" / "doctor.py",
            ROOT / ".github" / "workflows" / "validate.yml",
        ]:
            self.assertTrue(path.is_file(), path)

    def test_readme_keeps_single_install_and_multi_provider_positioning(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8").lower()
        self.assertIn("single-install", text)
        self.assertIn("npx skills add", text)
        self.assertIn("--all", text)
        for provider in ["claude code", "codex", "opencode", "cursor", "gemini", "copilot", "cline"]:
            self.assertIn(provider, text)
        self.assertIn("pinned upstream", text)
        self.assertIn("plan once", text)

    def test_each_skill_is_self_contained_for_installers_that_copy_only_skill_dirs(self):
        expected_assets = {
            "planonce-init": {"PROJECT.template.md", "STANDARDS_INDEX.template.yml", "POLICY.template.yml"},
            "planonce-task": {"ROUTING_DECISION.template.md"},
            "planonce-green-small": {"CONTEXT.template.md", "STATE.template.md", "VERIFY.template.md"},
            "planonce-brown-small": {"CONTEXT.template.md", "STATE.template.md", "VERIFY.template.md"},
            "planonce-green-normal": {"CONTEXT.template.md", "PLAN.template.md", "STATE.template.md", "VERIFY.template.md"},
            "planonce-brown-normal": {"CONTEXT.template.md", "PLAN.template.md", "STATE.template.md", "VERIFY.template.md"},
            "planonce-green-large": {"CONTEXT.template.md", "DESIGN.template.md", "PLAN.template.md", "STATE.template.md", "VERIFY.template.md"},
            "planonce-brown-large": {"CONTEXT.template.md", "DESIGN.template.md", "PLAN.template.md", "STATE.template.md", "VERIFY.template.md"},
            "planonce-security": {"SECURITY_REVIEW.template.md"},
            "planonce-security-fix": {"SECURITY_FIX.template.md"},
            "planonce-review": {"REVIEW.template.md"},
            "planonce-skill-audit": {"SKILL_AUDIT.template.md"},
        }
        for name, assets in expected_assets.items():
            skill = SKILLS / name
            self.assertTrue((skill / "references" / "UPSTREAM_GUIDANCE.md").is_file())
            self.assertTrue((skill / "references" / "PROVIDER_GUIDANCE.md").is_file())
            provider_ref = (skill / "references" / "PROVIDER_GUIDANCE.md").read_text(encoding="utf-8").lower()
            for provider in ["claude", "codex", "opencode", "cursor", "gemini", "copilot", "cline", "generic"]:
                self.assertIn(provider, provider_ref, f"{name}: missing provider {provider}")
            ref = (skill / "references" / "UPSTREAM_GUIDANCE.md").read_text(encoding="utf-8")
            self.assertIn("v3.0.0", ref)
            self.assertIn("v1.12.0", ref)
            found = {x.name for x in (skill / "assets").glob("*")}
            self.assertTrue(assets.issubset(found), f"{name}: missing {assets-found}")

    def test_large_templates_include_threat_model_and_risk_scaled_verification(self):
        for name in ["planonce-green-large", "planonce-brown-large"]:
            skill = SKILLS / name
            design = (skill / "assets" / "DESIGN.template.md").read_text(encoding="utf-8").lower()
            verify = (skill / "assets" / "VERIFY.template.md").read_text(encoding="utf-8").lower()
            instructions = (skill / "SKILL.md").read_text(encoding="utf-8").lower()
            self.assertIn("threat model", design)
            self.assertIn("threat model", instructions)
            for phrase in ["security", "migration", "compatibility", "performance", "observability", "ai/llm"]:
                self.assertIn(phrase, verify, f"{name}: missing {phrase}")


    def test_security_skill_is_scan_first_and_evidence_driven(self):
        skill = SKILLS / "planonce-security"
        text = (skill / "SKILL.md").read_text(encoding="utf-8").lower()
        for phrase in [
            "read-only by default", "threat model", "diff", "codebase", "deterministic",
            "secret", "dependency", "sast", "evidence", "confidence", "severity",
            "introduced", "pre-existing", "untrusted repository", "network consent",
            "do not install", "claim secure",
        ]:
            self.assertIn(phrase, text, f"security skill missing {phrase}")
        report = (skill / "assets" / "SECURITY_REVIEW.template.md").read_text(encoding="utf-8").lower()
        for phrase in ["revision", "scope", "finding id", "severity", "confidence", "origin", "evidence", "recommended fix", "residual risk"]:
            self.assertIn(phrase, report)

    def test_security_fix_skill_requires_explicit_finding_and_fresh_verification(self):
        skill = SKILLS / "planonce-security-fix"
        text = (skill / "SKILL.md").read_text(encoding="utf-8").lower()
        for phrase in [
            "explicit", "finding id", "stale", "minimal", "regression test", "reproducer",
            "legitimate behavior", "fresh verification", "blocked", "no drive-by",
            "security boundary", "human gate",
        ]:
            self.assertIn(phrase, text, f"security fix missing {phrase}")
        self.assertNotIn("auto-commit", text)
        self.assertNotIn("auto-push", text)

    def test_review_skill_has_ship_decision_and_backlog_contract(self):
        skill = SKILLS / "planonce-review"
        text = (skill / "SKILL.md").read_text(encoding="utf-8").lower()
        for phrase in [
            "diff-first", "requirements", "correctness", "tests", "operations", "observability",
            "migration", "performance", "security", "independent", "confidence",
            "introduced", "pre-existing", "backlog", "ready_with_backlog", "not_ready", "blocked",
            "ship decision", "fresh evidence",
        ]:
            self.assertIn(phrase, text, f"review missing {phrase}")
        report = (skill / "assets" / "REVIEW.template.md").read_text(encoding="utf-8").lower()
        for phrase in ["ship decision", "must fix", "backlog", "pre-existing", "verification evidence", "unverified"]:
            self.assertIn(phrase, report)

    def test_skill_audit_never_executes_untrusted_candidate_content(self):
        skill = SKILLS / "planonce-skill-audit"
        text = (skill / "SKILL.md").read_text(encoding="utf-8").lower()
        for phrase in [
            "treat candidate", "untrusted", "do not execute", "scripts", "hooks", "mcp",
            "prompt injection", "credential", "remote dependency", "fingerprint", "license",
            "install preview", "rollback", "snyk agent scan", "explicit consent", "sandbox",
        ]:
            self.assertIn(phrase, text, f"skill audit missing {phrase}")

    def test_six_workflows_route_through_review_and_security_gates(self):
        workflow_names = sorted(IMPLEMENTATION_WORKFLOWS)
        for name in workflow_names:
            text = (SKILLS / name / "SKILL.md").read_text(encoding="utf-8").lower()
            self.assertIn("planonce-review", text, f"{name} missing review gate")
            self.assertIn("security trigger", text, f"{name} missing security trigger")
        for name in ["planonce-green-large", "planonce-brown-large"]:
            text = (SKILLS / name / "SKILL.md").read_text(encoding="utf-8").lower()
            self.assertIn("planonce-security", text)
            self.assertIn("mandatory", text)

    def test_native_plugin_manifests_exist_without_duplication(self):
        claude = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        codex = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(claude["name"], "planonce")
        self.assertEqual(claude["version"], "1.0.0")
        self.assertEqual(codex["name"], "planonce")
        self.assertEqual(codex["version"], "1.0.0")
        self.assertEqual(codex["skills"], "./skills/")
        self.assertFalse((ROOT / "plugins" / "planonce" / "skills").exists(), "do not duplicate skill tree for plugins")

    def test_installation_docs_make_npx_primary_and_plugins_secondary(self):
        text = (ROOT / "docs" / "INSTALLATION.md").read_text(encoding="utf-8").lower()
        for phrase in ["npx skills add", "--all", "claude code", "codex", "opencode", "cursor", "gemini", "copilot", "cline", "plugin"]:
            self.assertIn(phrase, text)
        self.assertIn("primary", text)
        self.assertIn("no runtime dependency", text)


    def test_provider_registry_has_exact_npx_ids_and_paths(self):
        registry_path = ROOT / "providers" / "registry.json"
        self.assertTrue(registry_path.is_file())
        data = json.loads(registry_path.read_text(encoding="utf-8"))
        self.assertEqual(data["schema_version"], 1)
        providers = {item["npx_agent"]: item for item in data["providers"]}
        self.assertTrue(CORE_NPX_PROVIDER_IDS.issubset(providers), CORE_NPX_PROVIDER_IDS - providers.keys())
        self.assertEqual(providers["opencode"]["project_path"], ".agents/skills")
        self.assertEqual(providers["kiro-cli"]["project_path"], ".kiro/skills")
        self.assertEqual(providers["roo"]["project_path"], ".roo/skills")
        self.assertEqual(providers["windsurf"]["project_path"], ".windsurf/skills")
        self.assertEqual(providers["kilo"]["preferred_project_path"], ".kilo/skills")
        self.assertEqual(providers["kilo"]["portable_project_path"], ".agents/skills")
        self.assertIn("legacy", providers["kilo"]["cli_mapping_note"].lower())

    def test_install_command_generator_uses_registry_ids(self):
        import subprocess, sys
        script = ROOT / "scripts" / "install_matrix.py"
        self.assertTrue(script.is_file())
        result = subprocess.run(
            [sys.executable, str(script), "--providers", "opencode,kilo,kiro-cli,roo", "--repo", "owner/planonce-agent-skills"],
            cwd=ROOT, text=True, capture_output=True
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        out = result.stdout
        self.assertIn("--skill '*'", out)
        self.assertIn("-a opencode", out)
        self.assertIn("-a kilo", out)
        self.assertIn("-a kiro-cli", out)
        self.assertIn("-a roo", out)
        self.assertNotIn("-a kiro ", out)

    def test_extended_provider_docs_include_kilo_kiro_roo_windsurf(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8").lower()
        install = (ROOT / "docs" / "INSTALLATION.md").read_text(encoding="utf-8").lower()
        matrix = (ROOT / "docs" / "PROVIDER_MATRIX.md").read_text(encoding="utf-8").lower()
        for token in ["opencode", "kilo code", "kiro", "roo code", "windsurf", "qwen code", "goose", "openhands"]:
            self.assertIn(token, readme)
            self.assertIn(token, install)
            self.assertIn(token, matrix)
        self.assertIn("kiro-cli", install)
        self.assertIn("skill://.kiro/skills/*/skill.md", install)
        self.assertIn(".kilo/skills", install)
        self.assertIn(".agents/skills", install)

    def test_skill_provider_guidance_covers_extended_first_class_runtimes(self):
        for skill in SKILLS.glob("*/SKILL.md"):
            provider_ref = (skill.parent / "references" / "PROVIDER_GUIDANCE.md").read_text(encoding="utf-8").lower()
            for provider in ["kilo", "kiro", "roo", "windsurf"]:
                self.assertIn(provider, provider_ref, f"{skill.parent.name}: missing {provider}")

    def test_security_tools_are_optional_and_never_auto_installed(self):
        text = (ROOT / "docs" / "SECURITY_TOOLING.md").read_text(encoding="utf-8").lower()
        for tool in ["semgrep", "osv-scanner", "trivy", "gitleaks", "snyk agent scan"]:
            self.assertIn(tool, text)
        for phrase in ["optional", "must not auto-install", "network", "privacy", "repo-native"]:
            self.assertIn(phrase, text)

    def test_self_audit_scans_referenced_skill_resources(self):
        import subprocess, sys
        probe = SKILLS / "planonce-review" / "references" / "_audit_probe.md"
        probe.write_text("temporary test secret: AKIAABCDEFGHIJKLMNOP\n", encoding="utf-8")
        try:
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "audit_skill_pack.py")],
                cwd=ROOT, text=True, capture_output=True
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("aws-access-key", (result.stdout + result.stderr).lower())
            self.assertIn("_audit_probe.md", result.stdout + result.stderr)
        finally:
            probe.unlink(missing_ok=True)

    def test_release_gate_and_self_audit_exist(self):
        for path in [
            ROOT / "scripts" / "release_gate.py",
            ROOT / "scripts" / "audit_skill_pack.py",
            ROOT / "scripts" / "verify_release_manifest.py",
            ROOT / "docs" / "RELEASE_GATE.md",
        ]:
            self.assertTrue(path.is_file(), path)
        gate = (ROOT / "scripts" / "release_gate.py").read_text(encoding="utf-8")
        self.assertIn("verify_release_manifest.py", gate)
        self.assertIn("run_evals.py", gate)
        self.assertIn("test_*.py", gate)

    def test_eval_suite_covers_security_review_distribution(self):
        cases = json.loads((ROOT / "evals" / "cases.json").read_text(encoding="utf-8"))
        ids = {case["id"] for case in cases}
        required = {
            "security-diff-scan", "security-untrusted-repo", "security-missing-tools",
            "security-fix-stale-finding", "security-fix-verify",
            "review-ship-ready", "review-ready-with-backlog", "review-preexisting-not-blocker",
            "review-required-check-blocked", "skill-audit-no-execution", "distribution-npx-all",
            "distribution-native-plugin-manifests",
        }
        self.assertTrue(required.issubset(ids), required - ids)


    def test_provider_distribution_evals_cover_extended_targets(self):
        cases = json.loads((ROOT / "evals" / "cases.json").read_text(encoding="utf-8"))
        ids = {case["id"] for case in cases}
        required = {
            "distribution-opencode-target",
            "distribution-kilo-path-transition",
            "distribution-kiro-custom-agent",
            "distribution-roo-windsurf-targets",
        }
        self.assertTrue(required.issubset(ids), required - ids)

    def test_review_filters_noise_and_handles_live_production_evidence(self):
        text = (SKILLS / "planonce-review" / "SKILL.md").read_text(encoding="utf-8").lower()
        for phrase in ["80", "production evidence", "ci", "logs", "traces", "incident", "read-only"]:
            self.assertIn(phrase, text)

    def test_project_policy_template_controls_cross_cutting_gates(self):
        init = SKILLS / "planonce-init"
        self.assertTrue((init / "assets" / "POLICY.template.yml").is_file())
        policy = (init / "assets" / "POLICY.template.yml").read_text(encoding="utf-8").lower()
        for phrase in ["security", "review", "network", "human", "large", "normal"]:
            self.assertIn(phrase, policy)
        self.assertTrue((ROOT / "docs" / "POLICY.md").is_file())
        for name in ["planonce-security", "planonce-review"]:
            text = (SKILLS / name / "SKILL.md").read_text(encoding="utf-8").lower()
            self.assertIn(".planonce/policy.yml", text)


    def test_release_manifest_tracks_runtime_harmonization(self):
        manifest = json.loads((ROOT / "RELEASE_MANIFEST.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["version"], "1.0.0")
        self.assertEqual(manifest["release_profile"], "workflow-reliability-production")
        self.assertEqual(manifest["provider_targets_count"], 14)
        self.assertEqual(manifest["upstream_runtime"]["gsd_profile"], "core,audit")
        self.assertEqual(manifest["upstream_runtime"]["gsd_version"], "1.12.0")
        self.assertEqual(manifest["verification"]["contract_tests"], "58/58 PASS")


    def test_release_manifest_source_tree_hash_matches_release_tree(self):
        import hashlib
        manifest = json.loads((ROOT / "RELEASE_MANIFEST.json").read_text(encoding="utf-8"))
        excluded_dirs = {"__pycache__", ".pytest_cache"}
        files = []
        for path in ROOT.rglob("*"):
            if not path.is_file():
                continue
            rel = path.relative_to(ROOT)
            if rel.as_posix() == "RELEASE_MANIFEST.json":
                continue
            if any(part in excluded_dirs for part in rel.parts):
                continue
            files.append(path)
        files.sort(key=lambda path: path.relative_to(ROOT).as_posix())
        digest = hashlib.sha256()
        for path in files:
            rel = path.relative_to(ROOT).as_posix().encode("utf-8")
            digest.update(rel)
            digest.update(b"\0")
            digest.update(path.read_bytes())
            digest.update(b"\0")
        self.assertEqual(manifest["source_files_count"], len(files))
        self.assertEqual(manifest["source_tree_sha256"], digest.hexdigest())

    def test_release_has_no_active_root_claude_runtime_or_repo_metadata(self):
        self.assertFalse((ROOT / ".claude").exists(), "active GSD/Agent OS runtime must not live at repository root")
        # .git exists in the live repo; the test guards against .git leaking into release ZIPs (built elsewhere).
        # Skip the in-repo check: only enforce when not inside a git working tree.
        import subprocess as _sp
        _in_repo = False
        try:
            _sp.run(["git", "rev-parse", "--git-dir"], cwd=str(ROOT), check=True, capture_output=True)
            _in_repo = True
        except Exception:
            pass
        if not _in_repo:
            self.assertFalse((ROOT / ".git").exists(), "release ZIP must not embed repository metadata")
        for path in ROOT.rglob("*"):
            rel = path.relative_to(ROOT)
            self.assertNotIn(".gsd-staging", rel.parts)

    def test_upstream_runtime_layout_and_versions_are_harmonized(self):
        agent = ROOT / "upstream" / "agent-os"
        gsd = ROOT / "upstream" / "gsd-core"
        self.assertTrue((agent / "SOURCE" / "commands" / "agent-os" / "shape-spec.md").is_file())
        self.assertTrue((agent / "SOURCE" / "commands" / "agent-os" / "discover-standards.md").is_file())
        self.assertFalse((agent / "SOURCE" / ".git").exists())
        self.assertEqual((gsd / "runtime" / "VERSION").read_text().strip(), "1.12.0")
        profile = json.loads((gsd / "profiles" / "claude-core-audit" / "PROFILE.json").read_text(encoding="utf-8"))
        self.assertEqual(profile["profile"], "core,audit")
        required = {"gsd-new-project.md", "gsd-discuss-phase.md", "gsd-plan-phase.md", "gsd-execute-phase.md", "gsd-verify-work.md", "gsd-review.md", "gsd-code-review.md"}
        commands = {p.name for p in (gsd / "profiles" / "claude-core-audit" / "commands").glob("*.md")}
        self.assertTrue(required.issubset(commands), required - commands)

    def test_upstream_lock_matches_actual_runtime(self):
        lock = json.loads((ROOT / "upstream.lock.json").read_text(encoding="utf-8"))
        self.assertEqual(lock["planonce_version"], "1.0.0")
        self.assertEqual(lock["agent_os"]["tag"], "v3.0.0")
        self.assertTrue(lock["agent_os"]["commit"].startswith("809fb4e"))
        self.assertEqual(lock["gsd_core"]["tag"], "v1.12.0")
        self.assertTrue(lock["gsd_core"]["commit"].startswith("ceed559"))

    def test_each_implementation_workflow_has_self_contained_runtime_contract(self):
        for name in IMPLEMENTATION_WORKFLOWS:
            ref = SKILLS / name / "references" / "UPSTREAM_RUNTIME.md"
            self.assertTrue(ref.is_file(), f"{name} missing UPSTREAM_RUNTIME.md")
            text = ref.read_text(encoding="utf-8").lower()
            for phrase in ["planonce is the orchestration authority", "agent os", "gsd core", "do not invoke raw"]:
                self.assertIn(phrase, text, f"{name}: missing {phrase}")

    def test_no_machine_specific_paths_or_active_gsd_commands_leak_into_release(self):
        bad = []
        machine_markers = [
            "d:/" + "downloads/program files/nodejs",
            "h:/" + "sideprojects/planonce",
        ]
        for path in ROOT.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".zip", ".idx", ".pack", ".rev"}:
                continue
            try:
                text = path.read_text(encoding="utf-8").lower()
            except UnicodeDecodeError:
                continue
            if any(marker in text for marker in machine_markers):
                bad.append(str(path.relative_to(ROOT)))
        self.assertEqual(bad, [], f"machine-specific paths leaked: {bad}")

    def test_workflows_require_reliability_layer_semantics(self):
        for name in IMPLEMENTATION_WORKFLOWS:
            text = (SKILLS / name / "SKILL.md").read_text(encoding="utf-8").lower()
            for phrase in ["approved plan digest", "revision-bound evidence", "fix_reverify", "blocked_amend", "workspace safety"]:
                self.assertIn(phrase, text, f"{name}: missing {phrase}")

    def test_router_skill_is_classify_only_and_routes_to_canonical_workflows(self):
        text = (SKILLS / "planonce-task" / "SKILL.md").read_text(encoding="utf-8").lower()
        for phrase in ["classify only", "do not plan", "brownfield", "greenfield", "mandatory large", "selected_skill"]:
            self.assertIn(phrase, text)

    def test_python_scripts_compile(self):
        import py_compile
        for script in (ROOT / "scripts").glob("*.py"):
            py_compile.compile(str(script), doraise=True)


if __name__ == "__main__":
    unittest.main()
