from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "check_gated_plan", ROOT / "scripts" / "check_gated_plan.py"
)
assert SPEC is not None and SPEC.loader is not None
CHECKER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CHECKER
SPEC.loader.exec_module(CHECKER)


def git(*args: str, cwd: Path) -> None:
    subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    )


class GitBranchWorktreeTests(unittest.TestCase):
    def test_current_true_rejects_a_different_checkout(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            task_root = Path(temporary_directory)
            task_repo = task_root / "repo"
            task_worktree = task_root / "feature-worktree"
            task_repo.mkdir()
            git("init", "-b", "main", cwd=task_repo)
            git("config", "user.name", "Protocol Test", cwd=task_repo)
            git("config", "user.email", "protocol@example.test", cwd=task_repo)
            (task_repo / "README.md").write_text("fixture\n", encoding="utf-8")
            git("add", "README.md", cwd=task_repo)
            git("commit", "-m", "fixture", cwd=task_repo)
            git("worktree", "add", "-b", "feature/example", str(task_worktree), cwd=task_repo)

            task_check = {
                "id": "branch-worktree-bound",
                "type": "git_branch_worktree",
                "repo": ".",
                "branch": "feature/example",
                "current": True,
            }
            task_manifest = {"branch": "feature/example"}

            task_wrong_checkout = CHECKER.run_check(
                task_repo, task_check, task_manifest
            )
            task_right_checkout = CHECKER.run_check(
                task_worktree, task_check, task_manifest
            )

            self.assertFalse(task_wrong_checkout.passed)
            self.assertIn("current checkout", task_wrong_checkout.detail)
            self.assertTrue(task_right_checkout.passed)

    def test_current_defaults_false_for_cross_worktree_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            task_root = Path(temporary_directory)
            task_repo = task_root / "repo"
            task_worktree = task_root / "feature-worktree"
            task_repo.mkdir()
            git("init", "-b", "main", cwd=task_repo)
            git("config", "user.name", "Protocol Test", cwd=task_repo)
            git("config", "user.email", "protocol@example.test", cwd=task_repo)
            (task_repo / "README.md").write_text("fixture\n", encoding="utf-8")
            git("add", "README.md", cwd=task_repo)
            git("commit", "-m", "fixture", cwd=task_repo)
            git("worktree", "add", "-b", "feature/example", str(task_worktree), cwd=task_repo)

            task_result = CHECKER.run_check(
                task_repo,
                {
                    "id": "branch-worktree-inventory",
                    "type": "git_branch_worktree",
                    "repo": ".",
                    "branch": "feature/example",
                },
                {"branch": "feature/example"},
            )

            self.assertTrue(task_result.passed)


if __name__ == "__main__":
    unittest.main()
