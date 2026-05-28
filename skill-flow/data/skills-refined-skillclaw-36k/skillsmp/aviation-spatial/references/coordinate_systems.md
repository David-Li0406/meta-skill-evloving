# Coordinate Systems for Aviation

Reference for coordinate systems and projections used in aviation.

## Primary Coordinate System

### WGS84 (EPSG:4326)

- **EPSG Code:** 4326
- **Name:** World Geodetic System 1984
- **Type:** Geographic (lat/lon)
- **Units:** Degrees
- **Used by:** GPS, FAA data, aviation databases

```sql
-- Create geometry with WGS84
SELECT MakePoint(-122.4194, 37.7749, 4326);

-- Transform to/from other CRS
SELECT Transform(geometry, 4326) FROM other_table;
```

## Distance Calculations

### Great Circle (Geodesic)

Most accurate for aviation distances.

```sql
-- SpatiaLite geodesic distance (meters)
SELECT ST_Distance(
    MakePoint(-122.4194, 37.7749, 4326),  -- SFO
    MakePoint(-118.4085, 33.9425, 4326),  -- LAX
    1  -- Use ellipsoid
);
-- Result: ~543,000 meters (~293 nm)
```

### Haversine Formula

Good approximation for distances < 1000 nm.

```python
import math

def haversine_nm(lat1, lon1, lat2, lon2):
    """Calculate distance in nautical miles."""
    R = 3440.065  # Earth radius in nm

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (math.sin(dlat/2)**2 +
         math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2)

    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
```

## Unit Conversions

### Distance

| From | To | Factor |
|------|-----|--------|
| Nautical Miles | Meters | × 1852 |
| Nautical Miles | Statute Miles | × 1.15078 |
| Nautical Miles | Kilometers | × 1.852 |
| Meters | Nautical Miles | ÷ 1852 |
| Degrees (equator) | Nautical Miles | × 60 |

```sql
-- Degrees to approximate nautical miles at latitude
-- 1 degree longitude = 60 * cos(latitude) nm
-- 1 degree latitude = 60 nm

SELECT 60 * COS(RADIANS(latitude)) AS nm_per_degree_lon
FROM airports WHERE location_id = 'LAX';
```

### Altitude

| From | To | Factor |
|------|-----|--------|
| Feet | Meters | × 0.3048 |
| Meters | Feet | × 3.28084 |
| Flight Level | Feet | × 100 |

## Common Projections

### Web Mercator (EPSG:3857)

Used by web maps (OpenStreetMap, Google Maps).

```sql
-- Transform WGS84 to Web Mercator
SELECT Transform(geometry, 3857) FROM airports;

-- Transform Web Mercator to WGS84
SELECT Transform(geometry, 4326) FROM web_tiles;
```

### Lambert Conformal Conic

Used by FAA VFR/IFR charts.

- **Sectional Charts:** Custom Lambert per chart
- **IFR Low/High:** Lambert Conformal Conic

### UTM Zones

Good for local area calculations.

```python
def get_utm_zone(longitude):
    """Get UTM zone for a longitude."""
    return int((longitude + 180) / 6) + 1

def get_utm_epsg(latitude, longitude):
    """Get EPSG code for UTM zone at location."""
    zone = get_utm_zone(longitude)
    if latitude >= 0:
        return 32600 + zone  # Northern hemisphere
    else:
        return 32700 + zone  # Southern hemisphere
```

## Coordinate Format Conversions

### Decimal Degrees to DMS

```python
def dd_to_dms(decimal_degrees, is_longitude=False):
    """Convert decimal degrees to degrees/minutes/seconds."""
    if is_longitude:
        direction = 'E' if decimal_degrees >= 0 else 'W'
    else:
        direction = 'N' if decimal_degrees >= 0 else 'S'

    dd = abs(decimal_degrees)
    degrees = int(dd)
    minutes = int((dd - degrees) * 60)
    seconds = ((dd - degrees) * 60 - minutes) * 60

    return f"{degrees}°{minutes}'{seconds:.2f}\"{direction}"

# Example: 37.7749 → 37°46'29.64"N
```

### DMS to Decimal Degrees

```python
def dms_to_dd(degrees, minutes, seconds, direction):
    """Convert DMS to decimal degrees."""
    dd = degrees + minutes/60 + seconds/3600
    if direction in ('S', 'W'):
        dd = -dd
    return dd

# Example: 37°46'29.64"N → 37.7749
```

## Magnetic Variation

Convert between true and magnetic bearings.

```python
# East variation is positive, West is negative
# True = Magnetic + Variation
# Magnetic = True - Variation

def true_to_magnetic(true_heading, variation):
    """Convert true heading to magnetic."""
    return (true_heading - variation) % 360

def magnetic_to_true(magnetic_heading, variation):
    """Convert magnetic heading to true."""
    return (magnetic_heading + variation) % 360
```

## SpatiaLite Functions

### Coordinate Functions

```sql
-- Extract coordinates
SELECT ST_X(geometry), ST_Y(geometry) FROM airports;
SELECT X(geometry), Y(geometry) FROM airports;  -- Alias

-- Get bounding box
SELECT MbrMinX(geometry), MbrMinY(geometry),
       MbrMaxX(geometry), MbrMaxY(geometry)
FROM airspace;

-- Calculate centroid
SELECT ST_Centroid(geometry) FROM airspace;
```

### Geometry Constructors

```sql
-- Point
SELECT MakePoint(longitude, latitude, 4326);

-- Line
SELECT MakeLine(point1, point2);
SELECT MakeLine(MakePoint(-122, 37, 4326), MakePoint(-118, 34, 4326));

-- Polygon
SELECT MakePolygon(MakeLine(...));

-- Circle (approximated as polygon)
SELECT MakeCircle(center_x, center_y, radius_meters, 4326);
```

### Bounding Box Helpers

```sql
-- Build bounding box
SELECT BuildMbr(min_x, min_y, max_x, max_y, 4326);

-- Build circle bounding box (for radius searches)
SELECT BuildCircleMbr(center_x, center_y, radius_degrees, 4326);
```
