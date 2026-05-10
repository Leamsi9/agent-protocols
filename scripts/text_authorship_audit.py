#!/usr/bin/env python3
"""Deterministic prose audit for authorship-integrity review.

This is not an AI detector. It does not estimate authorship probability.
It only finds stable local signals that can help a human reviewer prioritize
passages for provenance, evidence, and style review.
"""

from __future__ import annotations

import argparse
import glob
import json
import math
import re
import statistics
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable


FORMULAIC_PHRASES = [
    "it is important to note",
    "it is worth noting",
    "plays a crucial role",
    "plays a pivotal role",
    "in today's",
    "in this context",
    "in conclusion",
    "as a result",
    "moreover",
    "furthermore",
    "additionally",
    "underscores the importance",
    "highlights the importance",
    "a testament to",
    "delve into",
    "navigating the complexities",
    "multifaceted",
    "robust framework",
    "seamless",
    "leverage",
    "utilize",
    "foster",
    "transformative",
    "not only",
    "but also",
]

ABSTRACT_TERMS = [
    "framework",
    "landscape",
    "ecosystem",
    "paradigm",
    "implications",
    "complexities",
    "stakeholders",
    "innovation",
    "efficiency",
    "optimization",
    "alignment",
    "governance",
    "sustainability",
    "scalability",
]

INTENSIFIERS = [
    "critical",
    "crucial",
    "substantial",
    "significant",
    "profound",
    "dramatic",
    "vast",
    "considerable",
    "essential",
]

HEDGES = [
    "may",
    "might",
    "could",
    "can",
    "likely",
    "suggests",
    "appears",
    "potentially",
]

CITATION_PATTERNS = [
    re.compile(r"\\(?:cite|citep|citet|parencite|textcite|autocite)\s*(?:\[[^\]]*\]\s*){0,2}\{[^}]+\}"),
    re.compile(r"@\w[\w:.-]+"),
]

WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9'_-]*")
NUMBER_RE = re.compile(r"\b\d+(?:[.,]\d+)*(?:%|[A-Za-z]+)?\b")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")
LATEX_COMMAND_WITH_TEXT_RE = re.compile(r"\\(?:section|subsection|subsubsection|paragraph|textbf|emph)\*?\{([^{}]*)\}")
LATEX_COMMAND_RE = re.compile(r"\\[A-Za-z]+\*?(?:\[[^\]]*\])?(?:\{[^{}]*\})?")


@dataclass
class BaselineStats:
    sentence_cv: float | None = None
    mean_sentence_words: float | None = None
    lexical_diversity: float | None = None
    marker_density: float | None = None


@dataclass
class SegmentAudit:
    segment_id: str
    source: str
    paragraph_index: int
    locator: str
    text: str
    word_count: int
    sentence_count: int
    mean_sentence_words: float
    sentence_cv: float
    lexical_diversity: float
    citation_count: int
    number_count: int
    formulaic_hits: list[str]
    abstract_term_count: int
    intensifier_count: int
    hedge_count: int
    score: int
    review_priority: str
    signals: list[str] = field(default_factory=list)
    baseline_delta: dict[str, float] = field(default_factory=dict)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Audit prose for deterministic authorship-integrity review signals. "
            "This is not an AI detector."
        )
    )
    parser.add_argument(
        "--input",
        action="append",
        required=True,
        dest="inputs",
        help="Input text file. Repeat for multiple files.",
    )
    parser.add_argument(
        "--format",
        choices=("auto", "latex", "markdown", "plain"),
        default="auto",
        help="Input format. Defaults to file-extension auto detection.",
    )
    parser.add_argument(
        "--baseline",
        action="append",
        default=[],
        help=(
            "Optional author baseline file or glob. Repeat to add more files. "
            "Metrics are used only for distance-to-baseline review signals."
        ),
    )
    parser.add_argument(
        "--min-words",
        type=int,
        default=35,
        help="Ignore paragraphs shorter than this many words.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON instead of text summary.",
    )
    parser.add_argument(
        "--ledger",
        type=Path,
        help="Write a TOML review ledger seeded from audit results.",
    )
    return parser.parse_args()


def expand_paths(patterns: Iterable[str]) -> list[Path]:
    paths: list[Path] = []
    for pattern in patterns:
        expanded = glob.glob(pattern)
        if expanded:
            paths.extend(Path(item) for item in expanded)
        else:
            paths.append(Path(pattern))
    return paths


def detect_format(path: Path, explicit: str) -> str:
    if explicit != "auto":
        return explicit
    suffix = path.suffix.lower()
    if suffix in {".tex", ".ltx"}:
        return "latex"
    if suffix in {".md", ".markdown"}:
        return "markdown"
    return "plain"


def strip_latex_comments(text: str) -> str:
    rendered_lines: list[str] = []
    for line in text.splitlines():
        chars: list[str] = []
        escaped = False
        for char in line:
            if char == "%" and not escaped:
                break
            chars.append(char)
            escaped = char == "\\" and not escaped
        rendered_lines.append("".join(chars))
    return "\n".join(rendered_lines)


def normalize_text(raw: str, fmt: str) -> str:
    text = raw
    if fmt == "latex":
        text = strip_latex_comments(text)
        text = re.sub(r"\$[^$]*\$", " MATH ", text)
        text = LATEX_COMMAND_WITH_TEXT_RE.sub(r"\1", text)
        for pattern in CITATION_PATTERNS:
            text = pattern.sub(" CITATION ", text)
        text = LATEX_COMMAND_RE.sub(" ", text)
        text = text.replace("{", " ").replace("}", " ")
    elif fmt == "markdown":
        text = re.sub(r"`[^`]*`", " CODE ", text)
        text = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", text)
        text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
        text = re.sub(r"^#{1,6}\s*", "", text, flags=re.MULTILINE)
    text = text.replace("\r\n", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    return text


def split_paragraphs(text: str) -> list[str]:
    candidates = re.split(r"\n\s*\n+", text)
    paragraphs: list[str] = []
    for candidate in candidates:
        paragraph = " ".join(line.strip() for line in candidate.splitlines()).strip()
        paragraph = re.sub(r"\s+", " ", paragraph)
        if paragraph:
            paragraphs.append(paragraph)
    return paragraphs


def words(text: str) -> list[str]:
    return WORD_RE.findall(text)


def sentence_lengths(text: str) -> list[int]:
    sentences = [item.strip() for item in SENTENCE_SPLIT_RE.split(text) if item.strip()]
    lengths = [len(words(sentence)) for sentence in sentences]
    return [length for length in lengths if length > 0] or [len(words(text))]


def coefficient_of_variation(values: list[int]) -> float:
    if not values:
        return 0.0
    mean = statistics.fmean(values)
    if mean == 0:
        return 0.0
    if len(values) == 1:
        return 0.0
    return statistics.pstdev(values) / mean


def phrase_hits(text: str, phrases: list[str]) -> list[str]:
    lower = text.lower()
    hits: list[str] = []
    for phrase in phrases:
        count = lower.count(phrase)
        hits.extend([phrase] * count)
    return hits


def token_hits(token_list: list[str], vocabulary: list[str]) -> int:
    vocab = set(vocabulary)
    return sum(1 for token in token_list if token.lower() in vocab)


def count_citations(raw_text: str) -> int:
    return sum(len(pattern.findall(raw_text)) for pattern in CITATION_PATTERNS)


def count_numbers(text: str) -> int:
    return len(NUMBER_RE.findall(text))


def round_float(value: float) -> float:
    return round(value, 4)


def audit_paragraph(
    *,
    segment_id: str,
    source: Path,
    paragraph_index: int,
    raw_paragraph: str,
    normalized_paragraph: str,
    baseline: BaselineStats | None,
) -> SegmentAudit:
    token_list = words(normalized_paragraph)
    lower_tokens = [token.lower() for token in token_list]
    lengths = sentence_lengths(normalized_paragraph)
    sentence_count = len(lengths)
    mean_sentence = statistics.fmean(lengths) if lengths else 0.0
    sentence_cv = coefficient_of_variation(lengths)
    lexical_diversity = len(set(lower_tokens)) / len(lower_tokens) if lower_tokens else 0.0
    formulaic = phrase_hits(normalized_paragraph, FORMULAIC_PHRASES)
    abstract_count = token_hits(lower_tokens, ABSTRACT_TERMS)
    intensifier_count = token_hits(lower_tokens, INTENSIFIERS)
    hedge_count = token_hits(lower_tokens, HEDGES)
    citation_count = count_citations(raw_paragraph)
    number_count = count_numbers(normalized_paragraph)

    score = 0
    signals: list[str] = []

    if formulaic:
        score += min(30, 10 * len(formulaic))
        signals.append("formulaic_phrases")
    if sentence_count >= 3 and sentence_cv < 0.28:
        score += 16
        signals.append("low_sentence_burstiness")
    if mean_sentence > 32:
        score += 10
        signals.append("long_mean_sentence")
    if lexical_diversity < 0.42 and len(token_list) >= 80:
        score += 8
        signals.append("low_lexical_diversity")
    if abstract_count >= 5:
        score += min(15, (abstract_count - 4) * 3)
        signals.append("high_abstraction_density")
    if intensifier_count >= 3 and citation_count == 0:
        score += 8
        signals.append("unsupported_intensifiers")
    if hedge_count >= 5:
        score += 5
        signals.append("heavy_hedging")
    if len(token_list) >= 90 and citation_count == 0 and number_count == 0:
        score += 8
        signals.append("low_specificity")

    baseline_delta: dict[str, float] = {}
    if baseline is not None:
        marker_density = len(formulaic) / max(1, len(token_list))
        comparisons = {
            "sentence_cv": sentence_cv,
            "mean_sentence_words": mean_sentence,
            "lexical_diversity": lexical_diversity,
            "marker_density": marker_density,
        }
        for key, value in comparisons.items():
            base_value = getattr(baseline, key)
            if base_value is None:
                continue
            delta = value - base_value
            baseline_delta[key] = round_float(delta)
        if baseline.sentence_cv is not None and sentence_cv + 0.12 < baseline.sentence_cv:
            score += 8
            signals.append("below_baseline_burstiness")
        if baseline.marker_density is not None and marker_density > baseline.marker_density + 0.015:
            score += 6
            signals.append("above_baseline_formulaic_density")

    if score >= 34:
        priority = "high"
    elif score >= 16:
        priority = "medium"
    else:
        priority = "low"

    return SegmentAudit(
        segment_id=segment_id,
        source=str(source),
        paragraph_index=paragraph_index,
        locator=f"{source}:paragraph {paragraph_index}",
        text=normalized_paragraph,
        word_count=len(token_list),
        sentence_count=sentence_count,
        mean_sentence_words=round_float(mean_sentence),
        sentence_cv=round_float(sentence_cv),
        lexical_diversity=round_float(lexical_diversity),
        citation_count=citation_count,
        number_count=number_count,
        formulaic_hits=sorted(set(formulaic)),
        abstract_term_count=abstract_count,
        intensifier_count=intensifier_count,
        hedge_count=hedge_count,
        score=score,
        review_priority=priority,
        signals=signals,
        baseline_delta=baseline_delta,
    )


def read_audits(paths: list[Path], fmt: str, min_words: int, baseline: BaselineStats | None) -> list[SegmentAudit]:
    audits: list[SegmentAudit] = []
    segment_counter = 1
    for path in paths:
        if not path.exists():
            raise FileNotFoundError(path)
        raw = path.read_text(encoding="utf-8")
        file_format = detect_format(path, fmt)
        normalized = normalize_text(raw, file_format)
        raw_paragraphs = split_paragraphs(raw)
        normalized_paragraphs = split_paragraphs(normalized)
        paired = zip(raw_paragraphs, normalized_paragraphs, strict=False)
        for paragraph_index, (raw_paragraph, normalized_paragraph) in enumerate(paired, start=1):
            if len(words(normalized_paragraph)) < min_words:
                continue
            segment_id = f"segment-{segment_counter:03d}"
            audits.append(
                audit_paragraph(
                    segment_id=segment_id,
                    source=path,
                    paragraph_index=paragraph_index,
                    raw_paragraph=raw_paragraph,
                    normalized_paragraph=normalized_paragraph,
                    baseline=baseline,
                )
            )
            segment_counter += 1
    return audits


def baseline_from_paths(paths: list[Path], fmt: str, min_words: int) -> BaselineStats | None:
    if not paths:
        return None
    audits = read_audits(paths, fmt, min_words, baseline=None)
    if not audits:
        return None
    marker_densities = [
        len(audit.formulaic_hits) / max(1, audit.word_count) for audit in audits
    ]
    return BaselineStats(
        sentence_cv=statistics.median(audit.sentence_cv for audit in audits),
        mean_sentence_words=statistics.median(audit.mean_sentence_words for audit in audits),
        lexical_diversity=statistics.median(audit.lexical_diversity for audit in audits),
        marker_density=statistics.median(marker_densities),
    )


def toml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def toml_array(values: list[str]) -> str:
    return "[" + ", ".join(toml_string(value) for value in values) + "]"


def write_ledger(path: Path, audits: list[SegmentAudit]) -> None:
    lines = [
        "# Generated by agent-protocols/scripts/text_authorship_audit.py.",
        "# This is a review-priority ledger, not an AI-authorship classification.",
        "",
    ]
    for audit in audits:
        status = "needs_revision" if audit.review_priority in {"medium", "high"} else "todo"
        lines.extend(
            [
                f"[{audit.segment_id}]",
                f"status = {toml_string(status)}",
                f"locator = {toml_string(audit.locator)}",
                'claim_role = "todo"',
                'human_source = "todo"',
                'revision_action = "pending"',
                'detector_signal = "not_run"',
                f"review_priority = {toml_string(audit.review_priority)}",
                f"score = {audit.score}",
                f"word_count = {audit.word_count}",
                f"signals = {toml_array(audit.signals)}",
                (
                    'notes = "Generated by deterministic local audit; '
                    'this is not an AI detector."'
                ),
                "",
            ]
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def print_text_summary(audits: list[SegmentAudit], baseline: BaselineStats | None) -> None:
    print("text_authorship_audit=ok")
    print("classifier=false")
    print("segment_count=" + str(len(audits)))
    if baseline is not None:
        print("baseline=loaded")
    for audit in audits:
        markers = ",".join(audit.formulaic_hits) if audit.formulaic_hits else "-"
        signals = ",".join(audit.signals) if audit.signals else "-"
        print(
            f"{audit.segment_id}\tpriority={audit.review_priority}\t"
            f"score={audit.score}\twords={audit.word_count}\t"
            f"cv={audit.sentence_cv}\tmarkers={markers}\tsignals={signals}\t"
            f"locator={audit.locator}"
        )


def main() -> int:
    args = parse_args()
    try:
        input_paths = expand_paths(args.inputs)
        baseline_paths = expand_paths(args.baseline)
        baseline = baseline_from_paths(baseline_paths, args.format, args.min_words)
        audits = read_audits(input_paths, args.format, args.min_words, baseline)
        if args.ledger is not None:
            write_ledger(args.ledger, audits)
        if args.json:
            payload = {
                "classifier": False,
                "note": "This is not an AI detector.",
                "baseline": asdict(baseline) if baseline is not None else None,
                "segments": [asdict(audit) for audit in audits],
            }
            print(json.dumps(payload, indent=2, sort_keys=True))
        else:
            print_text_summary(audits, baseline)
        return 0
    except (OSError, ValueError) as exc:
        print(f"text_authorship_audit_error={exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
