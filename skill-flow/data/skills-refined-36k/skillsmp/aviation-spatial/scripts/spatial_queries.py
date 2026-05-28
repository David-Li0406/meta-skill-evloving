#!/usr/bin/env python3
"""
Common spatial query functions for aviation database.

Usage:
    python spatial_queries.py --database aviation.db --test-nearest --lat 33.9425 --lon -118.4081
"""

import argparse
import sqlite3
import sys
from pathlib import Path
from typing import Optional


class AviationSpatialDB:
    """Spatial query interface for aviation database."""

    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.conn.enable_load_extension(True)

        # Try to load SpatiaLite
        try:
            self.conn.execute("SELECT load_extension('mod_spatialite')")
            self.has_spatialite = True
        except sqlite3.OperationalError:
            try:
                self.conn.execute("SELECT load_extension('libspatialite')")
                self.has_spatialite = True
            except sqlite3.OperationalError:
                self.has_spatialite = False
                print("Warning: SpatiaLite not available. Using fallback queries.")

    def find_nearby_airports(
        self,
        lat: float,
        lon: float,
        radius_nm: float = 50,
        limit: int = 20
    ) -> list[dict]:
        """Find airports within radius of a point."""

        if self.has_spatialite:
            # Use spatial index
            radius_deg = radius_nm / 60.0
            query = '''
                SELECT
                    location_id,
                    icao_id,
                    facility_name,
                    city_name,
                    state_code,
                    latitude,
                    longitude,
                    elevation_ft,
                    ST_Distance(geometry, MakePoint(?, ?, 4326), 1) / 1852.0 AS distance_nm
                FROM airports
                WHERE ROWID IN (
                    SELECT ROWID FROM SpatialIndex
                    WHERE f_table_name = 'airports'
                    AND f_geometry_column = 'geometry'
                    AND search_frame = BuildCircleMbr(?, ?, ?, 4326)
                )
                ORDER BY distance_nm
                LIMIT ?
            '''
            params = (lon, lat, lon, lat, radius_deg, limit)
        else:
            # Fallback to bounding box approximation
            radius_deg = radius_nm / 60.0
            query = '''
                SELECT
                    location_id,
                    icao_id,
                    facility_name,
                    city_name,
                    state_code,
                    latitude,
                    longitude,
                    elevation_ft,
                    (
                        3440.065 * 2 * ASIN(SQRT(
                            POWER(SIN(RADIANS(latitude - ?) / 2), 2) +
                            COS(RADIANS(?)) * COS(RADIANS(latitude)) *
                            POWER(SIN(RADIANS(longitude - ?) / 2), 2)
                        ))
                    ) AS distance_nm
                FROM airports
                WHERE latitude BETWEEN ? AND ?
                AND longitude BETWEEN ? AND ?
                ORDER BY distance_nm
                LIMIT ?
            '''
            params = (
                lat, lat, lon,
                lat - radius_deg, lat + radius_deg,
                lon - radius_deg, lon + radius_deg,
                limit
            )

        cursor = self.conn.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

    def find_airports_with_runway(
        self,
        lat: float,
        lon: float,
        min_length_ft: int,
        radius_nm: float = 50
    ) -> list[dict]:
        """Find airports with runway >= minimum length."""

        radius_deg = radius_nm / 60.0
        query = '''
            SELECT
                a.location_id,
                a.facility_name,
                a.latitude,
                a.longitude,
                MAX(r.length_ft) as longest_runway
            FROM airports a
            JOIN runways r ON a.facility_site_number = r.facility_site_number
            WHERE a.latitude BETWEEN ? AND ?
            AND a.longitude BETWEEN ? AND ?
            AND r.length_ft >= ?
            GROUP BY a.id
            ORDER BY longest_runway DESC
        '''

        cursor = self.conn.execute(query, (
            lat - radius_deg, lat + radius_deg,
            lon - radius_deg, lon + radius_deg,
            min_length_ft
        ))
        return [dict(row) for row in cursor.fetchall()]

    def find_airspace_at_point(
        self,
        lat: float,
        lon: float,
        altitude_ft: Optional[int] = None
    ) -> list[dict]:
        """Find airspaces containing a point."""

        if not self.has_spatialite:
            return []

        query = '''
            SELECT
                name,
                type,
                class,
                lower_altitude_ft,
                upper_altitude_ft
            FROM airspace
            WHERE ST_Contains(geometry, MakePoint(?, ?, 4326))
        '''
        params = [lon, lat]

        if altitude_ft is not None:
            query += '''
                AND (lower_altitude_ft IS NULL OR lower_altitude_ft <= ?)
                AND (upper_altitude_ft IS NULL OR upper_altitude_ft >= ?)
            '''
            params.extend([altitude_ft, altitude_ft])

        query += ' ORDER BY lower_altitude_ft'

        cursor = self.conn.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

    def find_obstacles_in_corridor(
        self,
        start_lat: float,
        start_lon: float,
        end_lat: float,
        end_lon: float,
        corridor_nm: float = 5,
        min_height_ft: int = 0
    ) -> list[dict]:
        """Find obstacles within corridor of a route."""

        corridor_deg = corridor_nm / 60.0

        if self.has_spatialite:
            query = '''
                SELECT
                    oas_number,
                    obstacle_type,
                    msl_height_ft,
                    agl_height_ft,
                    lighting,
                    latitude,
                    longitude
                FROM obstacles
                WHERE ROWID IN (
                    SELECT ROWID FROM SpatialIndex
                    WHERE f_table_name = 'obstacles'
                    AND search_frame = BuildMbr(?, ?, ?, ?, 4326)
                )
                AND msl_height_ft >= ?
                ORDER BY msl_height_ft DESC
                LIMIT 100
            '''
            params = (
                min(start_lon, end_lon) - corridor_deg,
                min(start_lat, end_lat) - corridor_deg,
                max(start_lon, end_lon) + corridor_deg,
                max(start_lat, end_lat) + corridor_deg,
                min_height_ft
            )
        else:
            query = '''
                SELECT
                    oas_number,
                    obstacle_type,
                    msl_height_ft,
                    agl_height_ft,
                    lighting,
                    latitude,
                    longitude
                FROM obstacles
                WHERE latitude BETWEEN ? AND ?
                AND longitude BETWEEN ? AND ?
                AND msl_height_ft >= ?
                ORDER BY msl_height_ft DESC
                LIMIT 100
            '''
            params = (
                min(start_lat, end_lat) - corridor_deg,
                max(start_lat, end_lat) + corridor_deg,
                min(start_lon, end_lon) - corridor_deg,
                max(start_lon, end_lon) + corridor_deg,
                min_height_ft
            )

        cursor = self.conn.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

    def find_nearby_navaids(
        self,
        lat: float,
        lon: float,
        radius_nm: float = 100,
        navaid_types: Optional[list[str]] = None
    ) -> list[dict]:
        """Find NAVAIDs within radius."""

        radius_deg = radius_nm / 60.0
        query = '''
            SELECT
                facility_id,
                name,
                type_category,
                frequency_mhz,
                latitude,
                longitude
            FROM navaids
            WHERE latitude BETWEEN ? AND ?
            AND longitude BETWEEN ? AND ?
        '''
        params = [
            lat - radius_deg, lat + radius_deg,
            lon - radius_deg, lon + radius_deg
        ]

        if navaid_types:
            placeholders = ','.join('?' * len(navaid_types))
            query += f' AND type_category IN ({placeholders})'
            params.extend(navaid_types)

        query += ' ORDER BY type_category, name'

        cursor = self.conn.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

    def close(self):
        self.conn.close()


def main():
    parser = argparse.ArgumentParser(description='Test spatial queries')
    parser.add_argument('--database', '-d', required=True, help='Database path')
    parser.add_argument('--lat', type=float, required=True, help='Latitude')
    parser.add_argument('--lon', type=float, required=True, help='Longitude')
    parser.add_argument('--test-nearest', action='store_true', help='Test nearest airports')
    parser.add_argument('--radius', type=float, default=50, help='Search radius (nm)')
    args = parser.parse_args()

    if not Path(args.database).exists():
        print(f"Error: {args.database} not found")
        sys.exit(1)

    db = AviationSpatialDB(args.database)

    if args.test_nearest:
        print(f"\nSearching for airports within {args.radius} nm of {args.lat}, {args.lon}...")
        airports = db.find_nearby_airports(args.lat, args.lon, args.radius)

        if airports:
            print(f"\nFound {len(airports)} airports:")
            for apt in airports[:10]:
                dist = apt.get('distance_nm', '?')
                if isinstance(dist, float):
                    dist = f"{dist:.1f}"
                print(f"  {apt['location_id']}: {apt['facility_name']} ({dist} nm)")
        else:
            print("No airports found")

    db.close()


if __name__ == '__main__':
    main()
