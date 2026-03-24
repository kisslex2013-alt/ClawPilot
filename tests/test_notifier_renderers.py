from __future__ import annotations

from clawpilot.models.progress import ProgressEvent, ProgressEventType, ProgressLevel
from clawpilot.notifier.renderers import render_blocker_message, render_completion_message, render_progress_event_message
from clawpilot.orchestration.contracts import ArtifactSummary, RunStatus, RunSummary, StepResult


def _summary() -> RunSummary:
    return RunSummary(workflow_name="smoke_check", task_id="t", run_id="r", status=RunStatus.succeeded, started_at="2026-03-24T00:00:00Z", finished_at="2026-03-24T00:01:00Z", step_results=[StepResult(step_key="command", status=RunStatus.succeeded, message="ok")], artifacts=[ArtifactSummary(kind="manifest", path="x", exists=True, source="y")], progress_event_count=1)


def test_render_progress_event_message():
    event = ProgressEvent(id="1", task_id="t", workflow_name="wf", workflow_run_id="r", event_type=ProgressEventType.task_accepted, level=ProgressLevel.info, phase="phase", step_key="step", message="accepted", created_at="2026-03-24T00:00:00Z")
    rendered = render_progress_event_message(event)
    assert "accepted" in rendered.text


def test_render_completion_message():
    assert "DONE" in render_completion_message(_summary()).text


def test_render_blocker_message():
    assert "BLOCKED" in render_blocker_message("x", "y").text
