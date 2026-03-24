from __future__ import annotations

from pathlib import Path


def ensure_local_runtime_dirs(base: str = ".clawpilot") -> dict[str, str]:
    root = Path(base)
    logs = root / "logs"
    runs = root / "runs"
    tmp = root / "tmp"
    root.mkdir(parents=True, exist_ok=True)
    logs.mkdir(parents=True, exist_ok=True)
    runs.mkdir(parents=True, exist_ok=True)
    tmp.mkdir(parents=True, exist_ok=True)
    return {"base": str(root), "logs": str(logs), "runs": str(runs), "tmp": str(tmp)}


def get_progress_log_path(base: str = ".clawpilot") -> str:
    return str(Path(base) / "logs" / "progress.jsonl")


def get_runs_dir(base: str = ".clawpilot") -> str:
    return str(Path(base) / "runs")
