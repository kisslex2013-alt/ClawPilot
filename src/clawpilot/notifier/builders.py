from __future__ import annotations

from clawpilot.models.manifest_snapshot import ManifestSnapshot
from clawpilot.models.progress import ProgressEvent, ProgressEventType, ProgressLevel
from clawpilot.orchestration.contracts import RunSummary
from clawpilot.notifier.contracts import NotificationMessage, ProgressNotificationPolicy
from clawpilot.notifier.models import NotificationEnvelope, RenderFormat, RenderPolicy
from clawpilot.notifier.policy import should_emit_digest, should_emit_live_update
from clawpilot.notifier.renderers import render_blocker_message, render_completion_message, render_failure_message, render_progress_event_message, render_run_summary_message


def build_live_progress_messages(events: list[ProgressEvent], policy: ProgressNotificationPolicy | None = None) -> list[NotificationEnvelope]:
    policy = policy or ProgressNotificationPolicy()
    items: list[NotificationEnvelope] = []
    for event in events:
        if should_emit_live_update(event, policy):
            rendered = render_progress_event_message(event, RenderPolicy(mode=policy.mode, include_artifacts=policy.include_artifacts, include_diffstat=policy.include_diffstat, max_lines=policy.max_lines, collapse_progress_steps=policy.collapse_progress_steps))
            items.append(NotificationEnvelope(kind=rendered.kind, title=rendered.title or event.phase, body=rendered.text, format=rendered.format, policy=RenderPolicy(mode=policy.mode, include_artifacts=policy.include_artifacts, include_diffstat=policy.include_diffstat, max_lines=policy.max_lines, collapse_progress_steps=policy.collapse_progress_steps)))
    return items


def build_digest_messages(summary: RunSummary, policy: ProgressNotificationPolicy | None = None) -> list[NotificationEnvelope]:
    policy = policy or ProgressNotificationPolicy()
    synthetic = ProgressEvent(id=f"{summary.run_id}:digest", task_id=summary.task_id, workflow_name=summary.workflow_name, workflow_run_id=summary.run_id, event_type=ProgressEventType.task_completed, level=ProgressLevel.info, phase="digest", step_key="summary", message="digest", created_at=summary.started_at)
    if not should_emit_digest([synthetic], policy):
        return []
    rendered = render_run_summary_message(summary, RenderPolicy(mode=policy.mode, include_artifacts=policy.include_artifacts, include_diffstat=policy.include_diffstat, max_lines=policy.max_lines, collapse_progress_steps=policy.collapse_progress_steps))
    return [NotificationEnvelope(kind=rendered.kind, title=rendered.title or summary.task_id, body=rendered.text, format=rendered.format, policy=RenderPolicy(mode=policy.mode, include_artifacts=policy.include_artifacts, include_diffstat=policy.include_diffstat, max_lines=policy.max_lines, collapse_progress_steps=policy.collapse_progress_steps))]


def build_blocker_notification(title: str, body: str) -> NotificationEnvelope:
    rendered = render_blocker_message(title, body)
    return NotificationEnvelope(kind=rendered.kind, title=rendered.title or title, body=rendered.text, format=rendered.format)


def build_completion_notification(summary: RunSummary) -> NotificationEnvelope:
    rendered = render_completion_message(summary)
    return NotificationEnvelope(kind=rendered.kind, title=rendered.title or summary.task_id, body=rendered.text, format=rendered.format)


def build_failure_notification(summary: RunSummary, body: str | None = None) -> NotificationEnvelope:
    rendered = render_failure_message(summary, body=body)
    return NotificationEnvelope(kind=rendered.kind, title=rendered.title or summary.task_id, body=rendered.text, format=rendered.format)
