from __future__ import annotations

from clawpilot.config import load_settings
from clawpilot.notifier.telegram_direct import build_telegram_target, describe_telegram_target
from clawpilot.notifier.transport import build_transport_spec, is_live_transport_mode
from clawpilot.notifier.senders import SenderMode, send_to_telegram_direct
from clawpilot.notifier.models import MessageKind, NotificationEnvelope


def test_target_description():
    assert "chat_id" in describe_telegram_target()
    assert build_telegram_target().api_base


def test_transport_resolution():
    assert is_live_transport_mode(SenderMode.telegram_direct) is True
    assert build_transport_spec(load_settings()).mode in {SenderMode.dry_run, SenderMode.file_log, SenderMode.disabled, SenderMode.telegram_direct}


def test_direct_sender_monkeypatch(monkeypatch):
    monkeypatch.setattr("clawpilot.notifier.telegram_direct.send_telegram_message", lambda **kwargs: {"attempted": True, "delivered": True, "target_summary": "x"})
    result = send_to_telegram_direct(NotificationEnvelope(kind=MessageKind.live_progress, title="t", body="b"))
    assert result.attempted is True
