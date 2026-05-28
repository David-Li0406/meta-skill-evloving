"""Temporal context for Layton.

Provides deterministic temporal information: time of day, work hours, day of week.
All calculations are based on the timezone in config.
"""

from datetime import datetime, time
from typing import Literal
from zoneinfo import ZoneInfo

from laytonlib.config import get_nested, load_config
from laytonlib.formatters import OutputFormatter

TimeOfDay = Literal["morning", "midday", "afternoon", "evening", "night"]


def classify_time_of_day(hour: int) -> TimeOfDay:
    """Classify the hour into a time of day period.

    Args:
        hour: Hour in 24-hour format (0-23)

    Returns:
        Time of day classification
    """
    if 5 <= hour <= 11:
        return "morning"
    elif 12 <= hour <= 13:
        return "midday"
    elif 14 <= hour <= 17:
        return "afternoon"
    elif 18 <= hour <= 21:
        return "evening"
    else:  # 22-23 or 0-4
        return "night"


def parse_time(time_str: str) -> time:
    """Parse a time string (HH:MM) into a time object.

    Args:
        time_str: Time in HH:MM format

    Returns:
        time object
    """
    parts = time_str.split(":")
    return time(int(parts[0]), int(parts[1]))


def is_within_work_hours(
    current_time: time,
    work_start: str,
    work_end: str,
) -> bool:
    """Check if current time is within work hours (inclusive).

    Args:
        current_time: Current time
        work_start: Work start time (HH:MM)
        work_end: Work end time (HH:MM)

    Returns:
        True if within work hours
    """
    start = parse_time(work_start)
    end = parse_time(work_end)

    # Simple comparison (assumes start < end, no overnight)
    return start <= current_time <= end


def get_temporal_context(timezone_str: str, work_start: str, work_end: str) -> dict:
    """Get full temporal context.

    Args:
        timezone_str: Timezone string (e.g., "America/Los_Angeles")
        work_start: Work start time (HH:MM)
        work_end: Work end time (HH:MM)

    Returns:
        Dict with temporal context fields
    """
    # Get current time in configured timezone
    try:
        tz = ZoneInfo(timezone_str)
    except Exception:
        # Fallback to UTC if timezone invalid
        tz = ZoneInfo("UTC")

    now = datetime.now(tz)

    return {
        "timestamp": now.isoformat(),
        "time_of_day": classify_time_of_day(now.hour),
        "day_of_week": now.strftime("%A"),
        "work_hours": is_within_work_hours(now.time(), work_start, work_end),
        "timezone": timezone_str,
    }


def format_human_context(context: dict) -> str:
    """Format context as human-readable summary.

    Args:
        context: Temporal context dict

    Returns:
        Human-readable summary string
    """
    day = context["day_of_week"]
    tod = context["time_of_day"]
    work = "within work hours" if context["work_hours"] else "outside work hours"

    return f"It's {day} {tod}, {work}."


def run_context(formatter: OutputFormatter) -> int:
    """Run the context command.

    Args:
        formatter: Output formatter

    Returns:
        Exit code (0=success, 1=error)
    """
    # Load config
    config = load_config()
    if config is None:
        formatter.error(
            "CONFIG_MISSING",
            "Config not found. Run 'layton config init' to create it.",
            next_steps=["layton config init"],
        )
        return 1

    # Get required config values
    try:
        timezone = get_nested(config, "timezone")
    except KeyError:
        formatter.error(
            "CONFIG_MISSING",
            "Config key 'timezone' not found.",
            next_steps=[
                "Run 'layton config init --force' to reset config",
                "Or run 'layton config set timezone \"UTC\"'",
            ],
        )
        return 1

    try:
        work_start = get_nested(config, "work.schedule.start")
        work_end = get_nested(config, "work.schedule.end")
    except KeyError:
        formatter.error(
            "CONFIG_MISSING",
            "Config key 'work.schedule.start' or 'work.schedule.end' not found.",
            next_steps=[
                "Run 'layton config init --force' to reset config",
                "Or run 'layton config set work.schedule.start \"09:00\"'",
            ],
        )
        return 1

    # Get temporal context
    context = get_temporal_context(timezone, work_start, work_end)

    # Output
    if formatter.human:
        # Add human-readable summary
        context["summary"] = format_human_context(context)

    formatter.success(context)
    return 0
