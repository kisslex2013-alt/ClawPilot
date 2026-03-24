from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field

from clawpilot.notifier.contracts import NotificationMessage, NotificationMode


class MessageKind(str, Enum):
    live_progress = "live_progress"
    digest = "digest"
    blocker = "blocker"
    approval_request = "approval_request"
    completion = "completion"
    failure = "failure"


class RenderFormat(str, Enum):
    plain_text = "plain_text"
    markdown = "markdown"


class RenderPolicy(BaseModel):
    mode: NotificationMode = NotificationMode.normal
    include_artifacts: bool = True
    include_diffstat: bool = False
    max_lines: int | None = None
    collapse_progress_steps: bool = True


class NotificationEnvelope(BaseModel):
    kind: MessageKind
    title: str
    body: str
    format: RenderFormat = RenderFormat.plain_text
    policy: RenderPolicy = Field(default_factory=RenderPolicy)


class RenderedMessage(BaseModel):
    kind: MessageKind
    text: str
    format: RenderFormat = RenderFormat.plain_text
    title: str | None = None
    notification: NotificationMessage | None = None
