from __future__ import annotations

from clawpilot.temporal.dev_server import build_dev_server_checklist, build_dev_server_start_hint, describe_local_temporal_dev_requirements


def test_dev_server_hints():
    req = describe_local_temporal_dev_requirements()
    assert req["namespace"] == "clawpilot"
    assert build_dev_server_start_hint()["hint"]
    assert len(build_dev_server_checklist()) >= 3
