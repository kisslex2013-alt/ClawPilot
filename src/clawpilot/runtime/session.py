from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from clawpilot.runtime.paths import ensure_local_runtime_dirs, get_progress_log_path


@dataclass(frozen=True)
class LocalRunSession:
    run_id: str
    workflow_name: str
    task_id: str
    mode: str
    started_at: str
    finished_at: str | None
    status: str
    runtime_base: str
    progress_log_path: str


def create_local_run_session(*, run_id: str, workflow_name: str, task_id: str, mode: str, runtime_base: str = ".clawpilot") -> LocalRunSession:
    ensure_local_runtime_dirs(runtime_base)
    started_at = datetime.now(timezone.utc).isoformat()
    return LocalRunSession(run_id=run_id, workflow_name=workflow_name, task_id=task_id, mode=mode, started_at=started_at, finished_at=None, status="running", runtime_base=runtime_base, progress_log_path=get_progress_log_path(runtime_base))


def close_local_run_session(session: LocalRunSession, *, status: str = "succeeded") -> LocalRunSession:
    return LocalRunSession(run_id=session.run_id, workflow_name=session.workflow_name, task_id=session.task_id, mode=session.mode, started_at=session.started_at, finished_at=datetime.now(timezone.utc).isoformat(), status=status, runtime_base=session.runtime_base, progress_log_path=session.progress_log_path)


def session_to_summary(session: LocalRunSession) -> dict[str, str | None]:
    return {
        "run_id": session.run_id,
        "workflow_name": session.workflow_name,
        "task_id": session.task_id,
        "mode": session.mode,
        "started_at": session.started_at,
        "finished_at": session.finished_at,
        "status": session.status,
        "runtime_base": session.runtime_base,
        "progress_log_path": session.progress_log_path,
    }
