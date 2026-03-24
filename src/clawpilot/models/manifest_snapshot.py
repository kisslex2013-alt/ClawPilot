from __future__ import annotations

from pydantic import BaseModel


class VerdictCounts(BaseModel):
    pass_count: int
    retry: int
    escalation: int


class ManifestArtifacts(BaseModel):
    latest_report: str | None = None
    latest_delta: str | None = None
    dashboard: str | None = None
    weekly_report: str | None = None
    disagreements: str | None = None
    manifest_path: str | None = None


class ManifestSnapshot(BaseModel):
    run_id: str
    mode: str
    workspace: str
    git_commit: str
    git_dirty: bool
    config_hash: str
    judge_stack: list[str]
    artifacts: ManifestArtifacts
    verdict_counts: VerdictCounts
    generated_at: str
