from __future__ import annotations

from dataclasses import dataclass

from temporalio import workflow

from clawpilot.activities.clawloop import ClawLoopRunPlan
from clawpilot.temporal.activities import (
    run_dashboard_activity,
    run_full_cycle_activity,
    run_manifest_activity,
    run_notify_activity,
    run_smoke_activity,
)


@dataclass(frozen=True)
class ClawloopFullCycleWorkflowInput:
    task_id: str
    run_id: str
    mode: str = "full-cycle"


@dataclass(frozen=True)
class ClawloopFullCycleWorkflowResult:
    task_id: str
    run_id: str
    status: str


@dataclass(frozen=True)
class SmokeCheckWorkflowInput:
    task_id: str
    run_id: str
    mode: str = "smoke"


@dataclass(frozen=True)
class SmokeCheckWorkflowResult:
    task_id: str
    run_id: str
    status: str


@dataclass(frozen=True)
class DashboardRefreshWorkflowInput:
    task_id: str
    run_id: str
    mode: str = "dashboard-refresh"


@dataclass(frozen=True)
class DashboardRefreshWorkflowResult:
    task_id: str
    run_id: str
    status: str


@workflow.defn(name="clawloop_full_cycle")
class ClawloopFullCycleWorkflow:
    @workflow.run
    async def run(self, input: ClawloopFullCycleWorkflowInput) -> ClawloopFullCycleWorkflowResult:
        # progress hook: workflow accepted
        await workflow.execute_activity(run_full_cycle_activity, ClawLoopRunPlan(command=["bash", "scripts/agent_eval_full_cycle.sh"], cwd="/root/clawloop", env={"RUN_ID": input.run_id, "MODE": input.mode}, dry_run=True), start_to_close_timeout=60)
        # progress hook: notify
        await workflow.execute_activity(run_notify_activity, ClawLoopRunPlan(command=["python3", "scripts/agent_eval_notify.py"], cwd="/root/clawloop", env={"RUN_ID": input.run_id, "MODE": "notify"}, dry_run=True), start_to_close_timeout=60)
        # progress hook: dashboard
        await workflow.execute_activity(run_dashboard_activity, ClawLoopRunPlan(command=["python3", "scripts/agent_eval_dashboard.py"], cwd="/root/clawloop", env={"RUN_ID": input.run_id, "MODE": "dashboard"}, dry_run=True), start_to_close_timeout=60)
        # progress hook: manifest
        await workflow.execute_activity(run_manifest_activity, ClawLoopRunPlan(command=["python3", "scripts/write_agent_eval_manifest.py"], cwd="/root/clawloop", env={"RUN_ID": input.run_id, "MODE": "manifest"}, dry_run=True), start_to_close_timeout=60)
        return ClawloopFullCycleWorkflowResult(task_id=input.task_id, run_id=input.run_id, status="planned")


@workflow.defn(name="smoke_check")
class SmokeCheckWorkflow:
    @workflow.run
    async def run(self, input: SmokeCheckWorkflowInput) -> SmokeCheckWorkflowResult:
        await workflow.execute_activity(run_smoke_activity, ClawLoopRunPlan(command=["bash", "scripts/agent_eval_full_cycle.sh", "--smoke"], cwd="/root/clawloop", env={"RUN_ID": input.run_id, "MODE": input.mode}, dry_run=True), start_to_close_timeout=30)
        return SmokeCheckWorkflowResult(task_id=input.task_id, run_id=input.run_id, status="planned")


@workflow.defn(name="dashboard_refresh")
class DashboardRefreshWorkflow:
    @workflow.run
    async def run(self, input: DashboardRefreshWorkflowInput) -> DashboardRefreshWorkflowResult:
        await workflow.execute_activity(run_dashboard_activity, ClawLoopRunPlan(command=["python3", "scripts/agent_eval_dashboard.py"], cwd="/root/clawloop", env={"RUN_ID": input.run_id, "MODE": input.mode}, dry_run=True), start_to_close_timeout=30)
        return DashboardRefreshWorkflowResult(task_id=input.task_id, run_id=input.run_id, status="planned")
