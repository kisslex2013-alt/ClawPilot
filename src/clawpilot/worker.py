from __future__ import annotations

from dataclasses import dataclass

from clawpilot.config import AppSettings, load_settings


@dataclass(frozen=True)
class WorkerTopology:
    orchestration_worker: str
    notifier_worker: str
    dashboard_sync_worker: str


def describe_worker_topology() -> WorkerTopology:
    """Placeholder for the future Temporal worker topology.

    The real worker will register workflow and activity implementations,
    connect to Temporal, and split orchestration/notifier/dashboard sync roles.
    """
    return WorkerTopology(
        orchestration_worker="workflow execution and orchestration",
        notifier_worker="telegram/digest notifications",
        dashboard_sync_worker="dashboard snapshot refresh",
    )


def build_worker_config_summary(settings: AppSettings | None = None) -> dict[str, str]:
    settings = settings or load_settings()
    return {
        "temporal_namespace": settings.temporal.namespace,
        "task_queue": settings.temporal.task_queue,
        "workspace": str(settings.openclaw.workspace),
        "clawloop_repo_path": str(settings.clawloop.repo_path),
    }
