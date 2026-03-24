from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class ArtifactKind(str, Enum):
    latest_report = "latest_report"
    latest_delta = "latest_delta"
    dashboard = "dashboard"
    weekly_report = "weekly_report"
    disagreements = "disagreements"
    manifest = "manifest"
    progress_log = "progress_log"
    test_report = "test_report"
    unknown = "unknown"


class ArtifactRef(BaseModel):
    kind: ArtifactKind
    path: str
    source: str
    exists: bool = True
    run_id: str | None = None


class ArtifactSummary(BaseModel):
    kind: ArtifactKind
    path: str
    exists: bool
    source: str
    run_id: str | None = None


class ArtifactCollection(BaseModel):
    items: list[ArtifactRef] = Field(default_factory=list)
