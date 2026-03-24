from __future__ import annotations

import subprocess
import sys

from clawpilot.temporal.worker_runtime import describe_worker_runtime


def test_worker_runtime_summary():
    summary = describe_worker_runtime()
    assert summary["connect_requested"] is False


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, "-m", "clawpilot.cli", *args], capture_output=True, text=True, check=True)


def test_cli_temporal_lists():
    assert "clawloop_full_cycle" in _run("list-temporal-workflows").stdout
    assert "run_full_cycle_activity" in _run("list-temporal-activities").stdout


def test_cli_validate_registration():
    assert '"ok": true' in _run("validate-registration").stdout


def test_cli_worker_plan():
    assert "temporal_namespace" in _run("show-worker-plan").stdout
