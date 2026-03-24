from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class NotificationMode(str, Enum):
    quiet = "quiet"
    normal = "normal"
    verbose = "verbose"


class NotificationMessage(BaseModel):
    task_id: str
    title: str
    body: str
    mode: NotificationMode = NotificationMode.normal


class ProgressNotificationPolicy(BaseModel):
    mode: NotificationMode = NotificationMode.normal
    allow_step_events: bool = True
    allow_digests: bool = True
    allow_approvals: bool = True
    include_artifacts: bool = True
    include_diffstat: bool = False
    max_lines: int | None = None
    collapse_progress_steps: bool = True
