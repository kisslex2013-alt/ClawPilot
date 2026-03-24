from __future__ import annotations

from dataclasses import dataclass

from clawpilot.config import AppSettings, load_settings
from clawpilot.notifier.transport import SenderMode


@dataclass(frozen=True)
class NotificationRoute:
    mode: SenderMode
    reason: str


@dataclass(frozen=True)
class NotificationRouteDecision:
    selected: NotificationRoute
    available: list[str]
    explicit: bool


def choose_sender_mode(settings: AppSettings | None = None, *, override: str | None = None) -> SenderMode:
    settings = settings or load_settings()
    if override:
        return SenderMode(override)
    if settings.notification_route_mode:
        return SenderMode(settings.notification_route_mode)
    if settings.notification_transport_mode:
        return SenderMode(settings.notification_transport_mode)
    if settings.prefer_openclaw_routing and settings.openclaw_routing_enabled:
        return SenderMode.openclaw_routing_stub
    return SenderMode.dry_run


def resolve_notification_route(settings: AppSettings | None = None, *, override: str | None = None) -> NotificationRouteDecision:
    settings = settings or load_settings()
    mode = choose_sender_mode(settings, override=override)
    reason = "explicit override" if override else "settings/default"
    return NotificationRouteDecision(selected=NotificationRoute(mode=mode, reason=reason), available=[m.value for m in SenderMode], explicit=bool(override))


def build_notification_route_plan(settings: AppSettings | None = None, *, override: str | None = None) -> dict[str, object]:
    decision = resolve_notification_route(settings, override=override)
    return {"selected": {"mode": decision.selected.mode.value, "reason": decision.selected.reason}, "available": decision.available, "explicit": decision.explicit}


def describe_notification_route(settings: AppSettings | None = None, *, override: str | None = None) -> str:
    plan = build_notification_route_plan(settings, override=override)
    return f"{plan['selected']['mode']} ({plan['selected']['reason']})"
