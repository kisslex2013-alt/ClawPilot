from __future__ import annotations

from clawpilot.models.progress import ProgressEvent, ProgressEventType, ProgressLevel
from clawpilot.orchestration.contracts import ArtifactSummary, RunStatus, RunSummary, StepResult
from clawpilot.notifier.builders import build_blocker_notification, build_completion_notification, build_digest_messages, build_live_progress_messages
from clawpilot.notifier.contracts import ProgressNotificationPolicy


def _sample_summary() -> RunSummary:
    return RunSummary(workflow_name="smoke_check", task_id="sample-task", run_id="sample-run", status=RunStatus.succeeded, started_at="2026-03-24T00:00:00Z", finished_at="2026-03-24T00:01:00Z", step_results=[StepResult(step_key="command", status=RunStatus.succeeded, message="done")], artifacts=[ArtifactSummary(kind="manifest", path=".clawpilot/runs/sample-run/manifest.json", exists=True, source="clawloop", run_id="sample-run")], progress_event_count=2, notes="sample")


def example_progress_feed() -> list[dict[str, object]]:
    events = [ProgressEvent(id="1", task_id="sample-task", workflow_name="smoke_check", workflow_run_id="sample-run", event_type=ProgressEventType.task_accepted, level=ProgressLevel.info, phase="run", step_key="accepted", message="Task accepted", created_at="2026-03-24T00:00:00Z")]
    return [item.model_dump() for item in build_live_progress_messages(events, ProgressNotificationPolicy())]


def example_digest_feed() -> list[dict[str, object]]:
    return [item.model_dump() for item in build_digest_messages(_sample_summary(), ProgressNotificationPolicy())]


def example_blocker_message() -> dict[str, object]:
    return build_blocker_notification("Need input", "Smoke run is blocked").model_dump()


def example_completion_message() -> dict[str, object]:
    return build_completion_notification(_sample_summary()).model_dump()
