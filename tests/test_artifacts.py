from __future__ import annotations

from clawpilot.artifacts.clawloop import detect_known_artifacts
from clawpilot.artifacts.contracts import ArtifactKind


def test_detect_artifacts(tmp_path):
    base = tmp_path
    (base / "reference/agent-eval").mkdir(parents=True)
    (base / "reference/agent-eval/dashboard.md").write_text("x")
    collection = detect_known_artifacts(str(base), run_id="r1")
    assert any(item.kind == ArtifactKind.dashboard and item.exists for item in collection.items)
