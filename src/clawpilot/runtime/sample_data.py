from __future__ import annotations

from datetime import datetime, timezone

from clawpilot.models.manifest_snapshot import ManifestArtifacts, ManifestSnapshot, VerdictCounts
from clawpilot.models.progress import ProgressEvent
from clawpilot.models.task_state import ArtifactRef, TaskPriority, TaskState, TaskStatus
from clawpilot.progress.builders import build_task_accepted, build_task_completed


def sample_progress_events(task_id: str = "sample-task", run_id: str = "sample-run") -> list[ProgressEvent]:
    now = datetime.now(timezone.utc).isoformat()
    return [
        build_task_accepted(task_id=task_id, workflow_name="demo", workflow_run_id=run_id, phase="foundation", step_key="accepted", message="Task accepted", created_at=now),
        build_task_completed(task_id=task_id, workflow_name="demo", workflow_run_id=run_id, phase="done", step_key="complete", message="Task completed", created_at=now),
    ]


def sample_task_state(task_id: str = "sample-task") -> TaskState:
    now = datetime.now(timezone.utc).isoformat()
    return TaskState(
        task_id=task_id,
        title="Sample task",
        status=TaskStatus.running,
        priority=TaskPriority.normal,
        current_phase="demo",
        current_step="step-1",
        progress_percent=50,
        needs_human_approval=False,
        blocker_reason=None,
        created_at=now,
        updated_at=now,
        artifact_refs=[ArtifactRef(kind="report", path="/tmp/report.md", source="demo")],
        last_progress_event_id=None,
    )


def sample_manifest_snapshot(run_id: str = "sample-run") -> ManifestSnapshot:
    now = datetime.now(timezone.utc).isoformat()
    return ManifestSnapshot(
        run_id=run_id,
        mode="demo",
        workspace="/tmp/workspace",
        git_commit="deadbeef",
        git_dirty=False,
        config_hash="sample",
        judge_stack=["demo-judge"],
        artifacts=ManifestArtifacts(dashboard="dashboard.md"),
        verdict_counts=VerdictCounts(pass_count=1, retry=0, escalation=0),
        generated_at=now,
    )
