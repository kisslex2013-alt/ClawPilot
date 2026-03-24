from __future__ import annotations

from dataclasses import dataclass

from clawpilot.config import AppSettings, load_settings
from clawpilot.notifier.senders import SenderMode


@dataclass(frozen=True)
class NotificationTransportSpec:
    mode: SenderMode
    enabled: bool
    target: str
    note: str | None = None


def build_transport_spec(settings: AppSettings | None = None) -> NotificationTransportSpec:
    settings = settings or load_settings()
    mode = SenderMode(settings.notification_transport_mode)
    if mode == SenderMode.file_log:
        return NotificationTransportSpec(mode=mode, enabled=True, target=settings.notification_log_dir, note="local file log transport")
    if mode == SenderMode.telegram_direct:
        return NotificationTransportSpec(mode=mode, enabled=settings.telegram_live_send_enabled, target=settings.telegram_chat_id or "<missing-chat-id>", note="direct Telegram transport; explicit live-send required")
    if mode == SenderMode.disabled:
        return NotificationTransportSpec(mode=mode, enabled=False, target="none", note="notifications disabled")
    return NotificationTransportSpec(mode=SenderMode.dry_run, enabled=False, target="local-preview", note="dry-run transport")


def describe_transport_mode(settings: AppSettings | None = None) -> dict[str, object]:
    spec = build_transport_spec(settings)
    return {"mode": spec.mode.value, "enabled": spec.enabled, "target": spec.target, "note": spec.note}


def resolve_default_transport(settings: AppSettings | None = None) -> NotificationTransportSpec:
    settings = settings or load_settings()
    if settings.telegram_transport_enabled:
        return NotificationTransportSpec(mode=SenderMode.file_log, enabled=True, target=settings.notification_log_dir, note="telegram transport not live by default; file log preferred")
    return build_transport_spec(settings)


def is_live_transport_mode(mode: SenderMode) -> bool:
    return mode == SenderMode.telegram_direct


def describe_transport_target(settings: AppSettings | None = None) -> str:
    spec = build_transport_spec(settings)
    return f"{spec.mode.value}:{spec.target}"
