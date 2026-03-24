from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from clawpilot.models.progress import ProgressEvent


def _run_dir(base: str, run_id: str) -> Path:
    return Path(base) / ".clawpilot" / "runs" / run_id


def progress_jsonl_path(base: str, run_id: str) -> Path:
    return _run_dir(base, run_id) / "progress.jsonl"


def summary_json_path(base: str, run_id: str) -> Path:
    return _run_dir(base, run_id) / "run-summary.json"


def command_result_json_path(base: str, run_id: str) -> Path:
    return _run_dir(base, run_id) / "command-result.json"


def write_progress_events_jsonl(*, base: str, run_id: str, events: Iterable[ProgressEvent]) -> str:
    path = progress_jsonl_path(base, run_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(event.model_dump_json() for event in events) + "\n", encoding="utf-8")
    return str(path)


def write_run_summary_json(*, base: str, run_id: str, summary: dict) -> str:
    path = summary_json_path(base, run_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    return str(path)


def write_command_result_json(*, base: str, run_id: str, result: dict) -> str:
    path = command_result_json_path(base, run_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    return str(path)
