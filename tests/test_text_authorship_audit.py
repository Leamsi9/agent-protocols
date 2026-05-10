#!/usr/bin/env python3
"""Regression tests for the deterministic text authorship audit tool."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
AUDIT = PACKAGE_ROOT / "scripts" / "text_authorship_audit.py"


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


class TextAuthorshipAuditTests(unittest.TestCase):
    def test_latex_extraction_scores_formulaic_passage(self) -> None:
        with tempfile.TemporaryDirectory() as raw_temp:
            root = Path(raw_temp)
            source = root / "paper.tex"
            source.write_text(
                r"""
                It is important to note that this robust framework plays a crucial role
                in navigating the complexities of governance. Moreover, the ecosystem
                highlights the importance of transformative innovation for stakeholders.
                Furthermore, the paragraph offers a broad landscape of implications
                without dates, units, calculations, or concrete source anchors \citep{doe2026}.
                """,
                encoding="utf-8",
            )
            completed = run(
                [
                    "python3",
                    str(AUDIT),
                    "--input",
                    str(source),
                    "--format",
                    "latex",
                    "--min-words",
                    "10",
                    "--json",
                ],
                cwd=root,
            )
            payload = json.loads(completed.stdout)
            self.assertFalse(payload["classifier"])
            self.assertEqual(len(payload["segments"]), 1)
            segment = payload["segments"][0]
            self.assertIn("formulaic_phrases", segment["signals"])
            self.assertIn("it is important to note", segment["formulaic_hits"])
            self.assertEqual(segment["citation_count"], 1)
            self.assertIn(segment["review_priority"], {"medium", "high"})

    def test_ledger_output_seeds_review_rows(self) -> None:
        with tempfile.TemporaryDirectory() as raw_temp:
            root = Path(raw_temp)
            source = root / "draft.md"
            ledger = root / "docs" / "temp" / "text-authorship-audit.toml"
            source.write_text(
                """
                It is worth noting that the broader landscape is multifaceted.
                Moreover, the framework provides a seamless ecosystem and paradigm
                for stakeholders. Furthermore, the paragraph stays critical, crucial,
                essential, generic, abstract, and unsupported by any concrete date,
                unit, source locator, denominator, or author note.
                """,
                encoding="utf-8",
            )
            run(
                [
                    "python3",
                    str(AUDIT),
                    "--input",
                    str(source),
                    "--format",
                    "markdown",
                    "--min-words",
                    "10",
                    "--ledger",
                    str(ledger),
                ],
                cwd=root,
            )
            rendered = ledger.read_text(encoding="utf-8")
            self.assertIn("[segment-001]", rendered)
            self.assertIn('detector_signal = "not_run"', rendered)
            self.assertIn('review_priority = "high"', rendered)
            self.assertIn("this is not an AI detector", rendered)

    def test_baseline_comparison_adds_delta_signals(self) -> None:
        with tempfile.TemporaryDirectory() as raw_temp:
            root = Path(raw_temp)
            baseline = root / "baseline.md"
            draft = root / "draft.md"
            baseline.write_text(
                """
                I start with a blunt claim. Then I add a short caveat, because the
                evidence is mixed. The numbers matter here: 17 cases, three dates,
                and one denominator. This is not elegant, but it is how the argument
                really developed while reading the sources.

                The second note is choppier. It asks a question? It answers it with a
                practical constraint. Then it narrows the claim again, because the
                source only covers one jurisdiction and one year.
                """,
                encoding="utf-8",
            )
            draft.write_text(
                """
                It is important to note that this robust framework can play a crucial
                role in the broader governance ecosystem. It is important to note that
                this robust framework can play a crucial role in the broader governance
                ecosystem. It is important to note that this robust framework can play
                a crucial role in the broader governance ecosystem.
                """,
                encoding="utf-8",
            )
            completed = run(
                [
                    "python3",
                    str(AUDIT),
                    "--input",
                    str(draft),
                    "--baseline",
                    str(baseline),
                    "--format",
                    "markdown",
                    "--min-words",
                    "10",
                    "--json",
                ],
                cwd=root,
            )
            payload = json.loads(completed.stdout)
            segment = payload["segments"][0]
            self.assertIsNotNone(payload["baseline"])
            self.assertIn("baseline_delta", segment)
            self.assertIn("above_baseline_formulaic_density", segment["signals"])
            self.assertIn("below_baseline_burstiness", segment["signals"])


if __name__ == "__main__":
    unittest.main()
