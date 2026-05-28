#!/usr/bin/env python3
"""
Parse FAA NASR RWY.txt (Runway) file into SQLite database.

The RWY.txt file contains runway data in fixed-width format.
Each airport can have multiple runways, and each runway has two
reciprocal ends (base end and reciprocal end).

Usage:
    python parse_nasr_rwy.py --input RWY.txt --output aviation.db
"""

import argparse
import sqlite3
import sys
from pathlib import Path
from typing import Optional


# RWY record field definitions (1-indexed positions from FAA spec)
RWY_FIELDS = {
    'record_type': (1, 3),              # Record type (RWY)
    'facility_site_number': (4, 14),    # Landing facility site number
    'state_code': (15, 16),             # State code
    'runway_id': (17, 23),              # Runway identification (e.g., "09/27")
    'runway_length': (24, 28),          # Physical runway length (feet)
    'runway_width': (29, 32),           # Physical runway width (feet)
    'surface_type': (33, 44),           # Runway surface type and condition
    'surface_treatment': (45, 49),      # Runway surface treatment
    'pcn': (50, 60),                    # Pavement classification number
    'edge_lights': (61, 65),            # Edge light intensity

    # Base end data
    'base_id': (66, 68),                # Base end identifier
    'base_true_hdg': (69, 71),          # Base end true alignment
    'base_ils_type': (72, 81),          # Base end ILS type
    'base_rgt_traffic': (82, 82),       # Base end right traffic pattern
    'base_rwy_markings': (83, 87),      # Base end runway markings
    'base_rwy_condition': (88, 88),     # Base end runway markings condition
    'base_latitude': (89, 103),         # Base end latitude (formatted)
    'base_lat_secs': (104, 115),        # Base end latitude (seconds)
    'base_longitude': (116, 130),       # Base end longitude (formatted)
    'base_lon_secs': (131, 143),        # Base end longitude (seconds)
    'base_elevation': (144, 150),       # Base end elevation (tenths of feet)
    'base_threshold_xing_ht': (151, 153), # Base end threshold crossing height
    'base_glide_path_angle': (154, 157), # Base end visual glide path angle
    'base_displaced_threshold': (158, 161), # Base end displaced threshold (feet)
    'base_tora': (162, 166),            # Base end TORA (feet)
    'base_toda': (167, 171),            # Base end TODA (feet)
    'base_asda': (172, 176),            # Base end ASDA (feet)
    'base_lda': (177, 181),             # Base end LDA (feet)
    'base_lahso': (182, 188),           # Base end LAHSO distance
    'base_lahso_id': (189, 195),        # Base end LAHSO intersecting runway
    'base_vgsi': (196, 200),            # Base end VGSI
    'base_rvr': (201, 203),             # Base end RVR equipment
    'base_reil': (204, 204),            # Base end REIL
    'base_centerline_lights': (205, 205), # Base end centerline lights
    'base_tdz_lights': (206, 206),      # Base end touchdown zone lights

    # Reciprocal end data
    'recip_id': (288, 290),             # Reciprocal end identifier
    'recip_true_hdg': (291, 293),       # Reciprocal end true alignment
    'recip_ils_type': (294, 303),       # Reciprocal end ILS type
    'recip_rgt_traffic': (304, 304),    # Reciprocal end right traffic pattern
    'recip_rwy_markings': (305, 309),   # Reciprocal end runway markings
    'recip_rwy_condition': (310, 310),  # Reciprocal end runway markings condition
    'recip_latitude': (311, 325),       # Reciprocal end latitude
    'recip_lat_secs': (326, 337),       # Reciprocal end latitude (seconds)
    'recip_longitude': (338, 352),      # Reciprocal end longitude
    'recip_lon_secs': (353, 365),       # Reciprocal end longitude (seconds)
    'recip_elevation': (366, 372),      # Reciprocal end elevation
    'recip_threshold_xing_ht': (373, 375), # Reciprocal end threshold crossing height
    'recip_glide_path_angle': (376, 379), # Reciprocal end visual glide path angle
    'recip_displaced_threshold': (380, 383), # Reciprocal end displaced threshold
    'recip_tora': (384, 388),           # Reciprocal end TORA
    'recip_toda': (389, 393),           # Reciprocal end TODA
    'recip_asda': (394, 398),           # Reciprocal end ASDA
    'recip_lda': (399, 403),            # Reciprocal end LDA
    'recip_lahso': (404, 410),          # Reciprocal end LAHSO distance
    'recip_lahso_id': (411, 417),       # Reciprocal end LAHSO intersecting runway
    'recip_vgsi': (418, 422),           # Reciprocal end VGSI
    'recip_rvr': (423, 425),            # Reciprocal end RVR equipment
    'recip_reil': (426, 426),           # Reciprocal end REIL
    'recip_centerline_lights': (427, 427), # Reciprocal end centerline lights
    'recip_tdz_lights': (428, 428),     # Reciprocal end touchdown zone lights
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


def parse_int(value: str) -> Optional[int]:
    """Parse an integer value, returning None if not valid."""
    value = value.strip()
    if value and value.isdigit():
        return int(value)
    return None


def parse_float(value: str, divisor: float = 1.0) -> Optional[float]:
    """Parse a float value with optional divisor."""
    try:
        value = value.strip()
        if value:
            return float(value) / divisor
        return None
    except ValueError:
        return None


def parse_rwy_record(line: str) -> Optional[dict]:
    """Parse a single RWY record line."""
    record_type = extract_field(line, *RWY_FIELDS['record_type'])

    if record_type != 'RWY':
        return None

    record = {}
    for field_name, (start, end) in RWY_FIELDS.items():
        record[field_name] = extract_field(line, start, end)

    # Parse numeric values
    record['length_ft'] = parse_int(record['runway_length'])
    record['width_ft'] = parse_int(record['runway_width'])

    # Parse base end coordinates
    record['base_latitude_dec'] = parse_coordinate(
        record['base_latitude'],
        record['base_lat_secs'],
        is_longitude=False
    )
    record['base_longitude_dec'] = parse_coordinate(
        record['base_longitude'],
        record['base_lon_secs'],
        is_longitude=True
    )
    record['base_elevation_ft'] = parse_float(record['base_elevation'], 10.0)
    record['base_true_heading'] = parse_int(record['base_true_hdg'])
    record['base_displaced_ft'] = parse_int(record['base_displaced_threshold'])
    record['base_tora_ft'] = parse_int(record['base_tora'])
    record['base_toda_ft'] = parse_int(record['base_toda'])
    record['base_asda_ft'] = parse_int(record['base_asda'])
    record['base_lda_ft'] = parse_int(record['base_lda'])

    # Parse reciprocal end coordinates
    record['recip_latitude_dec'] = parse_coordinate(
        record['recip_latitude'],
        record['recip_lat_secs'],
        is_longitude=False
    )
    record['recip_longitude_dec'] = parse_coordinate(
        record['recip_longitude'],
        record['recip_lon_secs'],
        is_longitude=True
    )
    record['recip_elevation_ft'] = parse_float(record['recip_elevation'], 10.0)
    record['recip_true_heading'] = parse_int(record['recip_true_hdg'])
    record['recip_displaced_ft'] = parse_int(record['recip_displaced_threshold'])
    record['recip_tora_ft'] = parse_int(record['recip_tora'])
    record['recip_toda_ft'] = parse_int(record['recip_toda'])
    record['recip_asda_ft'] = parse_int(record['recip_asda'])
    record['recip_lda_ft'] = parse_int(record['recip_lda'])

    return record


def create_runways_table(conn: sqlite3.Connection):
    """Create the runways table if it doesn't exist."""
    conn.execute('''
        CREATE TABLE IF NOT EXISTS runways (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            facility_site_number TEXT NOT NULL,
            runway_id TEXT NOT NULL,
            length_ft INTEGER,
            width_ft INTEGER,
            surface_type TEXT,
            surface_treatment TEXT,
            pcn TEXT,
            edge_lights TEXT,

            -- Base end
            base_id TEXT,
            base_true_heading INTEGER,
            base_latitude REAL,
            base_longitude REAL,
            base_elevation_ft REAL,
            base_displaced_ft INTEGER,
            base_tora_ft INTEGER,
            base_toda_ft INTEGER,
            base_asda_ft INTEGER,
            base_lda_ft INTEGER,
            base_ils_type TEXT,
            base_rgt_traffic TEXT,
            base_markings TEXT,
            base_vgsi TEXT,
            base_reil TEXT,
            base_centerline_lights TEXT,
            base_tdz_lights TEXT,

            -- Reciprocal end
            recip_id TEXT,
            recip_true_heading INTEGER,
            recip_latitude REAL,
            recip_longitude REAL,
            recip_elevation_ft REAL,
            recip_displaced_ft INTEGER,
            recip_tora_ft INTEGER,
            recip_toda_ft INTEGER,
            recip_asda_ft INTEGER,
            recip_lda_ft INTEGER,
            recip_ils_type TEXT,
            recip_rgt_traffic TEXT,
            recip_markings TEXT,
            recip_vgsi TEXT,
            recip_reil TEXT,
            recip_centerline_lights TEXT,
            recip_tdz_lights TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            UNIQUE(facility_site_number, runway_id),
            FOREIGN KEY (facility_site_number) REFERENCES airports(facility_site_number)
        )
    ''')

    conn.execute('CREATE INDEX IF NOT EXISTS idx_runways_facility ON runways(facility_site_number)')
    conn.execute('CREATE INDEX IF NOT EXISTS idx_runways_length ON runways(length_ft)')

    conn.commit()


def insert_runway(conn: sqlite3.Connection, record: dict) -> bool:
    """Insert a runway record into the database."""
    try:
        conn.execute('''
            INSERT OR REPLACE INTO runways (
                facility_site_number, runway_id, length_ft, width_ft,
                surface_type, surface_treatment, pcn, edge_lights,
                base_id, base_true_heading, base_latitude, base_longitude,
                base_elevation_ft, base_displaced_ft, base_tora_ft, base_toda_ft,
                base_asda_ft, base_lda_ft, base_ils_type, base_rgt_traffic,
                base_markings, base_vgsi, base_reil, base_centerline_lights, base_tdz_lights,
                recip_id, recip_true_heading, recip_latitude, recip_longitude,
                recip_elevation_ft, recip_displaced_ft, recip_tora_ft, recip_toda_ft,
                recip_asda_ft, recip_lda_ft, recip_ils_type, recip_rgt_traffic,
                recip_markings, recip_vgsi, recip_reil, recip_centerline_lights, recip_tdz_lights
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            record['facility_site_number'],
            record['runway_id'],
            record['length_ft'],
            record['width_ft'],
            record['surface_type'],
            record['surface_treatment'],
            record['pcn'],
            record['edge_lights'],
            record['base_id'],
            record['base_true_heading'],
            record['base_latitude_dec'],
            record['base_longitude_dec'],
            record['base_elevation_ft'],
            record['base_displaced_ft'],
            record['base_tora_ft'],
            record['base_toda_ft'],
            record['base_asda_ft'],
            record['base_lda_ft'],
            record['base_ils_type'],
            record['base_rgt_traffic'],
            record['base_rwy_markings'],
            record['base_vgsi'],
            record['base_reil'],
            record['base_centerline_lights'],
            record['base_tdz_lights'],
            record['recip_id'],
            record['recip_true_heading'],
            record['recip_latitude_dec'],
            record['recip_longitude_dec'],
            record['recip_elevation_ft'],
            record['recip_displaced_ft'],
            record['recip_tora_ft'],
            record['recip_toda_ft'],
            record['recip_asda_ft'],
            record['recip_lda_ft'],
            record['recip_ils_type'],
            record['recip_rgt_traffic'],
            record['recip_rwy_markings'],
            record['recip_vgsi'],
            record['recip_reil'],
            record['recip_centerline_lights'],
            record['recip_tdz_lights']
        ))
        return True

    except sqlite3.Error as e:
        print(f"Error inserting runway {record['runway_id']}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Parse FAA NASR RWY.txt into SQLite database'
    )

    parser.add_argument('--input', '-i', type=str, required=True, help='Path to RWY.txt file')
    parser.add_argument('--output', '-o', type=str, required=True, help='Path to SQLite database')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)

    conn = sqlite3.connect(args.output)
    create_runways_table(conn)

    print(f"Parsing {input_path}...")

    count = 0
    errors = 0

    with open(input_path, 'r', encoding='latin-1') as f:
        for line_num, line in enumerate(f, 1):
            record = parse_rwy_record(line)

            if record:
                if insert_runway(conn, record):
                    count += 1
                    if args.verbose and count % 1000 == 0:
                        print(f"  Processed {count} runways...")
                else:
                    errors += 1

    conn.commit()
    conn.close()

    print(f"\nParsing complete:")
    print(f"  Runways inserted: {count}")
    print(f"  Errors: {errors}")
    print(f"  Database: {args.output}")


if __name__ == '__main__':
    main()
