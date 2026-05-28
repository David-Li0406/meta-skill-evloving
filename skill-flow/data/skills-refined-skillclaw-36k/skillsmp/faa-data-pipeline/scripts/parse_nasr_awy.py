#!/usr/bin/env python3
"""
Parse FAA NASR AWY*.txt (Airways) files into SQLite database.

The AWY files contain airway data in fixed-width format.
Includes Victor Airways, Jet Routes, RNAV routes, etc.

AWY1: Airway segment data
AWY2: Airway segment fix data

Usage:
    python parse_nasr_awy.py --input ./faa_raw/ --output aviation.db
"""

import argparse
import sqlite3
import sys
from pathlib import Path
from typing import Optional


# AWY1 record field definitions (airway data)
AWY1_FIELDS = {
    'record_type': (1, 4),              # Record type (AWY1)
    'airway_id': (5, 9),                # Airway identifier (e.g., V1, J146)
    'airway_type': (10, 13),            # Airway type
    'sequence_number': (14, 18),        # Sequence number
    'from_fix': (19, 48),               # From fix name
    'from_fix_state': (49, 50),         # From fix state
    'from_fix_icao': (51, 52),          # From fix ICAO region
    'to_fix': (53, 82),                 # To fix name
    'to_fix_state': (83, 84),           # To fix state
    'to_fix_icao': (85, 86),            # To fix ICAO region
    'mea': (87, 91),                    # MEA (Minimum Enroute Altitude)
    'mea_direction': (92, 92),          # MEA direction
    'max_altitude': (93, 97),           # Maximum authorized altitude
    'moa': (98, 102),                   # MOA (Minimum Obstruction Altitude)
    'maa': (103, 107),                  # MAA (Maximum Authorized Altitude)
    'airway_segment_distance': (108, 111),  # Segment distance (NM)
    'changeover_point': (112, 115),     # Changeover point distance
    'mea_opposite': (116, 120),         # MEA in opposite direction
    'mca': (121, 125),                  # MCA (Minimum Crossing Altitude)
    'mca_direction': (126, 131),        # MCA direction
    'from_latitude': (132, 145),        # From fix latitude
    'from_longitude': (146, 160),       # From fix longitude
    'to_latitude': (161, 174),          # To fix latitude
    'to_longitude': (175, 189),         # To fix longitude
    'course_out': (190, 196),           # True course outbound
    'course_in': (197, 203),            # True course inbound
}

# AWY2 record field definitions (airway remarks)
AWY2_FIELDS = {
    'record_type': (1, 4),              # Record type (AWY2)
    'airway_id': (5, 9),                # Airway identifier
    'airway_type': (10, 13),            # Airway type
    'sequence_number': (14, 18),        # Sequence number
    'remark_type': (19, 28),            # Remark type
    'remark_text': (29, 228),           # Remark text
}


def parse_coordinate(coord_str: str) -> Optional[float]:
    """Parse a coordinate string to decimal degrees."""
    try:
        coord_str = coord_str.strip()
        if not coord_str:
            return None

        # Handle format like "33-56-33.000N" or decimal format
        if any(c in coord_str for c in ['-', 'N', 'S', 'E', 'W']):
            direction = coord_str[-1].upper()
            coord_str = coord_str[:-1]

            parts = coord_str.replace('-', ' ').split()
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

            decimal = degrees + (minutes / 60.0) + (secs / 3600.0)

            if direction in ('S', 'W'):
                decimal = -decimal

            return decimal
        else:
            return float(coord_str)

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


def parse_int(value: str) -> Optional[int]:
    """Parse an integer, returning None if invalid."""
    value = value.strip()
    if value:
        try:
            return int(value)
        except ValueError:
            pass
    return None


def parse_float(value: str) -> Optional[float]:
    """Parse a float, returning None if invalid."""
    value = value.strip()
    if value:
        try:
            return float(value)
        except ValueError:
            pass
    return None


def parse_awy1_record(line: str) -> Optional[dict]:
    """Parse a single AWY1 record line."""
    record_type = extract_field(line, *AWY1_FIELDS['record_type'])

    if record_type != 'AWY1':
        return None

    record = {}
    for field_name, (start, end) in AWY1_FIELDS.items():
        record[field_name] = extract_field(line, start, end)

    # Determine airway type category
    airway_id = record['airway_id'].upper()
    if airway_id.startswith('V'):
        record['airway_category'] = 'VICTOR'
    elif airway_id.startswith('J'):
        record['airway_category'] = 'JET'
    elif airway_id.startswith('T'):
        record['airway_category'] = 'TANGO'  # RNAV
    elif airway_id.startswith('Q'):
        record['airway_category'] = 'Q'  # RNAV
    else:
        record['airway_category'] = 'OTHER'

    # Parse numeric values
    record['sequence_num'] = parse_int(record['sequence_number'])
    record['mea_ft'] = parse_int(record['mea']) * 100 if parse_int(record['mea']) else None
    record['max_alt_ft'] = parse_int(record['max_altitude']) * 100 if parse_int(record['max_altitude']) else None
    record['moa_ft'] = parse_int(record['moa']) * 100 if parse_int(record['moa']) else None
    record['maa_ft'] = parse_int(record['maa']) * 100 if parse_int(record['maa']) else None
    record['distance_nm'] = parse_float(record['airway_segment_distance'])
    record['changeover_nm'] = parse_float(record['changeover_point'])

    # Parse coordinates
    record['from_lat'] = parse_coordinate(record['from_latitude'])
    record['from_lon'] = parse_coordinate(record['from_longitude'])
    record['to_lat'] = parse_coordinate(record['to_latitude'])
    record['to_lon'] = parse_coordinate(record['to_longitude'])

    # Parse courses
    record['course_out_deg'] = parse_float(record['course_out'])
    record['course_in_deg'] = parse_float(record['course_in'])

    return record


def create_airways_table(conn: sqlite3.Connection):
    """Create the airways and airway_segments tables."""
    # Main airways table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS airways (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            airway_id TEXT NOT NULL UNIQUE,
            airway_type TEXT,
            airway_category TEXT,
            segment_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Airway segments table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS airway_segments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            airway_id TEXT NOT NULL,
            sequence_number INTEGER,
            from_fix TEXT,
            from_fix_state TEXT,
            to_fix TEXT,
            to_fix_state TEXT,
            from_latitude REAL,
            from_longitude REAL,
            to_latitude REAL,
            to_longitude REAL,
            mea_ft INTEGER,
            max_altitude_ft INTEGER,
            moa_ft INTEGER,
            maa_ft INTEGER,
            distance_nm REAL,
            changeover_nm REAL,
            course_out_deg REAL,
            course_in_deg REAL,
            mea_direction TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            UNIQUE(airway_id, sequence_number),
            FOREIGN KEY (airway_id) REFERENCES airways(airway_id)
        )
    ''')

    conn.execute('CREATE INDEX IF NOT EXISTS idx_airways_id ON airways(airway_id)')
    conn.execute('CREATE INDEX IF NOT EXISTS idx_airways_category ON airways(airway_category)')
    conn.execute('CREATE INDEX IF NOT EXISTS idx_segments_airway ON airway_segments(airway_id)')
    conn.execute('CREATE INDEX IF NOT EXISTS idx_segments_fixes ON airway_segments(from_fix, to_fix)')

    conn.commit()


def insert_airway_segment(conn: sqlite3.Connection, record: dict) -> bool:
    """Insert an airway segment record."""
    try:
        # Insert or update airway
        conn.execute('''
            INSERT OR IGNORE INTO airways (airway_id, airway_type, airway_category)
            VALUES (?, ?, ?)
        ''', (record['airway_id'], record['airway_type'], record['airway_category']))

        # Insert segment
        conn.execute('''
            INSERT OR REPLACE INTO airway_segments (
                airway_id, sequence_number,
                from_fix, from_fix_state, to_fix, to_fix_state,
                from_latitude, from_longitude, to_latitude, to_longitude,
                mea_ft, max_altitude_ft, moa_ft, maa_ft,
                distance_nm, changeover_nm, course_out_deg, course_in_deg,
                mea_direction
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            record['airway_id'],
            record['sequence_num'],
            record['from_fix'],
            record['from_fix_state'],
            record['to_fix'],
            record['to_fix_state'],
            record['from_lat'],
            record['from_lon'],
            record['to_lat'],
            record['to_lon'],
            record['mea_ft'],
            record['max_alt_ft'],
            record['moa_ft'],
            record['maa_ft'],
            record['distance_nm'],
            record['changeover_nm'],
            record['course_out_deg'],
            record['course_in_deg'],
            record['mea_direction']
        ))

        return True

    except sqlite3.Error as e:
        print(f"Error inserting segment for {record['airway_id']}: {e}")
        return False


def update_airway_counts(conn: sqlite3.Connection):
    """Update segment counts for airways."""
    conn.execute('''
        UPDATE airways SET segment_count = (
            SELECT COUNT(*) FROM airway_segments
            WHERE airway_segments.airway_id = airways.airway_id
        )
    ''')
    conn.commit()


def main():
    parser = argparse.ArgumentParser(
        description='Parse FAA NASR AWY files into SQLite database'
    )

    parser.add_argument('--input', '-i', type=str, required=True,
                       help='Path to directory containing AWY*.txt files or single AWY.txt')
    parser.add_argument('--output', '-o', type=str, required=True, help='Path to SQLite database')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    args = parser.parse_args()

    input_path = Path(args.input)

    # Find AWY files
    if input_path.is_dir():
        awy_files = list(input_path.glob('AWY*.txt')) + list(input_path.glob('awy*.txt'))
    else:
        awy_files = [input_path] if input_path.exists() else []

    if not awy_files:
        print(f"Error: No AWY files found in {input_path}")
        sys.exit(1)

    conn = sqlite3.connect(args.output)
    create_airways_table(conn)

    total_count = 0
    total_errors = 0

    for awy_file in awy_files:
        print(f"Parsing {awy_file}...")

        count = 0
        errors = 0

        with open(awy_file, 'r', encoding='latin-1') as f:
            for line_num, line in enumerate(f, 1):
                record = parse_awy1_record(line)

                if record:
                    if insert_airway_segment(conn, record):
                        count += 1
                        if args.verbose and count % 1000 == 0:
                            print(f"  Processed {count} segments...")
                    else:
                        errors += 1

        print(f"  Segments: {count}, Errors: {errors}")
        total_count += count
        total_errors += errors

    # Update segment counts
    update_airway_counts(conn)

    conn.commit()
    conn.close()

    print(f"\nParsing complete:")
    print(f"  Total segments inserted: {total_count}")
    print(f"  Total errors: {total_errors}")
    print(f"  Database: {args.output}")


if __name__ == '__main__':
    main()
