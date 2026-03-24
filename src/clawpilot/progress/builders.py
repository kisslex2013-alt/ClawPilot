from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from clawpilot.models.progress import ProgressEvent, ProgressEventType, ProgressLevel


def _now(created_at: str | None) -> str:
    return created_at or datetime.now(timezone.utc).isoformat()


def _build(
    *,
    task_id: str,
    workflow_name: str,
    workflow_run_id: str,
    event_type: ProgressEventType,
    level: ProgressLevel,
    phase: str,
    step_key: str,
    message: str,
    created_at: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> ProgressEvent:
    return ProgressEvent(
        id=f"{workflow_run_id}:{step_key}:{event_type.value}",
        task_id=task_id,
        workflow_name=workflow_name,
        workflow_run_id=workflow_run_id,
        event_type=event_type,
        level=level,
        phase=phase,
        step_key=step_key,
        message=message,
        created_at=_now(created_at),
        metadata=metadata,
    )


def build_task_accepted(**kwargs: Any) -> ProgressEvent:
    return _build(event_type=ProgressEventType.task_accepted, level=ProgressLevel.info, **kwargs)


def build_phase_started(**kwargs: Any) -> ProgressEvent:
    return _build(event_type=ProgressEventType.phase_started, level=ProgressLevel.info, **kwargs)


def build_step_started(**kwargs: Any) -> ProgressEvent:
    return _build(event_type=ProgressEventType.step_started, level=ProgressLevel.info, **kwargs)


def build_step_completed(**kwargs: Any) -> ProgressEvent:
    return _build(event_type=ProgressEventType.step_completed, level=ProgressLevel.info, **kwargs)


def build_step_failed(**kwargs: Any) -> ProgressEvent:
    return _build(event_type=ProgressEventType.step_failed, level=ProgressLevel.error, **kwargs)


def build_blocked(**kwargs: Any) -> ProgressEvent:
    return _build(event_type=ProgressEventType.blocked, level=ProgressLevel.warning, **kwargs)


def build_approval_required(**kwargs: Any) -> ProgressEvent:
    return _build(event_type=ProgressEventType.approval_required, level=ProgressLevel.warning, **kwargs)


def build_task_completed(**kwargs: Any) -> ProgressEvent:
    return _build(event_type=ProgressEventType.task_completed, level=ProgressLevel.info, **kwargs)


def build_task_failed(**kwargs: Any) -> ProgressEvent:
    return _build(event_type=ProgressEventType.task_failed, level=ProgressLevel.error, **kwargs)
