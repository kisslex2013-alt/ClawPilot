from __future__ import annotations

from clawpilot.orchestration.registry import get_workflow_spec


def get_sample_workflow_name(name: str) -> str:
    return get_workflow_spec(name).name


def build_sample_workflow_submission(*, name: str, task_id: str, run_id: str, connect: bool = False) -> dict[str, object]:
    return {"workflow_name": get_sample_workflow_name(name), "task_id": task_id, "run_id": run_id, "connect": connect}
