#!/usr/bin/env python3
"""Regression tests for repo-state cleanup tooling and skill vendoring."""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
REPO_STATE = PACKAGE_ROOT / "scripts" / "repo_state.py"
INSTALLER = PACKAGE_ROOT / "scripts" / "install.py"


def run_ok(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    if completed.returncode != 0:
        raise AssertionError(
            "command failed\n"
            f"args: {' '.join(args)}\n"
            f"stdout:\n{completed.stdout}\n"
            f"stderr:\n{completed.stderr}"
        )
    return completed


def init_test_repo(repo_dir: Path) -> None:
    run_ok(["git", "init", "-b", "main", str(repo_dir)])
    run_ok(["git", "-C", str(repo_dir), "config", "user.name", "Test User"])
    run_ok(["git", "-C", str(repo_dir), "config", "user.email", "test@example.com"])
    (repo_dir / "README.md").write_text("seed\n", encoding="utf-8")
    run_ok(["git", "-C", str(repo_dir), "add", "README.md"])
    run_ok(["git", "-C", str(repo_dir), "commit", "-m", "initial"])


class RepoStateTests(unittest.TestCase):
    def test_repo_state_reports_and_safely_cleans_stale_shadowed_and_merged_orphans(self) -> None:
        with tempfile.TemporaryDirectory() as raw_temp:
            temp_dir = Path(raw_temp)
            repo_dir = temp_dir / "repo"
            attached_dir = temp_dir / "attached-worktree"
            stale_dir = temp_dir / "stale-worktree"
            scan_dir = temp_dir / ".worktrees"
            orphan_dir = scan_dir / "repo-orphaned"
            shadow_dir = scan_dir / "repo-shadowed"

            init_test_repo(repo_dir)
            scan_dir.mkdir()
            orphan_dir.mkdir()
            orphan_dir.joinpath(".git").write_text(
                f"gitdir: {repo_dir / '.git/worktrees/repo-orphaned-admin'}\n",
                encoding="utf-8",
            )

            run_ok(["git", "-C", str(repo_dir), "branch", "feature/orphaned"])
            run_ok(
                [
                    "git",
                    "-C",
                    str(repo_dir),
                    "worktree",
                    "add",
                    "-b",
                    "feature/attached",
                    str(attached_dir),
                ]
            )
            attached_dir.joinpath("dirty.txt").write_text("untracked\n", encoding="utf-8")
            shadow_dir.mkdir()
            shadow_dir.joinpath(".git").write_text(
                attached_dir.joinpath(".git").read_text(encoding="utf-8"),
                encoding="utf-8",
            )

            run_ok(
                [
                    "git",
                    "-C",
                    str(repo_dir),
                    "worktree",
                    "add",
                    "-b",
                    "feature/stale",
                    str(stale_dir),
                ]
            )
            shutil.rmtree(stale_dir)

            output = run_ok(
                [
                    "python3",
                    str(REPO_STATE),
                    "--repo",
                    str(repo_dir),
                    "--scan-dir",
                    str(scan_dir),
                    "--json",
                ]
            )
            payload = json.loads(output.stdout)
            self.assertEqual(payload["summary"]["stale_registered_worktrees"], 1)
            self.assertEqual(payload["summary"]["orphaned_checkout_dirs"], 1)
            self.assertEqual(payload["summary"]["shadowed_checkout_dirs"], 1)

            attached = next(
                branch
                for branch in payload["branches"]
                if branch["branch"] == "feature/attached"
            )
            self.assertTrue(attached["dirty"])

            cleaned = run_ok(
                [
                    "python3",
                    str(REPO_STATE),
                    "--repo",
                    str(repo_dir),
                    "--scan-dir",
                    str(scan_dir),
                    "--apply-safe-cleanup",
                    "--json",
                ]
            )
            cleaned_payload = json.loads(cleaned.stdout)
            self.assertEqual(cleaned_payload["summary"]["stale_registered_worktrees"], 0)
            self.assertEqual(cleaned_payload["summary"]["orphaned_checkout_dirs"], 0)
            self.assertEqual(cleaned_payload["summary"]["shadowed_checkout_dirs"], 0)
            self.assertFalse(orphan_dir.exists())
            self.assertFalse(shadow_dir.exists())
            self.assertTrue(
                any(
                    action["action"] == "git_worktree_prune"
                    for action in cleaned_payload["applied_actions"]
                )
            )
            self.assertFalse(
                subprocess.run(
                    [
                        "git",
                        "-C",
                        str(repo_dir),
                        "show-ref",
                        "--verify",
                        "--quiet",
                        "refs/heads/feature/orphaned",
                    ]
                ).returncode
                == 0
            )
            self.assertTrue(Path(cleaned_payload["quarantine_dir"]).is_dir())

    def test_installer_vendors_git_cleanup_skill(self) -> None:
        with tempfile.TemporaryDirectory() as raw_temp:
            target = Path(raw_temp) / "consumer"
            target.mkdir()
            run_ok(
                [
                    "python3",
                    str(INSTALLER),
                    "--target",
                    str(target),
                    "--repo-id",
                    "consumer",
                    "--yes",
                    "--skip-workspace-discovery",
                ]
            )
            skill = target / "agent-protocols" / "skills" / "git-cleanup" / "SKILL.md"
            self.assertTrue(skill.is_file())
            self.assertIn("name: git-cleanup", skill.read_text(encoding="utf-8"))

    def test_installer_vendors_citation_protocol_and_tools(self) -> None:
        with tempfile.TemporaryDirectory() as raw_temp:
            target = Path(raw_temp) / "consumer"
            target.mkdir()
            run_ok(
                [
                    "python3",
                    str(INSTALLER),
                    "--target",
                    str(target),
                    "--repo-id",
                    "consumer",
                    "--yes",
                    "--skip-workspace-discovery",
                ]
            )
            protocol = target / "agent-protocols" / "citation-verification-protocol.md"
            inventory = target / "agent-protocols" / "scripts" / "citation_inventory.py"
            ledger_gate = target / "agent-protocols" / "scripts" / "citation_check_audit_ledger.py"
            self.assertTrue(protocol.is_file())
            self.assertTrue(inventory.is_file())
            self.assertTrue(ledger_gate.is_file())
            self.assertIn("Level 1", protocol.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
