from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from clawpilot.config import AppSettings, load_settings


@dataclass(frozen=True)
class ClawLoopCommand:
    command: list[str]
    cwd: Path
    env: dict[str, str] = field(default_factory=dict)
    dry_run: bool = True


@dataclass(frozen=True)
class ClawLoopCommandResult:
    command: list[str]
    cwd: str
    env: dict[str, str]
    dry_run: bool


def _base_env(settings: AppSettings, run_id: str | None, mode: str | None) -> dict[str, str]:
    env = {
        "CLAWPILOT_ENV": settings.env,
        "CLAWPILOT_LOG_LEVEL": settings.log_level,
        "OPENCLAW_WORKSPACE": str(settings.openclaw.workspace),
        "CLAWLOOP_REPO_PATH": str(settings.clawloop.repo_path),
    }
    if run_id:
        env["RUN_ID"] = run_id
    if mode:
        env["MODE"] = mode
    return env


def build_full_cycle_command(*, settings: AppSettings | None = None, run_id: str | None = None, mode: str = "full-cycle", dry_run: bool = True) -> ClawLoopCommand:
    settings = settings or load_settings()
    return ClawLoopCommand(
        command=["bash", "scripts/agent_eval_full_cycle.sh"],
        cwd=settings.clawloop.repo_path,
        env=_base_env(settings, run_id, mode),
        dry_run=dry_run,
    )


def build_smoke_command(*, settings: AppSettings | None = None, run_id: str | None = None, mode: str = "smoke", dry_run: bool = True) -> ClawLoopCommand:
    settings = settings or load_settings()
    return ClawLoopCommand(
        command=["bash", "scripts/agent_eval_full_cycle.sh", "--smoke"],
        cwd=settings.clawloop.repo_path,
        env=_base_env(settings, run_id, mode),
        dry_run=dry_run,
    )


def build_dashboard_command(*, settings: AppSettings | None = None, run_id: str | None = None, mode: str = "dashboard", dry_run: bool = True) -> ClawLoopCommand:
    settings = settings or load_settings()
    return ClawLoopCommand(
        command=["python3", "scripts/agent_eval_dashboard.py"],
        cwd=settings.clawloop.repo_path,
        env=_base_env(settings, run_id, mode),
        dry_run=dry_run,
    )


def build_notify_command(*, settings: AppSettings | None = None, run_id: str | None = None, mode: str = "notify", dry_run: bool = True) -> ClawLoopCommand:
    settings = settings or load_settings()
    return ClawLoopCommand(
        command=["python3", "scripts/agent_eval_notify.py"],
        cwd=settings.clawloop.repo_path,
        env=_base_env(settings, run_id, mode),
        dry_run=dry_run,
    )


def build_manifest_command(*, settings: AppSettings | None = None, run_id: str | None = None, mode: str = "manifest", dry_run: bool = True) -> ClawLoopCommand:
    settings = settings or load_settings()
    return ClawLoopCommand(
        command=["python3", "scripts/write_agent_eval_manifest.py"],
        cwd=settings.clawloop.repo_path,
        env=_base_env(settings, run_id, mode),
        dry_run=dry_run,
    )
