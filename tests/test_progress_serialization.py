from __future__ import annotations

from clawpilot.models.progress import ProgressEvent, ProgressEventType, ProgressLevel
from clawpilot.progress.serialization import event_from_json, event_to_json, events_from_jsonl, events_to_jsonl


def _event() -> ProgressEvent:
    return ProgressEvent(
        id="1",
        task_id="task",
        workflow_name="wf",
        workflow_run_id="run",
        event_type=ProgressEventType.task_accepted,
        level=ProgressLevel.info,
        phase="phase",
        step_key="step",
        message="hello",
        created_at="2026-03-24T00:00:00Z",
        metadata={"x": 1},
    )


def test_roundtrip_json():
    event = _event()
    raw = event_to_json(event)
    assert event_from_json(raw) == event


def test_roundtrip_jsonl():
    events = [_event(), _event()]
    raw = events_to_jsonl(events)
    assert events_from_jsonl(raw) == events
