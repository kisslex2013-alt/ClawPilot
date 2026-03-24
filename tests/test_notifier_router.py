from __future__ import annotations

from clawpilot.notifier.router import build_notification_route_plan, choose_sender_mode, resolve_notification_route
from clawpilot.notifier.transport import SenderMode


def test_route_resolution_default():
    assert resolve_notification_route().selected.mode in {SenderMode.dry_run, SenderMode.file_log, SenderMode.disabled, SenderMode.telegram_direct, SenderMode.openclaw_routing_stub}


def test_explicit_override_wins():
    assert choose_sender_mode(override="file_log") == SenderMode.file_log


def test_route_plan_contains_selection():
    plan = build_notification_route_plan()
    assert "selected" in plan
