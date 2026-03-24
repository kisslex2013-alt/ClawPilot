from __future__ import annotations

import argparse
import json
import subprocess

from clawpilot.activities.clawloop import run_dashboard, run_full_cycle, run_manifest, run_notify, run_smoke
from clawpilot.artifacts.clawloop import detect_known_artifacts
from clawpilot.config import load_settings
from clawpilot.dev.runner import execute_dry_run_workflow
from clawpilot.orchestration.registry import list_activity_names, list_workflow_names
from clawpilot.progress.serialization import events_to_jsonl
from clawpilot.runtime.paths import ensure_local_runtime_dirs
from clawpilot.runtime.sample_data import sample_progress_events
from clawpilot.temporal.client import describe_client_target, maybe_connect_client
from clawpilot.temporal.dev_runner import build_dev_run_plan, maybe_run_connectivity_check, run_worker_preview
from clawpilot.temporal.dev_server import build_dev_server_checklist, build_dev_server_start_hint, describe_local_temporal_dev_requirements
from clawpilot.temporal.registry import get_temporal_activities, get_temporal_workflows, validate_registration_consistency
from clawpilot.temporal.worker_runtime import build_task_queue_name, create_worker_definition, describe_worker_runtime
from clawpilot.worker import build_connectivity_guardrails, build_local_dev_bootstrap_summary, maybe_build_local_worker_preview, describe_safe_dev_modes


def _print_settings() -> None:
    settings = load_settings()
    print(json.dumps({"temporal": settings.temporal.model_dump(), "database": {"url": "<hidden>"}, "clawloop": {"repo_path": str(settings.clawloop.repo_path)}, "openclaw": {"workspace": str(settings.openclaw.workspace), "config_path": str(settings.openclaw.config_path)}, "telegram": {"bot_token": bool(settings.telegram.bot_token), "chat_id": bool(settings.telegram.chat_id), "progress_mode": settings.telegram.progress_mode}, "log_level": settings.log_level, "env": settings.env}, indent=2, sort_keys=True))


def _print_run(name: str, result) -> None:
    print(json.dumps({"name": name, "command": result.plan.command, "cwd": result.plan.cwd, "env": {k: result.plan.env[k] for k in ("WORKSPACE", "RUN_ID", "MODE") if k in result.plan.env}, "result": {"return_code": result.result.return_code, "stdout": result.result.stdout, "stderr": result.result.stderr, "dry_run": result.result.dry_run, "started_at": result.result.started_at, "finished_at": result.result.finished_at}}, indent=2, sort_keys=True))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="clawpilot")
    sub = parser.add_subparsers(dest="cmd", required=True)
    for name in ("show-config", "check-env", "bootstrap-dev", "list-workflows", "list-activities", "list-temporal-workflows", "list-temporal-activities", "validate-registration", "show-worker-plan", "show-run-summary", "detect-artifacts", "sample-progress-jsonl", "temporal-client-target", "temporal-connectivity-check", "show-dev-server-hints", "show-task-queue", "show-worker-definition", "preview-worker", "preview-run-plan"):
        sub.add_parser(name)
    dry = sub.add_parser("dry-run")
    dry_sub = dry.add_subparsers(dest="dry_cmd", required=True)
    for name in ("full-cycle", "smoke", "dashboard", "notify", "manifest"):
        dry_sub.add_parser(name)
    wf = sub.add_parser("dry-run-workflow")
    wf_sub = wf.add_subparsers(dest="workflow_name", required=True)
    for name in ("full-cycle", "smoke-check", "dashboard-refresh"):
        wf_sub.add_parser(name)
    args = parser.parse_args(argv)

    if args.cmd == "show-config": _print_settings(); return 0
    if args.cmd == "check-env": return subprocess.call(["sh", "scripts/check-env.sh"])
    if args.cmd == "bootstrap-dev": print(json.dumps(ensure_local_runtime_dirs(), indent=2, sort_keys=True)); return 0
    if args.cmd == "list-workflows": print("\n".join(list_workflow_names())); return 0
    if args.cmd == "list-activities": print("\n".join(list_activity_names())); return 0
    if args.cmd == "list-temporal-workflows": print("\n".join(get_temporal_workflows())); return 0
    if args.cmd == "list-temporal-activities": print("\n".join(get_temporal_activities())); return 0
    if args.cmd == "validate-registration": print(json.dumps(validate_registration_consistency(), indent=2, sort_keys=True)); return 0
    if args.cmd == "show-worker-plan": print(json.dumps(maybe_build_local_worker_preview(), indent=2, sort_keys=True)); return 0
    if args.cmd == "sample-progress-jsonl": print(events_to_jsonl(sample_progress_events())); return 0
    if args.cmd == "show-run-summary": print(json.dumps(execute_dry_run_workflow(workflow_name="smoke_check", task_id="sample-task", run_id="sample-run"), indent=2, sort_keys=True)); return 0
    if args.cmd == "detect-artifacts": print(json.dumps([item.model_dump() for item in detect_known_artifacts(".", run_id="sample-run").items], indent=2, sort_keys=True)); return 0
    if args.cmd == "temporal-client-target": print(json.dumps(describe_client_target(), indent=2, sort_keys=True)); return 0
    if args.cmd == "temporal-connectivity-check": print(json.dumps(maybe_connect_client(connect="--connect" in (argv or [])), indent=2, sort_keys=True)); return 0
    if args.cmd == "show-dev-server-hints": print(json.dumps({"requirements": describe_local_temporal_dev_requirements(), "hint": build_dev_server_start_hint(), "checklist": build_dev_server_checklist()}, indent=2, sort_keys=True)); return 0
    if args.cmd == "show-task-queue": print(build_task_queue_name()); return 0
    if args.cmd == "show-worker-definition": print(json.dumps(create_worker_definition(), indent=2, sort_keys=True)); return 0
    if args.cmd == "preview-worker": print(json.dumps(run_worker_preview(workflow_name="smoke_check", task_id="sample-task", run_id="sample-run"), indent=2, sort_keys=True)); return 0
    if args.cmd == "preview-run-plan": print(json.dumps(build_dev_run_plan(workflow_name="smoke_check", task_id="sample-task", run_id="sample-run"), indent=2, sort_keys=True)); return 0
    if args.cmd == "dry-run":
        mapping = {"full-cycle": run_full_cycle, "smoke": run_smoke, "dashboard": run_dashboard, "notify": run_notify, "manifest": run_manifest}
        _print_run(args.dry_cmd, mapping[args.dry_cmd](dry_run=True)); return 0
    if args.cmd == "dry-run-workflow":
        mapping = {"full-cycle": "clawloop_full_cycle", "smoke-check": "smoke_check", "dashboard-refresh": "dashboard_refresh"}
        print(json.dumps(execute_dry_run_workflow(workflow_name=mapping[args.workflow_name], task_id="sample-task", run_id="sample-run"), indent=2, sort_keys=True)); return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
