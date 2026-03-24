from __future__ import annotations

import subprocess
import sys


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, "-m", "clawpilot.cli", *args], capture_output=True, text=True, check=True)


def test_show_config():
    result = _run("show-config")
    assert "temporal" in result.stdout


def test_sample_progress_jsonl():
    result = _run("sample-progress-jsonl")
    assert "task_accepted" in result.stdout


def test_dry_run_smoke():
    result = _run("dry-run", "smoke")
    assert "DRY-RUN" in result.stdout
