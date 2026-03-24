from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ProgressEventType(str, Enum):
    task_accepted = "task_accepted"
    phase_started = "phase_started"
    step_started = "step_started"
    step_completed = "step_completed"
    step_failed = "step_failed"
    retry_scheduled = "retry_scheduled"
    blocked = "blocked"
    approval_required = "approval_required"
    resumed = "resumed"
    task_completed = "task_completed"
    task_failed = "task_failed"


class ProgressLevel(str, Enum):
    info = "info"
    warning = "warning"
    error = "error"


class ProgressEvent(BaseModel):
    id: str
    task_id: str
    workflow_name: str
    workflow_run_id: str
    event_type: ProgressEventType
    level: ProgressLevel
    phase: str
    step_key: str
    message: str
    created_at: str
    metadata: dict[str, Any] | None = Field(default=None)
