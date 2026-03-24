from __future__ import annotations

from dataclasses import dataclass

from clawpilot.config import AppSettings, load_settings
from clawpilot.execution.guardrails import build_local_execution_guardrails
from clawpilot.notifier.transport import build_transport_spec, describe_transport_mode
from clawpilot.orchestration.registry import get_activity_specs, get_workflow_specs
from clawpilot.temporal.client import describe_client_target
from clawpilot.temporal.registry import describe_temporal_registration, validate_registration_consistency
from clawpilot.temporal.worker_runtime import build_task_queue_name, build_worker_identity, build_worker_options, describe_worker_runtime, maybe_create_worker_runtime


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
    return {"options": build_worker_options(settings).__dict__, "runtime": describe_worker_runtime(settings)}


def maybe_build_local_worker_preview(settings: AppSettings | None = None) -> dict[str, object]:
    settings = settings or load_settings()
    return {"temporal_namespace": settings.temporal.namespace, "topology": describe_worker_topology().__dict__, "registration": describe_temporal_registration(), "bootstrap": build_worker_bootstrap_plan(settings)}


def build_local_dev_bootstrap_summary(settings: AppSettings | None = None) -> dict[str, object]:
    settings = settings or load_settings()
    return {"client_target": describe_client_target(settings), "task_queue": build_task_queue_name(settings), "worker_identity": build_worker_identity(settings), "registration": describe_temporal_registration()}


def build_connectivity_guardrails() -> list[str]:
    return ["Preview mode is default.", "Connect mode is explicit.", "No worker loop runs by default.", "No live Temporal connection happens on import."]


def describe_safe_dev_modes() -> dict[str, object]:
    return {"preview": "local summaries only", "connect": "explicit and optional", "live": "future only"}


def build_local_execution_matrix() -> dict[str, object]:
    return {"smoke_check": "local_execute", "dashboard_refresh": "preview_only", "clawloop_full_cycle": "preview_only"}


def describe_v1_local_execute_policy() -> dict[str, object]:
    return {"allowed": ["smoke_check"], "blocked": ["dashboard_refresh", "clawloop_full_cycle"], "guardrails": build_local_execution_guardrails()}


def explain_why_full_cycle_is_not_default_execute() -> str:
    return "full_cycle remains guarded because it fans out into more artifacts and is not the first bounded local execution path."


def describe_notification_transport_modes() -> list[str]:
    return ["dry_run", "file_log", "disabled", "telegram_direct"]


def build_notification_transport_summary(settings: AppSettings | None = None) -> dict[str, object]:
    settings = settings or load_settings()
    return {"transport": describe_transport_mode(settings), "modes": describe_notification_transport_modes(), "spec": build_transport_spec(settings).__dict__}


def describe_live_transport_guardrails() -> list[str]:
    return ["telegram_direct requires explicit --live.", "No live send by default.", "No secret leakage in summaries.", "No routing integration yet."]


def build_telegram_transport_summary(settings: AppSettings | None = None) -> dict[str, object]:
    settings = settings or load_settings()
    return {"target": describe_client_target(settings), "guardrails": describe_live_transport_guardrails(), "enabled": settings.telegram_live_send_enabled}
