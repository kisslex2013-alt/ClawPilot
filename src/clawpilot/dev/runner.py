from __future__ import annotations

from clawpilot.activities.clawloop import run_dashboard, run_full_cycle, run_manifest, run_notify, run_smoke
from clawpilot.models.progress import ProgressEvent
from clawpilot.orchestration.contracts import RunStatus
from clawpilot.orchestration.summaries import build_run_summary, summarize_command_result
from clawpilot.runtime.sample_data import sample_progress_events
from clawpilot.runtime.session import close_local_run_session, create_local_run_session, session_to_summary


def execute_dry_run_workflow(*, workflow_name: str, task_id: str, run_id: str, runtime_base: str = ".clawpilot") -> dict:
    session = create_local_run_session(run_id=run_id, workflow_name=workflow_name, task_id=task_id, mode=workflow_name, runtime_base=runtime_base)
    if workflow_name == "clawloop_full_cycle":
        outcome = run_full_cycle(run_id=run_id, dry_run=True)
    elif workflow_name == "smoke_check":
        outcome = run_smoke(run_id=run_id, dry_run=True)
    elif workflow_name == "dashboard_refresh":
        outcome = run_dashboard(run_id=run_id, dry_run=True)
    else:
        raise KeyError(workflow_name)
    events: list[ProgressEvent] = sample_progress_events(task_id=task_id, run_id=run_id)
    summary = summarize_command_result(workflow_name=workflow_name, task_id=task_id, run_id=run_id, command_result=outcome.result, progress_event_count=len(events))
    closed = close_local_run_session(session, status=summary.status.value)
    return {"session": session_to_summary(closed), "summary": summary.model_dump(), "events": [event.model_dump() for event in events]}
