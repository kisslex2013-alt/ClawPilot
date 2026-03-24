from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from clawpilot.notifier.models import NotificationEnvelope, RenderedMessage
from clawpilot.notifier.persistence import build_notification_log_path, persist_rendered_message, persist_send_result


class SenderMode(str, Enum):
    dry_run = "dry_run"
    file_log = "file_log"
    disabled = "disabled"


@dataclass(frozen=True)
class SendResult:
    mode: SenderMode
    sent: bool
    transport: str
    target: str
    message_kind: str
    path: str | None = None
    note: str | None = None


@dataclass(frozen=True)
class SendBatchResult:
    mode: SenderMode
    sent: int
    skipped: int
    results: list[SendResult]


def send_to_dry_run_sink(message: RenderedMessage | NotificationEnvelope, *, target: str = "local-preview") -> SendResult:
    kind = getattr(message, "kind", "unknown")
    return SendResult(mode=SenderMode.dry_run, sent=False, transport="dry_run", target=target, message_kind=str(kind), note="dry-run sink; no network")


def send_to_file_log(message: RenderedMessage | NotificationEnvelope, *, base_dir: str = ".") -> SendResult:
    path = persist_rendered_message(base_dir=base_dir, message=message)
    return SendResult(mode=SenderMode.file_log, sent=False, transport="file_log", target=str(build_notification_log_path(base_dir)), message_kind=str(getattr(message, "kind", "unknown")), path=path, note="persisted to local notification log")


def send_rendered_message(message: RenderedMessage | NotificationEnvelope, *, mode: SenderMode = SenderMode.dry_run, base_dir: str = ".") -> SendResult:
    if mode == SenderMode.dry_run:
        result = send_to_dry_run_sink(message)
    elif mode == SenderMode.file_log:
        result = send_to_file_log(message, base_dir=base_dir)
    else:
        result = SendResult(mode=SenderMode.disabled, sent=False, transport="disabled", target="none", message_kind=str(getattr(message, "kind", "unknown")), note="explicitly disabled")
    persist_send_result(base_dir=base_dir, result=result)
    return result


def send_rendered_messages(messages: list[RenderedMessage | NotificationEnvelope], *, mode: SenderMode = SenderMode.dry_run, base_dir: str = ".") -> SendBatchResult:
    results = [send_rendered_message(message, mode=mode, base_dir=base_dir) for message in messages]
    return SendBatchResult(mode=mode, sent=sum(1 for r in results if r.sent), skipped=sum(1 for r in results if not r.sent), results=results)
