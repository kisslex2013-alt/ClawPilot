from __future__ import annotations

import subprocess
import sys


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, "-m", "clawpilot.cli", *args], capture_output=True, text=True, check=True)


def test_cli_temporal_dev_commands():
    assert "clawpilot-main" in _run("show-task-queue").stdout
    assert "namespace" in _run("temporal-client-target").stdout
    assert "task_queue" in _run("show-worker-definition").stdout
    assert "smoke_check" in _run("preview-worker").stdout
    assert "workflow_name" in _run("preview-run-plan").stdout
    assert "requirements" in _run("show-dev-server-hints").stdout
