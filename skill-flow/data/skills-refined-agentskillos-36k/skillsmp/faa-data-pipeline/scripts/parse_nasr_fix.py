#!/usr/bin/env python3
"""
Parse FAA NASR FIX.txt (Fixes/Waypoints) file into SQLite database.

The FIX.txt file contains navigational fix data in fixed-width format.
Includes intersection and waypoint data used in airways and procedures.

Usage:
    python parse_nasr_fix.py --input FIX.txt --output aviation.db
"""

import argparse
import sqlite3
import sys
from pathlib import Path
from typing import Optional


# FIX record field definitions (1-indexed positions)
FIX_FIELDS = {
    'record_type': (1, 4),              # Record type (FIX1, FIX2, etc.)
    'fix_id': (5, 34),                  # Fix identifier (5 characters typically)
    'fix_state_code': (35, 36),         # Fix state code
    'icao_region': (37, 38),            # ICAO region code
    'latitude_dms': (39, 52),           # Latitude (formatted)
    'latitude_secs': (53, 66),          # Latitude (seconds)
    'longitude_dms': (67, 81),          # Longitude (formatted)
    'longitude_secs': (82, 96),         # Longitude (seconds)
    'fix_category': (97, 99),           # Fix category (MIL/CIV/RNAV)
    'charting_info': (100, 121),        # Charting info
    'artcc_hi': (122, 125),             # High altitude ARTCC
    'artcc_lo': (126, 129),             # Low altitude ARTCC
    'fix_use': (130, 144),              # Fix use (RNAV, etc.)
    'nas_id': (145, 149),               # NAS identifier
    'publish_status': (150, 150),       # Published status
    'type': (151, 180),                 # Fix type description
    'prev_name': (181, 210),            # Previous name (if changed)
    'charting_type': (211, 212),        # Charting type
}


def parse_coordinate(dms: str, seconds: str, is_longitude: bool = False) -> Optional[float]:
    """Parse FAA coordinate format to decimal degrees."""
    try:
        dms = dms.strip()
        if not dms:
            return None

        direction = dms[-1].upper()
        dms = dms[:-1]

        parts = dms.replace('-', ' ').replace("'", ' ').replace('"', ' ').split()

        if len(parts) >= 3:
            degrees = float(parts[0])
            minutes = float(parts[1])
            secs = float(parts[2])
        elif len(parts) == 2:
            degrees = float(parts[0])
            minutes = float(parts[1])
            secs = 0.0
        else:
            degrees = float(parts[0])
            minutes = 0.0
            secs = 0.0

        if seconds.strip():
            try:
                secs = float(seconds.strip())
            except ValueError:
                pass

        decimal = degrees + (minutes / 60.0) + (secs / 3600.0)

        if direction in ('S', 'W'):
            decimal = -decimal

        return decimal

    except (ValueError, IndexError):
        return None


def extract_field(line: str, start: int, end: int) -> str:
    """Extract a field from a fixed-width line (1-indexed)."""
    start_idx = start - 1
    end_idx = end

    if len(line) >= end_idx:
        return line[start_idx:end_idx].strip()
    elif len(line) > start_idx:
        return line[start_idx:].strip()
    else:
        return ''


def parse_fix_record(line: str) -> Optional[dict]:
    """Parse a single FIX record line."""
    record_type = extract_field(line, *FIX_FIELDS['record_type'])

    # Only parse FIX1 records (primary fix data)
    if record_type != 'FIX1':
        return None

    record = {}
    for field_name, (start, end) in FIX_FIELDS.items():
        record[field_name] = extract_field(line, start, end)

    # Parse coordinates
    record['latitude'] = parse_coordinate(
        record['latitude_dms'],
        record['latitude_secs'],
        is_longitude=False
    )
    record['longitude'] = parse_coordinate(
        record['longitude_dms'],
        record['longitude_secs'],
        is_longitude=True
    )

    # Clean up fix_id (remove trailing spaces and extract 5-char ID)
    fix_id = record['fix_id'].strip()
    if fix_id:
        # The actual fix ID is typically the first 5 characters
        record['fix_id_clean'] = fix_id.split()[0] if ' ' in fix_id else fix_id[:5]
    else:
        record['fix_id_clean'] = ''

    # Determine fix type
    fix_type = record['fix_use'].upper()
    if 'RNAV' in fix_type:
        record['fix_type'] = 'RNAV'
    elif 'REP-PT' in fix_type or 'WAYPOINT' in fix_type:
        record['fix_type'] = 'WAYPOINT'
    elif 'CNF' in fix_type:
        record['fix_type'] = 'CNF'  # Computer Navigation Fix
    else:
        record['fix_type'] = 'FIX'

    return record


def create_fixes_table(conn: sqlite3.Connection):
    """Create the fixes table if it doesn't exist."""
    conn.execute('''
        CREATE TABLE IF NOT EXISTS fixes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fix_id TEXT NOT NULL,
            state_code TEXT,
            icao_region TEXT,
            latitude REAL,
            longitude REAL,
            fix_category TEXT,
            fix_type TEXT,
            fix_use TEXT,
            artcc_hi TEXT,
            artcc_lo TEXT,
            charting_info TEXT,
            nas_id TEXT,
            publish_status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            UNIQUE(fix_id, state_code)
        )
    ''')

    conn.execute('CREATE INDEX IF NOT EXISTS idx_fixes_id ON fixes(fix_id)')
    conn.execute('CREATE INDEX IF NOT EXISTS idx_fixes_coords ON fixes(latitude, longitude)')
    conn.execute('CREATE INDEX IF NOT EXISTS idx_fixes_type ON fixes(fix_type)')

    conn.commit()


def insert_fix(conn: sqlite3.Connection, record: dict) -> bool:
    """Insert a fix record into the database."""
    try:
        conn.execute('''
            INSERT OR REPLACE INTO fixes (
                fix_id, state_code, icao_region,
                latitude, longitude,
                fix_category, fix_type, fix_use,
                artcc_hi, artcc_lo,
                charting_info, nas_id, publish_status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            record['fix_id_clean'],
            record['fix_state_code'],
            record['icao_region'],
            record['latitude'],
            record['longitude'],
            record['fix_category'],
            record['fix_type'],
            record['fix_use'],
            record['artcc_hi'],
            record['artcc_lo'],
            record['charting_info'],
            record['nas_id'],
            record['publish_status']
        ))
        return True

    except sqlite3.Error as e:
        print(f"Error inserting fix {record['fix_id_clean']}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Parse FAA NASR FIX.txt into SQLite database'
    )

    parser.add_argument('--input', '-i', type=str, required=True, help='Path to FIX.txt file')
    parser.add_argument('--output', '-o', type=str, required=True, help='Path to SQLite database')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)

    conn = sqlite3.connect(args.output)
    create_fixes_table(conn)

    print(f"Parsing {input_path}...")

    count = 0
    errors = 0

    with open(input_path, 'r', encoding='latin-1') as f:
        for line_num, line in enumerate(f, 1):
            record = parse_fix_record(line)

            if record:
                if insert_fix(conn, record):
                    count += 1
                    if args.verbose and count % 5000 == 0:
                        print(f"  Processed {count} fixes...")
                else:
                    errors += 1

    conn.commit()
    conn.close()

    print(f"\nParsing complete:")
    print(f"  Fixes inserted: {count}")
    print(f"  Errors: {errors}")
    print(f"  Database: {args.output}")


if __name__ == '__main__':
    main()
