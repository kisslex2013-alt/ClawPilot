from __future__ import annotations

from clawpilot.models.progress import ProgressEvent, ProgressEventType, ProgressLevel
from clawpilot.notifier.contracts import NotificationMode, ProgressNotificationPolicy
from clawpilot.notifier.policy import apply_render_policy, group_progress_events, should_emit_digest, should_emit_live_update


def _event(kind: ProgressEventType) -> ProgressEvent:
    return ProgressEvent(id="1", task_id="t", workflow_name="wf", workflow_run_id="r", event_type=kind, level=ProgressLevel.info, phase="phase", step_key="step", message="m", created_at="2026-03-24T00:00:00Z")


def test_policy_helpers():
    policy = ProgressNotificationPolicy(mode=NotificationMode.quiet)
    assert should_emit_live_update(_event(ProgressEventType.step_started), policy) is False
    assert should_emit_live_update(_event(ProgressEventType.blocked), policy) is True
    assert should_emit_digest([_event(ProgressEventType.task_completed)], policy) is True
    assert group_progress_events([_event(ProgressEventType.step_started)], policy)
    assert apply_render_policy(policy)["mode"] == NotificationMode.quiet
