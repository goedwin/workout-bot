"""
Edwin 운동봇 — 매일 아침 텔레그램으로 오늘 운동 전송

사용법:
    python bot.py            # 오늘 운동 전송
    python bot.py monday     # 특정 요일 운동 전송 (테스트용)

환경변수 (.env):
    TELEGRAM_BOT_TOKEN — @BotFather에서 받은 토큰
    TELEGRAM_CHAT_ID   — 본인 chat id (@userinfobot에 메시지 보내면 알려줌)
"""

import os
import sys
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

from workouts import get_workout

load_dotenv(Path(__file__).parent / ".env")

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

DAY_NAMES = [
    "monday", "tuesday", "wednesday", "thursday",
    "friday", "saturday", "sunday",
]


def send_telegram(text: str) -> None:
    if not BOT_TOKEN or not CHAT_ID:
        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN과 TELEGRAM_CHAT_ID를 .env에 설정해주세요."
        )

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    resp = requests.post(
        url,
        data={"chat_id": CHAT_ID, "text": text},
        timeout=10,
    )
    resp.raise_for_status()


def main() -> None:
    if len(sys.argv) > 1:
        day = sys.argv[1].lower()
        if day not in DAY_NAMES:
            print(f"요일은 {DAY_NAMES} 중 하나여야 함")
            sys.exit(1)
    else:
        day = DAY_NAMES[datetime.now().weekday()]

    message = get_workout(day)
    print(message)
    print()

    if BOT_TOKEN and CHAT_ID:
        send_telegram(message)
        print("✅ 텔레그램 전송 완료")
    else:
        print("⚠️  .env 미설정 — 텔레그램 전송 SKIP (콘솔만 출력)")


if __name__ == "__main__":
    main()
