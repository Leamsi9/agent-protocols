#!/usr/bin/env python3
"""Vendor this package into a repository as agent-protocols/ and write its lock.

Run from the repository that uses the package. Files the package no longer
ships are removed; the repository-owned agent-protocols/local/ is left alone.
"""

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent.parent
SOURCE = "https://github.com/Leamsi9/agent-protocols"
SHIPPED = [
    "README.md",
    "VERSION",
    "LICENSE-MIT",
    "LICENSE-APACHE",
    "work-protocol.md",
    "citation-verification-protocol.md",
    "scripts",
    "skills",
]
LOCAL = "local"


def git(cwd, *args):
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def shipped_files():
    for name in SHIPPED:
        path = PACKAGE / name
        if path.is_file():
            yield Path(name)
        for child in sorted(path.rglob("*")) if path.is_dir() else ():
            if child.is_file() and "__pycache__" not in child.parts and child.suffix != ".pyc":
                yield child.relative_to(PACKAGE)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, help="repository root (default: current Git root)")
    args = parser.parse_args(argv)
    target = (args.target or Path(git(Path.cwd(), "rev-parse", "--show-toplevel"))).resolve()
    vendor = target / "agent-protocols"
    if vendor.resolve() == PACKAGE:
        sys.exit("Run the installer from the repository that uses the package")
    if git(PACKAGE, "status", "--porcelain"):
        sys.exit("Commit the package changes first; the lock records a commit")

    wanted = list(shipped_files())
    keep = {str(path) for path in wanted}
    if vendor.exists():
        for path in sorted(vendor.rglob("*"), reverse=True):
            relative = path.relative_to(vendor)
            if relative.parts[0] == LOCAL:
                continue
            if path.is_file() and str(relative) not in keep:
                path.unlink()
            elif path.is_dir() and not any(path.iterdir()):
                path.rmdir()
    hashes = {}
    for relative in wanted:
        destination = vendor / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(PACKAGE / relative, destination)
        hashes[str(relative)] = hashlib.sha256(destination.read_bytes()).hexdigest()
    lock = {
        "version": (PACKAGE / "VERSION").read_text().strip(),
        "source": SOURCE,
        "commit": git(PACKAGE, "rev-parse", "HEAD"),
        "files": hashes,
    }
    (target / "agent-protocols.lock.json").write_text(json.dumps(lock, indent=2) + "\n")
    print(f"agent-protocols {lock['version']} ({lock['commit'][:8]}): {len(hashes)} files")


if __name__ == "__main__":
    main()
