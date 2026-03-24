from __future__ import annotations

from clawpilot.orchestration.contracts import ActivitySpec, WorkflowSpec

_WORKFLOWS = [
    WorkflowSpec(name="clawloop_full_cycle", purpose="Run the full ClawLoop cycle.", input_model_name="ClawLoopFullCycleInput", result_model_name="ClawLoopFullCycleResult", expected_artifacts=["latest_report", "latest_delta", "dashboard", "weekly_report", "disagreements", "manifest"], notes="Dry-run supported; no Temporal dependency in registry."),
    WorkflowSpec(name="smoke_check", purpose="Run a minimal smoke verification.", input_model_name="SmokeCheckInput", result_model_name="SmokeCheckResult", expected_artifacts=["manifest", "progress_log"], notes="Used for health checks and quick validation."),
    WorkflowSpec(name="dashboard_refresh", purpose="Refresh dashboard-facing summaries.", input_model_name="DashboardRefreshInput", result_model_name="DashboardRefreshResult", expected_artifacts=["dashboard", "latest_report", "latest_delta"], notes="Local-only summary contract."),
]

_ACTIVITIES = [
    ActivitySpec(name="run_full_cycle", purpose="Execute the full ClawLoop dry-run path.", input_model_name="ClawLoopRunInput", result_model_name="ClawLoopRunResult", expected_artifacts=["latest_report", "latest_delta", "dashboard", "weekly_report", "disagreements", "manifest"], notes="Wraps scripts/agent_eval_full_cycle.sh."),
    ActivitySpec(name="run_smoke", purpose="Execute the smoke dry-run path.", input_model_name="ClawLoopRunInput", result_model_name="ClawLoopRunResult", expected_artifacts=["manifest"], notes="Wraps scripts/agent_eval_full_cycle.sh --smoke."),
    ActivitySpec(name="run_dashboard", purpose="Execute dashboard refresh dry-run path.", input_model_name="ClawLoopRunInput", result_model_name="ClawLoopRunResult", expected_artifacts=["dashboard"], notes="Wraps scripts/agent_eval_dashboard.py."),
    ActivitySpec(name="run_notify", purpose="Execute notify dry-run path.", input_model_name="ClawLoopRunInput", result_model_name="ClawLoopRunResult", expected_artifacts=["notification"], notes="Wraps scripts/agent_eval_notify.py."),
    ActivitySpec(name="run_manifest", purpose="Execute manifest generation dry-run path.", input_model_name="ClawLoopRunInput", result_model_name="ClawLoopRunResult", expected_artifacts=["manifest"], notes="Wraps scripts/write_agent_eval_manifest.py."),
]


def get_workflow_specs() -> list[WorkflowSpec]:
    return list(_WORKFLOWS)


def get_activity_specs() -> list[ActivitySpec]:
    return list(_ACTIVITIES)


def get_workflow_spec(name: str) -> WorkflowSpec:
    for spec in _WORKFLOWS:
        if spec.name == name:
            return spec
    raise KeyError(name)


def get_activity_spec(name: str) -> ActivitySpec:
    for spec in _ACTIVITIES:
        if spec.name == name:
            return spec
    raise KeyError(name)


def list_workflow_names() -> list[str]:
    return [spec.name for spec in _WORKFLOWS]


def list_activity_names() -> list[str]:
    return [spec.name for spec in _ACTIVITIES]
