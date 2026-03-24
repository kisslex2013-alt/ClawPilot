from __future__ import annotations

from clawpilot.temporal.local_smoke import build_local_smoke_plan, run_local_connectivity_smoke, summarize_local_smoke
from clawpilot.temporal.worker_runtime import build_worker_start_plan


def test_local_smoke_plan():
    plan = build_local_smoke_plan(workflow_name="smoke_check", task_id="t", run_id="r")
    assert plan["client_target"]["task_queue"] == "clawpilot-main"


def test_worker_start_plan():
    plan = build_worker_start_plan()
    assert plan.connect is False


def test_local_smoke_summary():
    summary = summarize_local_smoke(build_local_smoke_plan(workflow_name="smoke_check", task_id="t", run_id="r"))
    assert summary["workflow_name"] == "smoke_check"
