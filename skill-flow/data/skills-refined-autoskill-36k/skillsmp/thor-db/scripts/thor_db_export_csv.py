#!/usr/bin/env python3
"""
Export ThorDB tables to CSV or JSON for sharing/analysis.

Usage:
    thor_db_export_csv.py <path_to_thor10.db> [--format csv|json] [--output-dir DIR]
"""

import sqlite3
import sys
import argparse
import json
import csv
from pathlib import Path
from datetime import datetime


def export_times_csv(cursor, output_path):
    """Export times table to CSV."""
    cursor.execute("""
        SELECT category, element, count,
               duration,
               duration/1e9 AS seconds_total,
               (duration*1.0/count)/1e9 AS seconds_avg
        FROM times
        ORDER BY duration DESC
    """)
    rows = cursor.fetchall()

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['category', 'element', 'count', 'duration_ns', 'seconds_total', 'seconds_avg'])
        writer.writerows(rows)

    return len(rows)


def export_stats_csv(cursor, output_path):
    """Export stats table to CSV."""
    cursor.execute("""
        SELECT module, element, started,
               datetime(started, 'unixepoch') AS start_time,
               duration
        FROM stats
        ORDER BY started DESC
    """)
    rows = cursor.fetchall()

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['module', 'element', 'started_unix', 'start_time', 'duration_sec'])
        writer.writerows(rows)

    return len(rows)


def export_tbl_csv(cursor, output_path):
    """Export tbl (metadata) table to CSV."""
    cursor.execute("SELECT key, value FROM tbl ORDER BY key")
    rows = cursor.fetchall()

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['key', 'value'])
        writer.writerows(rows)

    return len(rows)


def export_times_json(cursor, output_path):
    """Export times table to JSON."""
    cursor.execute("""
        SELECT category, element, count,
               duration,
               duration/1e9 AS seconds_total,
               (duration*1.0/count)/1e9 AS seconds_avg
        FROM times
        ORDER BY duration DESC
    """)
    rows = cursor.fetchall()

    data = [{
        'category': r[0],
        'element': r[1],
        'count': r[2],
        'duration_ns': r[3],
        'seconds_total': r[4],
        'seconds_avg': r[5]
    } for r in rows]

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

    return len(data)


def export_stats_json(cursor, output_path):
    """Export stats table to JSON."""
    cursor.execute("""
        SELECT module, element, started, duration
        FROM stats
        ORDER BY started DESC
    """)
    rows = cursor.fetchall()

    data = [{
        'module': r[0],
        'element': r[1],
        'started_unix': r[2],
        'start_time': datetime.utcfromtimestamp(r[2]).isoformat() if r[2] else None,
        'duration_sec': r[3]
    } for r in rows]

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

    return len(data)


def export_tbl_json(cursor, output_path):
    """Export tbl (metadata) table to JSON."""
    cursor.execute("SELECT key, value FROM tbl ORDER BY key")
    rows = cursor.fetchall()

    data = {r[0]: r[1] for r in rows}

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

    return len(data)


def main():
    parser = argparse.ArgumentParser(description="Export ThorDB to CSV or JSON")
    parser.add_argument("dbpath", help="Path to thor10.db or thor11.db")
    parser.add_argument("--format", choices=['csv', 'json'], default='csv', help="Output format (default: csv)")
    parser.add_argument("--output-dir", "-o", default=".", help="Output directory (default: current)")
    args = parser.parse_args()

    dbpath = Path(args.dbpath)
    if not dbpath.exists():
        print(f"Error: Database not found: {dbpath}", file=sys.stderr)
        sys.exit(1)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    ext = args.format
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    try:
        conn = sqlite3.connect(str(dbpath))
        cursor = conn.cursor()

        # Check available tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {row[0] for row in cursor.fetchall()}

        print(f"Exporting from: {dbpath}")
        print(f"Output format: {args.format}")
        print(f"Output directory: {output_dir}")
        print()

        if 'times' in tables:
            out_path = output_dir / f"thor_times_{timestamp}.{ext}"
            if ext == 'csv':
                count = export_times_csv(cursor, out_path)
            else:
                count = export_times_json(cursor, out_path)
            print(f"  times: {count} rows -> {out_path}")

        if 'stats' in tables:
            out_path = output_dir / f"thor_stats_{timestamp}.{ext}"
            if ext == 'csv':
                count = export_stats_csv(cursor, out_path)
            else:
                count = export_stats_json(cursor, out_path)
            print(f"  stats: {count} rows -> {out_path}")

        if 'tbl' in tables:
            out_path = output_dir / f"thor_metadata_{timestamp}.{ext}"
            if ext == 'csv':
                count = export_tbl_csv(cursor, out_path)
            else:
                count = export_tbl_json(cursor, out_path)
            print(f"  tbl:   {count} entries -> {out_path}")

        conn.close()
        print("\nExport complete.")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
