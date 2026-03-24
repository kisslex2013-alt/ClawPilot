from __future__ import annotations

from dataclasses import dataclass

from clawpilot.config import AppSettings, load_settings


@dataclass(frozen=True)
class OpenClawRoutingTarget:
    workspace_path: str
    channel_name: str
    preview_only: bool


def build_openclaw_routing_target(settings: AppSettings | None = None) -> OpenClawRoutingTarget:
    settings = settings or load_settings()
    return OpenClawRoutingTarget(
        workspace_path=settings.openclaw_workspace_path or str(settings.openclaw.workspace),
        channel_name=settings.openclaw_channel_name or "default",
        preview_only=settings.openclaw_routing_preview_only,
    )


def describe_openclaw_routing_target(settings: AppSettings | None = None) -> dict[str, object]:
    target = build_openclaw_routing_target(settings)
    return {"workspace_path": target.workspace_path, "channel_name": target.channel_name, "preview_only": target.preview_only}


def preview_openclaw_route(message: object, settings: AppSettings | None = None) -> dict[str, object]:
    target = describe_openclaw_routing_target(settings)
    return {"implemented": False, "preview_only": True, "target": target, "message_kind": getattr(message, "kind", "unknown")}


def maybe_send_via_openclaw_routing(message: object, settings: AppSettings | None = None, *, preview_mode: bool = True) -> dict[str, object]:
    if preview_mode:
        return preview_openclaw_route(message, settings)
    return {"implemented": False, "preview_only": True, "error": "not implemented; preview only in this pack"}
