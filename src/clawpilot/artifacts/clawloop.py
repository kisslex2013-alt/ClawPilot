from __future__ import annotations

from pathlib import Path

from clawpilot.artifacts.contracts import ArtifactCollection, ArtifactKind, ArtifactRef

_KNOWN = {
    ArtifactKind.latest_report: "reference/agent-eval/latest-report.md",
    ArtifactKind.latest_delta: "reference/agent-eval/latest-delta.md",
    ArtifactKind.dashboard: "reference/agent-eval/dashboard.md",
    ArtifactKind.weekly_report: "reference/agent-eval/weekly-review-report.md",
    ArtifactKind.disagreements: "reference/agent-eval/judge-disagreements.md",
}


def detect_known_artifacts(base_path: str, run_id: str | None = None) -> ArtifactCollection:
    base = Path(base_path)
    items: list[ArtifactRef] = []
    for kind, rel in _KNOWN.items():
        path = base / rel
        items.append(ArtifactRef(kind=kind, path=str(path), source="clawloop", exists=path.exists(), run_id=run_id))
    if run_id:
        manifest = base / ".clawpilot" / "runs" / run_id / "manifest.json"
        if not manifest.exists():
            manifest = base / "reference/agent-eval/runs" / run_id / "manifest.json"
        items.append(ArtifactRef(kind=ArtifactKind.manifest, path=str(manifest), source="clawloop", exists=manifest.exists(), run_id=run_id))
    return ArtifactCollection(items=items)


def build_clawloop_artifact_refs(*, base_path: str, run_id: str | None = None) -> list[ArtifactRef]:
    return detect_known_artifacts(base_path, run_id=run_id).items


def summarize_artifact_collection(collection: ArtifactCollection) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in collection.items:
        counts[item.kind.value] = counts.get(item.kind.value, 0) + 1
    return counts
