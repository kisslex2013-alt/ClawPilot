from __future__ import annotations

from clawpilot.execution.contracts import ExecutionMode
from clawpilot.dev.runner import execute_local_workflow


def test_local_execute_blocked():
    result = execute_local_workflow(workflow_name="clawloop_full_cycle", task_id="t", run_id="r", mode=ExecutionMode.local_execute, execute=True)
    assert result["local_execution"]["allowed"] is False


def test_local_execute_preview():
    result = execute_local_workflow(workflow_name="smoke_check", task_id="t", run_id="r", mode=ExecutionMode.preview, execute=False)
    assert result["local_execution"]["allowed"] is False
