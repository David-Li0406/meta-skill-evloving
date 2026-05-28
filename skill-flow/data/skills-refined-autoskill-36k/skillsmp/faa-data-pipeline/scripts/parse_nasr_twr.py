#!/usr/bin/env python3
"""
Parse FAA NASR TWR.txt (Tower/Frequency) file into SQLite database.

The TWR.txt file contains airport communication frequencies in fixed-width format.
Includes tower, ground, approach, departure, ATIS, clearance delivery, etc.

Usage:
    python parse_nasr_twr.py --input TWR.txt --output aviation.db
"""

import argparse
import sqlite3
import sys
from pathlib import Path
from typing import Optional


# TWR1 record field definitions (tower data)
TWR1_FIELDS = {
    'record_type': (1, 4),              # Record type (TWR1)
    'terminal_id': (5, 8),              # Terminal communications facility ID
    'info_effective_date': (9, 18),     # Information effective date
    'facility_site_number': (19, 29),   # Landing facility site number
    'faa_region': (30, 32),             # FAA region code
    'state_code': (33, 34),             # Associated state code
    'state_name': (35, 64),             # Associated state name
    'city': (65, 104),                  # Associated city
    'facility_name': (105, 154),        # Airport name
    'latitude': (155, 168),             # Latitude
    'longitude': (169, 183),            # Longitude
    'tie_in_fss': (184, 187),           # Tie-in FSS
    'tie_in_fss_name': (188, 217),      # Tie-in FSS name
    'facility_type': (218, 229),        # Facility type (e.g., ATCT, NON-ATCT)
    'hours_operation': (230, 236),      # Hours of operation
    'hours_daylight': (237, 237),       # Hours of daylight operation
    'regulation_type': (238, 241),      # Regulation type
    'master_airport_id': (242, 245),    # Master airport location ID
    'master_airport_name': (246, 295),  # Master airport name
    'direction_finding': (296, 296),    # Direction finding equipment
}

# TWR3 record field definitions (frequency data)
TWR3_FIELDS = {
    'record_type': (1, 4),              # Record type (TWR3)
    'terminal_id': (5, 8),              # Terminal communications facility ID
    'freq_use': (9, 23),                # Frequency use (ATIS, GND, TWR, etc.)
    'frequency': (24, 67),              # Frequency(ies)
    'frequency_class': (68, 68),        # Frequency class
    'frequency_sectorization': (69, 138), # Sectorization narrative
}

# TWR7 record field definitions (satellite frequency data)
TWR7_FIELDS = {
    'record_type': (1, 4),              # Record type (TWR7)
    'terminal_id': (5, 8),              # Terminal communications facility ID
    'satellite_airport_id': (9, 12),    # Satellite airport location ID
    'satellite_airport_name': (13, 62), # Satellite airport name
    'master_airport_freq_use': (63, 77), # Master airport frequency use
    'satellite_airport_freq_use': (78, 92), # Satellite airport frequency use
    'satellite_frequency': (93, 101),   # Satellite frequency
}

# Frequency type mappings
FREQ_TYPES = {
    'ATIS': 'ATIS',
    'AWOS': 'AWOS',
    'ASOS': 'ASOS',
    'GND': 'GROUND',
    'TWR': 'TOWER',
    'APCH': 'APPROACH',
    'DEP': 'DEPARTURE',
    'CD': 'CLEARANCE',
    'CLNC': 'CLEARANCE',
    'CTAF': 'CTAF',
    'UNIC': 'UNICOM',
    'MULT': 'MULTICOM',
    'CNTR': 'CENTER',
    'EFAS': 'EFAS',  # Flight Watch
    'FSS': 'FSS',
    'EMERG': 'EMERGENCY',
    'PTD': 'PRETAXI',
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


def parse_coordinate(coord_str: str) -> Optional[float]:
    """Parse a coordinate string to decimal degrees."""
    try:
        coord_str = coord_str.strip()
        if not coord_str:
            return None

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


def parse_frequency(freq_str: str) -> list[dict]:
    """Parse frequency string and return list of frequencies."""
    frequencies = []
    freq_str = freq_str.strip()

    if not freq_str:
        return frequencies

    # Split on common delimiters
    parts = freq_str.replace('/', ' ').replace(',', ' ').split()

    for part in parts:
        try:
            # Clean up the frequency
            clean = ''.join(c for c in part if c.isdigit() or c == '.')
            if clean:
                freq_mhz = float(clean)
                # Valid aviation frequencies are typically 118.0-136.975 MHz (VHF)
                # or 225-400 MHz (UHF military)
                if 118.0 <= freq_mhz <= 137.0 or 225.0 <= freq_mhz <= 400.0:
                    frequencies.append({'frequency': freq_mhz})
                elif 1.0 <= freq_mhz <= 30.0:
                    # Could be HF frequency
                    frequencies.append({'frequency': freq_mhz})
        except ValueError:
            continue

    return frequencies


def normalize_freq_use(freq_use: str) -> str:
    """Normalize frequency use type."""
    freq_use = freq_use.upper().strip()

    for key, value in FREQ_TYPES.items():
        if key in freq_use:
            return value

    return freq_use


def parse_twr1_record(line: str) -> Optional[dict]:
    """Parse a TWR1 (tower) record."""
    record_type = extract_field(line, *TWR1_FIELDS['record_type'])

    if record_type != 'TWR1':
        return None

    record = {'type': 'tower'}
    for field_name, (start, end) in TWR1_FIELDS.items():
        record[field_name] = extract_field(line, start, end)

    record['latitude_dec'] = parse_coordinate(record['latitude'])
    record['longitude_dec'] = parse_coordinate(record['longitude'])

    return record


def parse_twr3_record(line: str) -> Optional[dict]:
    """Parse a TWR3 (frequency) record."""
    record_type = extract_field(line, *TWR3_FIELDS['record_type'])

    if record_type != 'TWR3':
        return None

    record = {'type': 'frequency'}
    for field_name, (start, end) in TWR3_FIELDS.items():
        record[field_name] = extract_field(line, start, end)

    record['freq_use_normalized'] = normalize_freq_use(record['freq_use'])
    record['parsed_frequencies'] = parse_frequency(record['frequency'])

    return record


def create_frequencies_table(conn: sqlite3.Connection):
    """Create the airport frequencies table."""
    conn.execute('''
        CREATE TABLE IF NOT EXISTS airport_frequencies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            facility_site_number TEXT,
            terminal_id TEXT,
            airport_name TEXT,
            frequency_type TEXT,
            frequency_mhz REAL,
            frequency_use TEXT,
            sectorization TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            UNIQUE(facility_site_number, frequency_type, frequency_mhz)
        )
    ''')

    conn.execute('CREATE INDEX IF NOT EXISTS idx_freqs_facility ON airport_frequencies(facility_site_number)')
    conn.execute('CREATE INDEX IF NOT EXISTS idx_freqs_terminal ON airport_frequencies(terminal_id)')
    conn.execute('CREATE INDEX IF NOT EXISTS idx_freqs_type ON airport_frequencies(frequency_type)')

    conn.commit()


def main():
    parser = argparse.ArgumentParser(
        description='Parse FAA NASR TWR.txt into SQLite database'
    )

    parser.add_argument('--input', '-i', type=str, required=True, help='Path to TWR.txt file')
    parser.add_argument('--output', '-o', type=str, required=True, help='Path to SQLite database')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)

    conn = sqlite3.connect(args.output)
    create_frequencies_table(conn)

    print(f"Parsing {input_path}...")

    # First pass: collect tower info
    towers = {}

    with open(input_path, 'r', encoding='latin-1') as f:
        for line in f:
            record = parse_twr1_record(line)
            if record:
                towers[record['terminal_id']] = record

    print(f"  Found {len(towers)} tower facilities")

    # Second pass: parse frequencies
    count = 0
    errors = 0

    with open(input_path, 'r', encoding='latin-1') as f:
        for line in f:
            record = parse_twr3_record(line)

            if record and record['parsed_frequencies']:
                terminal_id = record['terminal_id']
                tower = towers.get(terminal_id, {})

                for freq_data in record['parsed_frequencies']:
                    try:
                        conn.execute('''
                            INSERT OR REPLACE INTO airport_frequencies (
                                facility_site_number, terminal_id, airport_name,
                                frequency_type, frequency_mhz, frequency_use, sectorization
                            ) VALUES (?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            tower.get('facility_site_number', ''),
                            terminal_id,
                            tower.get('facility_name', ''),
                            record['freq_use_normalized'],
                            freq_data['frequency'],
                            record['freq_use'],
                            record['frequency_sectorization']
                        ))
                        count += 1

                        if args.verbose and count % 1000 == 0:
                            print(f"  Processed {count} frequencies...")

                    except sqlite3.Error as e:
                        errors += 1
                        if args.verbose:
                            print(f"  Error: {e}")

    conn.commit()
    conn.close()

    print(f"\nParsing complete:")
    print(f"  Frequencies inserted: {count}")
    print(f"  Errors: {errors}")
    print(f"  Database: {args.output}")


if __name__ == '__main__':
    main()
