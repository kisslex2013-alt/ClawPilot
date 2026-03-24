from __future__ import annotations

import subprocess
import sys


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, "-m", "clawpilot.cli", *args], capture_output=True, text=True, check=True)


def test_cli_telegram_direct_commands():
    assert "chat_id" in _run("show-telegram-target").stdout
    assert "preview" in _run("send-telegram-progress").stdout
    assert "live" in _run("send-telegram-progress", "--live").stdout
    assert "preview" in _run("send-telegram-blocker").stdout
