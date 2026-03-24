from __future__ import annotations

from clawpilot.orchestration.contracts import RunStatus
from clawpilot.temporal.client import check_temporal_connectivity, maybe_start_workflow
from clawpilot.temporal.execution import build_execution_request, summarize_execution_result


def test_preview_only_connectivity():
    result = check_temporal_connectivity(connect=False)
    assert result.connected is False


def test_preview_only_workflow_start():
    result = maybe_start_workflow(workflow_name="smoke_check", connect=False)
    assert result.status == RunStatus.planned


def test_execution_request_summary():
    request = build_execution_request(workflow_name="smoke_check", task_id="t", run_id="r", input_payload={"x": 1})
    result = summarize_execution_result(request=request, status=RunStatus.planned)
    assert result.workflow_name == "smoke_check"
