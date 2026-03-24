from __future__ import annotations

from clawpilot.config import AppSettings, load_settings
from clawpilot.temporal.client import describe_client_target
from clawpilot.temporal.execution import summarize_execution_result
from clawpilot.temporal.sample_workflows import get_sample_workflow_name
from clawpilot.temporal.worker_runtime import build_worker_start_plan, create_worker_definition
from clawpilot.temporal.client import maybe_start_workflow, check_temporal_connectivity


def build_local_smoke_plan(*, workflow_name: str, task_id: str, run_id: str, connect: bool = False, settings: AppSettings | None = None) -> dict[str, object]:
    settings = settings or load_settings()
    return {"client_target": describe_client_target(settings), "worker_definition": create_worker_definition(settings), "worker_start_plan": build_worker_start_plan(settings, connect=connect).__dict__, "execution_request": {"workflow_name": workflow_name, "task_id": task_id, "run_id": run_id, "connect": connect}, "connect": connect}


def run_local_connectivity_smoke(*, workflow_name: str, task_id: str, run_id: str, connect: bool = False, settings: AppSettings | None = None) -> dict[str, object]:
    settings = settings or load_settings()
    connectivity = check_temporal_connectivity(settings, connect=connect)
    execution = maybe_start_workflow(settings, workflow_name=workflow_name, task_id=task_id, run_id=run_id, connect=connect)
    return {"connectivity": connectivity.__dict__, "execution": execution.__dict__}


def summarize_local_smoke(plan: dict[str, object]) -> dict[str, object]:
    return {"workflow_name": plan["execution_request"]["workflow_name"], "connect": plan["connect"], "queue": plan["client_target"]["task_queue"]}
