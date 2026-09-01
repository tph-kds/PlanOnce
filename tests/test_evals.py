import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class EvalHarnessTests(unittest.TestCase):
    def test_deterministic_runtime_evals_pass(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "run_evals.py")],
            cwd=ROOT, text=True, capture_output=True
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("runtime evals: pass", (result.stdout + result.stderr).lower())

    def test_agent_eval_runner_scores_mock_adapter(self):
        # Skipped on Windows: subprocess command resolution differs from POSIX environments.
        import sys, os
        if os.name == "nt":
            self.skipTest("agent-eval adapter harness is POSIX-specific in this environment")
        adapter = ROOT / "tests" / "fixtures" / "mock_agent_adapter.py"
        result = subprocess.run(
            [
                sys.executable, str(ROOT / "scripts" / "run_agent_evals.py"),
                "--adapter-command", f"{sys.executable} {adapter}",
                "--cases", str(ROOT / "evals" / "agent_cases.json"),
            ],
            cwd=ROOT, text=True, capture_output=True
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("agent evals: pass", (result.stdout + result.stderr).lower())

    def test_agent_eval_cases_cover_routing_scope_and_ship_honesty(self):
        cases = json.loads((ROOT / "evals" / "agent_cases.json").read_text(encoding="utf-8"))
        ids = {case["id"] for case in cases}
        self.assertTrue({"agent-route-green-small", "agent-route-brown-normal", "agent-route-auth-large", "agent-evidence-honesty"}.issubset(ids))


if __name__ == "__main__":
    unittest.main()
