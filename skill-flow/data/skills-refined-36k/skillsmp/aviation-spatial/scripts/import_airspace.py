#!/usr/bin/env python3
"""
Import airspace data from GeoJSON into SpatiaLite database.

Usage:
    python import_airspace.py --input airspace.geojson --output aviation.db
"""

import argparse
import json
import sqlite3
import sys
from pathlib import Path


def import_airspace(input_path: str, db_path: str, verbose: bool = False):
    """Import airspace GeoJSON into database."""

    # Load GeoJSON
    print(f"Loading {input_path}...")
    with open(input_path, 'r') as f:
        data = json.load(f)

    if data.get('type') != 'FeatureCollection':
        print("Error: Input must be a GeoJSON FeatureCollection")
        sys.exit(1)

    features = data.get('features', [])
    print(f"Found {len(features)} features")

    # Connect to database
    conn = sqlite3.connect(db_path)
    conn.enable_load_extension(True)

    try:
        conn.execute("SELECT load_extension('mod_spatialite')")
    except sqlite3.OperationalError:
        try:
            conn.execute("SELECT load_extension('libspatialite')")
        except sqlite3.OperationalError:
            print("Warning: SpatiaLite not available. Using basic import.")

    # Import features
    count = 0
    errors = 0

    for feature in features:
        try:
            props = feature.get('properties', {})
            geometry = feature.get('geometry', {})

            if not geometry:
                continue

            # Extract properties
            name = props.get('name', props.get('NAME', 'Unknown'))
            airspace_type = props.get('type', props.get('TYPE', props.get('class', 'UNKNOWN')))
            airspace_class = props.get('class', props.get('CLASS', None))
            lower_alt = props.get('lower_altitude', props.get('LOWER', None))
            upper_alt = props.get('upper_altitude', props.get('UPPER', None))
            lower_ref = props.get('lower_ref', 'MSL')
            upper_ref = props.get('upper_ref', 'MSL')
            agency = props.get('controlling_agency', props.get('agency', None))

            # Convert geometry to WKT
            geom_type = geometry.get('type')
            coords = geometry.get('coordinates', [])

            if geom_type == 'Polygon':
                wkt = polygon_to_wkt(coords)
            elif geom_type == 'MultiPolygon':
                wkt = multipolygon_to_wkt(coords)
            else:
                if verbose:
                    print(f"  Skipping unsupported geometry type: {geom_type}")
                continue

            # Insert into database
            conn.execute('''
                INSERT INTO airspace (
                    name, type, class,
                    lower_altitude_ft, upper_altitude_ft,
                    lower_altitude_ref, upper_altitude_ref,
                    controlling_agency, geometry
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, GeomFromText(?, 4326))
            ''', (
                name, airspace_type, airspace_class,
                lower_alt, upper_alt,
                lower_ref, upper_ref,
                agency, wkt
            ))

            count += 1

            if verbose and count % 100 == 0:
                print(f"  Imported {count} airspaces...")

        except Exception as e:
            errors += 1
            if verbose:
                print(f"  Error: {e}")

    conn.commit()
    conn.close()

    print(f"\nImport complete:")
    print(f"  Imported: {count}")
    print(f"  Errors: {errors}")


def polygon_to_wkt(coords):
    """Convert GeoJSON polygon coordinates to WKT."""
    rings = []
    for ring in coords:
        points = ', '.join(f"{p[0]} {p[1]}" for p in ring)
        rings.append(f"({points})")
    return f"POLYGON({', '.join(rings)})"


def multipolygon_to_wkt(coords):
    """Convert GeoJSON multipolygon coordinates to WKT."""
    polygons = []
    for polygon in coords:
        rings = []
        for ring in polygon:
            points = ', '.join(f"{p[0]} {p[1]}" for p in ring)
            rings.append(f"({points})")
        polygons.append(f"({', '.join(rings)})")
    return f"MULTIPOLYGON({', '.join(polygons)})"


def main():
    parser = argparse.ArgumentParser(description='Import airspace GeoJSON')
    parser.add_argument('--input', '-i', required=True, help='Input GeoJSON file')
    parser.add_argument('--output', '-o', required=True, help='Output database')
    parser.add_argument('--verbose', '-v', action='store_true')
    args = parser.parse_args()

    if not Path(args.input).exists():
        print(f"Error: {args.input} not found")
        sys.exit(1)

    import_airspace(args.input, args.output, args.verbose)


if __name__ == '__main__':
    main()
