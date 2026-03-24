from __future__ import annotations

from collections import defaultdict

from clawpilot.models.progress import ProgressEvent
from clawpilot.notifier.contracts import NotificationMode, ProgressNotificationPolicy


def should_emit_live_update(event: ProgressEvent, policy: ProgressNotificationPolicy) -> bool:
    if policy.mode == NotificationMode.quiet:
        return event.event_type.value in {"blocked", "approval_required", "task_completed", "task_failed"}
    if policy.mode == NotificationMode.normal:
        return event.event_type.value != "step_started"
    return True


def should_emit_digest(events: list[ProgressEvent], policy: ProgressNotificationPolicy) -> bool:
    return policy.allow_digests and bool(events)


def group_progress_events(events: list[ProgressEvent], policy: ProgressNotificationPolicy) -> dict[str, list[ProgressEvent]]:
    grouped: dict[str, list[ProgressEvent]] = defaultdict(list)
    for event in events:
        key = event.phase if policy.collapse_progress_steps else event.id
        grouped[key].append(event)
    return dict(grouped)


def apply_render_policy(policy: ProgressNotificationPolicy) -> dict[str, object]:
    return policy.model_dump()
