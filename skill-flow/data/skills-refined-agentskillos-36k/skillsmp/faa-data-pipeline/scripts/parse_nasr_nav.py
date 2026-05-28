#!/usr/bin/env python3
"""
Parse FAA NASR NAV.txt (NAVAID) file into SQLite database.

The NAV.txt file contains navigation aid data in fixed-width format.
Includes VORs, VORTACs, VORDMEs, NDBs, TACANs, and other NAVAIDs.

Usage:
    python parse_nasr_nav.py --input NAV.txt --output aviation.db
"""

import argparse
import sqlite3
import sys
from pathlib import Path
from typing import Optional


# NAV record field definitions (1-indexed positions)
NAV_FIELDS = {
    'record_type': (1, 4),              # Record type (NAV1, NAV2, etc.)
    'facility_id': (5, 8),              # NAVAID facility identifier
    'facility_type': (9, 28),           # NAVAID facility type
    'official_id': (29, 32),            # Official facility ID
    'effective_date': (33, 42),         # Effective date
    'name': (43, 72),                   # Name of NAVAID
    'city': (73, 112),                  # City
    'state_code': (113, 114),           # State code
    'state_name': (115, 144),           # State name
    'faa_region': (145, 147),           # FAA region
    'country': (148, 177),              # Country
    'country_code': (178, 179),         # Country code
    'owner_name': (180, 229),           # Owner name
    'operator_name': (230, 279),        # Operator name
    'common_system_usage': (280, 280),  # Common system usage (Y/N)
    'public_use': (281, 281),           # Public use (Y/N)
    'navaid_class': (282, 292),         # NAVAID class
    'hours_of_operation': (293, 303),   # Hours of operation
    'artcc': (304, 307),                # High altitude ARTCC
    'artcc_name': (308, 337),           # High altitude ARTCC name
    'low_artcc': (338, 341),            # Low altitude ARTCC
    'low_artcc_name': (342, 371),       # Low altitude ARTCC name
    'latitude_dms': (372, 385),         # Latitude (formatted)
    'latitude_secs': (386, 397),        # Latitude (seconds)
    'longitude_dms': (398, 412),        # Longitude (formatted)
    'longitude_secs': (413, 425),       # Longitude (seconds)
    'survey_accuracy': (426, 426),      # Survey accuracy
    'latitude_tacan': (427, 440),       # TACAN latitude
    'longitude_tacan': (441, 455),      # TACAN longitude
    'elevation': (456, 462),            # Elevation (tenths of feet)
    'mag_variation': (463, 467),        # Magnetic variation
    'mag_var_year': (468, 471),         # Magnetic variation epoch year
    'simultaneous_voice': (472, 475),   # Simultaneous voice feature
    'power_output': (476, 479),         # Power output (watts)
    'automatic_voice_id': (480, 483),   # Automatic voice ID
    'monitoring_category': (484, 484),  # Monitoring category
    'radio_voice_call': (485, 514),     # Radio voice call
    'tacan_channel': (515, 518),        # TACAN channel
    'frequency': (519, 524),            # Frequency
    'transmitted_id': (525, 528),       # Transmitted ID
    'fan_marker_type': (529, 538),      # Fan marker type
    'fan_marker_name': (539, 568),      # Fan marker name
    'vor_service_volume': (569, 608),   # VOR standard service volume
    'dme_service_volume': (609, 648),   # DME standard service volume
    'low_alt_use': (649, 688),          # Low altitude facility used in structure
    'z_marker': (689, 689),             # Z marker
    'tweb_hours': (690, 698),           # TWEB hours
    'tweb_phone': (699, 718),           # TWEB phone number
    'fss': (719, 722),                  # FSS identifier
    'fss_name': (723, 752),             # FSS name
    'fss_hours': (753, 769),            # FSS hours
    'notam_accountability': (770, 773), # NOTAM accountability code
    'quad_id': (774, 777),              # Quadrant identification
    'nav_status': (778, 807),           # NAVAID status
    'pitch_flag': (808, 808),           # Pitch flag
    'catch_flag': (809, 809),           # Catch flag
    'sua_atcaa_flag': (810, 810),       # SUA/ATCAA flag
    'restriction_flag': (811, 811),     # Restriction flag
    'hiwas_flag': (812, 812),           # HIWAS flag
    'tweb_flag': (813, 813),            # TWEB flag
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


def parse_nav_record(line: str) -> Optional[dict]:
    """Parse a single NAV record line."""
    record_type = extract_field(line, *NAV_FIELDS['record_type'])

    # Only parse NAV1 records (primary NAVAID data)
    if record_type != 'NAV1':
        return None

    record = {}
    for field_name, (start, end) in NAV_FIELDS.items():
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

    # Parse elevation
    try:
        elev = record['elevation'].strip()
        if elev:
            record['elevation_ft'] = float(elev) / 10.0
        else:
            record['elevation_ft'] = None
    except ValueError:
        record['elevation_ft'] = None

    # Parse magnetic variation
    try:
        mag_var = record['mag_variation'].strip()
        if mag_var:
            # Format: DDDDW or DDDDE (e.g., "0150W" = 15.0 West)
            if mag_var[-1] in ('E', 'W'):
                var_value = float(mag_var[:-1]) / 10.0
                if mag_var[-1] == 'W':
                    var_value = -var_value
                record['magnetic_variation'] = var_value
            else:
                record['magnetic_variation'] = None
        else:
            record['magnetic_variation'] = None
    except ValueError:
        record['magnetic_variation'] = None

    # Parse frequency
    try:
        freq = record['frequency'].strip()
        if freq:
            record['frequency_mhz'] = float(freq)
        else:
            record['frequency_mhz'] = None
    except ValueError:
        record['frequency_mhz'] = None

    # Determine NAVAID type category
    navaid_type = record['facility_type'].upper()
    if 'VORTAC' in navaid_type:
        record['type_category'] = 'VORTAC'
    elif 'VOR/DME' in navaid_type or 'VORDME' in navaid_type:
        record['type_category'] = 'VORDME'
    elif 'VOR' in navaid_type:
        record['type_category'] = 'VOR'
    elif 'TACAN' in navaid_type:
        record['type_category'] = 'TACAN'
    elif 'NDB' in navaid_type or 'NDBDME' in navaid_type:
        record['type_category'] = 'NDB'
    elif 'DME' in navaid_type:
        record['type_category'] = 'DME'
    else:
        record['type_category'] = 'OTHER'

    return record


def create_navaids_table(conn: sqlite3.Connection):
    """Create the navaids table if it doesn't exist."""
    conn.execute('''
        CREATE TABLE IF NOT EXISTS navaids (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            facility_id TEXT NOT NULL,
            facility_type TEXT,
            type_category TEXT,
            official_id TEXT,
            name TEXT,
            city TEXT,
            state_code TEXT,
            state_name TEXT,
            country TEXT,
            latitude REAL,
            longitude REAL,
            elevation_ft REAL,
            magnetic_variation REAL,
            frequency_mhz REAL,
            tacan_channel TEXT,
            transmitted_id TEXT,
            navaid_class TEXT,
            artcc TEXT,
            low_artcc TEXT,
            vor_service_volume TEXT,
            dme_service_volume TEXT,
            hours_of_operation TEXT,
            public_use TEXT,
            nav_status TEXT,
            effective_date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            UNIQUE(facility_id, facility_type)
        )
    ''')

    conn.execute('CREATE INDEX IF NOT EXISTS idx_navaids_id ON navaids(facility_id)')
    conn.execute('CREATE INDEX IF NOT EXISTS idx_navaids_type ON navaids(type_category)')
    conn.execute('CREATE INDEX IF NOT EXISTS idx_navaids_coords ON navaids(latitude, longitude)')

    conn.commit()


def insert_navaid(conn: sqlite3.Connection, record: dict) -> bool:
    """Insert a NAVAID record into the database."""
    try:
        conn.execute('''
            INSERT OR REPLACE INTO navaids (
                facility_id, facility_type, type_category, official_id, name,
                city, state_code, state_name, country,
                latitude, longitude, elevation_ft, magnetic_variation,
                frequency_mhz, tacan_channel, transmitted_id, navaid_class,
                artcc, low_artcc, vor_service_volume, dme_service_volume,
                hours_of_operation, public_use, nav_status, effective_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            record['facility_id'],
            record['facility_type'],
            record['type_category'],
            record['official_id'],
            record['name'],
            record['city'],
            record['state_code'],
            record['state_name'],
            record['country'],
            record['latitude'],
            record['longitude'],
            record['elevation_ft'],
            record['magnetic_variation'],
            record['frequency_mhz'],
            record['tacan_channel'],
            record['transmitted_id'],
            record['navaid_class'],
            record['artcc'],
            record['low_artcc'],
            record['vor_service_volume'],
            record['dme_service_volume'],
            record['hours_of_operation'],
            record['public_use'],
            record['nav_status'],
            record['effective_date']
        ))
        return True

    except sqlite3.Error as e:
        print(f"Error inserting NAVAID {record['facility_id']}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Parse FAA NASR NAV.txt into SQLite database'
    )

    parser.add_argument('--input', '-i', type=str, required=True, help='Path to NAV.txt file')
    parser.add_argument('--output', '-o', type=str, required=True, help='Path to SQLite database')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)

    conn = sqlite3.connect(args.output)
    create_navaids_table(conn)

    print(f"Parsing {input_path}...")

    count = 0
    errors = 0

    with open(input_path, 'r', encoding='latin-1') as f:
        for line_num, line in enumerate(f, 1):
            record = parse_nav_record(line)

            if record:
                if insert_navaid(conn, record):
                    count += 1
                    if args.verbose and count % 500 == 0:
                        print(f"  Processed {count} NAVAIDs...")
                else:
                    errors += 1

    conn.commit()
    conn.close()

    print(f"\nParsing complete:")
    print(f"  NAVAIDs inserted: {count}")
    print(f"  Errors: {errors}")
    print(f"  Database: {args.output}")


if __name__ == '__main__':
    main()
