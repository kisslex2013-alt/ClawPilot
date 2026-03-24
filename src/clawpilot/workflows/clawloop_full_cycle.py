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
    """Contract for the full ClawLoop cycle.

    Expected activity sequence:
    - full cycle
    - notify
    - dashboard
    - manifest

    Progress events should be emitted at each stage boundary.
    """

    @workflow.run
    async def run(self, input: ClawLoopFullCycleInput) -> ClawLoopFullCycleResult:
        return ClawLoopFullCycleResult(task_id=input.task_id, run_id=input.run_id, status="planned")
