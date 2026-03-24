from __future__ import annotations

from clawpilot.execution.persistence import write_command_result_json, write_progress_events_jsonl, write_run_summary_json
from clawpilot.runtime.sample_data import sample_progress_events


def test_persistence(tmp_path):
    base = str(tmp_path)
    run_id = "r1"
    progress = write_progress_events_jsonl(base=base, run_id=run_id, events=sample_progress_events())
    summary = write_run_summary_json(base=base, run_id=run_id, summary={"run_id": run_id})
    command = write_command_result_json(base=base, run_id=run_id, result={"ok": True})
    assert progress.endswith("progress.jsonl")
    assert summary.endswith("run-summary.json")
    assert command.endswith("command-result.json")
