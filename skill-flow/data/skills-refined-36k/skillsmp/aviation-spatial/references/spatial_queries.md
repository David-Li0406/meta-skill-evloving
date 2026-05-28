# Spatial Query Patterns

Common SpatiaLite queries for aviation applications.

## Setup

All queries assume SpatiaLite is loaded and geometry columns use EPSG:4326 (WGS84).

```sql
-- Load SpatiaLite extension
SELECT load_extension('mod_spatialite');

-- Initialize spatial metadata
SELECT InitSpatialMetaData();
```

## Proximity Queries

### Find Airports Within Radius

```sql
-- Find airports within 50nm of a point
-- Parameters: lon, lat, radius_nm

SELECT
    id,
    location_id,
    facility_name,
    latitude,
    longitude,
    elevation_ft,
    -- Distance in nautical miles (approximate)
    ST_Distance(
        geometry,
        MakePoint(:lon, :lat, 4326),
        1
    ) / 1852.0 AS distance_nm
FROM airports
WHERE ROWID IN (
    SELECT ROWID FROM SpatialIndex
    WHERE f_table_name = 'airports'
    AND f_geometry_column = 'geometry'
    AND search_frame = BuildCircleMbr(:lon, :lat, :radius_degrees, 4326)
)
AND ST_Distance(
    geometry,
    MakePoint(:lon, :lat, 4326),
    1
) <= :radius_nm * 1852.0
ORDER BY distance_nm
LIMIT 50;
```

### Python Helper Function

```python
def find_airports_within_radius(conn, lat: float, lon: float, radius_nm: float):
    """Find airports within radius of a point."""
    # Convert NM to approximate degrees (1 degree ≈ 60 NM at equator)
    radius_deg = radius_nm / 60.0

    query = '''
        SELECT
            location_id,
            facility_name,
            latitude,
            longitude,
            elevation_ft,
            ST_Distance(
                geometry,
                MakePoint(?, ?, 4326),
                1
            ) / 1852.0 AS distance_nm
        FROM airports
        WHERE ROWID IN (
            SELECT ROWID FROM SpatialIndex
            WHERE f_table_name = 'airports'
            AND f_geometry_column = 'geometry'
            AND search_frame = BuildCircleMbr(?, ?, ?, 4326)
        )
        ORDER BY distance_nm
        LIMIT 50
    '''

    cursor = conn.execute(query, (lon, lat, lon, lat, radius_deg))
    return cursor.fetchall()
```

## Airspace Containment

### Check if Point is Within Airspace

```sql
-- Find all airspaces containing a point at an altitude
SELECT
    id,
    name,
    type,
    class,
    lower_altitude_ft,
    upper_altitude_ft
FROM airspace
WHERE ST_Contains(geometry, MakePoint(:lon, :lat, 4326))
AND :altitude_ft >= lower_altitude_ft
AND :altitude_ft <= upper_altitude_ft
ORDER BY lower_altitude_ft;
```

### Find Airspaces Along Route

```sql
-- Find airspaces that intersect a route line
SELECT DISTINCT
    a.id,
    a.name,
    a.type,
    a.class,
    a.lower_altitude_ft,
    a.upper_altitude_ft
FROM airspace a
WHERE ST_Intersects(
    a.geometry,
    MakeLine(
        MakePoint(:start_lon, :start_lat, 4326),
        MakePoint(:end_lon, :end_lat, 4326)
    )
)
ORDER BY a.type, a.name;
```

## Runway Queries

### Find Airports with Runway >= Minimum Length

```sql
SELECT
    a.location_id,
    a.facility_name,
    a.latitude,
    a.longitude,
    MAX(r.length_ft) as longest_runway,
    ST_Distance(
        a.geometry,
        MakePoint(:lon, :lat, 4326),
        1
    ) / 1852.0 AS distance_nm
FROM airports a
JOIN runways r ON a.facility_site_number = r.facility_site_number
WHERE a.ROWID IN (
    SELECT ROWID FROM SpatialIndex
    WHERE f_table_name = 'airports'
    AND search_frame = BuildCircleMbr(:lon, :lat, :radius_deg, 4326)
)
AND r.length_ft >= :min_length_ft
GROUP BY a.id
HAVING longest_runway >= :min_length_ft
ORDER BY distance_nm;
```

## Obstacle Queries

### Find Obstacles Along Route Corridor

```sql
-- Find obstacles within a corridor around a route
-- corridor_width in nautical miles

SELECT
    o.id,
    o.oas_number,
    o.obstacle_type,
    o.msl_height_ft,
    o.agl_height_ft,
    o.lighting,
    ST_Distance(
        o.geometry,
        MakeLine(
            MakePoint(:start_lon, :start_lat, 4326),
            MakePoint(:end_lon, :end_lat, 4326)
        ),
        1
    ) / 1852.0 AS distance_from_route_nm
FROM obstacles o
WHERE o.ROWID IN (
    SELECT ROWID FROM SpatialIndex
    WHERE f_table_name = 'obstacles'
    AND search_frame = BuildMbr(
        MIN(:start_lon, :end_lon) - :corridor_deg,
        MIN(:start_lat, :end_lat) - :corridor_deg,
        MAX(:start_lon, :end_lon) + :corridor_deg,
        MAX(:start_lat, :end_lat) + :corridor_deg,
        4326
    )
)
AND ST_Distance(
    o.geometry,
    MakeLine(
        MakePoint(:start_lon, :start_lat, 4326),
        MakePoint(:end_lon, :end_lat, 4326)
    ),
    1
) <= :corridor_nm * 1852.0
AND o.msl_height_ft >= :min_height_ft
ORDER BY o.msl_height_ft DESC;
```

### Find Highest Obstacle in Area

```sql
SELECT
    oas_number,
    obstacle_type,
    msl_height_ft,
    agl_height_ft,
    latitude,
    longitude
FROM obstacles
WHERE ROWID IN (
    SELECT ROWID FROM SpatialIndex
    WHERE f_table_name = 'obstacles'
    AND search_frame = BuildCircleMbr(:lon, :lat, :radius_deg, 4326)
)
ORDER BY msl_height_ft DESC
LIMIT 1;
```

## NAVAID Queries

### Find NAVAIDs by Type Within Radius

```sql
SELECT
    n.facility_id,
    n.name,
    n.type_category,
    n.frequency_mhz,
    n.latitude,
    n.longitude,
    ST_Distance(
        n.geometry,
        MakePoint(:lon, :lat, 4326),
        1
    ) / 1852.0 AS distance_nm
FROM navaids n
WHERE n.type_category IN ('VOR', 'VORTAC', 'VORDME')
AND n.ROWID IN (
    SELECT ROWID FROM SpatialIndex
    WHERE f_table_name = 'navaids'
    AND search_frame = BuildCircleMbr(:lon, :lat, :radius_deg, 4326)
)
ORDER BY distance_nm;
```

## Creating Spatial Indexes

```sql
-- Create R-Tree spatial index for airports
SELECT CreateSpatialIndex('airports', 'geometry');

-- Create R-Tree spatial index for obstacles
SELECT CreateSpatialIndex('obstacles', 'geometry');

-- Create R-Tree spatial index for airspace
SELECT CreateSpatialIndex('airspace', 'geometry');

-- Create R-Tree spatial index for navaids
SELECT CreateSpatialIndex('navaids', 'geometry');

-- Create R-Tree spatial index for fixes
SELECT CreateSpatialIndex('fixes', 'geometry');
```

## Utility Functions

### Create Point Geometry from Lat/Lon

```sql
-- Add geometry column to table
SELECT AddGeometryColumn('airports', 'geometry', 4326, 'POINT', 'XY');

-- Populate geometry from lat/lon columns
UPDATE airports
SET geometry = MakePoint(longitude, latitude, 4326)
WHERE longitude IS NOT NULL AND latitude IS NOT NULL;
```

### Calculate Distance Between Points

```sql
-- Distance in meters (geodesic)
SELECT ST_Distance(
    MakePoint(:lon1, :lat1, 4326),
    MakePoint(:lon2, :lat2, 4326),
    1  -- Use ellipsoid (geodesic)
) AS distance_meters;

-- Distance in nautical miles
SELECT ST_Distance(
    MakePoint(:lon1, :lat1, 4326),
    MakePoint(:lon2, :lat2, 4326),
    1
) / 1852.0 AS distance_nm;
```

### Calculate Bearing

```sql
-- Azimuth (bearing) from point 1 to point 2
SELECT Degrees(
    ST_Azimuth(
        MakePoint(:lon1, :lat1, 4326),
        MakePoint(:lon2, :lat2, 4326)
    )
) AS bearing_degrees;
```
