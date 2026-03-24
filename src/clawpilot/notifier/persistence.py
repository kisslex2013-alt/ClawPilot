from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


def build_notification_log_path(base_dir: str = ".") -> str:
    return str(Path(base_dir) / ".clawpilot" / "notifications" / "notifications.jsonl")


def persist_rendered_message(*, base_dir: str, message: object) -> str:
    path = Path(build_notification_log_path(base_dir))
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = message.model_dump() if hasattr(message, "model_dump") else dict(message)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"ts": datetime.now(timezone.utc).isoformat(), "message": payload}, ensure_ascii=False, sort_keys=True) + "\n")
    return str(path)


def persist_send_attempt(*, base_dir: str, payload: dict) -> str:
    path = Path(base_dir) / ".clawpilot" / "notifications" / "send-attempts.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"ts": datetime.now(timezone.utc).isoformat(), **payload}, ensure_ascii=False, sort_keys=True) + "\n")
    return str(path)


def persist_send_result(*, base_dir: str, result: object) -> str:
    path = Path(base_dir) / ".clawpilot" / "notifications" / "send-results.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = result.__dict__ if hasattr(result, "__dict__") else dict(result)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"ts": datetime.now(timezone.utc).isoformat(), **payload}, ensure_ascii=False, sort_keys=True) + "\n")
    return str(path)


def load_recent_notification_log(*, base_dir: str = ".", limit: int = 10) -> list[dict[str, object]]:
    path = Path(build_notification_log_path(base_dir))
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").splitlines()[-limit:]
    return [json.loads(line) for line in lines if line.strip()]
