#!/usr/bin/env python3
"""
Parse FAA CIFP (Coded Instrument Flight Procedures) data into SQLite database.

CIFP data is in ARINC 424 format with 132-byte fixed-width records.
Contains:
- Airport reference points
- Approaches (ILS, RNAV, VOR, etc.)
- SIDs (Standard Instrument Departures)
- STARs (Standard Terminal Arrival Routes)
- Airways
- NAVAIDs

Usage:
    python parse_cifp.py --input FAACIFP18 --output aviation.db
"""

import argparse
import sqlite3
import sys
from pathlib import Path
from typing import Optional


# ARINC 424 record structure (1-indexed positions)
COMMON_FIELDS = {
    'record_type': (1, 1),              # Record type (S = standard)
    'customer_area': (2, 4),            # Customer/area code (USA)
    'section_code': (5, 5),             # Section code (P=airport, D=navaid, etc.)
    'subsection_code': (6, 6),          # Subsection code
}

# Airport (P) records - Section code 'P'
AIRPORT_FIELDS = {
    'airport_id': (7, 10),              # Airport ICAO identifier
    'icao_code': (11, 12),              # ICAO code
    'subsection': (13, 13),             # Subsection (A=ref point, F=approach, etc.)
    'ata_designator': (14, 16),         # ATA designator
    'continuation': (22, 22),           # Continuation record number
    'speed_limit_alt': (23, 27),        # Speed limit altitude
    'longest_runway': (28, 30),         # Longest runway (hundreds of feet)
    'ifr_capability': (31, 31),         # IFR capability
    'longest_surface': (32, 32),        # Longest runway surface code
    'latitude': (33, 41),               # ARP latitude (DDMMSSSS + N/S)
    'longitude': (42, 51),              # ARP longitude (DDDMMSSSS + E/W)
    'mag_variation': (52, 56),          # Magnetic variation
    'elevation': (57, 61),              # Airport elevation (feet)
    'speed_limit': (62, 64),            # Speed limit (knots)
    'recommended_navaid': (65, 68),     # Recommended NAVAID
    'transition_altitude': (79, 83),    # Transition altitude (feet)
    'transition_level': (84, 88),       # Transition level
    'public_military': (89, 89),        # Public/military indicator
    'time_zone': (90, 92),              # Time zone
    'daylight_indicator': (93, 93),     # Daylight savings indicator
    'magnetic_true_indicator': (94, 94), # Magnetic/true indicator
    'datum_code': (95, 97),             # Datum code
    'airport_name': (98, 128),          # Airport name
}

# Procedure records (SID/STAR/Approach)
PROCEDURE_FIELDS = {
    'airport_id': (7, 10),              # Airport ICAO identifier
    'icao_code': (11, 12),              # ICAO code
    'subsection': (13, 13),             # D=SID, E=STAR, F=Approach
    'procedure_id': (14, 19),           # Procedure identifier
    'route_type': (20, 20),             # Route type
    'transition_id': (21, 25),          # Transition identifier
    'sequence_number': (27, 29),        # Sequence number
    'fix_id': (30, 34),                 # Fix identifier
    'fix_icao': (35, 36),               # Fix ICAO code
    'fix_section': (37, 37),            # Fix section code
    'fix_subsection': (38, 38),         # Fix subsection code
    'continuation': (39, 39),           # Continuation record
    'waypoint_desc': (40, 43),          # Waypoint description code
    'turn_direction': (44, 44),         # Turn direction
    'rnp': (45, 47),                    # RNP value
    'path_termination': (48, 49),       # Path termination (IF, TF, CF, etc.)
    'turn_valid': (50, 50),             # Turn direction valid
    'rec_navaid': (51, 54),             # Recommended NAVAID
    'rec_navaid_icao': (55, 56),        # Recommended NAVAID ICAO
    'arc_radius': (57, 62),             # Arc radius
    'theta': (63, 66),                  # Theta (bearing)
    'rho': (67, 70),                    # Rho (distance)
    'outbound_mag_course': (71, 74),    # Outbound magnetic course
    'route_holding_dist_time': (75, 78), # Route distance or holding time
    'altitude_description': (83, 83),   # Altitude description
    'altitude1': (85, 89),              # Altitude 1
    'altitude2': (90, 94),              # Altitude 2
    'transition_altitude': (95, 99),    # Transition altitude
    'speed_limit': (100, 102),          # Speed limit
    'vertical_angle': (103, 106),       # Vertical angle
    'center_fix': (107, 111),           # Center fix
    'center_icao': (112, 113),          # Center fix ICAO
    'center_section': (114, 114),       # Center fix section
    'center_subsection': (115, 115),    # Center fix subsection
    'gns_fms_indicator': (116, 116),    # GNSS/FMS indicator
    'speed_limit_desc': (118, 118),     # Speed limit description
    'route_qual1': (119, 119),          # Route qualifier 1
    'route_qual2': (120, 120),          # Route qualifier 2
}

# Path termination types
LEG_TYPES = {
    'IF': 'Initial Fix',
    'TF': 'Track to Fix',
    'CF': 'Course to Fix',
    'DF': 'Direct to Fix',
    'FA': 'Fix to Altitude',
    'FC': 'Track from Fix to Distance',
    'FD': 'Track from Fix to DME',
    'FM': 'From Fix to Manual Termination',
    'CA': 'Course to Altitude',
    'CD': 'Course to DME Distance',
    'CI': 'Course to Intercept',
    'CR': 'Course to Radial Termination',
    'RF': 'Constant Radius Arc',
    'AF': 'Arc to Fix',
    'VA': 'Heading to Altitude',
    'VD': 'Heading to DME Distance',
    'VI': 'Heading to Intercept',
    'VM': 'Heading to Manual Termination',
    'VR': 'Heading to Radial Termination',
    'PI': 'Procedure Turn',
    'HA': 'Racetrack to Altitude',
    'HF': 'Racetrack to Fix',
    'HM': 'Racetrack to Manual Termination',
}


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


def parse_latitude(lat_str: str) -> Optional[float]:
    """Parse ARINC 424 latitude (DDMMSSSS + N/S)."""
    try:
        lat_str = lat_str.strip()
        if not lat_str or len(lat_str) < 8:
            return None

        direction = lat_str[-1]
        numbers = lat_str[:-1]

        degrees = int(numbers[0:2])
        minutes = int(numbers[2:4])
        seconds = int(numbers[4:]) / 100.0

        decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)

        if direction == 'S':
            decimal = -decimal

        return decimal

    except (ValueError, IndexError):
        return None


def parse_longitude(lon_str: str) -> Optional[float]:
    """Parse ARINC 424 longitude (DDDMMSSSS + E/W)."""
    try:
        lon_str = lon_str.strip()
        if not lon_str or len(lon_str) < 9:
            return None

        direction = lon_str[-1]
        numbers = lon_str[:-1]

        degrees = int(numbers[0:3])
        minutes = int(numbers[3:5])
        seconds = int(numbers[5:]) / 100.0

        decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)

        if direction == 'W':
            decimal = -decimal

        return decimal

    except (ValueError, IndexError):
        return None


def parse_altitude(alt_str: str) -> Optional[int]:
    """Parse altitude string."""
    try:
        alt_str = alt_str.strip()
        if not alt_str:
            return None

        # Remove leading zeros
        alt_str = alt_str.lstrip('0')
        if not alt_str:
            return 0

        # Handle FL altitudes
        if alt_str.startswith('FL'):
            return int(alt_str[2:]) * 100

        return int(alt_str)

    except ValueError:
        return None


def parse_mag_variation(var_str: str) -> Optional[float]:
    """Parse magnetic variation (DDDDT where T = E/W/T)."""
    try:
        var_str = var_str.strip()
        if not var_str or len(var_str) < 2:
            return None

        direction = var_str[-1]
        value = float(var_str[:-1]) / 10.0

        if direction == 'W':
            value = -value

        return value

    except ValueError:
        return None


def create_procedures_table(conn: sqlite3.Connection):
    """Create the procedures tables."""

    # Main procedures table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS procedures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            airport_id TEXT NOT NULL,
            procedure_id TEXT NOT NULL,
            procedure_type TEXT,
            procedure_name TEXT,
            transition_id TEXT,
            route_type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            UNIQUE(airport_id, procedure_id, transition_id)
        )
    ''')

    # Procedure legs table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS procedure_legs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            airport_id TEXT NOT NULL,
            procedure_id TEXT NOT NULL,
            transition_id TEXT,
            sequence_number INTEGER,
            fix_id TEXT,
            fix_icao TEXT,
            path_termination TEXT,
            path_termination_desc TEXT,
            turn_direction TEXT,
            outbound_course REAL,
            distance_time TEXT,
            altitude_desc TEXT,
            altitude1 INTEGER,
            altitude2 INTEGER,
            speed_limit INTEGER,
            vertical_angle REAL,
            rnp REAL,
            arc_radius REAL,
            center_fix TEXT,
            waypoint_desc TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (airport_id, procedure_id, transition_id)
                REFERENCES procedures(airport_id, procedure_id, transition_id)
        )
    ''')

    conn.execute('CREATE INDEX IF NOT EXISTS idx_procedures_airport ON procedures(airport_id)')
    conn.execute('CREATE INDEX IF NOT EXISTS idx_procedures_type ON procedures(procedure_type)')
    conn.execute('CREATE INDEX IF NOT EXISTS idx_legs_procedure ON procedure_legs(airport_id, procedure_id)')
    conn.execute('CREATE INDEX IF NOT EXISTS idx_legs_fix ON procedure_legs(fix_id)')

    conn.commit()


def parse_procedure_record(line: str) -> Optional[dict]:
    """Parse a procedure record (SID/STAR/Approach)."""
    if len(line) < 132:
        return None

    section = extract_field(line, 5, 5)
    subsection = extract_field(line, 13, 13)

    # Only parse procedure records
    if section != 'P' or subsection not in ('D', 'E', 'F'):
        return None

    record = {}
    for field_name, (start, end) in PROCEDURE_FIELDS.items():
        record[field_name] = extract_field(line, start, end)

    # Determine procedure type
    if subsection == 'D':
        record['procedure_type'] = 'SID'
    elif subsection == 'E':
        record['procedure_type'] = 'STAR'
    elif subsection == 'F':
        record['procedure_type'] = 'APPROACH'

    # Parse path termination
    path_term = record['path_termination']
    record['path_termination_desc'] = LEG_TYPES.get(path_term, '')

    # Parse numeric values
    try:
        record['sequence_num'] = int(record['sequence_number']) if record['sequence_number'] else 0
    except ValueError:
        record['sequence_num'] = 0

    try:
        course_str = record['outbound_mag_course']
        if course_str:
            record['outbound_course_deg'] = float(course_str) / 10.0
        else:
            record['outbound_course_deg'] = None
    except ValueError:
        record['outbound_course_deg'] = None

    record['altitude1_ft'] = parse_altitude(record['altitude1'])
    record['altitude2_ft'] = parse_altitude(record['altitude2'])

    try:
        speed = record['speed_limit']
        record['speed_limit_kts'] = int(speed) if speed else None
    except ValueError:
        record['speed_limit_kts'] = None

    try:
        rnp_str = record['rnp']
        if rnp_str:
            record['rnp_value'] = float(rnp_str) / 10.0
        else:
            record['rnp_value'] = None
    except ValueError:
        record['rnp_value'] = None

    try:
        arc_str = record['arc_radius']
        if arc_str:
            record['arc_radius_nm'] = float(arc_str) / 1000.0
        else:
            record['arc_radius_nm'] = None
    except ValueError:
        record['arc_radius_nm'] = None

    try:
        va_str = record['vertical_angle']
        if va_str:
            record['vertical_angle_deg'] = float(va_str) / 100.0
        else:
            record['vertical_angle_deg'] = None
    except ValueError:
        record['vertical_angle_deg'] = None

    return record


def insert_procedure_leg(conn: sqlite3.Connection, record: dict) -> bool:
    """Insert a procedure leg."""
    try:
        # Insert or update procedure
        conn.execute('''
            INSERT OR IGNORE INTO procedures (
                airport_id, procedure_id, procedure_type, transition_id, route_type
            ) VALUES (?, ?, ?, ?, ?)
        ''', (
            record['airport_id'],
            record['procedure_id'],
            record['procedure_type'],
            record['transition_id'],
            record['route_type']
        ))

        # Insert leg
        conn.execute('''
            INSERT INTO procedure_legs (
                airport_id, procedure_id, transition_id, sequence_number,
                fix_id, fix_icao, path_termination, path_termination_desc,
                turn_direction, outbound_course, distance_time,
                altitude_desc, altitude1, altitude2, speed_limit,
                vertical_angle, rnp, arc_radius, center_fix, waypoint_desc
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            record['airport_id'],
            record['procedure_id'],
            record['transition_id'],
            record['sequence_num'],
            record['fix_id'],
            record['fix_icao'],
            record['path_termination'],
            record['path_termination_desc'],
            record['turn_direction'],
            record['outbound_course_deg'],
            record['route_holding_dist_time'],
            record['altitude_description'],
            record['altitude1_ft'],
            record['altitude2_ft'],
            record['speed_limit_kts'],
            record['vertical_angle_deg'],
            record['rnp_value'],
            record['arc_radius_nm'],
            record['center_fix'],
            record['waypoint_desc']
        ))

        return True

    except sqlite3.Error as e:
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Parse FAA CIFP (ARINC 424) data into SQLite database'
    )

    parser.add_argument('--input', '-i', type=str, required=True, help='Path to CIFP file')
    parser.add_argument('--output', '-o', type=str, required=True, help='Path to SQLite database')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)

    conn = sqlite3.connect(args.output)
    create_procedures_table(conn)

    print(f"Parsing {input_path}...")

    procedures_count = 0
    legs_count = 0
    errors = 0

    with open(input_path, 'r', encoding='latin-1') as f:
        for line_num, line in enumerate(f, 1):
            record = parse_procedure_record(line)

            if record:
                if insert_procedure_leg(conn, record):
                    legs_count += 1
                    if args.verbose and legs_count % 10000 == 0:
                        print(f"  Processed {legs_count} procedure legs...")
                else:
                    errors += 1

    # Count unique procedures
    cursor = conn.execute('SELECT COUNT(*) FROM procedures')
    procedures_count = cursor.fetchone()[0]

    conn.commit()
    conn.close()

    print(f"\nParsing complete:")
    print(f"  Procedures: {procedures_count}")
    print(f"  Procedure legs: {legs_count}")
    print(f"  Errors: {errors}")
    print(f"  Database: {args.output}")


if __name__ == '__main__':
    main()
