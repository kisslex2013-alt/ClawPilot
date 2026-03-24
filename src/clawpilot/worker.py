from __future__ import annotations

from dataclasses import dataclass

from clawpilot.config import AppSettings, load_settings
from clawpilot.orchestration.registry import get_activity_specs, get_workflow_specs
from clawpilot.temporal.registry import describe_temporal_registration, validate_registration_consistency
from clawpilot.temporal.worker_runtime import build_worker_options, describe_worker_runtime


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


def build_local_worker_contract_summary(settings: AppSettings | None = None) -> dict[str, object]:
    settings = settings or load_settings()
    return {"temporal_namespace": settings.temporal.namespace, "task_queue": settings.temporal.task_queue, "workflows": describe_registered_workflows(), "activities": describe_registered_activities()}


def build_temporal_registration_summary() -> dict[str, object]:
    return validate_registration_consistency()


def build_worker_bootstrap_plan(settings: AppSettings | None = None) -> dict[str, object]:
    settings = settings or load_settings()
    return {"options": build_worker_options(settings).model_dump(), "runtime": describe_worker_runtime(settings)}


def maybe_build_local_worker_preview(settings: AppSettings | None = None) -> dict[str, object]:
    return {"topology": describe_worker_topology().__dict__, "registration": describe_temporal_registration(), "bootstrap": build_worker_bootstrap_plan(settings)}
