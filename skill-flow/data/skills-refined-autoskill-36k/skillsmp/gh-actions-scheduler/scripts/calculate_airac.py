#!/usr/bin/env python3
"""
Calculate AIRAC cycle dates.

AIRAC (Aeronautical Information Regulation and Control) cycles are 28-day
periods used for publishing aeronautical data updates.

Usage:
    python calculate_airac.py --year 2025
    python calculate_airac.py --next
    python calculate_airac.py --cycle 2505
"""

import argparse
from datetime import date, timedelta
from typing import Optional


# AIRAC epoch: A known cycle start date
# Cycle 2501 started on 2025-01-23
AIRAC_EPOCH = date(2025, 1, 23)
AIRAC_EPOCH_CYCLE = 2501
CYCLE_DAYS = 28


def get_cycle_start(cycle_id: int) -> date:
    """Get the effective date for a given cycle ID."""
    # Calculate cycles since epoch
    year = cycle_id // 100
    cycle_num = cycle_id % 100

    epoch_year = AIRAC_EPOCH_CYCLE // 100
    epoch_num = AIRAC_EPOCH_CYCLE % 100

    # Calculate total cycles difference
    year_diff = year - epoch_year
    cycles_diff = (year_diff * 13) + (cycle_num - epoch_num)

    return AIRAC_EPOCH + timedelta(days=cycles_diff * CYCLE_DAYS)


def get_cycle_id(dt: date) -> int:
    """Get the cycle ID for a given date."""
    days_since_epoch = (dt - AIRAC_EPOCH).days
    cycles_since_epoch = days_since_epoch // CYCLE_DAYS

    # Calculate year and cycle number
    total_cycles = (AIRAC_EPOCH_CYCLE % 100) + cycles_since_epoch
    year_offset = total_cycles // 13
    cycle_in_year = (total_cycles % 13) + 1

    if cycle_in_year > 13:
        year_offset += 1
        cycle_in_year = 1

    year = (AIRAC_EPOCH_CYCLE // 100) + year_offset

    return year * 100 + cycle_in_year


def get_current_cycle() -> tuple[int, date, date]:
    """Get current cycle info: (cycle_id, start_date, end_date)."""
    today = date.today()
    cycle_id = get_cycle_id(today)
    start = get_cycle_start(cycle_id)
    end = start + timedelta(days=CYCLE_DAYS - 1)
    return cycle_id, start, end


def get_next_airac() -> tuple[int, date]:
    """Get the next AIRAC cycle."""
    cycle_id, start, end = get_current_cycle()
    next_start = end + timedelta(days=1)

    # Calculate next cycle ID
    cycle_num = cycle_id % 100
    year = cycle_id // 100

    if cycle_num >= 13:
        next_id = (year + 1) * 100 + 1
    else:
        next_id = year * 100 + cycle_num + 1

    return next_id, next_start


def get_cycles_for_year(year: int) -> list[tuple[int, date]]:
    """Get all AIRAC cycles for a given year."""
    cycles = []

    # Start with first cycle of the year
    cycle_id = year * 100 + 1
    start_date = get_cycle_start(cycle_id)

    # If first cycle starts before this year, adjust
    while start_date.year < year:
        cycle_id += 1
        start_date = get_cycle_start(cycle_id)

    # Collect cycles until we reach next year
    while start_date.year == year:
        cycles.append((cycle_id, start_date))

        cycle_num = cycle_id % 100
        if cycle_num >= 13:
            cycle_id = (year + 1) * 100 + 1
        else:
            cycle_id += 1

        start_date = get_cycle_start(cycle_id)

    return cycles


def get_chart_cycles(year: int) -> list[tuple[int, date]]:
    """Get chart update cycles (every other cycle, starting with odd)."""
    all_cycles = get_cycles_for_year(year)
    return [(c, d) for c, d in all_cycles if (c % 100) % 2 == 1]


def generate_cron_expression(dt: date, hour: int = 9, minute: int = 1) -> str:
    """Generate cron expression for a specific date."""
    return f"{minute} {hour} {dt.day} {dt.month} *"


def main():
    parser = argparse.ArgumentParser(description='AIRAC Cycle Calculator')
    parser.add_argument('--year', '-y', type=int, help='Show cycles for year')
    parser.add_argument('--next', '-n', action='store_true', help='Show next cycle')
    parser.add_argument('--cycle', '-c', type=int, help='Show info for cycle ID')
    parser.add_argument('--current', action='store_true', help='Show current cycle')
    parser.add_argument('--cron', action='store_true', help='Include cron expressions')
    args = parser.parse_args()

    if args.cycle:
        start = get_cycle_start(args.cycle)
        end = start + timedelta(days=CYCLE_DAYS - 1)
        print(f"Cycle {args.cycle}:")
        print(f"  Effective: {start}")
        print(f"  Expires:   {end}")
        if args.cron:
            print(f"  Cron:      {generate_cron_expression(start)}")

    elif args.next:
        cycle_id, start = get_next_airac()
        print(f"Next AIRAC cycle: {cycle_id}")
        print(f"Effective date:   {start}")
        if args.cron:
            print(f"Cron expression:  {generate_cron_expression(start)}")

    elif args.current:
        cycle_id, start, end = get_current_cycle()
        today = date.today()
        days_remaining = (end - today).days

        print(f"Current cycle: {cycle_id}")
        print(f"Effective:     {start}")
        print(f"Expires:       {end}")
        print(f"Days remaining: {days_remaining}")

    elif args.year:
        cycles = get_cycles_for_year(args.year)
        chart_cycles = {c for c, _ in get_chart_cycles(args.year)}

        print(f"AIRAC Cycles for {args.year}:")
        print()
        print("Cycle  Effective    Chart")
        print("-" * 30)

        for cycle_id, start in cycles:
            chart_flag = "Yes" if cycle_id in chart_cycles else ""
            cron = f"  # {generate_cron_expression(start)}" if args.cron else ""
            print(f"{cycle_id}   {start}   {chart_flag:3}{cron}")

    else:
        # Default: show current and next
        cycle_id, start, end = get_current_cycle()
        next_id, next_start = get_next_airac()

        print(f"Current: {cycle_id} ({start} to {end})")
        print(f"Next:    {next_id} ({next_start})")


if __name__ == '__main__':
    main()
