from __future__ import annotations

from temporalio import activity

from clawpilot.activities.clawloop import (
    ClawLoopRunPlan,
    ClawLoopRunResult,
    prepare_dashboard_run,
    prepare_full_cycle_run,
    prepare_manifest_run,
    prepare_notify_run,
    prepare_smoke_run,
    run_dashboard,
    run_full_cycle,
    run_manifest,
    run_notify,
    run_smoke,
)


@activity.defn(name="run_full_cycle_activity")
def run_full_cycle_activity(input: ClawLoopRunPlan) -> ClawLoopRunResult:
    return run_full_cycle(run_id=input.env.get("RUN_ID"), dry_run=input.dry_run)


@activity.defn(name="run_smoke_activity")
def run_smoke_activity(input: ClawLoopRunPlan) -> ClawLoopRunResult:
    return run_smoke(run_id=input.env.get("RUN_ID"), dry_run=input.dry_run)


@activity.defn(name="run_dashboard_activity")
def run_dashboard_activity(input: ClawLoopRunPlan) -> ClawLoopRunResult:
    return run_dashboard(run_id=input.env.get("RUN_ID"), dry_run=input.dry_run)


@activity.defn(name="run_notify_activity")
def run_notify_activity(input: ClawLoopRunPlan) -> ClawLoopRunResult:
    return run_notify(run_id=input.env.get("RUN_ID"), dry_run=input.dry_run)


@activity.defn(name="run_manifest_activity")
def run_manifest_activity(input: ClawLoopRunPlan) -> ClawLoopRunResult:
    return run_manifest(run_id=input.env.get("RUN_ID"), dry_run=input.dry_run)
