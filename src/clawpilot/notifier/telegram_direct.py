from __future__ import annotations

from dataclasses import dataclass
from urllib import error, parse, request

from clawpilot.config import AppSettings, load_settings


@dataclass(frozen=True)
class TelegramTarget:
    api_base: str
    bot_token: str
    chat_id: str
    timeout_seconds: float


def build_telegram_target(settings: AppSettings | None = None) -> TelegramTarget:
    settings = settings or load_settings()
    return TelegramTarget(api_base=settings.telegram_api_base, bot_token=settings.telegram_bot_token, chat_id=settings.telegram_chat_id, timeout_seconds=settings.telegram_send_timeout_seconds)


def describe_telegram_target(settings: AppSettings | None = None) -> dict[str, object]:
    target = build_telegram_target(settings)
    return {"api_base": target.api_base, "chat_id": target.chat_id, "bot_token": bool(target.bot_token), "timeout_seconds": target.timeout_seconds, "target": f"{target.api_base}/bot<redacted>/sendMessage"}


def send_telegram_message(*, target: TelegramTarget, text: str, parse_mode: str | None = None) -> dict[str, object]:
    if not target.bot_token or not target.chat_id:
        return {"attempted": True, "delivered": False, "error": "missing token or chat_id", "target_summary": describe_telegram_target()}
    url = f"{target.api_base.rstrip('/')}/bot{target.bot_token}/sendMessage"
    payload = {"chat_id": target.chat_id, "text": text}
    if parse_mode:
        payload["parse_mode"] = parse_mode
    data = parse.urlencode(payload).encode("utf-8")
    req = request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with request.urlopen(req, timeout=target.timeout_seconds) as resp:  # nosec B310
            body = resp.read().decode("utf-8", errors="replace")
            return {"attempted": True, "delivered": True, "status": resp.status, "body": body, "target_summary": describe_telegram_target()}
    except error.URLError as exc:
        return {"attempted": True, "delivered": False, "error": str(exc), "target_summary": describe_telegram_target()}
