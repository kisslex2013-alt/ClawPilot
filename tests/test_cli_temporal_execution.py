from __future__ import annotations

import subprocess
import sys


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, "-m", "clawpilot.cli", *args], capture_output=True, text=True, check=True)


def test_cli_temporal_execution_commands():
    assert "workflow_name" in _run("temporal-smoke-plan").stdout
    assert "connected" in _run("temporal-connectivity-smoke").stdout
    assert "connect" in _run("temporal-worker-start-plan").stdout
    assert "smoke_check" in _run("temporal-start-workflow", "smoke-check").stdout
