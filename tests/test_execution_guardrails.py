from __future__ import annotations

from pathlib import Path

from clawpilot.execution.contracts import ExecutionMode, LocalExecutionRequest
from clawpilot.execution.guardrails import can_execute_workflow_locally, validate_local_execution_request


def test_guardrails():
    assert can_execute_workflow_locally("smoke_check") is True
    assert can_execute_workflow_locally("clawloop_full_cycle") is False
    req = LocalExecutionRequest(workflow_name="clawloop_full_cycle", mode=ExecutionMode.local_execute, cwd=Path("/root/clawpilot"), command_summary=["x"], explicit_opt_in=True)
    result = validate_local_execution_request(req)
    assert result.allowed is False
