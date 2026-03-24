from __future__ import annotations

from dataclasses import dataclass

from clawpilot.config import AppSettings, load_settings
from clawpilot.orchestration.registry import get_activity_specs, get_workflow_specs


@dataclass(frozen=True)
class WorkerTopology:
    orchestration_worker: str
    notifier_worker: str
    dashboard_sync_worker: str


def describe_worker_topology() -> WorkerTopology:
    return WorkerTopology(orchestration_worker="workflow execution and orchestration", notifier_worker="telegram/digest notifications", dashboard_sync_worker="dashboard snapshot refresh")


def describe_registered_workflows() -> list[str]:
    return [spec.name for spec in get_workflow_specs()]


def describe_registered_activities() -> list[str]:
    return [spec.name for spec in get_activity_specs()]


def build_local_worker_contract_summary(settings: AppSettings | None = None) -> dict[str, str | list[str]]:
    settings = settings or load_settings()
    return {"temporal_namespace": settings.temporal.namespace, "task_queue": settings.temporal.task_queue, "workflows": describe_registered_workflows(), "activities": describe_registered_activities()}
