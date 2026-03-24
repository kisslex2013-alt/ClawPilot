from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from clawpilot.orchestration.contracts import RunStatus


@dataclass(frozen=True)
class WorkflowExecutionRequest:
    workflow_name: str
    task_id: str
    run_id: str
    input_payload: dict[str, Any]
    connect: bool = False


@dataclass(frozen=True)
class WorkflowExecutionResult:
    workflow_name: str
    task_id: str
    run_id: str
    status: RunStatus
    summary: str
    details: dict[str, Any]


@dataclass(frozen=True)
class ConnectivityCheckResult:
    connected: bool
    target: dict[str, Any]
    message: str


@dataclass(frozen=True)
class WorkerStartResult:
    connect: bool
    started: bool
    summary: str
    details: dict[str, Any]


def build_execution_request(*, workflow_name: str, task_id: str, run_id: str, input_payload: dict[str, Any], connect: bool = False) -> WorkflowExecutionRequest:
    return WorkflowExecutionRequest(workflow_name=workflow_name, task_id=task_id, run_id=run_id, input_payload=input_payload, connect=connect)


def summarize_execution_result(*, request: WorkflowExecutionRequest, status: RunStatus, details: dict[str, Any] | None = None) -> WorkflowExecutionResult:
    return WorkflowExecutionResult(workflow_name=request.workflow_name, task_id=request.task_id, run_id=request.run_id, status=status, summary=f"{request.workflow_name} {status.value}", details=details or {})


def summarize_connectivity_result(*, connected: bool, target: dict[str, Any], message: str) -> ConnectivityCheckResult:
    return ConnectivityCheckResult(connected=connected, target=target, message=message)
