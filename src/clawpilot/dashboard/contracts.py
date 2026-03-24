from __future__ import annotations

from pydantic import BaseModel


class RunArtifactLink(BaseModel):
    kind: str
    path: str
    source: str


class TaskCard(BaseModel):
    task_id: str
    title: str
    status: str
    current_phase: str
    blocker_state: str | None = None
    approval_state: str | None = None
    updated_at: str


class RunSummaryView(BaseModel):
    run_id: str
    task_id: str
    status: str
    summary: str | None = None
    artifacts: list[RunArtifactLink]
