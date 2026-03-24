from __future__ import annotations

from dataclasses import dataclass

from clawpilot.notifier.models import NotificationEnvelope, RenderedMessage
from clawpilot.notifier.openclaw_routing import preview_openclaw_route
from clawpilot.notifier.persistence import build_notification_log_path, persist_rendered_message, persist_send_result
from clawpilot.notifier.telegram_direct import build_telegram_target, send_telegram_message
from clawpilot.notifier.transport import SenderMode


@dataclass(frozen=True)
class SendResult:
    mode: SenderMode
    sent: bool
    attempted: bool
    delivered: bool
    transport_mode: str
    target_summary: str
    message_kind: str
    path: str | None = None
    error: str | None = None
    note: str | None = None


@dataclass(frozen=True)
class SendBatchResult:
    mode: SenderMode
    sent: int
    skipped: int
    results: list[SendResult]


def send_to_dry_run_sink(message: RenderedMessage | NotificationEnvelope, *, target: str = "local-preview") -> SendResult:
    kind = getattr(message, "kind", "unknown")
    return SendResult(mode=SenderMode.dry_run, sent=False, attempted=False, delivered=False, transport_mode="dry_run", target_summary=target, message_kind=str(kind), note="dry-run sink; no network")


def send_to_file_log(message: RenderedMessage | NotificationEnvelope, *, base_dir: str = ".") -> SendResult:
    path = persist_rendered_message(base_dir=base_dir, message=message)
    return SendResult(mode=SenderMode.file_log, sent=False, attempted=False, delivered=False, transport_mode="file_log", target_summary=str(build_notification_log_path(base_dir)), message_kind=str(getattr(message, "kind", "unknown")), path=path, note="persisted to local notification log")


def send_to_telegram_direct(message: RenderedMessage | NotificationEnvelope, *, base_dir: str = ".") -> SendResult:
    target = build_telegram_target()
    payload = message.model_dump() if hasattr(message, "model_dump") else dict(message)
    outcome = send_telegram_message(target=target, text=payload.get("text") or payload.get("body") or str(payload))
    return SendResult(mode=SenderMode.telegram_direct, sent=bool(outcome.get("delivered")), attempted=bool(outcome.get("attempted")), delivered=bool(outcome.get("delivered")), transport_mode="telegram_direct", target_summary=str(outcome.get("target_summary")), message_kind=str(getattr(message, "kind", "unknown")), error=outcome.get("error"), note="explicit live send" if outcome.get("delivered") else "live send failed or not delivered")


def send_to_openclaw_routing_stub(message: RenderedMessage | NotificationEnvelope, *, base_dir: str = ".") -> SendResult:
    preview = preview_openclaw_route(message)
    return SendResult(mode=SenderMode.openclaw_routing_stub, sent=False, attempted=False, delivered=False, transport_mode="openclaw_routing_stub", target_summary=str(preview["target"]), message_kind=str(getattr(message, "kind", "unknown")), note="preview/stub only")


def send_rendered_message(message: RenderedMessage | NotificationEnvelope, *, mode: SenderMode = SenderMode.dry_run, base_dir: str = ".") -> SendResult:
    if mode == SenderMode.dry_run:
        result = send_to_dry_run_sink(message)
    elif mode == SenderMode.file_log:
        result = send_to_file_log(message, base_dir=base_dir)
    elif mode == SenderMode.telegram_direct:
        result = send_to_telegram_direct(message, base_dir=base_dir)
    elif mode == SenderMode.openclaw_routing_stub:
        result = send_to_openclaw_routing_stub(message, base_dir=base_dir)
    else:
        result = SendResult(mode=SenderMode.disabled, sent=False, attempted=False, delivered=False, transport_mode="disabled", target_summary="none", message_kind=str(getattr(message, "kind", "unknown")), note="explicitly disabled")
    persist_send_result(base_dir=base_dir, result=result)
    return result


def send_rendered_messages(messages: list[RenderedMessage | NotificationEnvelope], *, mode: SenderMode = SenderMode.dry_run, base_dir: str = ".") -> SendBatchResult:
    results = [send_rendered_message(message, mode=mode, base_dir=base_dir) for message in messages]
    return SendBatchResult(mode=mode, sent=sum(1 for r in results if r.sent), skipped=sum(1 for r in results if not r.sent), results=results)
