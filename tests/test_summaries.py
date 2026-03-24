from __future__ import annotations

from clawpilot.activities.runner import run_command
from clawpilot.models.progress import ProgressEventType, ProgressLevel, ProgressEvent
from clawpilot.orchestration.contracts import RunStatus
from clawpilot.orchestration.summaries import build_run_summary, summarize_command_result, summarize_progress_events


def test_run_summary():
    result = run_command(["echo", "x"], cwd="/tmp", dry_run=True)
    summary = summarize_command_result(workflow_name="smoke_check", task_id="t1", run_id="r1", command_result=result, progress_event_count=2)
    assert summary.status == RunStatus.succeeded
    assert summary.progress_event_count == 2


def test_progress_counts():
    events = [ProgressEvent(id="1", task_id="t", workflow_name="w", workflow_run_id="r", event_type=ProgressEventType.task_accepted, level=ProgressLevel.info, phase="p", step_key="s", message="m", created_at="2026-03-24T00:00:00Z")]
    counts = summarize_progress_events(events)
    assert counts["task_accepted"] == 1
