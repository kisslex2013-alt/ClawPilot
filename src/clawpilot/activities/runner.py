from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import subprocess
from typing import Sequence


@dataclass(frozen=True)
class CommandResult:
    command: list[str]
    cwd: str
    return_code: int
    stdout: str
    stderr: str
    dry_run: bool
    started_at: str
    finished_at: str


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def run_command(
    command: Sequence[str],
    *,
    cwd: str,
    env: dict[str, str] | None = None,
    dry_run: bool = True,
    timeout: float | None = None,
    check: bool = False,
) -> CommandResult:
    started_at = _now()
    if dry_run:
        finished_at = _now()
        return CommandResult(
            command=list(command),
            cwd=cwd,
            return_code=0,
            stdout="DRY-RUN: command not executed\n",
            stderr="",
            dry_run=True,
            started_at=started_at,
            finished_at=finished_at,
        )

    proc = subprocess.run(  # nosec B603
        list(command),
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=check,
    )
    finished_at = _now()
    return CommandResult(
        command=list(command),
        cwd=cwd,
        return_code=proc.returncode,
        stdout=proc.stdout,
        stderr=proc.stderr,
        dry_run=False,
        started_at=started_at,
        finished_at=finished_at,
    )
