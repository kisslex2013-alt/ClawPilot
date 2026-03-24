from __future__ import annotations

import subprocess
import sys


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, "-m", "clawpilot.cli", *args], capture_output=True, text=True, check=True)


def test_cli_local_execute_commands():
    smoke = _run("local-exec", "smoke-check").stdout
    assert "mode" in smoke
    assert "preview" in smoke
    assert "blocked" in _run("local-exec", "full-cycle").stdout
    assert "run_summary" in _run("show-latest-run-summary").stdout or "NOT AVAILABLE" in _run("show-latest-run-summary").stdout
