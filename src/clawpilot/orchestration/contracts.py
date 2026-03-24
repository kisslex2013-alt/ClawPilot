from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class RunStatus(str, Enum):
    planned = "planned"
    running = "running"
    succeeded = "succeeded"
    failed = "failed"
    blocked = "blocked"
    cancelled = "cancelled"


class WorkflowSpec(BaseModel):
    name: str
    purpose: str
    input_model_name: str
    result_model_name: str
    safe_by_default: bool = True
    dry_run_supported: bool = True
    expected_artifacts: list[str] = Field(default_factory=list)
    notes: str | None = None


class ActivitySpec(BaseModel):
    name: str
    purpose: str
    input_model_name: str
    result_model_name: str
    safe_by_default: bool = True
    dry_run_supported: bool = True
    expected_artifacts: list[str] = Field(default_factory=list)
    notes: str | None = None


class RunRequest(BaseModel):
    workflow_name: str
    task_id: str
    run_id: str
    mode: str
    dry_run: bool = True


class RunResult(BaseModel):
    workflow_name: str
    task_id: str
    run_id: str
    status: RunStatus
    notes: str | None = None


class StepResult(BaseModel):
    step_key: str
    status: RunStatus
    message: str
    started_at: str | None = None
    finished_at: str | None = None
    details: dict[str, Any] = Field(default_factory=dict)


class ArtifactSummary(BaseModel):
    kind: str
    path: str
    exists: bool
    source: str
    run_id: str | None = None


class RunSummary(BaseModel):
    workflow_name: str
    task_id: str
    run_id: str
    status: RunStatus
    started_at: str
    finished_at: str | None = None
    step_results: list[StepResult] = Field(default_factory=list)
    artifacts: list[ArtifactSummary] = Field(default_factory=list)
    progress_event_count: int = 0
    notes: str | None = None
