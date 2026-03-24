from __future__ import annotations

import argparse
import json
import subprocess
import sys

from clawpilot.activities.clawloop import run_dashboard, run_full_cycle, run_manifest, run_notify, run_smoke
from clawpilot.config import load_settings
from clawpilot.progress.serialization import events_to_jsonl
from clawpilot.runtime.paths import ensure_local_runtime_dirs
from clawpilot.runtime.sample_data import sample_progress_events


def _print_settings() -> None:
    settings = load_settings()
    print(json.dumps({
        "temporal": settings.temporal.model_dump(),
        "database": {"url": "<hidden>"},
        "clawloop": {"repo_path": str(settings.clawloop.repo_path)},
        "openclaw": {"workspace": str(settings.openclaw.workspace), "config_path": str(settings.openclaw.config_path)},
        "telegram": {"bot_token": bool(settings.telegram.bot_token), "chat_id": bool(settings.telegram.chat_id), "progress_mode": settings.telegram.progress_mode},
        "log_level": settings.log_level,
        "env": settings.env,
    }, indent=2, sort_keys=True))


def _print_run(name: str, result) -> None:
    print(json.dumps({
        "name": name,
        "command": result.plan.command,
        "cwd": result.plan.cwd,
        "env": {k: result.plan.env[k] for k in ("WORKSPACE", "RUN_ID", "MODE") if k in result.plan.env},
        "result": {
            "return_code": result.result.return_code,
            "stdout": result.result.stdout,
            "stderr": result.result.stderr,
            "dry_run": result.result.dry_run,
            "started_at": result.result.started_at,
            "finished_at": result.result.finished_at,
        },
    }, indent=2, sort_keys=True))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="clawpilot")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("show-config")
    sub.add_parser("check-env")
    sub.add_parser("bootstrap-dev")
    dry = sub.add_parser("dry-run")
    dry_sub = dry.add_subparsers(dest="dry_cmd", required=True)
    for name in ("full-cycle", "smoke", "dashboard", "notify", "manifest"):
        dry_sub.add_parser(name)
    sub.add_parser("sample-progress-jsonl")
    args = parser.parse_args(argv)

    if args.cmd == "show-config":
        _print_settings()
        return 0
    if args.cmd == "check-env":
        return subprocess.call(["sh", "scripts/check-env.sh"])
    if args.cmd == "bootstrap-dev":
        print(json.dumps(ensure_local_runtime_dirs(), indent=2, sort_keys=True))
        return 0
    if args.cmd == "sample-progress-jsonl":
        print(events_to_jsonl(sample_progress_events()))
        return 0

    if args.cmd == "dry-run":
        if args.dry_cmd == "full-cycle":
            _print_run("full-cycle", run_full_cycle(dry_run=True))
        elif args.dry_cmd == "smoke":
            _print_run("smoke", run_smoke(dry_run=True))
        elif args.dry_cmd == "dashboard":
            _print_run("dashboard", run_dashboard(dry_run=True))
        elif args.dry_cmd == "notify":
            _print_run("notify", run_notify(dry_run=True))
        elif args.dry_cmd == "manifest":
            _print_run("manifest", run_manifest(dry_run=True))
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
