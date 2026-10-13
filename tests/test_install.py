import json
import subprocess
import sys
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PACKAGE / "scripts"))

import install  # noqa: E402


def test_install_vendors_package_removes_retired_files_and_keeps_local(tmp_path, monkeypatch):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    vendor = tmp_path / "agent-protocols"
    (vendor / "local").mkdir(parents=True)
    (vendor / "local" / "routing.json").write_text("{}")
    (vendor / "substantive-work-protocol.md").write_text("retired")
    monkeypatch.setattr(install, "git", lambda cwd, *args: "" if args[0] == "status" else (
        str(tmp_path) if args[0] == "rev-parse" and "--show-toplevel" in args else "c" * 40))
    install.main(["--target", str(tmp_path)])
    lock = json.loads((tmp_path / "agent-protocols.lock.json").read_text())
    assert lock["version"] == (PACKAGE / "VERSION").read_text().strip()
    assert "work-protocol.md" in lock["files"]
    assert (vendor / "work-protocol.md").is_file()
    assert not (vendor / "substantive-work-protocol.md").exists()
    assert (vendor / "local" / "routing.json").read_text() == "{}"
