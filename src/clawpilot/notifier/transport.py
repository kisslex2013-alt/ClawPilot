from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from clawpilot.config import AppSettings, load_settings


class SenderMode(str, Enum):
    dry_run = "dry_run"
    file_log = "file_log"
    disabled = "disabled"
    telegram_direct = "telegram_direct"
    openclaw_routing_stub = "openclaw_routing_stub"


@dataclass(frozen=True)
class NotificationTransportSpec:
    mode: SenderMode
    enabled: bool
    target: str
    note: str | None = None


def build_transport_spec(settings: AppSettings | None = None) -> NotificationTransportSpec:
    settings = settings or load_settings()
    mode = SenderMode(settings.notification_transport_mode or "dry_run")
    if mode == SenderMode.file_log:
        return NotificationTransportSpec(mode=mode, enabled=True, target=settings.notification_log_dir, note="local only")
    if mode == SenderMode.telegram_direct:
        return NotificationTransportSpec(mode=mode, enabled=settings.telegram_live_send_enabled, target=settings.telegram_chat_id or "<missing-chat-id>", note="live capable with explicit opt-in")
    if mode == SenderMode.disabled:
        return NotificationTransportSpec(mode=mode, enabled=False, target="none", note="local only")
    if mode == SenderMode.openclaw_routing_stub:
        return NotificationTransportSpec(mode=mode, enabled=False, target=settings.openclaw_channel_name or "default", note="preview only")
    return NotificationTransportSpec(mode=SenderMode.dry_run, enabled=False, target="local-preview", note="preview only")


def describe_transport_mode(settings: AppSettings | None = None) -> dict[str, object]:
    spec = build_transport_spec(settings)
    return {"mode": spec.mode.value, "enabled": spec.enabled, "target": spec.target, "note": spec.note}


def resolve_default_transport(settings: AppSettings | None = None) -> NotificationTransportSpec:
    settings = settings or load_settings()
    if settings.notification_route_mode:
        return build_transport_spec(settings)
    if settings.telegram_transport_enabled:
        return NotificationTransportSpec(mode=SenderMode.file_log, enabled=True, target=settings.notification_log_dir, note="local only")
    return build_transport_spec(settings)


def is_live_transport_mode(mode: SenderMode) -> bool:
    return mode == SenderMode.telegram_direct


def is_preview_only_transport(mode: SenderMode) -> bool:
    return mode in {SenderMode.dry_run, SenderMode.file_log, SenderMode.disabled, SenderMode.openclaw_routing_stub}


def is_live_capable_transport(mode: SenderMode) -> bool:
    return mode == SenderMode.telegram_direct


def describe_transport_target(settings: AppSettings | None = None) -> str:
    spec = build_transport_spec(settings)
    return f"{spec.mode.value}:{spec.target}:{spec.note or 'n/a'}"
