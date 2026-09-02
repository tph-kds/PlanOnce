import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


class ReliabilityContractTests(unittest.TestCase):
    def test_frontmatter_parser_and_plan_digest_are_stable(self):
        from reliability import parse_frontmatter, plan_digest

        text_lf = "---\nschema: planonce.plan/v1\nchange_id: auth\nworkflow: brown-normal\n---\n# Plan  \n\n- item\n"
        text_crlf = text_lf.replace("\n", "\r\n")
        fm = parse_frontmatter(text_lf)
        self.assertEqual(fm["schema"], "planonce.plan/v1")
        self.assertEqual(fm["change_id"], "auth")
        self.assertEqual(plan_digest(text_lf), plan_digest(text_crlf))
        self.assertRegex(plan_digest(text_lf), r"^sha256:[0-9a-f]{64}$")

    def test_failure_route_distinguishes_fix_from_amendment(self):
        from reliability import failure_route

        self.assertEqual(failure_route(plan_invalid=False, implementation_defect=True), "FIX_REVERIFY")
        self.assertEqual(failure_route(plan_invalid=True, implementation_defect=False), "BLOCKED_AMEND")
        self.assertEqual(failure_route(plan_invalid=True, implementation_defect=True), "BLOCKED_AMEND")
        self.assertEqual(failure_route(plan_invalid=False, implementation_defect=False), "DIAGNOSE")

    def test_validate_work_detects_plan_digest_drift(self):
        from reliability import plan_digest, validate_work_artifacts

        with tempfile.TemporaryDirectory() as td:
            work = Path(td)
            plan = work / "PLAN.md"
            state = work / "STATE.md"
            plan.write_text("---\nschema: planonce.plan/v1\nchange_id: c1\nworkflow: brown-normal\n---\n# Plan\n- A\n", encoding="utf-8")
            digest = plan_digest(plan.read_text(encoding="utf-8"))
            state.write_text(
                "---\nschema: planonce.state/v1\nchange_id: c1\nworkflow: brown-normal\n"
                f"approved_plan_digest: {digest}\nstatus: IN_PROGRESS\n---\n# State\n",
                encoding="utf-8",
            )
            self.assertEqual(validate_work_artifacts(work), [])
            plan.write_text(plan.read_text(encoding="utf-8") + "- silently changed\n", encoding="utf-8")
            errors = validate_work_artifacts(work)
            self.assertTrue(any("approved plan digest" in e.lower() for e in errors), errors)

    def test_revision_bound_evidence_becomes_stale_after_change(self):
        from reliability import plan_digest, validate_work_artifacts, workspace_snapshot

        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True)
            (repo / "app.txt").write_text("v1\n", encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-qm", "init"], cwd=repo, check=True)
            snap = workspace_snapshot(repo)
            work = repo / ".planonce" / "work" / "c1"
            work.mkdir(parents=True)
            plan = work / "PLAN.md"
            plan.write_text("---\nschema: planonce.plan/v1\nchange_id: c1\nworkflow: brown-normal\n---\n# Plan\n", encoding="utf-8")
            digest = plan_digest(plan.read_text(encoding="utf-8"))
            (work / "STATE.md").write_text(
                "---\nschema: planonce.state/v1\nchange_id: c1\nworkflow: brown-normal\n"
                f"approved_plan_digest: {digest}\nstatus: IMPLEMENTED_NOT_VERIFIED\n---\n# State\n",
                encoding="utf-8",
            )
            (work / "VERIFY.md").write_text(
                "---\nschema: planonce.verify/v1\nchange_id: c1\n"
                f"revision: {snap['revision']}\nworking_tree_digest: {snap['working_tree_digest']}\n"
                f"plan_digest: {digest}\nevidence_status: FRESH\n---\n# Verify\n",
                encoding="utf-8",
            )
            self.assertEqual(validate_work_artifacts(work, repo=repo), [])
            (repo / "app.txt").write_text("v2\n", encoding="utf-8")
            errors = validate_work_artifacts(work, repo=repo)
            self.assertTrue(any("stale" in e.lower() for e in errors), errors)

    def test_scope_lock_rejects_overlap_recovers_expired_and_releases(self):
        from reliability import LockConflict, acquire_scope_locks, release_scope_locks

        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            acquired = acquire_scope_locks(repo, owner="worker-a", scopes=["src/auth.py"], ttl_seconds=60, now=1000)
            self.assertEqual(len(acquired), 1)
            with self.assertRaises(LockConflict):
                acquire_scope_locks(repo, owner="worker-b", scopes=["./src/auth.py"], ttl_seconds=60, now=1010)
            release_scope_locks(repo, owner="worker-a", scopes=["src/auth.py"])
            acquired2 = acquire_scope_locks(repo, owner="worker-b", scopes=["src/auth.py"], ttl_seconds=10, now=1100)
            self.assertEqual(len(acquired2), 1)
            acquired3 = acquire_scope_locks(repo, owner="worker-c", scopes=["src/auth.py"], ttl_seconds=10, now=1200)
            self.assertEqual(len(acquired3), 1)
            release_scope_locks(repo, owner="worker-c", scopes=["src/auth.py"])

    def test_partial_lock_acquire_rolls_back(self):
        from reliability import LockConflict, acquire_scope_locks

        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            acquire_scope_locks(repo, owner="worker-a", scopes=["src/b.py"], ttl_seconds=60, now=1000)
            with self.assertRaises(LockConflict):
                acquire_scope_locks(repo, owner="worker-b", scopes=["src/a.py", "src/b.py"], ttl_seconds=60, now=1010)
            lock_dir = repo / ".planonce" / "locks"
            payloads = [json.loads(p.read_text(encoding="utf-8")) for p in lock_dir.glob("*.json")]
            self.assertEqual({p["owner"] for p in payloads}, {"worker-a"})

    def test_route_helper_selects_expected_workflows(self):
        from route_task import route_task

        self.assertEqual(route_task(existing=False, size="small")["selected_skill"], "planonce-green-small")
        self.assertEqual(route_task(existing=True, size="normal")["selected_skill"], "planonce-brown-normal")
        # Security-sensitive does not automatically mean Large: refresh-token rotation preserving API stays Normal
        self.assertEqual(route_task(existing=True, size="normal", security_sensitive=True)["selected_skill"], "planonce-brown-normal")
        self.assertTrue(route_task(existing=True, size="normal", security_sensitive=True)["needs_security_review"])
        self.assertEqual(route_task(existing=True, size="small", security_boundary=True)["selected_skill"], "planonce-brown-small")
        self.assertEqual(route_task(existing=True, size="small", auth_model_change=True)["selected_skill"], "planonce-brown-large")
        self.assertEqual(route_task(existing=True, size="small", tenant_isolation_change=True)["selected_skill"], "planonce-brown-large")
        self.assertEqual(route_task(existing=True, size="small", credential_architecture_change=True)["selected_skill"], "planonce-brown-large")
        self.assertEqual(route_task(existing=False, size="normal", destructive_migration=True)["selected_skill"], "planonce-green-large")
        self.assertEqual(route_task(existing=True, size="small", public_contract_break=True)["selected_skill"], "planonce-brown-large")

    def test_artifact_templates_have_versioned_frontmatter(self):
        implementation = [
            "planonce-green-small", "planonce-green-normal", "planonce-green-large",
            "planonce-brown-small", "planonce-brown-normal", "planonce-brown-large",
        ]
        required = {"CONTEXT.template.md": "planonce.context/v1", "STATE.template.md": "planonce.state/v1", "VERIFY.template.md": "planonce.verify/v1"}
        for name in implementation:
            assets = ROOT / "skills" / name / "assets"
            for filename, schema in required.items():
                text = (assets / filename).read_text(encoding="utf-8")
                self.assertTrue(text.startswith("---\n"), f"{name}/{filename}")
                self.assertIn(f"schema: {schema}", text)
            plan = assets / "PLAN.template.md"
            if plan.exists():
                self.assertIn("schema: planonce.plan/v1", plan.read_text(encoding="utf-8"))
            design = assets / "DESIGN.template.md"
            if design.exists():
                self.assertIn("schema: planonce.design/v1", design.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
