#!/usr/bin/env python3
"""Check that a citation content-support ledger covers every BibTeX key."""

from __future__ import annotations

import argparse
import sys
import tomllib
from pathlib import Path

from citation_inventory import parse_all_bib_entries


PASSING_STATUSES = {"verified", "not_applicable"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bib", action="append", type=Path, required=True)
    parser.add_argument("--support", type=Path, required=True)
    return parser.parse_args()


def check_content_support(bib_paths: list[Path], support_path: Path) -> tuple[bool, list[str]]:
    if not support_path.exists():
        return False, [f"missing content support ledger: {support_path}"]

    bib_keys = {entry.key for entry in parse_all_bib_entries(bib_paths)}
    payload = tomllib.loads(support_path.read_text(encoding="utf-8"))
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
        passed, messages = check_content_support(args.bib, args.support)
    except Exception as exc:  # noqa: BLE001 - CLI should report audit failure.
        print(f"content support check error: {exc}", file=sys.stderr)
        return 1

    stream = sys.stdout if passed else sys.stderr
    for message in messages:
        print(message, file=stream)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
