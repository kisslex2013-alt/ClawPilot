from __future__ import annotations

from clawpilot.config import AppSettings, load_settings
from clawpilot.dev.runner import execute_dry_run_workflow
from clawpilot.temporal.client import describe_client_target, maybe_connect_client
from clawpilot.temporal.dev_server import build_dev_server_checklist, build_dev_server_start_hint


def build_dev_run_plan(*, workflow_name: str, task_id: str, run_id: str, connect: bool = False, settings: AppSettings | None = None) -> dict[str, object]:
    settings = settings or load_settings()
    return {"workflow_name": workflow_name, "task_id": task_id, "run_id": run_id, "connect": connect, "client_target": describe_client_target(settings), "server_hints": build_dev_server_start_hint(settings), "checklist": build_dev_server_checklist(settings)}


def run_worker_preview(*, workflow_name: str, task_id: str, run_id: str, settings: AppSettings | None = None) -> dict[str, object]:
    return execute_dry_run_workflow(workflow_name=workflow_name, task_id=task_id, run_id=run_id)


def maybe_run_connectivity_check(*, settings: AppSettings | None = None, connect: bool = False) -> dict[str, object]:
    settings = settings or load_settings()
    if not connect:
        return {"connected": False, "target": describe_client_target(settings)}
    return maybe_connect_client(settings, connect=True)
