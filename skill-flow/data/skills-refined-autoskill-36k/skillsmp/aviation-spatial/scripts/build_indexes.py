#!/usr/bin/env python3
"""
Build spatial indexes for aviation database.

Populates geometry columns from lat/lon and creates R-Tree indexes.

Usage:
    python build_indexes.py --database aviation.db
"""

import argparse
import sqlite3
import sys
from pathlib import Path


def build_indexes(db_path: str, verbose: bool = False):
    """Build spatial indexes for all geometry tables."""

    conn = sqlite3.connect(db_path)
    conn.enable_load_extension(True)

    # Load SpatiaLite
    try:
        conn.execute("SELECT load_extension('mod_spatialite')")
    except sqlite3.OperationalError:
        try:
            conn.execute("SELECT load_extension('libspatialite')")
        except sqlite3.OperationalError:
            print("Error: SpatiaLite extension required for spatial indexes")
            sys.exit(1)

    print("Building spatial indexes...")

    # Populate point geometries
    point_tables = [
        ('airports', 'longitude', 'latitude'),
        ('navaids', 'longitude', 'latitude'),
        ('fixes', 'longitude', 'latitude'),
        ('obstacles', 'longitude', 'latitude'),
    ]

    for table, lon_col, lat_col in point_tables:
        print(f"  Updating {table} geometry...")
        try:
            result = conn.execute(f'''
                UPDATE {table}
                SET geometry = MakePoint({lon_col}, {lat_col}, 4326)
                WHERE {lon_col} IS NOT NULL
                AND {lat_col} IS NOT NULL
                AND geometry IS NULL
            ''')
            if verbose:
                print(f"    Updated {result.rowcount} rows")
        except sqlite3.OperationalError as e:
            print(f"    Warning: {e}")

    # Populate runway geometries (lines)
    print("  Updating runways geometry...")
    try:
        conn.execute('''
            UPDATE runways
            SET geometry = MakeLine(
                MakePoint(base_longitude, base_latitude, 4326),
                MakePoint(recip_longitude, recip_latitude, 4326)
            )
            WHERE base_longitude IS NOT NULL
            AND base_latitude IS NOT NULL
            AND recip_longitude IS NOT NULL
            AND recip_latitude IS NOT NULL
            AND geometry IS NULL
        ''')
    except sqlite3.OperationalError as e:
        print(f"    Warning: {e}")

    conn.commit()

    # Create spatial indexes
    spatial_tables = [
        'airports',
        'navaids',
        'fixes',
        'obstacles',
        'runways',
        'airspace',
    ]

    for table in spatial_tables:
        print(f"  Creating spatial index for {table}...")
        try:
            # Check if table has geometry column
            cursor = conn.execute(f"PRAGMA table_info({table})")
            columns = [row[1] for row in cursor.fetchall()]

            if 'geometry' not in columns:
                print(f"    Skipped (no geometry column)")
                continue

            # Check if index already exists
            cursor = conn.execute('''
                SELECT name FROM sqlite_master
                WHERE type = 'table'
                AND name = ?
            ''', (f"idx_{table}_geometry",))

            if cursor.fetchone():
                print(f"    Index already exists")
                continue

            # Create spatial index
            conn.execute(f"SELECT CreateSpatialIndex('{table}', 'geometry')")
            print(f"    Created")

        except sqlite3.OperationalError as e:
            print(f"    Warning: {e}")

    conn.commit()

    # Analyze tables for query optimization
    print("\nAnalyzing tables...")
    conn.execute("ANALYZE")
    conn.commit()

    # Get statistics
    print("\nDatabase statistics:")
    for table in ['airports', 'navaids', 'fixes', 'obstacles', 'airspace']:
        try:
            cursor = conn.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]

            cursor = conn.execute(f'''
                SELECT COUNT(*) FROM {table}
                WHERE geometry IS NOT NULL
            ''')
            geom_count = cursor.fetchone()[0]

            print(f"  {table}: {count} total, {geom_count} with geometry")
        except sqlite3.OperationalError:
            pass

    conn.close()
    print("\nDone!")


def main():
    parser = argparse.ArgumentParser(description='Build spatial indexes')
    parser.add_argument('--database', '-d', required=True, help='Database path')
    parser.add_argument('--verbose', '-v', action='store_true')
    args = parser.parse_args()

    if not Path(args.database).exists():
        print(f"Error: {args.database} not found")
        sys.exit(1)

    build_indexes(args.database, args.verbose)


if __name__ == '__main__':
    main()
