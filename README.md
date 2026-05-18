# Obsidian Tools
# Obsidian CLI Automation System

Python utility for automatically generating Obsidian daily notes and monthly index pages.

## Features

- Create today's daily note
- Create a specific daily note
- Create all daily notes for a month
- Create a monthly calendar index page
- Automatically creates directory structure
- Skips existing files safely
- Adds navigation links:
    - My Notes
    - Monthly page
    - Yesterday
    - Tomorrow
- Loads recurring annual events from a central file
- Supports multiple events on the same date
- Supports out-of-order event definitions
- Creates Obsidian-compatible wikilinks
- Generates compact monthly calendars using link aliases

---

# Directory Structure

Example generated structure:

```
My Thoughts/
├── 2026/
│   ├── June_2026.md
│   └── 06_June/
│       ├── 2026_06_01.md
│       ├── 2026_06_02.md
│       └── ...
└── Misc_Notes/
    └── Event_Days.md
```

---

# Daily Note Format

Generated daily notes contain:

- Day heading
- Navigation links
- Todo block
- Annual events block (if applicable)
- Health Data block

Example:

```
**==Thursday==**
[[My Notes]] – [[2026/June_2026|June 2026]] – [[2026/06_June/2026_06_11|Yesterday]] – [[2026/06_June/2026_06_13|Tomorrow]]

> [!abstract] To do
> - [ ] todo items  
> - [ ]


> [!example] Annual events
> - Chuck's birthday
 
> [!info] Health Data
> Health Notes/Blood Pressure
>
> 🏋️ ?? x ??
```

---

# Annual Events File

Location:

```
/media/cmckenna/cmckenna/obsidian/My Thoughts/Misc_Notes/Event_Days.md
```

Format:

```
06/12 Friend's birthday (2005)
06/25 Bought car (2021)
06/25 Surgery (2020)
07/04 Independence day (1776)
```

Notes:

- Dates may be out of order
- Multiple events per day are supported
- Invalid lines are ignored safely

---

# Commands

## Create today's note

```
obsidianTools.py today
```

Creates:

```
YYYY/MM_Month/YYYY_MM_DD.md
```

for the current day.

---

## Create a specific daily note

```
obsidianTools.py daily 2026-06-12
```

Creates:

```
2026/06_June/2026_06_12.md
```

---

## Create an entire month of daily notes

```
obsidianTools.py month 2026-06
```

Creates all daily notes for June 2026.

---

## Create a monthly calendar index

```
obsidianTools.py index 2026-06
```

Creates:

```
2026/June_2026.md
```

Example output:

```
| Sun | Mon | Tue | Wed | Thu | Fri | Sat |
|---|---|---|---|---|---|---|
|  | [[2026/06_June/2026_06_01\|1]] | [[2026/06_June/2026_06_02\|2]] | ... |
```

---

# Validation

The script validates date formats.

Accepted formats:

```
daily  YYYY-MM-DDmonth  YYYY-MMindex  YYYY-MM
```

Examples:

```
obsidianTools.py daily 2026-06-15
obsidianTools.py month 2026-06
obsidianTools.py index 2026-06
```

Invalid formats will produce argparse errors.

---

# Requirements

- Python 3
- Obsidian
- Linux/macOS/WSL compatible

No external Python packages required.

Uses only:

- argparse
- calendar
- datetime
- pathlib

---

# Suggested Permissions

```
chmod +x obsidianTools.py
```

---

# Example Workflow

Generate an entire month and calendar index:

```
./obsidianTools.py month 2026-06./obsidianTools.py index 2026-06
```

Open in Obsidian:

```
2026/June_2026.md
```

Select a day from the calendar grid.



---
# weatherWidget.py
Runs every 10 minutes and outputs the current weather for my home weather station
See https://github.com/chuckularone/WeatherCharts for how the data gets there


> [!info] Weather
>
> 🌡️ **Temperature:** 62 °F  
> 🧭 **Pressure:** 30.10 inHg  
> 💧 **Humidity:** 43%  
> 🌬️ **Wind:** 2 MPH  
> 💨 **Gusts:** 5 MPH

