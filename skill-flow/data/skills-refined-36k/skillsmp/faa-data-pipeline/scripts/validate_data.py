#!/usr/bin/env python3
"""
Validate FAA aviation database integrity.

Checks:
- Expected record counts
- Foreign key relationships
- Coordinate ranges
- Required field presence
- Identifier format validation

Usage:
    python validate_data.py --database aviation.db
    python validate_data.py --database aviation.db --expected-airports 19000
"""

import argparse
import sqlite3
import sys
from pathlib import Path


# Expected minimums for US aviation data
EXPECTED_COUNTS = {
    'airports': 19000,
    'runways': 25000,
    'navaids': 3000,
    'fixes': 50000,
    'airways': 300,
    'airway_segments': 5000,
    'procedures': 10000,
    'procedure_legs': 100000,
    'obstacles': 500000,
    'charts': 10000,
    'airport_frequencies': 20000,
}


def check_table_exists(conn: sqlite3.Connection, table: str) -> bool:
    """Check if a table exists in the database."""
    cursor = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
        (table,)
    )
    return cursor.fetchone() is not None


def get_table_count(conn: sqlite3.Connection, table: str) -> int:
    """Get the row count for a table."""
    if not check_table_exists(conn, table):
        return -1
    cursor = conn.execute(f"SELECT COUNT(*) FROM {table}")
    return cursor.fetchone()[0]


def check_coordinate_ranges(conn: sqlite3.Connection) -> list[str]:
    """Validate coordinate ranges for all tables with lat/lon."""
    issues = []

    tables_with_coords = [
        ('airports', 'latitude', 'longitude'),
        ('navaids', 'latitude', 'longitude'),
        ('fixes', 'latitude', 'longitude'),
        ('obstacles', 'latitude', 'longitude'),
    ]

    for table, lat_col, lon_col in tables_with_coords:
        if not check_table_exists(conn, table):
            continue

        # Check latitude range (-90 to 90)
        cursor = conn.execute(f'''
            SELECT COUNT(*) FROM {table}
            WHERE {lat_col} IS NOT NULL
            AND ({lat_col} < -90 OR {lat_col} > 90)
        ''')
        invalid_lat = cursor.fetchone()[0]
        if invalid_lat > 0:
            issues.append(f"{table}: {invalid_lat} records with invalid latitude")

        # Check longitude range (-180 to 180)
        cursor = conn.execute(f'''
            SELECT COUNT(*) FROM {table}
            WHERE {lon_col} IS NOT NULL
            AND ({lon_col} < -180 OR {lon_col} > 180)
        ''')
        invalid_lon = cursor.fetchone()[0]
        if invalid_lon > 0:
            issues.append(f"{table}: {invalid_lon} records with invalid longitude")

        # Check for null coordinates
        cursor = conn.execute(f'''
            SELECT COUNT(*) FROM {table}
            WHERE {lat_col} IS NULL OR {lon_col} IS NULL
        ''')
        null_coords = cursor.fetchone()[0]
        if null_coords > 0:
            issues.append(f"{table}: {null_coords} records with null coordinates")

    return issues


def check_required_fields(conn: sqlite3.Connection) -> list[str]:
    """Check for required fields that should not be null."""
    issues = []

    required_checks = [
        ('airports', 'location_id', 'location_id'),
        ('airports', 'facility_name', 'facility_name'),
        ('navaids', 'facility_id', 'facility_id'),
        ('fixes', 'fix_id', 'fix_id'),
        ('procedures', 'procedure_id', 'procedure_id'),
        ('obstacles', 'oas_number', 'oas_number'),
    ]

    for table, field, desc in required_checks:
        if not check_table_exists(conn, table):
            continue

        cursor = conn.execute(f'''
            SELECT COUNT(*) FROM {table}
            WHERE {field} IS NULL OR {field} = ''
        ''')
        null_count = cursor.fetchone()[0]
        if null_count > 0:
            issues.append(f"{table}: {null_count} records with missing {desc}")

    return issues


def check_foreign_keys(conn: sqlite3.Connection) -> list[str]:
    """Check foreign key relationships."""
    issues = []

    # Runways should reference valid airports
    if check_table_exists(conn, 'runways') and check_table_exists(conn, 'airports'):
        cursor = conn.execute('''
            SELECT COUNT(*) FROM runways r
            LEFT JOIN airports a ON r.facility_site_number = a.facility_site_number
            WHERE a.id IS NULL
        ''')
        orphan_runways = cursor.fetchone()[0]
        if orphan_runways > 0:
            issues.append(f"runways: {orphan_runways} orphan records (no matching airport)")

    # Procedure legs should reference valid procedures
    if check_table_exists(conn, 'procedure_legs') and check_table_exists(conn, 'procedures'):
        cursor = conn.execute('''
            SELECT COUNT(DISTINCT pl.airport_id || pl.procedure_id)
            FROM procedure_legs pl
            LEFT JOIN procedures p ON pl.airport_id = p.airport_id
                AND pl.procedure_id = p.procedure_id
            WHERE p.id IS NULL
        ''')
        orphan_legs = cursor.fetchone()[0]
        if orphan_legs > 0:
            issues.append(f"procedure_legs: {orphan_legs} orphan procedure references")

    return issues


def check_identifier_formats(conn: sqlite3.Connection) -> list[str]:
    """Check identifier format validity."""
    issues = []

    # Airport identifiers should be 3-4 characters
    if check_table_exists(conn, 'airports'):
        cursor = conn.execute('''
            SELECT COUNT(*) FROM airports
            WHERE LENGTH(location_id) < 3 OR LENGTH(location_id) > 4
        ''')
        invalid_ids = cursor.fetchone()[0]
        if invalid_ids > 0:
            issues.append(f"airports: {invalid_ids} records with invalid identifier length")

    # ICAO identifiers should be 4 characters when present
    if check_table_exists(conn, 'airports'):
        cursor = conn.execute('''
            SELECT COUNT(*) FROM airports
            WHERE icao_id IS NOT NULL AND icao_id != ''
            AND LENGTH(icao_id) != 4
        ''')
        invalid_icao = cursor.fetchone()[0]
        if invalid_icao > 0:
            issues.append(f"airports: {invalid_icao} records with invalid ICAO identifier")

    return issues


def get_statistics(conn: sqlite3.Connection) -> dict:
    """Get database statistics."""
    stats = {}

    for table in EXPECTED_COUNTS.keys():
        stats[table] = get_table_count(conn, table)

    # Additional statistics
    if check_table_exists(conn, 'airports'):
        cursor = conn.execute('SELECT COUNT(DISTINCT state_code) FROM airports')
        stats['states'] = cursor.fetchone()[0]

    if check_table_exists(conn, 'procedures'):
        cursor = conn.execute('SELECT COUNT(*) FROM procedures WHERE procedure_type = "APPROACH"')
        stats['approaches'] = cursor.fetchone()[0]
        cursor = conn.execute('SELECT COUNT(*) FROM procedures WHERE procedure_type = "SID"')
        stats['sids'] = cursor.fetchone()[0]
        cursor = conn.execute('SELECT COUNT(*) FROM procedures WHERE procedure_type = "STAR"')
        stats['stars'] = cursor.fetchone()[0]

    return stats


def main():
    parser = argparse.ArgumentParser(description='Validate FAA aviation database')
    parser.add_argument('--database', '-d', required=True, help='Path to SQLite database')
    parser.add_argument('--expected-airports', type=int, help='Expected minimum airports')
    parser.add_argument('--strict', action='store_true', help='Fail on any issue')
    parser.add_argument('--verbose', '-v', action='store_true')
    args = parser.parse_args()

    db_path = Path(args.database)
    if not db_path.exists():
        print(f"Error: Database not found: {db_path}")
        sys.exit(1)

    conn = sqlite3.connect(args.database)
    print(f"Validating {args.database}...")

    all_issues = []

    # Check record counts
    print("\n=== Record Counts ===")
    stats = get_statistics(conn)
    for table, count in stats.items():
        if count == -1:
            print(f"  {table}: TABLE NOT FOUND")
            continue

        expected = EXPECTED_COUNTS.get(table, 0)
        if args.expected_airports and table == 'airports':
            expected = args.expected_airports

        status = "OK" if count >= expected else "LOW"
        if count < expected:
            all_issues.append(f"{table}: {count} records (expected >= {expected})")

        print(f"  {table}: {count:,} {'[' + status + ']' if expected > 0 else ''}")

    # Check coordinate ranges
    print("\n=== Coordinate Validation ===")
    coord_issues = check_coordinate_ranges(conn)
    all_issues.extend(coord_issues)
    if coord_issues:
        for issue in coord_issues:
            print(f"  WARNING: {issue}")
    else:
        print("  All coordinates valid")

    # Check required fields
    print("\n=== Required Fields ===")
    field_issues = check_required_fields(conn)
    all_issues.extend(field_issues)
    if field_issues:
        for issue in field_issues:
            print(f"  WARNING: {issue}")
    else:
        print("  All required fields present")

    # Check foreign keys
    print("\n=== Foreign Key Relationships ===")
    fk_issues = check_foreign_keys(conn)
    all_issues.extend(fk_issues)
    if fk_issues:
        for issue in fk_issues:
            print(f"  WARNING: {issue}")
    else:
        print("  All relationships valid")

    # Check identifier formats
    print("\n=== Identifier Formats ===")
    id_issues = check_identifier_formats(conn)
    all_issues.extend(id_issues)
    if id_issues:
        for issue in id_issues:
            print(f"  WARNING: {issue}")
    else:
        print("  All identifiers valid")

    conn.close()

    # Summary
    print("\n=== Summary ===")
    if all_issues:
        print(f"  {len(all_issues)} issues found:")
        for issue in all_issues:
            print(f"    - {issue}")
        if args.strict:
            sys.exit(1)
    else:
        print("  All validations passed!")


if __name__ == '__main__':
    main()
