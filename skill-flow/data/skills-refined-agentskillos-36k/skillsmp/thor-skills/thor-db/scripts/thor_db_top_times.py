#!/usr/bin/env python3
"""
Analyze ThorDB timing data to find performance hotspots.

Usage:
    thor_db_top_times.py <path_to_thor10.db> [--top N] [--by-category]
"""

import sqlite3
import sys
import argparse
from pathlib import Path


def get_top_by_total(cursor, limit=20):
    """Get elements with highest total time."""
    cursor.execute("""
        SELECT category, element, count,
               duration/1e9 AS seconds_total,
               (duration*1.0/count)/1e9 AS seconds_avg
        FROM times
        ORDER BY duration DESC
        LIMIT ?
    """, (limit,))
    return cursor.fetchall()


def get_top_by_average(cursor, limit=20, min_count=5):
    """Get elements with highest average time per invocation."""
    cursor.execute("""
        SELECT category, element, count,
               (duration*1.0/count)/1e9 AS seconds_avg,
               duration/1e9 AS seconds_total
        FROM times
        WHERE count >= ?
        ORDER BY (duration*1.0/count) DESC
        LIMIT ?
    """, (min_count, limit))
    return cursor.fetchall()


def get_by_category(cursor):
    """Get time totals grouped by category."""
    cursor.execute("""
        SELECT category,
               SUM(count) AS total_invocations,
               SUM(duration)/1e9 AS total_seconds
        FROM times
        GROUP BY category
        ORDER BY total_seconds DESC
    """)
    return cursor.fetchall()


def print_table(headers, rows, title=None):
    """Print formatted table."""
    if title:
        print(f"\n{'=' * 60}")
        print(f" {title}")
        print('=' * 60)

    if not rows:
        print("  No data found.")
        return

    # Calculate column widths
    widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            widths[i] = max(widths[i], len(str(val)[:50]))

    # Print header
    header_line = " | ".join(h.ljust(widths[i]) for i, h in enumerate(headers))
    print(header_line)
    print("-" * len(header_line))

    # Print rows
    for row in rows:
        formatted = []
        for i, val in enumerate(row):
            if isinstance(val, float):
                formatted.append(f"{val:.3f}".rjust(widths[i]))
            else:
                formatted.append(str(val)[:50].ljust(widths[i]))
        print(" | ".join(formatted))


def main():
    parser = argparse.ArgumentParser(description="Analyze ThorDB timing data")
    parser.add_argument("dbpath", help="Path to thor10.db or thor11.db")
    parser.add_argument("--top", type=int, default=20, help="Number of results (default: 20)")
    parser.add_argument("--by-category", action="store_true", help="Show totals by category")
    parser.add_argument("--min-count", type=int, default=5, help="Minimum invocations for avg (default: 5)")
    args = parser.parse_args()

    dbpath = Path(args.dbpath)
    if not dbpath.exists():
        print(f"Error: Database not found: {dbpath}", file=sys.stderr)
        sys.exit(1)

    try:
        conn = sqlite3.connect(str(dbpath))
        cursor = conn.cursor()

        # Check if times table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='times'")
        if not cursor.fetchone():
            print("Error: 'times' table not found in database", file=sys.stderr)
            sys.exit(1)

        print(f"ThorDB Analysis: {dbpath}")

        if args.by_category:
            rows = get_by_category(cursor)
            print_table(
                ["Category", "Invocations", "Total (sec)"],
                rows,
                "Time by Category"
            )
        else:
            # Top by total time
            rows = get_top_by_total(cursor, args.top)
            print_table(
                ["Category", "Element", "Count", "Total (sec)", "Avg (sec)"],
                rows,
                f"Top {args.top} by Total Time"
            )

            # Top by average time
            rows = get_top_by_average(cursor, args.top, args.min_count)
            print_table(
                ["Category", "Element", "Count", "Avg (sec)", "Total (sec)"],
                rows,
                f"Top {args.top} by Average Time (min {args.min_count} invocations)"
            )

        conn.close()

    except sqlite3.Error as e:
        print(f"SQLite error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
