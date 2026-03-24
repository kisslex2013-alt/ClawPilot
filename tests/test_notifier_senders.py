from __future__ import annotations

from clawpilot.notifier.models import MessageKind, NotificationEnvelope
from clawpilot.notifier.senders import SenderMode, send_rendered_message, send_rendered_messages


def _msg() -> NotificationEnvelope:
    return NotificationEnvelope(kind=MessageKind.live_progress, title="t", body="b")


def test_dry_run_sender():
    result = send_rendered_message(_msg(), mode=SenderMode.dry_run)
    assert result.sent is False


def test_file_log_sender(tmp_path):
    result = send_rendered_message(_msg(), mode=SenderMode.file_log, base_dir=str(tmp_path))
    assert result.path


def test_disabled_sender():
    result = send_rendered_messages([_msg()], mode=SenderMode.disabled)
    assert result.skipped == 1
