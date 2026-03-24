from __future__ import annotations

import subprocess
import sys


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, "-m", "clawpilot.cli", *args], capture_output=True, text=True, check=True)


def test_cli_notifier_commands():
    assert "live_progress" in _run("render-progress-feed").stdout
    assert "digest" in _run("render-digest").stdout
    assert "BLOCKED" in _run("render-blocker").stdout
    assert "DONE" in _run("render-completion").stdout
