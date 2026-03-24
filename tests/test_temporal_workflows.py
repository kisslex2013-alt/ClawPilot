from __future__ import annotations

from clawpilot.temporal.workflows import ClawloopFullCycleWorkflow, DashboardRefreshWorkflow, SmokeCheckWorkflow


def test_temporal_imports():
    assert ClawloopFullCycleWorkflow.__name__ == "ClawloopFullCycleWorkflow"
    assert SmokeCheckWorkflow.__name__ == "SmokeCheckWorkflow"
    assert DashboardRefreshWorkflow.__name__ == "DashboardRefreshWorkflow"
