from __future__ import annotations

from clawpilot.temporal.client import build_client_options, describe_client_target, maybe_connect_client


def test_client_options():
    target = describe_client_target()
    assert target["namespace"] == "clawpilot"
    assert build_client_options().task_queue == "clawpilot-main"


def test_no_connect_path():
    result = maybe_connect_client(connect=False)
    assert result["connected"] is False
