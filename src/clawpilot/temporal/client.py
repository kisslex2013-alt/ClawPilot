from __future__ import annotations

from dataclasses import dataclass

from clawpilot.config import AppSettings, load_settings
from clawpilot.temporal.execution import ConnectivityCheckResult, WorkflowExecutionRequest, WorkflowExecutionResult, build_execution_request, summarize_connectivity_result, summarize_execution_result
from clawpilot.orchestration.contracts import RunStatus


@dataclass(frozen=True)
class ClientOptions:
    address: str
    namespace: str
    task_queue: str
    enable_tls: bool
    connect_timeout_seconds: float
    worker_identity: str | None


def build_client_options(settings: AppSettings | None = None) -> ClientOptions:
    settings = settings or load_settings()
    return ClientOptions(address=settings.temporal.address, namespace=settings.temporal.namespace, task_queue=settings.temporal.task_queue, enable_tls=settings.temporal.enable_tls, connect_timeout_seconds=settings.temporal.connect_timeout_seconds, worker_identity=settings.temporal.worker_identity)


def describe_client_target(settings: AppSettings | None = None) -> dict[str, object]:
    options = build_client_options(settings)
    return {"address": options.address, "namespace": options.namespace, "task_queue": options.task_queue, "enable_tls": options.enable_tls, "connect_timeout_seconds": options.connect_timeout_seconds, "worker_identity": options.worker_identity, "connect_requested": False}


def check_temporal_connectivity(settings: AppSettings | None = None, connect: bool = False) -> ConnectivityCheckResult:
    target = describe_client_target(settings)
    if not connect:
        return summarize_connectivity_result(connected=False, target=target, message="preview only; connect not requested")
    try:
        from temporalio.client import Client
    except Exception as exc:  # pragma: no cover
        return summarize_connectivity_result(connected=False, target=target, message=f"temporalio unavailable: {exc}")
    return summarize_connectivity_result(connected=False, target={**target, "client_class": getattr(Client, '__name__', 'Client')}, message="live connect path not enabled in this build")


def maybe_connect_client(settings: AppSettings | None = None, connect: bool = False) -> dict[str, object]:
    result = check_temporal_connectivity(settings, connect=connect)
    return {"connected": result.connected, "target": result.target, "message": result.message}


def maybe_start_workflow(settings: AppSettings | None = None, workflow_name: str = "smoke_check", task_id: str = "sample-task", run_id: str = "sample-run", connect: bool = False) -> WorkflowExecutionResult:
    settings = settings or load_settings()
    request = build_execution_request(workflow_name=workflow_name, task_id=task_id, run_id=run_id, input_payload={"workflow_name": workflow_name, "task_id": task_id, "run_id": run_id}, connect=connect)
    if not connect:
        return summarize_execution_result(request=request, status=RunStatus.planned, details={"mode": "preview"})
    return summarize_execution_result(request=request, status=RunStatus.planned, details={"mode": "connect-explicit", "target": describe_client_target(settings)})
