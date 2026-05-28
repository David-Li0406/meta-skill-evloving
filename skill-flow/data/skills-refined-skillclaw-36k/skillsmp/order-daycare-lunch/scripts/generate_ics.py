#!/usr/bin/env python3
"""
Generate ICS calendar file for days when child's lunch needs to be packed.

This script creates all-day calendar events with "Free" availability for each
day that lunch was not ordered from the catering service.
"""

import argparse
import sys
from datetime import datetime
from typing import List


def generate_ics_event(
    date: datetime,
    child_name: str,
    location: str,
    timezone: str
) -> str:
    """Generate a single ICS event for packing lunch."""
    date_str = date.strftime("%Y%m%d")
    uid = f"pack-lunch-{date_str}@school-lunch"
    
    event = f"""BEGIN:VEVENT
UID:{uid}
DTSTART;VALUE=DATE:{date_str}
DTEND;VALUE=DATE:{date_str}
SUMMARY:Pack {child_name}'s Lunch
DESCRIPTION:No lunch ordered today. Pack lunch for {child_name} at {location}.
TRANSP:TRANSPARENT
STATUS:CONFIRMED
SEQUENCE:0
END:VEVENT"""
    
    return event


def generate_ics_file(
    month: int,
    year: int,
    skipped_days: List[int],
    child_name: str = "Child",
    location: str = "School/Preschool",
    timezone: str = "America/New_York"
) -> str:
    """Generate complete ICS file content."""
    
    # Validate inputs
    if not 1 <= month <= 12:
        raise ValueError(f"Invalid month: {month}. Must be 1-12.")
    
    if year < 2000 or year > 2100:
        raise ValueError(f"Invalid year: {year}. Must be 2000-2100.")
    
    if not skipped_days:
        raise ValueError("No skipped days provided.")
    
    # ICS header
    ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//School Lunch Tracker//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH
X-WR-CALNAME:Pack {child_name}'s Lunch
X-WR-TIMEZONE:{timezone}
"""
    
    # Generate events for each skipped day
    events = []
    for day in sorted(skipped_days):
        try:
            date = datetime(year, month, day)
            event = generate_ics_event(date, child_name, location, timezone)
            events.append(event)
        except ValueError as e:
            print(f"Warning: Invalid date {month}/{day}/{year} - {e}", file=sys.stderr)
            continue
    
    # Add all events
    ics_content += "\n".join(events)
    
    # ICS footer
    ics_content += "\nEND:VCALENDAR\n"
    
    return ics_content


def main():
    parser = argparse.ArgumentParser(
        description="Generate ICS calendar file for packing lunch days",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -m 7 -y 2025 -d 3,9,16,21,31
  %(prog)s --month 11 --year 2025 --skipped-days 4,13,17,24 --output nov-lunch.ics
  %(prog)s -m 8 -y 2025 -d 5,12,19,26 --child-name "Sam" --location "School"
        """
    )
    
    # Required arguments
    parser.add_argument(
        "-m", "--month",
        type=int,
        required=True,
        help="Month number (1-12)"
    )
    
    parser.add_argument(
        "-y", "--year",
        type=int,
        required=True,
        help="Year (e.g., 2025)"
    )
    
    parser.add_argument(
        "-d", "--skipped-days",
        type=str,
        required=True,
        help="Comma-separated list of day numbers (e.g., '3,9,16,21,31')"
    )
    
    # Optional arguments
    parser.add_argument(
        "-o", "--output",
        type=str,
        help="Output filename (default: pack-lunch-MMYYYY.ics)"
    )
    
    parser.add_argument(
        "--child-name",
        type=str,
        default="Child",
        help="Child's name (default: Child)"
    )

    parser.add_argument(
        "--location",
        type=str,
        default="School/Preschool",
        help="School/classroom location (default: School/Preschool)"
    )
    
    parser.add_argument(
        "--timezone",
        type=str,
        default="America/New_York",
        help="Timezone (default: America/New_York)"
    )
    
    args = parser.parse_args()
    
    # Parse skipped days
    try:
        skipped_days = [int(d.strip()) for d in args.skipped_days.split(",")]
    except ValueError:
        print("Error: --skipped-days must be comma-separated integers", file=sys.stderr)
        sys.exit(1)
    
    # Generate output filename if not provided
    if not args.output:
        month_names = [
            "january", "february", "march", "april", "may", "june",
            "july", "august", "september", "october", "november", "december"
        ]
        month_name = month_names[args.month - 1]
        args.output = f"pack-lunch-{month_name}-{args.year}.ics"
    
    # Generate ICS content
    try:
        ics_content = generate_ics_file(
            month=args.month,
            year=args.year,
            skipped_days=skipped_days,
            child_name=args.child_name,
            location=args.location,
            timezone=args.timezone
        )
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Write to file
    try:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(ics_content)
        print(f"✓ Generated {args.output}")
        print(f"  Events created: {len(skipped_days)}")
        print(f"  Month: {args.month}/{args.year}")
        print(f"  Skipped days: {sorted(skipped_days)}")
    except IOError as e:
        print(f"Error writing file: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
