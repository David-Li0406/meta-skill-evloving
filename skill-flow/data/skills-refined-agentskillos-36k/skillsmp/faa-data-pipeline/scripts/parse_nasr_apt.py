#!/usr/bin/env python3
"""
Parse FAA NASR APT.txt (Airport) file into SQLite database.

The APT.txt file contains airport facility data in fixed-width format.
Each record type is identified by the first 3 characters.

Record Types:
- APT: Airport basic data
- ATT: Attendance schedule
- RWY: Runway data (separate parser)
- ARS: Arresting system data
- RMK: Remarks

Usage:
    python parse_nasr_apt.py --input APT.txt --output aviation.db
"""

import argparse
import sqlite3
import sys
from pathlib import Path
from typing import Optional


# APT record field definitions (1-indexed positions from FAA spec)
APT_FIELDS = {
    'record_type': (1, 3),           # Record type (APT)
    'facility_site_number': (4, 14), # Landing facility site number
    'facility_type': (15, 27),       # Landing facility type
    'location_id': (28, 31),         # Location identifier (FAA ID)
    'effective_date': (32, 41),      # Information effective date
    'faa_region': (42, 44),          # FAA region code
    'faa_district': (45, 48),        # FAA district/field office code
    'state_code': (49, 50),          # Associated state post office code
    'state_name': (51, 70),          # Associated state name
    'county_name': (71, 91),         # Associated county name
    'county_state': (92, 93),        # Associated county's state
    'city_name': (94, 133),          # Associated city name
    'facility_name': (134, 183),     # Official facility name
    'ownership_type': (184, 185),    # Ownership type (PU, PR, MA, MN, MR)
    'use_type': (186, 187),          # Facility use (PU, PR)
    'owner_name': (188, 222),        # Owner's name
    'owner_address': (223, 294),     # Owner's address
    'owner_city_state_zip': (295, 339), # Owner's city, state, ZIP
    'owner_phone': (340, 355),       # Owner's phone
    'manager_name': (356, 390),      # Manager's name
    'manager_address': (391, 462),   # Manager's address
    'manager_city_state_zip': (463, 507), # Manager's city, state, ZIP
    'manager_phone': (508, 523),     # Manager's phone
    'latitude_dms': (524, 538),      # ARP latitude (formatted)
    'latitude_secs': (539, 550),     # ARP latitude (seconds)
    'longitude_dms': (551, 565),     # ARP longitude (formatted)
    'longitude_secs': (566, 578),    # ARP longitude (seconds)
    'coord_method': (579, 579),      # ARP determination method
    'elevation': (580, 586),         # ARP elevation (tenths of feet)
    'elevation_method': (587, 587),  # Elevation determination method
    'mag_variation': (588, 590),     # Magnetic variation
    'mag_var_direction': (591, 591), # Magnetic variation direction (E/W)
    'mag_var_year': (592, 595),      # Magnetic variation epoch year
    'pattern_altitude': (596, 599),  # Traffic pattern altitude (AGL)
    'sectional_chart': (600, 629),   # Sectional chart on which facility appears
    'distance_from_cbd': (630, 631), # Distance from central business district
    'direction_from_cbd': (632, 634), # Direction from CBD
    'land_area': (635, 639),         # Acres of land
    'boundary_artcc': (640, 643),    # Boundary ARTCC identifier
    'boundary_artcc_name': (644, 673), # Boundary ARTCC name
    'resp_artcc': (674, 677),        # Responsible ARTCC identifier
    'resp_artcc_name': (678, 707),   # Responsible ARTCC name
    'tie_in_fss': (708, 711),        # Tie-in FSS identifier
    'tie_in_fss_name': (712, 741),   # Tie-in FSS name
    'fss_local_phone': (742, 757),   # FSS local phone
    'fss_toll_free': (758, 773),     # FSS toll-free phone
    'notam_facility': (774, 777),    # NOTAM facility identifier
    'notam_d_available': (778, 778), # NOTAM D availability
    'activation_date': (779, 785),   # Activation date
    'status': (786, 787),            # Airport status code
    'certification_type': (788, 802), # FAR 139 certification type
    'federal_agreements': (803, 809), # Federal agreements
    'airspace_determination': (810, 822), # Airspace analysis determination
    'customs_entry': (823, 823),     # Customs airport of entry
    'customs_landing': (824, 824),   # Customs landing rights airport
    'military_joint_use': (825, 825), # Military/civil joint use
    'military_landing': (826, 826),  # Military landing rights
    'icao_id': (1211, 1217),         # ICAO identifier
}


def parse_coordinate(dms: str, seconds: str, is_longitude: bool = False) -> Optional[float]:
    """
    Parse FAA coordinate format to decimal degrees.

    Args:
        dms: Degrees-minutes-seconds string (e.g., "33-56-33.000N")
        seconds: High-precision seconds string
        is_longitude: True if parsing longitude

    Returns:
        Decimal degrees or None if parsing fails
    """
    try:
        dms = dms.strip()
        if not dms:
            return None

        # Extract direction (last character)
        direction = dms[-1].upper()
        dms = dms[:-1]

        # Parse degrees, minutes, seconds
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

        # Use high-precision seconds if available
        if seconds.strip():
            try:
                secs = float(seconds.strip())
            except ValueError:
                pass

        # Calculate decimal degrees
        decimal = degrees + (minutes / 60.0) + (secs / 3600.0)

        # Apply direction
        if direction in ('S', 'W'):
            decimal = -decimal

        return decimal

    except (ValueError, IndexError):
        return None


def extract_field(line: str, start: int, end: int) -> str:
    """
    Extract a field from a fixed-width line (1-indexed).

    Args:
        line: Full line of text
        start: Start position (1-indexed)
        end: End position (1-indexed, inclusive)

    Returns:
        Stripped field value
    """
    # Convert to 0-indexed
    start_idx = start - 1
    end_idx = end

    if len(line) >= end_idx:
        return line[start_idx:end_idx].strip()
    elif len(line) > start_idx:
        return line[start_idx:].strip()
    else:
        return ''


def parse_apt_record(line: str) -> Optional[dict]:
    """
    Parse a single APT record line.

    Args:
        line: Raw line from APT.txt

    Returns:
        Dictionary of parsed fields or None if not an APT record
    """
    record_type = extract_field(line, *APT_FIELDS['record_type'])

    if record_type != 'APT':
        return None

    # Extract all fields
    record = {}
    for field_name, (start, end) in APT_FIELDS.items():
        record[field_name] = extract_field(line, start, end)

    # Parse coordinates
    lat_decimal = parse_coordinate(
        record['latitude_dms'],
        record['latitude_secs'],
        is_longitude=False
    )

    lon_decimal = parse_coordinate(
        record['longitude_dms'],
        record['longitude_secs'],
        is_longitude=True
    )

    record['latitude'] = lat_decimal
    record['longitude'] = lon_decimal

    # Parse elevation
    try:
        elev_str = record['elevation'].replace('.', '').strip()
        if elev_str:
            record['elevation_ft'] = float(elev_str) / 10.0
        else:
            record['elevation_ft'] = None
    except ValueError:
        record['elevation_ft'] = None

    # Parse magnetic variation
    try:
        mag_var = record['mag_variation'].strip()
        mag_dir = record['mag_var_direction'].strip()
        if mag_var:
            var_value = float(mag_var)
            if mag_dir == 'W':
                var_value = -var_value
            record['magnetic_variation'] = var_value
        else:
            record['magnetic_variation'] = None
    except ValueError:
        record['magnetic_variation'] = None

    return record


def create_airports_table(conn: sqlite3.Connection):
    """Create the airports table if it doesn't exist."""
    conn.execute('''
        CREATE TABLE IF NOT EXISTS airports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            facility_site_number TEXT UNIQUE NOT NULL,
            location_id TEXT NOT NULL,
            icao_id TEXT,
            facility_name TEXT NOT NULL,
            facility_type TEXT,
            city_name TEXT,
            state_code TEXT,
            state_name TEXT,
            county_name TEXT,
            latitude REAL,
            longitude REAL,
            elevation_ft REAL,
            magnetic_variation REAL,
            ownership_type TEXT,
            use_type TEXT,
            owner_name TEXT,
            manager_name TEXT,
            pattern_altitude INTEGER,
            sectional_chart TEXT,
            boundary_artcc TEXT,
            resp_artcc TEXT,
            tie_in_fss TEXT,
            notam_facility TEXT,
            status TEXT,
            customs_entry TEXT,
            military_joint_use TEXT,
            effective_date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create indexes for common queries
    conn.execute('CREATE INDEX IF NOT EXISTS idx_airports_location_id ON airports(location_id)')
    conn.execute('CREATE INDEX IF NOT EXISTS idx_airports_icao_id ON airports(icao_id)')
    conn.execute('CREATE INDEX IF NOT EXISTS idx_airports_state ON airports(state_code)')
    conn.execute('CREATE INDEX IF NOT EXISTS idx_airports_coords ON airports(latitude, longitude)')

    conn.commit()


def insert_airport(conn: sqlite3.Connection, record: dict) -> bool:
    """
    Insert an airport record into the database.

    Args:
        conn: SQLite connection
        record: Parsed airport record

    Returns:
        True if insert successful
    """
    try:
        conn.execute('''
            INSERT OR REPLACE INTO airports (
                facility_site_number, location_id, icao_id, facility_name,
                facility_type, city_name, state_code, state_name, county_name,
                latitude, longitude, elevation_ft, magnetic_variation,
                ownership_type, use_type, owner_name, manager_name,
                pattern_altitude, sectional_chart, boundary_artcc, resp_artcc,
                tie_in_fss, notam_facility, status, customs_entry,
                military_joint_use, effective_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            record['facility_site_number'],
            record['location_id'],
            record['icao_id'] if record['icao_id'] else None,
            record['facility_name'],
            record['facility_type'],
            record['city_name'],
            record['state_code'],
            record['state_name'],
            record['county_name'],
            record['latitude'],
            record['longitude'],
            record['elevation_ft'],
            record['magnetic_variation'],
            record['ownership_type'],
            record['use_type'],
            record['owner_name'],
            record['manager_name'],
            int(record['pattern_altitude']) if record['pattern_altitude'].isdigit() else None,
            record['sectional_chart'],
            record['boundary_artcc'],
            record['resp_artcc'],
            record['tie_in_fss'],
            record['notam_facility'],
            record['status'],
            record['customs_entry'],
            record['military_joint_use'],
            record['effective_date']
        ))
        return True

    except sqlite3.Error as e:
        print(f"Error inserting airport {record['location_id']}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Parse FAA NASR APT.txt into SQLite database'
    )

    parser.add_argument(
        '--input', '-i',
        type=str,
        required=True,
        help='Path to APT.txt file'
    )

    parser.add_argument(
        '--output', '-o',
        type=str,
        required=True,
        help='Path to output SQLite database'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output'
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)

    # Connect to database
    conn = sqlite3.connect(args.output)
    create_airports_table(conn)

    # Parse file
    print(f"Parsing {input_path}...")

    count = 0
    errors = 0

    with open(input_path, 'r', encoding='latin-1') as f:
        for line_num, line in enumerate(f, 1):
            record = parse_apt_record(line)

            if record:
                if insert_airport(conn, record):
                    count += 1
                    if args.verbose and count % 1000 == 0:
                        print(f"  Processed {count} airports...")
                else:
                    errors += 1

    conn.commit()
    conn.close()

    print(f"\nParsing complete:")
    print(f"  Airports inserted: {count}")
    print(f"  Errors: {errors}")
    print(f"  Database: {args.output}")


if __name__ == '__main__':
    main()
