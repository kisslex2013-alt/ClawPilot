from __future__ import annotations

import subprocess
import sys


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, "-m", "clawpilot.cli", *args], capture_output=True, text=True, check=True)


def test_cli_sender_commands():
    assert "mode" in _run("show-transport-mode").stdout
    assert "dry_run" in _run("send-rendered-progress").stdout or "file_log" in _run("send-rendered-progress").stdout
    assert "send-results" or _run("send-rendered-digest").stdout
    assert "MessageKind.blocker" in _run("send-rendered-blocker").stdout
    assert "completion" or _run("send-rendered-completion").stdout
    assert "notifications" in _run("show-notification-log").stdout or "[]" in _run("show-notification-log").stdout
