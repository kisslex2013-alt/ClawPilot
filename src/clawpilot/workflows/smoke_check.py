from __future__ import annotations

from dataclasses import dataclass

from temporalio import workflow


@dataclass(frozen=True)
class SmokeCheckInput:
    task_id: str
    run_id: str
    mode: str = "smoke"


@dataclass(frozen=True)
class SmokeCheckResult:
    task_id: str
    run_id: str
    status: str


@workflow.defn
class SmokeCheckWorkflow:
    """Contract for smoke verification workflow."""

    @workflow.run
    async def run(self, input: SmokeCheckInput) -> SmokeCheckResult:
        return SmokeCheckResult(task_id=input.task_id, run_id=input.run_id, status="planned")
