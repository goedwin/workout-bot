"""
Edwin 운동 스케줄 로더

데이터 단일 소스: workouts.json (웹앱 index.html 과 공유)
스케줄을 바꾸려면 workouts.json 만 수정하면 봇/웹 둘 다 반영됨.
"""

import json
from pathlib import Path

_data = json.loads(
    (Path(__file__).parent / "workouts.json").read_text(encoding="utf-8")
)

WORKOUTS = _data["days"]

# 매일 끝에 붙는 식단/생활 리마인더 (workouts.json 의 daily_reminder 로 구성)
_reminder_lines = "\n".join(f"• {item}" for item in _data["daily_reminder"])
DAILY_REMINDER = (
    "\n━━━━━━━━━━━━━━━━━━━\n"
    "🥗 오늘 식단/생활 체크\n"
    "━━━━━━━━━━━━━━━━━━━\n"
    f"{_reminder_lines}\n"
)


def get_workout(day_name: str) -> str:
    """day_name: 'monday' ~ 'sunday' (영어 소문자)"""
    w = WORKOUTS[day_name]

    lines = [f"💪 {w['title']}", f"⏱ {w['duration']}", ""]

    if w["warmup"]:
        lines.append(f"🔥 워밍업: {w['warmup']}")
        lines.append("")

    lines.append("📋 본운동")
    for ex in w["main"]:
        name, scheme = ex["name"], ex["scheme"]
        if scheme:
            lines.append(f"  • {name} — {scheme}")
        else:
            lines.append(f"  • {name}")

    if w.get("note"):
        lines.append("")
        lines.append(f"💡 {w['note']}")

    lines.append(DAILY_REMINDER)

    return "\n".join(lines)
