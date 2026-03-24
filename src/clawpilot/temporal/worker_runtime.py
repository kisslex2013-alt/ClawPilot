from __future__ import annotations

from dataclasses import asdict, dataclass

from clawpilot.config import AppSettings, load_settings
from clawpilot.temporal.client import build_client_options, maybe_connect_client


@dataclass(frozen=True)
class WorkerOptions:
    namespace: str
    task_queue: str
    workflows: list[str]
    activities: list[str]
    worker_identity: str | None


@dataclass(frozen=True)
class WorkerStartPlan:
    connect: bool
    worker_definition: dict[str, object]
    guardrails: list[str]


def build_task_queue_name(settings: AppSettings | None = None) -> str:
    return (settings or load_settings()).temporal.task_queue


def build_worker_identity(settings: AppSettings | None = None) -> str | None:
    return (settings or load_settings()).temporal.worker_identity


def build_worker_options(settings: AppSettings | None = None) -> WorkerOptions:
    settings = settings or load_settings()
    return WorkerOptions(namespace=settings.temporal.namespace, task_queue=settings.temporal.task_queue, workflows=["clawloop_full_cycle", "smoke_check", "dashboard_refresh"], activities=["run_full_cycle_activity", "run_smoke_activity", "run_dashboard_activity", "run_notify_activity", "run_manifest_activity"], worker_identity=settings.temporal.worker_identity)


def describe_worker_runtime(settings: AppSettings | None = None) -> dict[str, object]:
    options = build_worker_options(settings)
    return {"namespace": options.namespace, "task_queue": options.task_queue, "workflows": options.workflows, "activities": options.activities, "worker_identity": options.worker_identity, "connect_requested": False}


def create_worker_components(*, settings: AppSettings | None = None) -> dict[str, object]:
    return {"options": asdict(build_worker_options(settings)), "runtime": describe_worker_runtime(settings)}


def create_worker_definition(settings: AppSettings | None = None) -> dict[str, object]:
    return {"client": build_client_options(settings).__dict__, "worker": asdict(build_worker_options(settings))}


def build_worker_start_plan(settings: AppSettings | None = None, connect: bool = False) -> WorkerStartPlan:
    return WorkerStartPlan(connect=connect, worker_definition=create_worker_definition(settings), guardrails=["Preview mode is default.", "Connect must be explicit.", "No infinite loop by default."])


def maybe_start_worker_once(settings: AppSettings | None = None, connect: bool = False) -> dict[str, object]:
    plan = build_worker_start_plan(settings, connect=connect)
    if not connect:
        return {"started": False, "plan": asdict(plan)}
    return {"started": False, "plan": asdict(plan), "client": maybe_connect_client(settings, connect=True), "note": "live worker start is intentionally not automatic"}


def maybe_create_worker_runtime(settings: AppSettings | None = None, connect: bool = False) -> dict[str, object]:
    if not connect:
        return {"connect": False, "definition": create_worker_definition(settings), "runtime": describe_worker_runtime(settings)}
    return {"connect": True, "client": maybe_connect_client(settings, connect=True), "definition": create_worker_definition(settings), "runtime": describe_worker_runtime(settings)}
