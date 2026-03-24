from __future__ import annotations

from dataclasses import dataclass

from clawpilot.config import AppSettings, load_settings


@dataclass(frozen=True)
class WorkerOptions:
    namespace: str
    task_queue: str
    workflows: list[str]
    activities: list[str]


def build_worker_options(settings: AppSettings | None = None) -> WorkerOptions:
    settings = settings or load_settings()
    return WorkerOptions(namespace=settings.temporal.namespace, task_queue=settings.temporal.task_queue, workflows=["clawloop_full_cycle", "smoke_check", "dashboard_refresh"], activities=["run_full_cycle_activity", "run_smoke_activity", "run_dashboard_activity", "run_notify_activity", "run_manifest_activity"])


def describe_worker_runtime(settings: AppSettings | None = None) -> dict[str, object]:
    options = build_worker_options(settings)
    return {"namespace": options.namespace, "task_queue": options.task_queue, "workflows": options.workflows, "activities": options.activities, "connect_requested": False}


def create_worker_components(*, settings: AppSettings | None = None) -> dict[str, object]:
    return {"options": build_worker_options(settings).model_dump(), "runtime": describe_worker_runtime(settings)}


def maybe_create_client(*, connect: bool = False, settings: AppSettings | None = None) -> dict[str, object]:
    options = build_worker_options(settings)
    return {"connect": connect, "namespace": options.namespace, "task_queue": options.task_queue}
