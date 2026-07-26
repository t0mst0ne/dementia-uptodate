"""Send weekly report notifications to a Telegram chat via Bot API.

Requires environment variables:
- TELEGRAM_BOT_TOKEN: token from @BotFather
- TELEGRAM_CHAT_ID: target chat/channel/group ID

If either is missing the notification is skipped (no error), so local runs
and forks without credentials keep working.
"""

import os

import httpx

TELEGRAM_API = "https://api.telegram.org/bot{token}/sendMessage"


def is_configured() -> bool:
    return bool(os.environ.get("TELEGRAM_BOT_TOKEN") and os.environ.get("TELEGRAM_CHAT_ID"))


def send_message(text: str) -> bool:
    """Send a Markdown-formatted message. Returns True on success."""
    if not is_configured():
        return False
    resp = httpx.post(
        TELEGRAM_API.format(token=os.environ["TELEGRAM_BOT_TOKEN"]),
        json={
            "chat_id": os.environ["TELEGRAM_CHAT_ID"],
            "text": text,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True,
        },
        timeout=15,
    )
    resp.raise_for_status()
    return True
