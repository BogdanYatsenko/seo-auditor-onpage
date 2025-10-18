import os, requests

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
MANAGER_CHAT_ID = os.getenv('MANAGER_CHAT_ID', '')

def notify_manager(text: str) -> None:
    if not BOT_TOKEN or not MANAGER_CHAT_ID:
        return
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": int(MANAGER_CHAT_ID), "text": text, "parse_mode": "HTML"},
            timeout=10,
        )
    except Exception:
        pass
