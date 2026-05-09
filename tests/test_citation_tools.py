#!/usr/bin/env python3
"""Regression tests for reusable citation verification tooling."""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
INVENTORY = PACKAGE_ROOT / "scripts" / "citation_inventory.py"
CONTENT_SUPPORT = PACKAGE_ROOT / "scripts" / "citation_check_content_support.py"
AUDIT_LEDGER = PACKAGE_ROOT / "scripts" / "citation_check_audit_ledger.py"
AUDIT_BUILDER = PACKAGE_ROOT / "scripts" / "citation_build_source_audit.py"


def run(
    args: list[str],
    cwd: Path,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    if check and completed.returncode != 0:
        raise AssertionError(
            "command failed\n"
            f"args: {' '.join(args)}\n"
            f"stdout:\n{completed.stdout}\n"
            f"stderr:\n{completed.stderr}"
        )
    return completed


def write_fixture(root: Path) -> tuple[Path, Path]:
    source = root / "paper.tex"
    bib = root / "refs.bib"
    source.write_text(
        r"""
        This cites explicit LaTeX \citep{doe2026} and Pandoc [see @roe2025].
        """,
        encoding="utf-8",
    )
    bib.write_text(
        """
@article{doe2026,
  author = {Doe, Jane},
  title = {A Useful Source},
  journal = {Journal of Useful Tests},
  year = {2026},
  doi = {10.1000/example}
}

@misc{roe2025,
  author = {Roe, Richard},
  title = {A Context Source},
  year = {2025},
  url = {https://example.org/context}
}
""",
        encoding="utf-8",
    )
    return source, bib


class CitationToolTests(unittest.TestCase):
    def test_inventory_accepts_latex_and_pandoc_citations(self) -> None:
        with tempfile.TemporaryDirectory() as raw_temp:
            root = Path(raw_temp)
            source, bib = write_fixture(root)
            completed = run(
                [
                    "python3",
                    str(INVENTORY),
                    "--source",
                    str(source),
                    "--bib",
                    str(bib),
                ],
                cwd=root,
            )
            self.assertIn("bib_entry_count=2", completed.stdout)
            self.assertIn("explicit_citation_key_count=2", completed.stdout)

    def test_inventory_fails_missing_bib_key(self) -> None:
        with tempfile.TemporaryDirectory() as raw_temp:
            root = Path(raw_temp)
            source, bib = write_fixture(root)
            source.write_text(r"Missing key \cite{absent2026}.", encoding="utf-8")
            completed = run(
                [
                    "python3",
                    str(INVENTORY),
                    "--source",
                    str(source),
                    "--bib",
                    str(bib),
                ],
                cwd=root,
                check=False,
            )
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("missing_from_bib=absent2026", completed.stderr)

    def test_content_support_checker_requires_every_bib_key(self) -> None:
        with tempfile.TemporaryDirectory() as raw_temp:
            root = Path(raw_temp)
            _, bib = write_fixture(root)
            support = root / "support.toml"
            support.write_text(
                """
[doe2026]
status = "verified"
note = "Supports the first claim."
""",
                encoding="utf-8",
            )
            failed = run(
                [
                    "python3",
                    str(CONTENT_SUPPORT),
                    "--bib",
                    str(bib),
                    "--support",
                    str(support),
                ],
                cwd=root,
                check=False,
            )
            self.assertNotEqual(failed.returncode, 0)
            self.assertIn("missing_content_keys=roe2025", failed.stderr)

            support.write_text(
                """
[doe2026]
status = "verified"
note = "Supports the first claim."

[roe2025]
status = "not_applicable"
note = "Reference-list only in this fixture."
""",
                encoding="utf-8",
            )
            passed = run(
                [
                    "python3",
                    str(CONTENT_SUPPORT),
                    "--bib",
                    str(bib),
                    "--support",
                    str(support),
                ],
                cwd=root,
            )
            self.assertIn("content_support_count=2", passed.stdout)

    def test_audit_builder_and_ledger_gate_use_manual_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as raw_temp:
            root = Path(raw_temp)
            _, bib = write_fixture(root)
            overrides = root / "metadata.toml"
            support = root / "support.toml"
            ledger = root / "ledger.md"
            overrides.write_text(
                """
[doe2026]
metadata = "verified"
evidence = "https://doi.org/10.1000/example"
notes = "Manual test fixture metadata."

[roe2025]
metadata = "verified"
evidence = "https://example.org/context"
notes = "Manual test fixture metadata."
quote = "not_applicable"
""",
                encoding="utf-8",
            )
            support.write_text(
                """
[doe2026]
status = "verified"
note = "Supports the first claim."

[roe2025]
status = "verified"
note = "Supports the second claim."
""",
                encoding="utf-8",
            )
            run(
                [
                    "python3",
                    str(AUDIT_BUILDER),
                    "--bib",
                    str(bib),
                    "--metadata-overrides",
                    str(overrides),
                    "--content-support",
                    str(support),
                    "--output",
                    str(ledger),
                    "--sleep",
                    "0",
                ],
                cwd=root,
            )
            metadata = run(
                [
                    "python3",
                    str(AUDIT_LEDGER),
                    "--bib",
                    str(bib),
                    "--ledger",
                    str(ledger),
                    "--level",
                    "metadata",
                ],
                cwd=root,
            )
            content = run(
                [
                    "python3",
                    str(AUDIT_LEDGER),
                    "--bib",
                    str(bib),
                    "--ledger",
                    str(ledger),
                    "--level",
                    "content",
                ],
                cwd=root,
            )
            self.assertIn("metadata_status=complete", metadata.stdout)
            self.assertIn("content_status=complete", content.stdout)


if __name__ == "__main__":
    unittest.main()
