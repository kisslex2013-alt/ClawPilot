from __future__ import annotations

from clawpilot.runtime.paths import ensure_local_runtime_dirs, get_progress_log_path, get_runs_dir


def test_runtime_dirs(tmp_path):
    base = tmp_path / ".clawpilot"
    paths = ensure_local_runtime_dirs(str(base))
    assert base.exists()
    assert (base / "logs").exists()
    assert (base / "runs").exists()
    assert (base / "tmp").exists()
    assert paths["base"] == str(base)
    assert get_runs_dir(str(base)).endswith("runs")
    assert get_progress_log_path(str(base)).endswith("progress.jsonl")
