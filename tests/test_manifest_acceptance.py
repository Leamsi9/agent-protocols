from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

CHECKER = Path(__file__).resolve().parents[1] / "scripts/check_gated_plan.py"


class ManifestAcceptanceTests(unittest.TestCase):
    def check(self, manifest: str):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "plan.toml"
            path.write_text(manifest)
            result = subprocess.run(
                [sys.executable, str(CHECKER), str(path), "--json"],
                capture_output=True, text=True,
            )
            return result.returncode, json.loads(result.stdout)

    def test_empty_phase_rejected(self):
        code, result = self.check('[phases.accept]\nchecks = []\n')
        self.assertNotEqual(code, 0)
        self.assertFalse(result["passed"])

    def test_omitted_phase_rejected(self):
        code, _ = self.check('phase_order = ["accept"]\n[phases.verify]\nchecks=[]\n[phases.accept]\ndepends_on=["verify"]\nchecks=[]\n')
        self.assertNotEqual(code, 0)

    def test_cyclic_dependencies_rejected(self):
        check = '\n[[phases.{name}.checks]]\nid="proof"\ntype="path_exists"\npath="plan.toml"\n'
        code, result = self.check('[phases.a]\ndepends_on=["b"]' + check.format(name="a") + '[phases.b]\ndepends_on=["a"]' + check.format(name="b"))
        self.assertNotEqual(code, 0)
        self.assertIn("cycles", result["error"])

    def test_unknown_dependency_rejected(self):
        code, result = self.check('[phases.a]\ndepends_on=["missing"]\n[[phases.a.checks]]\nid="proof"\ntype="path_exists"\npath="plan.toml"\n')
        self.assertNotEqual(code, 0)
        self.assertIn("unknown phase", result["error"])

    def test_duplicate_phase_rejected(self):
        code, _ = self.check('phase_order=["a","a"]\n[phases.a]\nchecks=[]\n')
        self.assertNotEqual(code, 0)

    def test_invalid_graph_runs_no_commands(self):
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory) / "must-not-exist"
            manifest = f'''phase_order=["accept","verify"]
[phases.accept]
depends_on=["verify"]
[[phases.accept.checks]]
id="side-effect"
type="command"
command="touch {marker}"
[phases.verify]
[[phases.verify.checks]]
id="proof"
type="path_exists"
path="missing"
'''
            code, _ = self.check(manifest)
            self.assertFalse(marker.exists())
            self.assertNotEqual(code, 0)

    def test_valid_dependency_chain(self):
        code, result = self.check('''phase_order=["a","b"]
[phases.a]
[[phases.a.checks]]
id="plan"
type="path_exists"
path="plan.toml"
[phases.b]
depends_on=["a"]
[[phases.b.checks]]
id="plan"
type="path_exists"
path="plan.toml"
''')
        self.assertEqual(code, 0)
        self.assertTrue(result["passed"])

    def test_unittest_counts_through_cli(self):
        for count, suffix, accepted in [(0, "", False), (1, " (skipped=1)", False), (1, " (expected failures=1)", False), (1, "", True)]:
            with self.subTest(count=count, suffix=suffix):
                command = f"printf 'Ran {count} tests in 0.01s\\n\\nOK{suffix}\\n'"
                manifest = '''[phases.accept]
[[phases.accept.checks]]
id="tests"
type="command"
min_tests=1
max_skipped=0
max_expected_failures=0
command=''' + json.dumps(command) + '\n'
                code, result = self.check(manifest)
                self.assertEqual(code == 0, accepted)
                self.assertEqual(result["passed"], accepted)

    def test_failed_suite_hidden_by_pipeline_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            script = Path(directory) / "bad_test.py"
            script.write_text("import unittest\nclass T(unittest.TestCase):\n def test_bad(self): self.fail('bad')\nunittest.main()\n")
            command = f"{sys.executable} {script} | cat"
            code, result = self.check('[phases.a]\n[[phases.a.checks]]\nid="suite"\ntype="command"\nmin_tests=1\ncommand=' + json.dumps(command) + '\n')
            self.assertNotEqual(code, 0)
            self.assertFalse(result["passed"])

    def test_duplicate_dependency_and_check_ids(self):
        for extra, expected in [('depends_on=["a","a"]', 'duplicate dependencies'), ('', 'duplicate check ids')]:
            check_a = '[phases.a]\n[[phases.a.checks]]\nid="a"\ntype="path_exists"\npath="plan.toml"\n'
            check_b = f'[phases.b]\n{extra}\n[[phases.b.checks]]\nid="b"\ntype="path_exists"\npath="plan.toml"\n'
            if not extra:
                check_b += '[[phases.b.checks]]\nid="b"\ntype="path_exists"\npath="plan.toml"\n'
            code, result = self.check(check_a + check_b)
            self.assertNotEqual(code, 0)
            self.assertIn(expected, result["error"])

    def test_later_invalid_phase_prevents_earlier_execution(self):
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory) / "must-not-exist"
            code, _ = self.check('[phases.a]\n[[phases.a.checks]]\nid="command"\ntype="command"\ncommand=' + json.dumps(f"touch {marker}") + '\n[phases.b]\nchecks=[]\n')
            self.assertNotEqual(code, 0)
            self.assertFalse(marker.exists())

    def test_explicitly_allowed_skips_and_expected_failures(self):
        for field, summary in [("max_skipped", "skipped=1"), ("max_expected_failures", "expected failures=1")]:
            command = f"printf 'Ran 2 tests in 0.01s\\n\\nOK ({summary})\\n'"
            code, result = self.check('[phases.a]\n[[phases.a.checks]]\nid="suite"\ntype="command"\nmin_tests=1\n' + field + '=1\ncommand=' + json.dumps(command) + '\n')
            self.assertEqual(code, 0, result)
