from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Any

from clawpilot.activities.runner import CommandResult, run_command
from clawpilot.config import AppSettings, load_settings


@dataclass(frozen=True)
class ClawLoopRunInput:
    run_id: str
    mode: str
    dry_run: bool = True


@dataclass(frozen=True)
class ClawLoopRunPlan:
    command: list[str]
    cwd: str
    env: dict[str, str]
    dry_run: bool = True


@dataclass(frozen=True)
class ClawLoopRunResult:
    plan: ClawLoopRunPlan
    result: CommandResult


def _base_env(settings: AppSettings, run_id: str | None, mode: str | None) -> dict[str, str]:
    env = dict(os.environ)
    env.update(
        {
            "CLAWPILOT_ENV": settings.env,
            "CLAWPILOT_LOG_LEVEL": settings.log_level,
            "OPENCLAW_WORKSPACE": str(settings.openclaw.workspace),
            "CLAWLOOP_REPO_PATH": str(settings.clawloop.repo_path),
            "WORKSPACE": str(settings.openclaw.workspace),
        }
    )
    if run_id:
        env["RUN_ID"] = run_id
    if mode:
        env["MODE"] = mode
    return env


def _plan(settings: AppSettings, command: list[str], *, run_id: str | None, mode: str, dry_run: bool) -> ClawLoopRunPlan:
    return ClawLoopRunPlan(command=command, cwd=str(settings.clawloop.repo_path), env=_base_env(settings, run_id, mode), dry_run=dry_run)


def prepare_full_cycle_run(*, settings: AppSettings | None = None, run_id: str | None = None, dry_run: bool = True) -> ClawLoopRunPlan:
    settings = settings or load_settings()
    return _plan(settings, ["bash", "scripts/agent_eval_full_cycle.sh"], run_id=run_id, mode="full-cycle", dry_run=dry_run)


def prepare_smoke_run(*, settings: AppSettings | None = None, run_id: str | None = None, dry_run: bool = True) -> ClawLoopRunPlan:
    settings = settings or load_settings()
    return _plan(settings, ["bash", "scripts/agent_eval_full_cycle.sh", "--smoke"], run_id=run_id, mode="smoke", dry_run=dry_run)


def prepare_dashboard_run(*, settings: AppSettings | None = None, run_id: str | None = None, dry_run: bool = True) -> ClawLoopRunPlan:
    settings = settings or load_settings()
    return _plan(settings, ["python3", "scripts/agent_eval_dashboard.py"], run_id=run_id, mode="dashboard", dry_run=dry_run)


def prepare_notify_run(*, settings: AppSettings | None = None, run_id: str | None = None, dry_run: bool = True) -> ClawLoopRunPlan:
    settings = settings or load_settings()
    return _plan(settings, ["python3", "scripts/agent_eval_notify.py"], run_id=run_id, mode="notify", dry_run=dry_run)


def prepare_manifest_run(*, settings: AppSettings | None = None, run_id: str | None = None, dry_run: bool = True) -> ClawLoopRunPlan:
    settings = settings or load_settings()
    return _plan(settings, ["python3", "scripts/write_agent_eval_manifest.py"], run_id=run_id, mode="manifest", dry_run=dry_run)


def build_full_cycle_command(*, settings: AppSettings | None = None, run_id: str | None = None, dry_run: bool = True) -> ClawLoopRunPlan:
    return prepare_full_cycle_run(settings=settings, run_id=run_id, dry_run=dry_run)


def build_smoke_command(*, settings: AppSettings | None = None, run_id: str | None = None, dry_run: bool = True) -> ClawLoopRunPlan:
    return prepare_smoke_run(settings=settings, run_id=run_id, dry_run=dry_run)


def build_dashboard_command(*, settings: AppSettings | None = None, run_id: str | None = None, dry_run: bool = True) -> ClawLoopRunPlan:
    return prepare_dashboard_run(settings=settings, run_id=run_id, dry_run=dry_run)


def build_notify_command(*, settings: AppSettings | None = None, run_id: str | None = None, dry_run: bool = True) -> ClawLoopRunPlan:
    return prepare_notify_run(settings=settings, run_id=run_id, dry_run=dry_run)


def build_manifest_command(*, settings: AppSettings | None = None, run_id: str | None = None, dry_run: bool = True) -> ClawLoopRunPlan:
    return prepare_manifest_run(settings=settings, run_id=run_id, dry_run=dry_run)


def _run(plan: ClawLoopRunPlan, timeout: float | None = None) -> ClawLoopRunResult:
    result = run_command(plan.command, cwd=plan.cwd, env=plan.env, dry_run=plan.dry_run, timeout=timeout)
    return ClawLoopRunResult(plan=plan, result=result)


def run_full_cycle(*, settings: AppSettings | None = None, run_id: str | None = None, dry_run: bool = True, timeout: float | None = None) -> ClawLoopRunResult:
    return _run(prepare_full_cycle_run(settings=settings, run_id=run_id, dry_run=dry_run), timeout=timeout)


def run_smoke(*, settings: AppSettings | None = None, run_id: str | None = None, dry_run: bool = True, timeout: float | None = None) -> ClawLoopRunResult:
    return _run(prepare_smoke_run(settings=settings, run_id=run_id, dry_run=dry_run), timeout=timeout)


def run_dashboard(*, settings: AppSettings | None = None, run_id: str | None = None, dry_run: bool = True, timeout: float | None = None) -> ClawLoopRunResult:
    return _run(prepare_dashboard_run(settings=settings, run_id=run_id, dry_run=dry_run), timeout=timeout)


def run_notify(*, settings: AppSettings | None = None, run_id: str | None = None, dry_run: bool = True, timeout: float | None = None) -> ClawLoopRunResult:
    return _run(prepare_notify_run(settings=settings, run_id=run_id, dry_run=dry_run), timeout=timeout)


def run_manifest(*, settings: AppSettings | None = None, run_id: str | None = None, dry_run: bool = True, timeout: float | None = None) -> ClawLoopRunResult:
    return _run(prepare_manifest_run(settings=settings, run_id=run_id, dry_run=dry_run), timeout=timeout)
