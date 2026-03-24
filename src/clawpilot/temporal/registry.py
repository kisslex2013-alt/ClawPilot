from __future__ import annotations

from clawpilot.orchestration.registry import get_activity_specs, get_workflow_specs
from clawpilot.temporal.activities import run_dashboard_activity, run_full_cycle_activity, run_manifest_activity, run_notify_activity, run_smoke_activity
from clawpilot.temporal.workflows import ClawloopFullCycleWorkflow, DashboardRefreshWorkflow, SmokeCheckWorkflow


def get_temporal_workflows() -> list[str]:
    return ["clawloop_full_cycle", "smoke_check", "dashboard_refresh"]


def get_temporal_activities() -> list[str]:
    return ["run_full_cycle_activity", "run_smoke_activity", "run_dashboard_activity", "run_notify_activity", "run_manifest_activity"]


def describe_temporal_registration() -> dict[str, list[str]]:
    return {"workflows": get_temporal_workflows(), "activities": get_temporal_activities()}


def validate_registration_consistency() -> dict[str, object]:
    workflow_names = {spec.name for spec in get_workflow_specs()}
    activity_names = {spec.name for spec in get_activity_specs()}
    temporal = describe_temporal_registration()
    workflow_matches = workflow_names == {"clawloop_full_cycle", "smoke_check", "dashboard_refresh"}
    activity_matches = activity_names == {"run_full_cycle", "run_smoke", "run_dashboard", "run_notify", "run_manifest"}
    return {"ok": workflow_matches and activity_matches, "workflow_names": sorted(workflow_names), "activity_names": sorted(activity_names), "temporal": temporal}
