from __future__ import annotations

from clawpilot.notifier.models import MessageKind, NotificationEnvelope
from clawpilot.notifier.openclaw_routing import describe_openclaw_routing_target, maybe_send_via_openclaw_routing, preview_openclaw_route


def test_openclaw_routing_is_preview_only():
    env = NotificationEnvelope(kind=MessageKind.live_progress, title="t", body="b")
    assert preview_openclaw_route(env)["preview_only"] is True
    assert maybe_send_via_openclaw_routing(env, preview_mode=False)["preview_only"] is True
    assert "workspace_path" in describe_openclaw_routing_target()
