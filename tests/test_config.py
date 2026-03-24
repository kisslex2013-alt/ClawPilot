from __future__ import annotations

from clawpilot.config import load_settings


def test_load_settings_from_env(monkeypatch):
    monkeypatch.setenv("TEMPORAL_NAMESPACE", "ns")
    monkeypatch.setenv("TEMPORAL_TASK_QUEUE", "q")
    monkeypatch.setenv("TEMPORAL_ADDRESS", "addr")
    monkeypatch.setenv("DATABASE_URL", "postgresql://x")
    monkeypatch.setenv("CLAWLOOP_REPO_PATH", "/tmp/clawloop")
    monkeypatch.setenv("OPENCLAW_WORKSPACE", "/tmp/workspace")
    monkeypatch.setenv("OPENCLAW_CONFIG_PATH", "/tmp/openclaw.json")
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "chat")
    monkeypatch.setenv("TELEGRAM_PROGRESS_MODE", "quiet")
    monkeypatch.setenv("CLAWPILOT_LOG_LEVEL", "debug")
    monkeypatch.setenv("CLAWPILOT_ENV", "production")

    settings = load_settings()

    assert settings.temporal.namespace == "ns"
    assert settings.temporal.task_queue == "q"
    assert settings.database.url == "postgresql://x"
    assert settings.clawloop.repo_path.as_posix() == "/tmp/clawloop"
    assert settings.openclaw.workspace.as_posix() == "/tmp/workspace"
    assert settings.telegram.progress_mode == "quiet"
    assert settings.log_level == "debug"
    assert settings.env == "production"


def test_load_settings_defaults(monkeypatch):
    for key in [
        "TEMPORAL_NAMESPACE",
        "TEMPORAL_TASK_QUEUE",
        "TEMPORAL_ADDRESS",
        "DATABASE_URL",
        "CLAWLOOP_REPO_PATH",
        "OPENCLAW_WORKSPACE",
        "OPENCLAW_CONFIG_PATH",
        "TELEGRAM_BOT_TOKEN",
        "TELEGRAM_CHAT_ID",
        "TELEGRAM_PROGRESS_MODE",
        "CLAWPILOT_LOG_LEVEL",
        "CLAWPILOT_ENV",
    ]:
        monkeypatch.delenv(key, raising=False)

    settings = load_settings()
    assert settings.temporal.namespace == "clawpilot"
    assert settings.telegram.progress_mode == "normal"


def test_basic_validation():
    settings = load_settings()
    assert settings.temporal.address
    assert settings.database.url
