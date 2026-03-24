from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path


def check_path_exists(path: str | Path) -> bool:
    return Path(path).exists()


def check_command_available(cmd: str) -> bool:
    return shutil.which(cmd) is not None


@dataclass(frozen=True)
class EnvironmentSummary:
    path_exists: bool
    command_available: bool
    workspace: str | None = None
    mode: str | None = None


def summarize_environment(*, path: str | Path, command: str, workspace: str | None = None, mode: str | None = None) -> EnvironmentSummary:
    return EnvironmentSummary(
        path_exists=check_path_exists(path),
        command_available=check_command_available(command),
        workspace=workspace,
        mode=mode,
    )
