from __future__ import annotations

from dataclasses import dataclass

from temporalio import workflow


@dataclass(frozen=True)
class DashboardRefreshInput:
    task_id: str
    run_id: str
    mode: str = "dashboard-refresh"


@dataclass(frozen=True)
class DashboardRefreshResult:
    task_id: str
    run_id: str
    status: str


@workflow.defn
class DashboardRefreshWorkflow:
    """Contract for dashboard refresh workflow."""

    @workflow.run
    async def run(self, input: DashboardRefreshInput) -> DashboardRefreshResult:
        return DashboardRefreshResult(task_id=input.task_id, run_id=input.run_id, status="planned")
