#!/usr/bin/env python3
"""
Identify slow YARA rules and scan elements for tuning hints.

Analyzes ThorDB to find:
- Slow deep_scan elements (likely YARA rules)
- Slow bulk_scan elements
- Patterns suggesting tuning opportunities

Usage:
    thor_db_slow_rules_hint.py <path_to_thor10.db> [--threshold SEC]
"""

import sqlite3
import sys
import argparse
from pathlib import Path
from collections import defaultdict


def analyze_deep_scan(cursor, threshold_sec=1.0):
    """Find slow deep_scan elements (typically YARA rules)."""
    cursor.execute("""
        SELECT element, count,
               duration/1e9 AS seconds_total,
               (duration*1.0/count)/1e9 AS seconds_avg
        FROM times
        WHERE category = 'deep_scan'
          AND (duration*1.0/count)/1e9 > ?
        ORDER BY duration DESC
    """, (threshold_sec,))
    return cursor.fetchall()


def analyze_bulk_scan(cursor, threshold_sec=0.5):
    """Find slow bulk_scan elements."""
    cursor.execute("""
        SELECT element, count,
               duration/1e9 AS seconds_total,
               (duration*1.0/count)/1e9 AS seconds_avg
        FROM times
        WHERE category = 'bulk_scan'
          AND (duration*1.0/count)/1e9 > ?
        ORDER BY duration DESC
    """, (threshold_sec,))
    return cursor.fetchall()


def analyze_hooks(cursor):
    """Find slow hooks."""
    cursor.execute("""
        SELECT element, count,
               duration/1e9 AS seconds_total,
               (duration*1.0/count)/1e9 AS seconds_avg
        FROM times
        WHERE category = 'hooks'
        ORDER BY duration DESC
        LIMIT 10
    """)
    return cursor.fetchall()


def get_category_totals(cursor):
    """Get overall time by category."""
    cursor.execute("""
        SELECT category, SUM(duration)/1e9 AS total_seconds
        FROM times
        GROUP BY category
        ORDER BY total_seconds DESC
    """)
    return cursor.fetchall()


def suggest_tuning(slow_deep, slow_bulk, category_totals):
    """Generate tuning suggestions based on analysis."""
    suggestions = []

    total_time = sum(t[1] for t in category_totals)
    deep_scan_time = next((t[1] for t in category_totals if t[0] == 'deep_scan'), 0)
    bulk_scan_time = next((t[1] for t in category_totals if t[0] == 'bulk_scan'), 0)

    if total_time > 0:
        deep_pct = (deep_scan_time / total_time) * 100
        bulk_pct = (bulk_scan_time / total_time) * 100

        if deep_pct > 50:
            suggestions.append(f"deep_scan is {deep_pct:.1f}% of total time - consider YARA rule optimization")

        if bulk_pct > 30:
            suggestions.append(f"bulk_scan is {bulk_pct:.1f}% of total time - consider file size/type limits")

    if len(slow_deep) > 10:
        suggestions.append(f"{len(slow_deep)} slow YARA rules found - consider --init-filter for worst offenders")

    # Check for pattern in slow rules
    rule_prefixes = defaultdict(int)
    for row in slow_deep:
        element = row[0]
        if '_' in element:
            prefix = element.split('_')[0]
            rule_prefixes[prefix] += 1

    for prefix, count in sorted(rule_prefixes.items(), key=lambda x: -x[1])[:3]:
        if count >= 3:
            suggestions.append(f"Multiple slow rules with prefix '{prefix}' ({count} rules) - consider filtering")

    return suggestions


def main():
    parser = argparse.ArgumentParser(description="Find slow rules for tuning hints")
    parser.add_argument("dbpath", help="Path to thor10.db or thor11.db")
    parser.add_argument("--threshold", type=float, default=1.0,
                        help="Avg seconds threshold for 'slow' (default: 1.0)")
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

        print(f"ThorDB Slow Rules Analysis: {dbpath}")
        print(f"Threshold: > {args.threshold}s average per invocation")
        print("=" * 60)

        # Category totals
        category_totals = get_category_totals(cursor)
        print("\nTime by Category:")
        for cat, seconds in category_totals:
            print(f"  {cat}: {seconds:.1f}s")

        # Slow deep_scan (YARA rules)
        slow_deep = analyze_deep_scan(cursor, args.threshold)
        print(f"\nSlow deep_scan elements (likely YARA rules): {len(slow_deep)}")
        if slow_deep:
            print("-" * 60)
            print(f"{'Element':<40} {'Count':>8} {'Total(s)':>10} {'Avg(s)':>10}")
            print("-" * 60)
            for element, count, total, avg in slow_deep[:15]:
                print(f"{element[:40]:<40} {count:>8} {total:>10.2f} {avg:>10.3f}")
            if len(slow_deep) > 15:
                print(f"  ... and {len(slow_deep) - 15} more")

        # Slow bulk_scan
        slow_bulk = analyze_bulk_scan(cursor, args.threshold / 2)
        print(f"\nSlow bulk_scan elements: {len(slow_bulk)}")
        if slow_bulk:
            print("-" * 60)
            for element, count, total, avg in slow_bulk[:10]:
                print(f"  {element[:50]}: {total:.1f}s total, {avg:.3f}s avg ({count} calls)")

        # Hooks overview
        hooks = analyze_hooks(cursor)
        if hooks:
            print("\nTop hooks by time:")
            for element, count, total, avg in hooks[:5]:
                print(f"  {element}: {total:.1f}s total")

        # Tuning suggestions
        suggestions = suggest_tuning(slow_deep, slow_bulk, category_totals)
        if suggestions:
            print("\n" + "=" * 60)
            print("TUNING SUGGESTIONS")
            print("=" * 60)
            for suggestion in suggestions:
                print(f"  • {suggestion}")

        # Filter command hints
        if slow_deep:
            worst = [r[0] for r in slow_deep[:5] if r[3] > args.threshold * 2]
            if worst:
                print("\nExample filter command for worst offenders:")
                filter_list = ",".join(worst[:3])
                print(f"  thor64.exe --init-filter {filter_list} -p C:\\")

        conn.close()

    except sqlite3.Error as e:
        print(f"SQLite error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
