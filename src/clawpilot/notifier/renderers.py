from __future__ import annotations

from clawpilot.models.manifest_snapshot import ManifestSnapshot
from clawpilot.models.progress import ProgressEvent
from clawpilot.orchestration.contracts import RunSummary
from clawpilot.notifier.models import MessageKind, NotificationEnvelope, RenderFormat, RenderedMessage, RenderPolicy


def _fmt(text: str, format: RenderFormat) -> str:
    return text if format == RenderFormat.plain_text else text.replace("*", "\\*")


def render_progress_event_message(event: ProgressEvent, policy: RenderPolicy | None = None, format: RenderFormat = RenderFormat.plain_text) -> RenderedMessage:
    policy = policy or RenderPolicy()
    text = f"[{event.level.value}] {event.task_id}: {event.message}"
    return RenderedMessage(kind=MessageKind.live_progress, text=_fmt(text, format), format=format, title=event.phase)


def render_run_summary_message(summary: RunSummary, policy: RenderPolicy | None = None, format: RenderFormat = RenderFormat.plain_text) -> RenderedMessage:
    policy = policy or RenderPolicy()
    lines = [f"Run {summary.run_id} ({summary.workflow_name})", f"Status: {summary.status.value}"]
    if policy.include_artifacts and summary.artifacts:
        lines.append(f"Artifacts: {len(summary.artifacts)}")
    return RenderedMessage(kind=MessageKind.digest, text=_fmt("\n".join(lines), format), format=format, title=summary.task_id)


def render_blocker_message(title: str, body: str, format: RenderFormat = RenderFormat.plain_text) -> RenderedMessage:
    return RenderedMessage(kind=MessageKind.blocker, text=_fmt(f"BLOCKED: {title}\n{body}", format), format=format, title=title)


def render_approval_request_message(title: str, body: str, format: RenderFormat = RenderFormat.plain_text) -> RenderedMessage:
    return RenderedMessage(kind=MessageKind.approval_request, text=_fmt(f"APPROVAL NEEDED: {title}\n{body}", format), format=format, title=title)


def render_completion_message(summary: RunSummary, format: RenderFormat = RenderFormat.plain_text) -> RenderedMessage:
    return RenderedMessage(kind=MessageKind.completion, text=_fmt(f"DONE: {summary.workflow_name} ({summary.run_id})", format), format=format, title=summary.task_id)


def render_failure_message(summary: RunSummary, body: str | None = None, format: RenderFormat = RenderFormat.plain_text) -> RenderedMessage:
    text = f"FAILED: {summary.workflow_name} ({summary.run_id})"
    if body:
        text = f"{text}\n{body}"
    return RenderedMessage(kind=MessageKind.failure, text=_fmt(text, format), format=format, title=summary.task_id)
