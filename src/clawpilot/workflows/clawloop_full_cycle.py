from __future__ import annotations

from dataclasses import dataclass

from temporalio import workflow


@dataclass(frozen=True)
class ClawLoopFullCycleInput:
    task_id: str
    run_id: str
    mode: str = "full-cycle"


@dataclass(frozen=True)
class ClawLoopFullCycleResult:
    task_id: str
    run_id: str
    status: str


@workflow.defn
class ClawLoopFullCycleWorkflow:
    """Workflow contract for the full cycle.

    Expected steps:
    - full cycle
    - notify
    - dashboard
    - manifest

    Progress hook points belong around each step boundary.
    """

    @workflow.run
    async def run(self, input: ClawLoopFullCycleInput) -> ClawLoopFullCycleResult:
        return ClawLoopFullCycleResult(task_id=input.task_id, run_id=input.run_id, status="planned")
