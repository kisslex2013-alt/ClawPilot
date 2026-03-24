from __future__ import annotations

from clawpilot.temporal.registry import describe_temporal_registration, validate_registration_consistency


def test_temporal_registry():
    reg = describe_temporal_registration()
    assert "clawloop_full_cycle" in reg["workflows"]
    assert "run_smoke_activity" in reg["activities"]
    assert validate_registration_consistency()["ok"] is True
