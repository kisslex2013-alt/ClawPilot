from __future__ import annotations

from clawpilot.activities.runner import run_command


def test_run_command_dry_run():
    result = run_command(["echo", "hello"], cwd="/tmp", dry_run=True)
    assert result.dry_run is True
    assert result.return_code == 0
    assert result.command == ["echo", "hello"]
