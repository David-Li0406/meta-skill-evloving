#!/usr/bin/env python3
"""Generate daily log files for the seasons skill from JSON data.

Overview
--------
Generates 365 daily markdown files, one for each day of the year.
Each file contains seasonal wisdom based on Japan's 72 micro-seasons (kō).

Data Flow
---------
    seasons_data.json  →  generate_logs.py  →  logs/2026-01-01.md
       (72 seasons)         (this script)       logs/2026-01-02.md
                                                ...
                                                (365 files)

Processing Pipeline
-------------------
    Date (e.g., Jan 24)
           ↓
    get_ko_for_date()  →  find matching kō (#70: Jan 20-24)
           ↓
    get_day_index()    →  day position within kō (day 4 of 5)
           ↓
    generate_log_content()  →  select practice[4], build markdown
           ↓
    Write to logs/2026-01-24.md

"""

from datetime import date, timedelta

from seasons_utils import (
    LOGS_DIR,
    Ko,
    format_date_range,
    get_day_index,
    get_image_filename,
    get_ko_for_date,
    load_ko_list,
)


def generate_log_content(ko: Ko, day_index: int) -> str:
    """Generate the markdown content for a log file."""
    practice = ko["practices"][day_index % len(ko["practices"])]
    date_range = format_date_range(ko["start"], ko["end"])
    image_filename = get_image_filename(ko)

    resources = "\n".join(f"- {r}" for r in ko["resources"])

    return f"""## 第{ko["num"]}候 · {ko["romaji"]}

### "{ko["english"]}"

> {date_range} · {ko["sekki_jp"]} ({ko["sekki_en"]})

<img src="../images/{image_filename}" alt="{ko["english"]}" width="480">

**Why now?** {ko["why_now"]}

**Insight:** {ko["insight"]}

**Today's practice:** {practice}

> **💬** "{ko["quote"]}"
> — {ko["author"]}

**Learn more:**

{resources}
"""


def generate_all_logs(year: int = 2026) -> None:
    """Generate log files for every day of the year."""
    ko_list = load_ko_list()
    LOGS_DIR.mkdir(exist_ok=True)

    start = date(year, 1, 1)
    end = date(year, 12, 31)
    generated = skipped = 0

    current = start
    while current <= end:
        ko = get_ko_for_date(current, ko_list)
        if ko:
            day_index = get_day_index(current, ko)
            content = generate_log_content(ko, day_index)
            (LOGS_DIR / f"{current.isoformat()}.md").write_text(content)
            generated += 1
        else:
            print(f"Warning: No kō found for {current}")
            skipped += 1
        current += timedelta(days=1)

    print(f"Generated {generated} log files, skipped {skipped}")


if __name__ == "__main__":
    generate_all_logs()
