from __future__ import annotations

from clawpilot.models.manifest_snapshot import ManifestArtifacts, ManifestSnapshot, VerdictCounts
from clawpilot.models.progress import ProgressEvent, ProgressEventType, ProgressLevel
from clawpilot.models.task_state import ArtifactRef, TaskPriority, TaskState, TaskStatus
from clawpilot.progress.builders import build_blocked, build_task_accepted


def test_progress_event_validation():
    event = ProgressEvent(
        id="1",
        task_id="t1",
        workflow_name="wf",
        workflow_run_id="r1",
        event_type=ProgressEventType.task_accepted,
        level=ProgressLevel.info,
        phase="foundation",
        step_key="start",
        message="accepted",
        created_at="2026-03-24T00:00:00Z",
        metadata={"a": 1},
    )
    assert event.task_id == "t1"


def test_task_state_validation():
    state = TaskState(
        task_id="t1",
        title="Task",
        status=TaskStatus.running,
        priority=TaskPriority.normal,
        current_phase="phase",
        current_step="step",
        progress_percent=50,
        needs_human_approval=False,
        blocker_reason=None,
        created_at="2026-03-24T00:00:00Z",
        updated_at="2026-03-24T00:00:00Z",
        artifact_refs=[ArtifactRef(kind="report", path="/tmp/r.md", source="clawloop")],
        last_progress_event_id=None,
    )
    assert state.priority == TaskPriority.normal


def test_manifest_snapshot_validation():
    snapshot = ManifestSnapshot(
        run_id="run",
        mode="full",
        workspace="/tmp",
        git_commit="abc",
        git_dirty=False,
        config_hash="hash",
        judge_stack=["judge"],
        artifacts=ManifestArtifacts(dashboard="dash.md"),
        verdict_counts=VerdictCounts(pass_count=1, retry=0, escalation=0),
        generated_at="2026-03-24T00:00:00Z",
    )
    assert snapshot.artifacts.dashboard == "dash.md"


def test_progress_builders():
    event = build_task_accepted(
        task_id="t1",
        workflow_name="wf",
        workflow_run_id="run1",
        phase="phase",
        step_key="step",
        message="accepted",
        created_at="2026-03-24T00:00:00Z",
    )
    assert event.event_type == ProgressEventType.task_accepted
    assert event.level == ProgressLevel.info

    blocked = build_blocked(
        task_id="t1",
        workflow_name="wf",
        workflow_run_id="run1",
        phase="phase",
        step_key="step",
        message="blocked",
        created_at="2026-03-24T00:00:00Z",
    )
    assert blocked.level == ProgressLevel.warning
