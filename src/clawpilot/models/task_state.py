from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


class TaskStatus(str, Enum):
    new = "new"
    planned = "planned"
    running = "running"
    verifying = "verifying"
    waiting_human = "waiting_human"
    blocked = "blocked"
    done = "done"
    failed = "failed"
    cancelled = "cancelled"


class TaskPriority(str, Enum):
    low = "low"
    normal = "normal"
    high = "high"
    critical = "critical"


class ArtifactRef(BaseModel):
    kind: str
    path: str
    source: str
    run_id: str | None = None


class TaskState(BaseModel):
    task_id: str
    title: str
    status: TaskStatus
    priority: TaskPriority
    current_phase: str
    current_step: str
    progress_percent: float
    needs_human_approval: bool
    blocker_reason: str | None
    created_at: str
    updated_at: str
    artifact_refs: list[ArtifactRef]
    last_progress_event_id: str | None
