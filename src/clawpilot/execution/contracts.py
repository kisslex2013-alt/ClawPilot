from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class ExecutionMode(str, Enum):
    preview = "preview"
    dry_run = "dry_run"
    local_execute = "local_execute"


class LocalExecutionPolicy(BaseModel):
    workflow_name: str
    allowed: bool = False
    requires_explicit_opt_in: bool = True
    notes: str | None = None


class LocalExecutionRequest(BaseModel):
    workflow_name: str
    mode: ExecutionMode = ExecutionMode.preview
    cwd: Path
    command_summary: list[str] = Field(default_factory=list)
    run_id: str | None = None
    explicit_opt_in: bool = False


class LocalExecutionResult(BaseModel):
    workflow_name: str
    mode: ExecutionMode
    cwd: str
    allowed: bool
    requires_explicit_opt_in: bool
    command_summary: list[str] = Field(default_factory=list)
    artifact_summary: dict[str, Any] | None = None
    progress_log_path: str | None = None
    run_summary_path: str | None = None
    notes: str | None = None
