#!/usr/bin/env python3
"""
Initialize a SpatiaLite database for aviation data.

Creates all tables with geometry columns and spatial indexes.

Usage:
    python init_spatialite.py --output aviation.db
"""

import argparse
import sqlite3
import sys
from pathlib import Path


def init_spatialite(db_path: str):
    """Initialize SpatiaLite database with aviation schema."""
    conn = sqlite3.connect(db_path)
    conn.enable_load_extension(True)

    # Try to load SpatiaLite
    try:
        conn.execute("SELECT load_extension('mod_spatialite')")
    except sqlite3.OperationalError:
        try:
            conn.execute("SELECT load_extension('libspatialite')")
        except sqlite3.OperationalError:
            print("Warning: SpatiaLite extension not available.")
            print("Spatial functions will not work. Install SpatiaLite.")

    # Initialize spatial metadata
    try:
        conn.execute("SELECT InitSpatialMetaData(1)")
    except sqlite3.OperationalError:
        pass  # Already initialized

    # Create tables
    print("Creating tables...")

    # Airports
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
            latitude REAL,
            longitude REAL,
            elevation_ft REAL,
            magnetic_variation REAL,
            has_tower INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Runways
    conn.execute('''
        CREATE TABLE IF NOT EXISTS runways (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            facility_site_number TEXT NOT NULL,
            runway_id TEXT NOT NULL,
            length_ft INTEGER,
            width_ft INTEGER,
            surface_type TEXT,
            base_id TEXT,
            base_heading INTEGER,
            base_latitude REAL,
            base_longitude REAL,
            recip_id TEXT,
            recip_heading INTEGER,
            recip_latitude REAL,
            recip_longitude REAL,
            ils_type TEXT,
            FOREIGN KEY (facility_site_number) REFERENCES airports(facility_site_number)
        )
    ''')

    # NAVAIDs
    conn.execute('''
        CREATE TABLE IF NOT EXISTS navaids (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            facility_id TEXT NOT NULL,
            facility_type TEXT,
            type_category TEXT,
            name TEXT,
            latitude REAL,
            longitude REAL,
            elevation_ft REAL,
            frequency_mhz REAL,
            tacan_channel TEXT,
            magnetic_variation REAL,
            nav_status TEXT
        )
    ''')

    # Fixes
    conn.execute('''
        CREATE TABLE IF NOT EXISTS fixes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fix_id TEXT NOT NULL,
            state_code TEXT,
            latitude REAL,
            longitude REAL,
            fix_type TEXT,
            fix_use TEXT
        )
    ''')

    # Obstacles
    conn.execute('''
        CREATE TABLE IF NOT EXISTS obstacles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            oas_number TEXT UNIQUE NOT NULL,
            state TEXT,
            city TEXT,
            latitude REAL,
            longitude REAL,
            obstacle_type TEXT,
            agl_height_ft INTEGER,
            msl_height_ft INTEGER,
            lighting TEXT
        )
    ''')

    # Airspace
    conn.execute('''
        CREATE TABLE IF NOT EXISTS airspace (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            class TEXT,
            lower_altitude_ft INTEGER,
            upper_altitude_ft INTEGER,
            lower_altitude_ref TEXT,
            upper_altitude_ref TEXT,
            controlling_agency TEXT
        )
    ''')

    # Add geometry columns
    print("Adding geometry columns...")

    geometry_tables = [
        ('airports', 'POINT'),
        ('navaids', 'POINT'),
        ('fixes', 'POINT'),
        ('obstacles', 'POINT'),
        ('runways', 'LINESTRING'),
        ('airspace', 'MULTIPOLYGON'),
    ]

    for table, geom_type in geometry_tables:
        try:
            conn.execute(f'''
                SELECT AddGeometryColumn('{table}', 'geometry', 4326, '{geom_type}', 'XY')
            ''')
            print(f"  Added geometry to {table}")
        except sqlite3.OperationalError as e:
            if 'already exists' in str(e).lower():
                print(f"  {table} geometry already exists")
            else:
                print(f"  Warning: {table}: {e}")

    # Create regular indexes
    print("Creating indexes...")

    indexes = [
        ('idx_airports_location', 'airports', 'location_id'),
        ('idx_airports_icao', 'airports', 'icao_id'),
        ('idx_airports_state', 'airports', 'state_code'),
        ('idx_navaids_id', 'navaids', 'facility_id'),
        ('idx_navaids_type', 'navaids', 'type_category'),
        ('idx_fixes_id', 'fixes', 'fix_id'),
        ('idx_obstacles_msl', 'obstacles', 'msl_height_ft'),
        ('idx_airspace_type', 'airspace', 'type'),
        ('idx_runways_facility', 'runways', 'facility_site_number'),
    ]

    for idx_name, table, column in indexes:
        try:
            conn.execute(f'CREATE INDEX IF NOT EXISTS {idx_name} ON {table}({column})')
        except sqlite3.OperationalError:
            pass

    conn.commit()
    conn.close()

    print(f"\nDatabase initialized: {db_path}")


def main():
    parser = argparse.ArgumentParser(description='Initialize SpatiaLite aviation database')
    parser.add_argument('--output', '-o', required=True, help='Output database path')
    args = parser.parse_args()

    init_spatialite(args.output)


if __name__ == '__main__':
    main()
