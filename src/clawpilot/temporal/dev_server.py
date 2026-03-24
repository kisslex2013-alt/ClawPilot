from __future__ import annotations

from clawpilot.config import AppSettings, load_settings


def describe_local_temporal_dev_requirements(settings: AppSettings | None = None) -> dict[str, object]:
    settings = settings or load_settings()
    return {"address": settings.temporal.address, "namespace": settings.temporal.namespace, "task_queue": settings.temporal.task_queue, "dev_connect_enabled": settings.temporal.dev_connect_enabled, "notes": ["Temporal server must already exist if connect mode is used.", "Unit tests do not require a live server."]}


def build_dev_server_start_hint(settings: AppSettings | None = None) -> dict[str, object]:
    requirements = describe_local_temporal_dev_requirements(settings)
    return {"hint": "Start Temporal locally using your preferred dev setup outside this repo.", "requirements": requirements}


def build_dev_server_checklist(settings: AppSettings | None = None) -> list[str]:
    req = describe_local_temporal_dev_requirements(settings)
    return [f"Confirm server at {req['address']}", f"Confirm namespace {req['namespace']}", f"Confirm task queue {req['task_queue']}", "Use preview mode first", "Use --connect only when the server is actually available"]
