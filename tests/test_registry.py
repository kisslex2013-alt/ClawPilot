from __future__ import annotations

from clawpilot.orchestration.registry import get_activity_spec, get_workflow_spec, list_activity_names, list_workflow_names


def test_registry_lookup():
    assert "smoke_check" in list_workflow_names()
    assert "run_smoke" in list_activity_names()
    assert get_workflow_spec("smoke_check").name == "smoke_check"
    assert get_activity_spec("run_smoke").name == "run_smoke"
