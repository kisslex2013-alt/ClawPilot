from __future__ import annotations

import json

from clawpilot.models.progress import ProgressEvent


def event_to_json(event: ProgressEvent) -> str:
    return event.model_dump_json()


def event_from_json(raw: str) -> ProgressEvent:
    return ProgressEvent.model_validate_json(raw)


def events_to_jsonl(events: list[ProgressEvent]) -> str:
    return "\n".join(event_to_json(event) for event in events)


def events_from_jsonl(raw: str) -> list[ProgressEvent]:
    items: list[ProgressEvent] = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        items.append(ProgressEvent.model_validate_json(line))
    return items
