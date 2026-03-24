from __future__ import annotations

import os
from pathlib import Path

from pydantic import BaseModel, Field, field_validator


class TemporalSettings(BaseModel):
    namespace: str = "clawpilot"
    task_queue: str = "clawpilot-main"
    address: str = "localhost:7233"
    enable_tls: bool = False
    connect_timeout_seconds: float = 5.0
    worker_identity: str | None = None
    dev_connect_enabled: bool = False


class DatabaseSettings(BaseModel):
    url: str = "postgresql://clawpilot:clawpilot@localhost:5432/clawpilot"


class ClawLoopSettings(BaseModel):
    repo_path: Path = Path("/root/clawloop")

    @field_validator("repo_path")
    @classmethod
    def validate_repo_path(cls, value: Path) -> Path:
        if not value.as_posix().strip():
            raise ValueError("repo_path must not be empty")
        return value


class OpenClawSettings(BaseModel):
    workspace: Path = Path("/root/.openclaw/workspace")
    config_path: Path = Path("/root/.openclaw/openclaw.json")

    @field_validator("workspace", "config_path")
    @classmethod
    def validate_path(cls, value: Path) -> Path:
        if not value.as_posix().strip():
            raise ValueError("path must not be empty")
        return value


class TelegramSettings(BaseModel):
    bot_token: str = ""
    chat_id: str = ""
    progress_mode: str = "normal"


class AppSettings(BaseModel):
    temporal: TemporalSettings = Field(default_factory=TemporalSettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    clawloop: ClawLoopSettings = Field(default_factory=ClawLoopSettings)
    openclaw: OpenClawSettings = Field(default_factory=OpenClawSettings)
    telegram: TelegramSettings = Field(default_factory=TelegramSettings)
    notification_transport_mode: str = "dry_run"
    notification_log_dir: str = ".clawpilot/notifications"
    telegram_transport_enabled: bool = False
    telegram_bot_token: str = ""
    telegram_chat_id: str = ""
    telegram_api_base: str = "https://api.telegram.org"
    telegram_send_timeout_seconds: float = 5.0
    telegram_live_send_enabled: bool = False
    notification_route_mode: str | None = None
    prefer_openclaw_routing: bool = False
    openclaw_routing_enabled: bool = False
    openclaw_workspace_path: str | None = None
    openclaw_channel_name: str | None = None
    openclaw_routing_preview_only: bool = True
    log_level: str = "info"
    env: str = "development"

    @field_validator("log_level", "env", "notification_transport_mode", "telegram_api_base")
    @classmethod
    def validate_non_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("value must not be empty")
        return value


def load_settings() -> AppSettings:
    return AppSettings(
        temporal=TemporalSettings(
            namespace=os.getenv("TEMPORAL_NAMESPACE", "clawpilot"),
            task_queue=os.getenv("TEMPORAL_TASK_QUEUE", "clawpilot-main"),
            address=os.getenv("TEMPORAL_ADDRESS", "localhost:7233"),
            enable_tls=os.getenv("TEMPORAL_ENABLE_TLS", "false").lower() in {"1", "true", "yes", "on"},
            connect_timeout_seconds=float(os.getenv("TEMPORAL_CONNECT_TIMEOUT_SECONDS", "5.0")),
            worker_identity=os.getenv("TEMPORAL_WORKER_IDENTITY") or None,
            dev_connect_enabled=os.getenv("TEMPORAL_DEV_CONNECT_ENABLED", "false").lower() in {"1", "true", "yes", "on"},
        ),
        database=DatabaseSettings(url=os.getenv("DATABASE_URL", "postgresql://clawpilot:clawpilot@localhost:5432/clawpilot")),
        clawloop=ClawLoopSettings(repo_path=Path(os.getenv("CLAWLOOP_REPO_PATH", "/root/clawloop"))),
        openclaw=OpenClawSettings(
            workspace=Path(os.getenv("OPENCLAW_WORKSPACE", "/root/.openclaw/workspace")),
            config_path=Path(os.getenv("OPENCLAW_CONFIG_PATH", "/root/.openclaw/openclaw.json")),
        ),
        telegram=TelegramSettings(
            bot_token=os.getenv("TELEGRAM_BOT_TOKEN", ""),
            chat_id=os.getenv("TELEGRAM_CHAT_ID", ""),
            progress_mode=os.getenv("TELEGRAM_PROGRESS_MODE", "normal"),
        ),
        notification_transport_mode=os.getenv("NOTIFICATION_TRANSPORT_MODE", "dry_run"),
        notification_log_dir=os.getenv("NOTIFICATION_LOG_DIR", ".clawpilot/notifications"),
        telegram_transport_enabled=os.getenv("TELEGRAM_TRANSPORT_ENABLED", "false").lower() in {"1", "true", "yes", "on"},
        telegram_bot_token=os.getenv("TELEGRAM_BOT_TOKEN", ""),
        telegram_chat_id=os.getenv("TELEGRAM_CHAT_ID", ""),
        telegram_api_base=os.getenv("TELEGRAM_API_BASE", "https://api.telegram.org"),
        telegram_send_timeout_seconds=float(os.getenv("TELEGRAM_SEND_TIMEOUT_SECONDS", "5.0")),
        telegram_live_send_enabled=os.getenv("TELEGRAM_LIVE_SEND_ENABLED", "false").lower() in {"1", "true", "yes", "on"},
        notification_route_mode=os.getenv("NOTIFICATION_ROUTE_MODE") or None,
        prefer_openclaw_routing=os.getenv("PREFER_OPENCLAW_ROUTING", "false").lower() in {"1", "true", "yes", "on"},
        openclaw_routing_enabled=os.getenv("OPENCLAW_ROUTING_ENABLED", "false").lower() in {"1", "true", "yes", "on"},
        openclaw_workspace_path=os.getenv("OPENCLAW_WORKSPACE_PATH") or None,
        openclaw_channel_name=os.getenv("OPENCLAW_CHANNEL_NAME") or None,
        openclaw_routing_preview_only=os.getenv("OPENCLAW_ROUTING_PREVIEW_ONLY", "true").lower() in {"1", "true", "yes", "on"},
        log_level=os.getenv("CLAWPILOT_LOG_LEVEL", "info"),
        env=os.getenv("CLAWPILOT_ENV", "development"),
    )
