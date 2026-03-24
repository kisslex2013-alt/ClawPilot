from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable

from clawpilot.activities.runner import CommandResult
from clawpilot.artifacts.contracts import ArtifactRef, ArtifactSummary, ArtifactCollection, ArtifactKind
from clawpilot.models.progress import ProgressEvent
from clawpilot.orchestration.contracts import RunStatus, RunSummary, StepResult


def build_step_result(*, step_key: str, status: RunStatus, message: str, started_at: str | None = None, finished_at: str | None = None, details: dict | None = None) -> StepResult:
    return StepResult(step_key=step_key, status=status, message=message, started_at=started_at, finished_at=finished_at, details=details or {})


def build_artifact_summary(*, kind: str, path: str, exists: bool, source: str, run_id: str | None = None) -> ArtifactSummary:
    return ArtifactSummary(kind=kind, path=path, exists=exists, source=source, run_id=run_id)


def build_run_summary(*, workflow_name: str, task_id: str, run_id: str, status: RunStatus, step_results: list[StepResult], artifacts: list[ArtifactSummary], progress_event_count: int, started_at: str | None = None, finished_at: str | None = None, notes: str | None = None) -> RunSummary:
    started_at = started_at or datetime.now(timezone.utc).isoformat()
    return RunSummary(workflow_name=workflow_name, task_id=task_id, run_id=run_id, status=status, started_at=started_at, finished_at=finished_at, step_results=step_results, artifacts=artifacts, progress_event_count=progress_event_count, notes=notes)


def summarize_command_result(*, workflow_name: str, task_id: str, run_id: str, command_result: CommandResult, progress_event_count: int, artifacts: list[ArtifactSummary] | None = None) -> RunSummary:
    status = RunStatus.succeeded if command_result.return_code == 0 else RunStatus.failed
    step = build_step_result(step_key="command", status=status, message="dry-run command completed" if status == RunStatus.succeeded else "dry-run command failed", started_at=command_result.started_at, finished_at=command_result.finished_at, details={"command": command_result.command, "cwd": command_result.cwd, "return_code": command_result.return_code, "dry_run": command_result.dry_run})
    return build_run_summary(workflow_name=workflow_name, task_id=task_id, run_id=run_id, status=status, step_results=[step], artifacts=artifacts or [], progress_event_count=progress_event_count, started_at=command_result.started_at, finished_at=command_result.finished_at, notes="derived from command result")


def summarize_progress_events(events: Iterable[ProgressEvent]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for event in events:
        counts[event.event_type.value] = counts.get(event.event_type.value, 0) + 1
    return counts
