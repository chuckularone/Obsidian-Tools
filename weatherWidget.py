#!/usr/bin/env python3

from datetime import datetime
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

SOURCE_URL = "http://blog.theshanty.us/weatherdata/currStats.out"

OUTPUT_FILE = Path(
    "/media/cmckenna/cmckenna/obsidian/My Thoughts/Misc_Notes/currentWeather.md"
)


def fetchWeatherData():
    with urlopen(SOURCE_URL, timeout=20) as response:
        text = response.read().decode("utf-8").strip()

    lines = [line.strip() for line in text.splitlines()]

    if len(lines) < 5:
        raise ValueError("Weather data file has fewer than 5 lines")

    return {
        "temperature": lines[0],
        "pressure": lines[1],
        "humidity": lines[2],
        "windSpeed": lines[3],
        "windGust": lines[4],
    }


def buildMarkdown(data):
    now = datetime.now()

    try:
        temp = float(data["temperature"])
    except ValueError:
        temp = 0

    calloutType = "info"

    if temp >= 100:
        calloutType = "danger"

    return f"""# Current Weather

_Last updated: {now:%A, %B %-d, %Y at %-I:%M %p}_

> [!{calloutType}] Weather
> 🌡️ **Temperature:** {data["temperature"]} °F  
> 🧭 **Pressure:** {data["pressure"]} inHg  
> 💧 **Humidity:** {data["humidity"]}%  
> 🌬️ **Wind:** {data["windSpeed"]} MPH  
> 💨 **Gusts:** {data["windGust"]} MPH
"""


def main():
    try:
        data = fetchWeatherData()
        markdown = buildMarkdown(data)

        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_FILE.write_text(markdown, encoding="utf-8")

        print(f"Updated: {OUTPUT_FILE}")

    except (URLError, HTTPError, TimeoutError, ValueError) as err:
        print(f"ERROR: {err}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
