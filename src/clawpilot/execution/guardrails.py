from __future__ import annotations

from clawpilot.execution.contracts import ExecutionMode, LocalExecutionPolicy, LocalExecutionRequest, LocalExecutionResult

_ALLOWLIST = {"smoke_check": True, "dashboard_refresh": False, "clawloop_full_cycle": False}


def can_execute_workflow_locally(workflow_name: str) -> bool:
    return _ALLOWLIST.get(workflow_name, False)


def require_explicit_local_execute(mode: ExecutionMode) -> bool:
    return mode == ExecutionMode.local_execute


def build_local_execution_guardrails() -> list[str]:
    return ["smoke_check is the only local_execute allowlisted workflow in v1.", "dashboard_refresh remains preview-only by default.", "clawloop_full_cycle is preview-only in this pack.", "local_execute requires explicit opt-in."]


def validate_local_execution_request(request: LocalExecutionRequest) -> LocalExecutionResult:
    allowed = can_execute_workflow_locally(request.workflow_name) and request.mode == ExecutionMode.local_execute and request.explicit_opt_in
    if not allowed:
        return LocalExecutionResult(workflow_name=request.workflow_name, mode=request.mode, cwd=str(request.cwd), allowed=False, requires_explicit_opt_in=require_explicit_local_execute(request.mode), command_summary=request.command_summary, notes="blocked by guardrails")
    return LocalExecutionResult(workflow_name=request.workflow_name, mode=request.mode, cwd=str(request.cwd), allowed=True, requires_explicit_opt_in=True, command_summary=request.command_summary, notes="allowed by guardrails")
