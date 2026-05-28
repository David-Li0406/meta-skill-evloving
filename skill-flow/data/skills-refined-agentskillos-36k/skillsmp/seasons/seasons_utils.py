"""Shared utilities for the seasons skill.

This module provides common functions for working with the 72 Japanese
micro-seasons (kō) data, used by both download_images.py and generate_logs.py.
"""

import json
from calendar import month_name
from datetime import date
from pathlib import Path
from typing import TypedDict

# Paths
SKILL_DIR = Path(__file__).parent
DATA_FILE = SKILL_DIR / "seasons_data.json"
IMAGES_DIR = SKILL_DIR / "images"
LOGS_DIR = SKILL_DIR / "logs"


class Ko(TypedDict):
    """Type definition for a kō (micro-season) record."""

    num: int
    romaji: str
    english: str
    slug: str
    start: list[int]  # [month, day]
    end: list[int]  # [month, day]
    sekki_jp: str
    sekki_en: str
    quote: str
    author: str
    why_now: str
    insight: str
    resources: list[str]
    practices: list[str]


def load_ko_list() -> list[Ko]:
    """Load kō data from JSON as a list."""
    return json.loads(DATA_FILE.read_text())["ko"]


def load_ko_dict() -> dict[int, Ko]:
    """Load kō data from JSON as a dict indexed by number."""
    return {ko["num"]: ko for ko in load_ko_list()}


def get_image_filename(ko: Ko) -> str:
    """Get the image filename for a kō."""
    return f"{ko['num']:02d}-{ko['slug']}.jpg"


def get_image_path(ko: Ko) -> Path:
    """Get the full image path for a kō."""
    return IMAGES_DIR / get_image_filename(ko)


def format_date_range(start: list[int], end: list[int]) -> str:
    """Format a date range for display (e.g., 'January 20-24')."""
    sm, sd = start
    em, ed = end
    if sm == em:
        return f"{month_name[sm]} {sd}-{ed}"
    return f"{month_name[sm]} {sd}-{month_name[em]} {ed}"


def date_in_range(d: date, start: list[int], end: list[int]) -> bool:
    """Check if a date falls within a kō's date range.

    Handles three cases:
    1. Same month (e.g., Jan 20-24)
    2. Adjacent months (e.g., Apr 30-May 4)
    3. Year boundary (e.g., Dec 27-Jan 4)
    """
    sm, sd = start
    em, ed = end
    m, day = d.month, d.day

    if sm == em:
        # Same month: Jan 20-24
        return m == sm and sd <= day <= ed
    elif sm < em:
        # Adjacent months in same year: Apr 30-May 4
        return (m == sm and day >= sd) or (m == em and day <= ed)
    else:
        # Year boundary: Dec 27-Jan 4 (sm=12, em=1)
        # Match Dec 27-31 OR Jan 1-4
        return (m == sm and day >= sd) or (m == em and day <= ed)


def get_ko_for_date(d: date, ko_list: list[Ko] | None = None) -> Ko | None:
    """Find which kō a given date falls into."""
    if ko_list is None:
        ko_list = load_ko_list()
    for ko in ko_list:
        if date_in_range(d, ko["start"], ko["end"]):
            return ko
    return None


def get_day_index(d: date, ko: Ko) -> int:
    """Get the 0-indexed day position within a kō period.

    For kō #70 (Jan 20-24), Jan 20 returns 0, Jan 21 returns 1, etc.
    Handles year boundary correctly for kō like #66 (Dec 27-Jan 4).
    """
    sm, sd = ko["start"]
    # For year-boundary kō where date is in the end month (Jan),
    # the start was in the previous year (Dec)
    if sm > d.month:
        year = d.year - 1
    else:
        year = d.year
    start_date = date(year, sm, sd)
    return (d - start_date).days
