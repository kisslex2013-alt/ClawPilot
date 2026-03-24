from __future__ import annotations

import subprocess
import sys

from clawpilot.dev.runner import execute_dry_run_workflow


def test_execute_dry_run_workflow():
    result = execute_dry_run_workflow(workflow_name="smoke_check", task_id="task", run_id="run")
    assert result["summary"]["status"] == "succeeded"
    assert result["session"]["run_id"] == "run"


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, "-m", "clawpilot.cli", *args], capture_output=True, text=True, check=True)


def test_cli_list_workflows():
    assert "smoke_check" in _run("list-workflows").stdout


def test_cli_list_activities():
    assert "run_smoke" in _run("list-activities").stdout


def test_cli_dry_run_workflow_smoke_check():
    out = _run("dry-run-workflow", "smoke-check").stdout
    assert '"workflow_name": "smoke_check"' in out


def test_cli_detect_artifacts():
    out = _run("detect-artifacts").stdout
    assert "reference/agent-eval" in out
