from __future__ import annotations

import os
from pathlib import Path

from pydantic import BaseModel, Field, field_validator


class TemporalSettings(BaseModel):
    namespace: str = "clawpilot"
    task_queue: str = "clawpilot-main"
    address: str = "localhost:7233"


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
    log_level: str = "info"
    env: str = "development"

    @field_validator("log_level", "env")
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
        log_level=os.getenv("CLAWPILOT_LOG_LEVEL", "info"),
        env=os.getenv("CLAWPILOT_ENV", "development"),
    )
