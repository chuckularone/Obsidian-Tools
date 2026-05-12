#!/usr/bin/env python3

import argparse
import calendar
from datetime import datetime, timedelta
from pathlib import Path

VAULT_ROOT = Path("/media/cmckenna/cmckenna/obsidian/My Thoughts")


def ordinal(n):
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def monthDir(dt):
    return f"{dt:%m}_{dt:%B}"


def dailyPath(dt):
    return (
        VAULT_ROOT
        / f"{dt:%Y}"
        / monthDir(dt)
        / f"{dt:%Y_%m_%d}.md"
    )


def obsidianDailyLink(dt, label):
    return f"[[{dt:%Y}/{monthDir(dt)}/{dt:%Y_%m_%d}|{label}]]"


def monthlyLink(dt):
    return f"[[{dt:%Y}/{dt:%B}_{dt:%Y}|{dt:%B} {dt:%Y}]]"


def buildDailyNote(dt):
    yesterday = dt - timedelta(days=1)
    tomorrow = dt + timedelta(days=1)

    return (
        f"**=={dt:%A}==**\n"
        f"[[My Notes]] – "
        f"{monthlyLink(dt)} – "
        f"{obsidianDailyLink(yesterday, 'Yesterday')} – "
        f"{obsidianDailyLink(tomorrow, 'Tomorrow')}\n\n"
        f"> [!abstract] To do\n"
        f"> - [ ] todo items\n"
        f"> - [ ] \n"
        f"\n"
        f"> [!info] Health Data \n"
        f">Health Notes/Blood Pressure\n"
        f">\n"
        f">🏋️ ?? x ??\n"
    )


def createDaily(dt):
    path = dailyPath(dt)
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        print(f"Already exists: {path}")
        return

    content = buildDailyNote(dt)
    path.write_text(content, encoding="utf-8")

    print(f"Created: {path}")

def createMonth(year, month):
    numberOfDays = calendar.monthrange(year, month)[1]

    for day in range(1, numberOfDays + 1):
        dt = datetime(year, month, day)
        createDaily(dt)

def main():
    parser = argparse.ArgumentParser(
        description="Obsidian CLI Automation System"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    todayParser = subparsers.add_parser("today")
    todayParser.set_defaults(func=lambda args: createDaily(datetime.today()))

    dailyParser = subparsers.add_parser("daily")
    dailyParser.add_argument("date", help="Date in YYYY-MM-DD format")
    dailyParser.set_defaults(
        func=lambda args: createDaily(
            datetime.strptime(args.date, "%Y-%m-%d")
        )
    )
    monthParser = subparsers.add_parser("month")
    monthParser.add_argument("month", help="Month in YYYY-MM format")
    monthParser.set_defaults(
        func=lambda args: createMonth(
            int(args.month[0:4]),
            int(args.month[5:7])
        )
    )
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
