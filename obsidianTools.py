#!/usr/bin/env python3

import argparse
import calendar
from datetime import datetime, timedelta
from pathlib import Path

VAULT_ROOT = Path("/media/cmckenna/cmckenna/obsidian/My Thoughts")
EVENT_DAYS_FILE = VAULT_ROOT / "Misc_Notes" / "Event_Days.md"


def monthDir(dt):
    return f"{dt:%m}_{dt:%B}"


def dailyPath(dt):
    return VAULT_ROOT / f"{dt:%Y}" / monthDir(dt) / f"{dt:%Y_%m_%d}.md"


def obsidianDailyLink(dt, label):
    return f"[[{dt:%Y}/{monthDir(dt)}/{dt:%Y_%m_%d}|{label}]]"


def monthlyLink(dt):
    return f"[[{dt:%Y}/{dt:%B}_{dt:%Y}|{dt:%B} {dt:%Y}]]"


def loadAnnualEvents():
    events = {}

    if not EVENT_DAYS_FILE.exists():
        return events

    with EVENT_DAYS_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            parts = line.split(maxsplit=1)

            if len(parts) != 2:
                continue

            dateText, eventText = parts

            try:
                datetime.strptime(dateText, "%m/%d")
            except ValueError:
                continue

            events.setdefault(dateText, []).append(eventText)

    return events


def buildAnnualEventsBlock(dt, annualEvents):
    key = f"{dt:%m/%d}"
    events = annualEvents.get(key, [])

    if not events:
        return ""

    lines = [
        "> [!example] Annual events"
    ]

    for event in events:
        lines.append(f"> - {event}")

    return "\n".join(lines) + "\n\n"


def buildDailyNote(dt, annualEvents):
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
        f"{buildAnnualEventsBlock(dt, annualEvents)}"
        f"> [!info] Health Data \n"
        f">Health Notes/Blood Pressure\n"
        f">\n"
        f">🏋️ ?? x ??\n"
    )


def createDaily(dt, annualEvents):
    path = dailyPath(dt)
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        print(f"Already exists: {path}")
        return

    content = buildDailyNote(dt, annualEvents)
    path.write_text(content, encoding="utf-8")

    print(f"Created: {path}")


def createMonth(year, month, annualEvents):
    numberOfDays = calendar.monthrange(year, month)[1]

    for day in range(1, numberOfDays + 1):
        dt = datetime(year, month, day)
        createDaily(dt, annualEvents)


def createMonthIndex(year, month):
    dt = datetime(year, month, 1)
    path = VAULT_ROOT / f"{year}" / f"{dt:%B}_{year}.md"
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        print(f"Already exists: {path}")
        return

    cal = calendar.Calendar(firstweekday=6)

    lines = [
        f"# {dt:%B} {year}",
        "",
        "| Sun | Mon | Tue | Wed | Thu | Fri | Sat |",
        "|---|---|---|---|---|---|---|",
    ]

    for week in cal.monthdatescalendar(year, month):
        row = []

        for day in week:
            if day.month == month:
                link = obsidianDailyLink(day, str(day.day)).replace("|", "\\|")
                row.append(link)
            else:
                row.append("")

        lines.append("| " + " | ".join(row) + " |")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Created: {path}")


def parseDailyDate(dateText):
    try:
        return datetime.strptime(dateText, "%Y-%m-%d")
    except ValueError:
        raise argparse.ArgumentTypeError(
            "Date must be in YYYY-MM-DD format"
        )


def parseMonth(monthText):
    try:
        dt = datetime.strptime(monthText, "%Y-%m")
        return dt.year, dt.month
    except ValueError:
        raise argparse.ArgumentTypeError(
            "Month must be in YYYY-MM format"
        )


def main():
    parser = argparse.ArgumentParser(
        description="Obsidian CLI Automation System"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    todayParser = subparsers.add_parser("today")
    todayParser.set_defaults(commandName="today")

    dailyParser = subparsers.add_parser("daily")
    dailyParser.add_argument(
        "date",
        type=parseDailyDate,
        help="Date in YYYY-MM-DD format"
    )
    dailyParser.set_defaults(commandName="daily")

    monthParser = subparsers.add_parser("month")
    monthParser.add_argument(
        "month",
        type=parseMonth,
        help="Month in YYYY-MM format"
    )
    monthParser.set_defaults(commandName="month")

    indexParser = subparsers.add_parser("index")
    indexParser.add_argument(
        "month",
        type=parseMonth,
        help="Month in YYYY-MM format"
    )
    indexParser.set_defaults(commandName="index")

    args = parser.parse_args()
    annualEvents = loadAnnualEvents()

    if args.commandName == "today":
        createDaily(datetime.today(), annualEvents)

    elif args.commandName == "daily":
        createDaily(args.date, annualEvents)

    elif args.commandName == "month":
        year, month = args.month
        createMonth(year, month, annualEvents)

    elif args.commandName == "index":
        year, month = args.month
        createMonthIndex(year, month)


if __name__ == "__main__":
    main()
