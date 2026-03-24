from __future__ import annotations

from dataclasses import dataclass

from clawpilot.config import AppSettings, load_settings


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
    return ClientOptions(
        address=settings.temporal.address,
        namespace=settings.temporal.namespace,
        task_queue=settings.temporal.task_queue,
        enable_tls=settings.temporal.enable_tls,
        connect_timeout_seconds=settings.temporal.connect_timeout_seconds,
        worker_identity=settings.temporal.worker_identity,
    )


def describe_client_target(settings: AppSettings | None = None) -> dict[str, object]:
    options = build_client_options(settings)
    return {
        "address": options.address,
        "namespace": options.namespace,
        "task_queue": options.task_queue,
        "enable_tls": options.enable_tls,
        "connect_timeout_seconds": options.connect_timeout_seconds,
        "worker_identity": options.worker_identity,
        "connect_requested": False,
    }


def maybe_connect_client(settings: AppSettings | None = None, connect: bool = False) -> dict[str, object]:
    options = build_client_options(settings)
    if not connect:
        return {"connected": False, "target": describe_client_target(settings)}
    try:
        from temporalio.client import Client
    except Exception as exc:  # pragma: no cover
        return {"connected": False, "error": f"temporalio unavailable: {exc}", "target": describe_client_target(settings)}
    return {"connected": False, "error": "live connect not enabled in this build", "target": describe_client_target(settings), "client_class": getattr(Client, '__name__', 'Client')}
