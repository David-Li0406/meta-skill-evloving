#!/usr/bin/env python3
"""
Parse FAA DOF (Digital Obstacle File) into SQLite database.

The DOF contains obstacle data (towers, buildings, antennas, etc.)
in fixed-width ASCII format. Updated daily.

Usage:
    python parse_dof.py --input DOF.DAT --output aviation.db
    python parse_dof.py --input DOF.DAT --output aviation.db --mode update
"""

import argparse
import sqlite3
import sys
from pathlib import Path
from typing import Optional


# DOF record field definitions (1-indexed positions)
DOF_FIELDS = {
    'oas_number': (1, 9),
    'verification_status': (11, 18),
    'country': (20, 21),
    'state': (23, 24),
    'city': (26, 41),
    'latitude_dms': (43, 54),
    'longitude_dms': (56, 68),
    'obstacle_type': (70, 87),
    'quantity': (89, 89),
    'agl_height': (91, 95),
    'msl_height': (97, 101),
    'lighting': (103, 103),
    'horizontal_accuracy': (105, 105),
    'vertical_accuracy': (107, 107),
    'mark_indicator': (109, 109),
    'faa_study_number': (111, 124),
    'action': (126, 126),
    'jdate': (128, 134),
}

LIGHTING_CODES = {
    'R': 'Red', 'D': 'Dual', 'W': 'White', 'F': 'Flood',
    'N': 'None', 'S': 'Strobe', 'C': 'Medium Strobe',
    'H': 'High Intensity', 'M': 'Medium', 'L': 'Low', 'U': 'Unknown',
}


def extract_field(line: str, start: int, end: int) -> str:
    start_idx = start - 1
    if len(line) >= end:
        return line[start_idx:end].strip()
    elif len(line) > start_idx:
        return line[start_idx:].strip()
    return ''


def parse_coordinate(dms: str, is_longitude: bool = False) -> Optional[float]:
    try:
        dms = dms.strip()
        if not dms:
            return None
        direction = dms[-1].upper()
        parts = dms[:-1].split('-')
        if len(parts) >= 3:
            degrees = float(parts[0])
            minutes = float(parts[1])
            seconds = float(parts[2])
        else:
            return None
        decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
        if direction in ('S', 'W'):
            decimal = -decimal
        return decimal
    except (ValueError, IndexError):
        return None


def parse_dof_record(line: str) -> Optional[dict]:
    if not line.strip() or line.startswith('#') or 'OAS' in line[:10]:
        return None
    if len(line) < 100:
        return None

    record = {name: extract_field(line, s, e) for name, (s, e) in DOF_FIELDS.items()}
    if not record['oas_number']:
        return None

    record['latitude'] = parse_coordinate(record['latitude_dms'])
    record['longitude'] = parse_coordinate(record['longitude_dms'])
    if record['latitude'] is None or record['longitude'] is None:
        return None

    record['agl_height_ft'] = int(record['agl_height']) if record['agl_height'].isdigit() else None
    record['msl_height_ft'] = int(record['msl_height']) if record['msl_height'].isdigit() else None
    record['lighting_desc'] = LIGHTING_CODES.get(record['lighting'], 'Unknown')

    return record


def create_obstacles_table(conn: sqlite3.Connection):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS obstacles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            oas_number TEXT UNIQUE NOT NULL,
            country TEXT, state TEXT, city TEXT,
            latitude REAL NOT NULL, longitude REAL NOT NULL,
            obstacle_type TEXT, agl_height_ft INTEGER, msl_height_ft INTEGER,
            lighting TEXT, lighting_desc TEXT,
            horizontal_accuracy TEXT, vertical_accuracy TEXT,
            mark_indicator TEXT, faa_study_number TEXT,
            action TEXT, verification_status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.execute('CREATE INDEX IF NOT EXISTS idx_obstacles_coords ON obstacles(latitude, longitude)')
    conn.execute('CREATE INDEX IF NOT EXISTS idx_obstacles_msl ON obstacles(msl_height_ft)')
    conn.commit()


def main():
    parser = argparse.ArgumentParser(description='Parse FAA DOF into SQLite')
    parser.add_argument('--input', '-i', required=True, help='Path to DOF.DAT')
    parser.add_argument('--output', '-o', required=True, help='Path to SQLite database')
    parser.add_argument('--mode', '-m', choices=['replace', 'update'], default='replace')
    parser.add_argument('--verbose', '-v', action='store_true')
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: {input_path} not found")
        sys.exit(1)

    conn = sqlite3.connect(args.output)
    create_obstacles_table(conn)

    print(f"Parsing {input_path}...")
    count = errors = 0

    with open(input_path, 'r', encoding='latin-1') as f:
        for line in f:
            record = parse_dof_record(line)
            if record:
                try:
                    conn.execute('''
                        INSERT OR REPLACE INTO obstacles (
                            oas_number, country, state, city, latitude, longitude,
                            obstacle_type, agl_height_ft, msl_height_ft,
                            lighting, lighting_desc, horizontal_accuracy, vertical_accuracy,
                            mark_indicator, faa_study_number, action, verification_status
                        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    ''', (
                        record['oas_number'], record['country'], record['state'], record['city'],
                        record['latitude'], record['longitude'], record['obstacle_type'],
                        record['agl_height_ft'], record['msl_height_ft'],
                        record['lighting'], record['lighting_desc'],
                        record['horizontal_accuracy'], record['vertical_accuracy'],
                        record['mark_indicator'], record['faa_study_number'],
                        record['action'], record['verification_status']
                    ))
                    count += 1
                    if args.verbose and count % 50000 == 0:
                        print(f"  Processed {count} obstacles...")
                except sqlite3.Error:
                    errors += 1

    conn.commit()
    conn.close()
    print(f"\nComplete: {count} obstacles, {errors} errors")


if __name__ == '__main__':
    main()
