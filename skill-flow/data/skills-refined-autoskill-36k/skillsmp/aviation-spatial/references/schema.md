# SpatiaLite Aviation Schema

Complete schema for aviation spatial database.

## Tables with Geometry

### Airports

```sql
CREATE TABLE airports (
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
    longest_runway_ft INTEGER,
    has_tower INTEGER DEFAULT 0,
    has_lighting INTEGER DEFAULT 0,
    fuel_available TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add geometry column
SELECT AddGeometryColumn('airports', 'geometry', 4326, 'POINT', 'XY');

-- Create spatial index
SELECT CreateSpatialIndex('airports', 'geometry');

-- Regular indexes
CREATE INDEX idx_airports_location ON airports(location_id);
CREATE INDEX idx_airports_icao ON airports(icao_id);
CREATE INDEX idx_airports_state ON airports(state_code);
```

### Runways

```sql
CREATE TABLE runways (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    facility_site_number TEXT NOT NULL,
    runway_id TEXT NOT NULL,
    length_ft INTEGER,
    width_ft INTEGER,
    surface_type TEXT,
    base_id TEXT,
    base_heading INTEGER,
    recip_id TEXT,
    recip_heading INTEGER,
    base_latitude REAL,
    base_longitude REAL,
    recip_latitude REAL,
    recip_longitude REAL,
    ils_type TEXT,
    FOREIGN KEY (facility_site_number) REFERENCES airports(facility_site_number)
);

-- Add geometry for runway line
SELECT AddGeometryColumn('runways', 'geometry', 4326, 'LINESTRING', 'XY');
SELECT CreateSpatialIndex('runways', 'geometry');
```

### NAVAIDs

```sql
CREATE TABLE navaids (
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
    vor_service_volume TEXT,
    dme_service_volume TEXT,
    nav_status TEXT
);

SELECT AddGeometryColumn('navaids', 'geometry', 4326, 'POINT', 'XY');
SELECT CreateSpatialIndex('navaids', 'geometry');
CREATE INDEX idx_navaids_type ON navaids(type_category);
```

### Fixes

```sql
CREATE TABLE fixes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fix_id TEXT NOT NULL,
    state_code TEXT,
    latitude REAL,
    longitude REAL,
    fix_type TEXT,
    fix_use TEXT,
    artcc_hi TEXT,
    artcc_lo TEXT
);

SELECT AddGeometryColumn('fixes', 'geometry', 4326, 'POINT', 'XY');
SELECT CreateSpatialIndex('fixes', 'geometry');
CREATE INDEX idx_fixes_id ON fixes(fix_id);
```

### Obstacles

```sql
CREATE TABLE obstacles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    oas_number TEXT UNIQUE NOT NULL,
    state TEXT,
    city TEXT,
    latitude REAL,
    longitude REAL,
    obstacle_type TEXT,
    agl_height_ft INTEGER,
    msl_height_ft INTEGER,
    lighting TEXT,
    horizontal_accuracy TEXT,
    vertical_accuracy TEXT
);

SELECT AddGeometryColumn('obstacles', 'geometry', 4326, 'POINT', 'XY');
SELECT CreateSpatialIndex('obstacles', 'geometry');
CREATE INDEX idx_obstacles_msl ON obstacles(msl_height_ft);
CREATE INDEX idx_obstacles_state ON obstacles(state);
```

### Airspace

```sql
CREATE TABLE airspace (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL,           -- CLASS_B, CLASS_C, MOA, RESTRICTED, etc.
    class TEXT,                   -- B, C, D, E
    lower_altitude_ft INTEGER,
    upper_altitude_ft INTEGER,
    lower_altitude_ref TEXT,      -- MSL, AGL
    upper_altitude_ref TEXT,
    controlling_agency TEXT,
    times_of_use TEXT,
    effective_date TEXT,
    expiration_date TEXT
);

-- Polygon geometry for airspace boundaries
SELECT AddGeometryColumn('airspace', 'geometry', 4326, 'MULTIPOLYGON', 'XY');
SELECT CreateSpatialIndex('airspace', 'geometry');
CREATE INDEX idx_airspace_type ON airspace(type);
CREATE INDEX idx_airspace_class ON airspace(class);
```

### Airways

```sql
CREATE TABLE airways (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    airway_id TEXT NOT NULL UNIQUE,
    airway_type TEXT,
    airway_category TEXT
);

CREATE TABLE airway_segments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    airway_id TEXT NOT NULL,
    sequence_number INTEGER,
    from_fix TEXT,
    to_fix TEXT,
    mea_ft INTEGER,
    maa_ft INTEGER,
    distance_nm REAL,
    FOREIGN KEY (airway_id) REFERENCES airways(airway_id)
);

-- Line geometry for airway segments
SELECT AddGeometryColumn('airway_segments', 'geometry', 4326, 'LINESTRING', 'XY');
SELECT CreateSpatialIndex('airway_segments', 'geometry');
```

## Populating Geometry

After importing data, populate geometry columns:

```sql
-- Airports
UPDATE airports
SET geometry = MakePoint(longitude, latitude, 4326)
WHERE longitude IS NOT NULL AND latitude IS NOT NULL;

-- NAVAIDs
UPDATE navaids
SET geometry = MakePoint(longitude, latitude, 4326)
WHERE longitude IS NOT NULL AND latitude IS NOT NULL;

-- Fixes
UPDATE fixes
SET geometry = MakePoint(longitude, latitude, 4326)
WHERE longitude IS NOT NULL AND latitude IS NOT NULL;

-- Obstacles
UPDATE obstacles
SET geometry = MakePoint(longitude, latitude, 4326)
WHERE longitude IS NOT NULL AND latitude IS NOT NULL;

-- Runways (line from base to reciprocal)
UPDATE runways
SET geometry = MakeLine(
    MakePoint(base_longitude, base_latitude, 4326),
    MakePoint(recip_longitude, recip_latitude, 4326)
)
WHERE base_longitude IS NOT NULL
AND base_latitude IS NOT NULL
AND recip_longitude IS NOT NULL
AND recip_latitude IS NOT NULL;

-- Airway segments
UPDATE airway_segments
SET geometry = MakeLine(
    (SELECT geometry FROM fixes WHERE fix_id = from_fix LIMIT 1),
    (SELECT geometry FROM fixes WHERE fix_id = to_fix LIMIT 1)
)
WHERE from_fix IN (SELECT fix_id FROM fixes)
AND to_fix IN (SELECT fix_id FROM fixes);
```

## Views

### Airports with Runway Info

```sql
CREATE VIEW v_airports_full AS
SELECT
    a.location_id,
    a.icao_id,
    a.facility_name,
    a.city_name,
    a.state_code,
    a.latitude,
    a.longitude,
    a.elevation_ft,
    a.geometry,
    MAX(r.length_ft) as longest_runway_ft,
    COUNT(r.id) as runway_count,
    MAX(CASE WHEN r.ils_type IS NOT NULL THEN 1 ELSE 0 END) as has_ils
FROM airports a
LEFT JOIN runways r ON a.facility_site_number = r.facility_site_number
GROUP BY a.id;
```

### Nearby Everything

```sql
-- Parameterized view via function
CREATE VIEW v_nearby_features AS
SELECT 'airport' as feature_type, location_id as id, facility_name as name,
       latitude, longitude, geometry
FROM airports
UNION ALL
SELECT 'navaid', facility_id, name, latitude, longitude, geometry
FROM navaids
UNION ALL
SELECT 'fix', fix_id, fix_id, latitude, longitude, geometry
FROM fixes;
```
