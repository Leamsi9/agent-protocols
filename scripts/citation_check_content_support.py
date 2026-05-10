#!/usr/bin/env python3
"""Check or scaffold citation content-support ledgers for every BibTeX key."""

from __future__ import annotations

import argparse
import json
import sys
import tomllib
from pathlib import Path

from citation_inventory import BibEntry, parse_all_bib_entries


PASSING_STATUSES = {"verified", "not_applicable"}
DEFAULT_STATUS = "todo"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bib", action="append", type=Path, required=True)
    parser.add_argument("--support", type=Path, required=True)
    parser.add_argument(
        "--update",
        action="store_true",
        help=(
            "Create or update the support ledger before checking it. Existing rows "
            "are preserved, and missing BibTeX keys are seeded with status=todo."
        ),
    )
    parser.add_argument(
        "--merge-from",
        action="append",
        type=Path,
        default=[],
        help=(
            "Existing content-support ledger to use as seed evidence before the "
            "--support file is applied. May be passed more than once."
        ),
    )
    return parser.parse_args()


def load_support_payload(path: Path) -> dict[str, dict[str, str]]:
    if not path.exists():
        return {}
    raw_payload = tomllib.loads(path.read_text(encoding="utf-8"))
    payload: dict[str, dict[str, str]] = {}
    for key, value in raw_payload.items():
        if isinstance(value, dict):
            payload[str(key)] = {
                str(field): str(field_value) for field, field_value in value.items()
            }
    return payload


def toml_string(value: str) -> str:
    return json.dumps(value)


def render_support_payload(entries: list[BibEntry], payload: dict[str, dict[str, str]]) -> str:
    lines = [
        "# Manual content-support ledger for the source_content gate.",
        "# Each row records why the source content supports the way the manuscript uses it.",
        "# The --update mode preserves existing evidence and seeds missing rows as todo.",
        "",
    ]
    for entry in entries:
        row = dict(payload.get(entry.key, {}))
        status = row.pop("status", DEFAULT_STATUS).strip() or DEFAULT_STATUS
        note = row.pop("note", "").strip()
        lines.append(f"[{entry.key}]")
        lines.append(f"status = {toml_string(status)}")
        lines.append(f"note = {toml_string(note)}")
        for field in sorted(row):
            lines.append(f"{field} = {toml_string(row[field])}")
        lines.append("")
    return "\n".join(lines)


def update_support_ledger(
    entries: list[BibEntry],
    support_path: Path,
    merge_from: list[Path],
) -> None:
    payload: dict[str, dict[str, str]] = {}
    for seed_path in merge_from:
        if seed_path.exists():
            payload.update(load_support_payload(seed_path))
    if support_path.exists():
        payload.update(load_support_payload(support_path))
    support_path.parent.mkdir(parents=True, exist_ok=True)
    support_path.write_text(render_support_payload(entries, payload), encoding="utf-8")


def check_content_support(
    bib_paths: list[Path],
    support_path: Path,
    *,
    update: bool = False,
    merge_from: list[Path] | None = None,
) -> tuple[bool, list[str]]:
    entries = parse_all_bib_entries(bib_paths)
    if update:
        update_support_ledger(entries, support_path, merge_from or [])
    if not support_path.exists():
        return False, [f"missing content support ledger: {support_path}"]

    bib_keys = {entry.key for entry in entries}
    payload = load_support_payload(support_path)
    support_keys = set(payload)

    messages: list[str] = []
    missing = sorted(bib_keys - support_keys)
    extra = sorted(support_keys - bib_keys)
    bad_status: list[str] = []
    missing_note: list[str] = []
    for key, value in payload.items():
        if not isinstance(value, dict):
            bad_status.append(key)
            continue
        status = str(value.get("status", "")).strip()
        note = str(value.get("note", "")).strip()
        if status not in PASSING_STATUSES:
            bad_status.append(key)
        if not note:
            missing_note.append(key)

    if missing:
        messages.append("missing_content_keys=" + ", ".join(missing))
    if extra:
        messages.append("extra_content_keys=" + ", ".join(extra))
    if bad_status:
        messages.append("bad_content_status_keys=" + ", ".join(sorted(bad_status)))
    if missing_note:
        messages.append("missing_content_note_keys=" + ", ".join(sorted(missing_note)))

    if messages:
        return False, messages
    return True, [f"content_support_count={len(support_keys)}", "content_support_status=complete"]


def main() -> int:
    args = parse_args()
    try:
        passed, messages = check_content_support(
            args.bib,
            args.support,
            update=args.update,
            merge_from=args.merge_from,
        )
    except Exception as exc:  # noqa: BLE001 - CLI should report audit failure.
        print(f"content support check error: {exc}", file=sys.stderr)
        return 1

    stream = sys.stdout if passed else sys.stderr
    for message in messages:
        print(message, file=stream)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
