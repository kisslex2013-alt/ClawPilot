from __future__ import annotations

from clawpilot.notifier.transport import build_transport_spec, describe_transport_mode, resolve_default_transport


def test_transport_resolution():
    spec = build_transport_spec()
    assert spec.mode.value in {"dry_run", "file_log", "disabled"}
    assert describe_transport_mode()["mode"]
    assert resolve_default_transport().target
