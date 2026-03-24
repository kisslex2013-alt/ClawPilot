from __future__ import annotations

from clawpilot.activities.clawloop import (
    build_dashboard_command,
    build_full_cycle_command,
    build_manifest_command,
    build_notify_command,
    build_smoke_command,
)
from clawpilot.config import load_settings


def test_build_full_cycle_command():
    cmd = build_full_cycle_command(settings=load_settings(), run_id="run1")
    assert cmd.command[:2] == ["bash", "scripts/agent_eval_full_cycle.sh"]
    assert cmd.env["RUN_ID"] == "run1"


def test_build_smoke_command():
    cmd = build_smoke_command(settings=load_settings(), run_id="run1")
    assert cmd.command[-1] == "--smoke"


def test_build_dashboard_command():
    cmd = build_dashboard_command(settings=load_settings(), run_id="run1")
    assert cmd.command[0] == "python3"
    assert "dashboard" in cmd.env["MODE"]


def test_build_notify_command():
    cmd = build_notify_command(settings=load_settings(), run_id="run1")
    assert cmd.command[1] == "scripts/agent_eval_notify.py"


def test_build_manifest_command():
    cmd = build_manifest_command(settings=load_settings(), run_id="run1")
    assert cmd.command[1] == "scripts/write_agent_eval_manifest.py"
