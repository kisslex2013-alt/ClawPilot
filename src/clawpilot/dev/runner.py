from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

from clawpilot.activities.clawloop import run_dashboard, run_full_cycle, run_manifest, run_notify, run_smoke
from clawpilot.execution.contracts import ExecutionMode, LocalExecutionRequest, LocalExecutionResult
from clawpilot.execution.guardrails import validate_local_execution_request
from clawpilot.execution.persistence import write_command_result_json, write_progress_events_jsonl, write_run_summary_json
from clawpilot.models.progress import ProgressEvent
from clawpilot.orchestration.contracts import RunStatus
from clawpilot.orchestration.summaries import summarize_command_result
from clawpilot.runtime.sample_data import sample_progress_events
from clawpilot.runtime.session import close_local_run_session, create_local_run_session, session_to_summary
from clawpilot.artifacts.clawloop import detect_known_artifacts, summarize_artifact_collection


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


def execute_local_workflow(*, workflow_name: str, task_id: str, run_id: str, mode: ExecutionMode, execute: bool = False, runtime_base: str = ".clawpilot", timeout_seconds: float | None = None) -> dict:
    session = create_local_run_session(run_id=run_id, workflow_name=workflow_name, task_id=task_id, mode=mode.value, runtime_base=runtime_base)
    request = LocalExecutionRequest(workflow_name=workflow_name, mode=mode, cwd=Path("/root/clawpilot"), command_summary=[workflow_name], run_id=run_id, explicit_opt_in=execute)
    guard = validate_local_execution_request(request)
    events = sample_progress_events(task_id=task_id, run_id=run_id)
    artifact_collection = detect_known_artifacts(".", run_id=run_id)
    artifact_summary = summarize_artifact_collection(artifact_collection)
    command_result = {"command": [workflow_name], "return_code": 0, "dry_run": True, "stdout": "", "stderr": ""}
    if guard.allowed and execute:
        if workflow_name == "smoke_check":
            outcome = run_smoke(run_id=run_id, dry_run=False, timeout=timeout_seconds)
        elif workflow_name == "dashboard_refresh":
            outcome = run_dashboard(run_id=run_id, dry_run=False, timeout=timeout_seconds)
        elif workflow_name == "clawloop_full_cycle":
            outcome = run_full_cycle(run_id=run_id, dry_run=False, timeout=timeout_seconds)
        else:
            outcome = run_smoke(run_id=run_id, dry_run=True)
        command_result = {"command": outcome.result.command, "return_code": outcome.result.return_code, "dry_run": outcome.result.dry_run, "stdout": outcome.result.stdout, "stderr": outcome.result.stderr}
    summary = summarize_command_result(workflow_name=workflow_name, task_id=task_id, run_id=run_id, command_result=type("CR", (), {"return_code": command_result["return_code"], "command": command_result["command"], "cwd": str(session.runtime_base), "stdout": command_result.get("stdout", ""), "stderr": command_result.get("stderr", ""), "dry_run": command_result.get("dry_run", True), "started_at": session.started_at, "finished_at": session.started_at})(), progress_event_count=len(events), artifacts=[])
    progress_path = write_progress_events_jsonl(base=runtime_base, run_id=run_id, events=events)
    summary_payload = summary.model_dump()
    summary_payload["artifacts"] = [artifact.model_dump() for artifact in artifact_collection.items]
    summary_path = write_run_summary_json(base=runtime_base, run_id=run_id, summary=summary_payload)
    command_path = write_command_result_json(base=runtime_base, run_id=run_id, result=command_result)
    closed = close_local_run_session(session, status=summary.status.value)
    return {"local_execution": guard.model_dump(), "session": session_to_summary(closed), "summary": summary_payload, "paths": {"progress": progress_path, "summary": summary_path, "command": command_path}, "artifacts": artifact_summary, "events": [event.model_dump() for event in events]}
