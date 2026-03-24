from __future__ import annotations

from clawpilot.models.progress import ProgressEvent, ProgressEventType, ProgressLevel
from clawpilot.notifier.builders import build_blocker_notification, build_completion_notification, build_digest_messages, build_live_progress_messages
from clawpilot.notifier.contracts import ProgressNotificationPolicy
from clawpilot.orchestration.contracts import ArtifactSummary, RunStatus, RunSummary, StepResult


def _summary() -> RunSummary:
    return RunSummary(workflow_name="smoke_check", task_id="t", run_id="r", status=RunStatus.succeeded, started_at="2026-03-24T00:00:00Z", finished_at="2026-03-24T00:01:00Z", step_results=[StepResult(step_key="command", status=RunStatus.succeeded, message="ok")], artifacts=[ArtifactSummary(kind="manifest", path="x", exists=True, source="y")], progress_event_count=1)


def test_build_live_progress_messages():
    event = ProgressEvent(id="1", task_id="t", workflow_name="wf", workflow_run_id="r", event_type=ProgressEventType.blocked, level=ProgressLevel.warning, phase="phase", step_key="step", message="blocked", created_at="2026-03-24T00:00:00Z")
    assert build_live_progress_messages([event], ProgressNotificationPolicy()).count is not None


def test_build_digest_messages():
    assert build_digest_messages(_summary(), ProgressNotificationPolicy())


def test_blocker_and_completion_notifications():
    assert "BLOCKED" in build_blocker_notification("x", "y").body
    assert "DONE" in build_completion_notification(_summary()).body
