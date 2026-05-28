---
name: mapbox
description: "Geospatial services for geocoding, directions, distance matrices, and route optimization using the Mapbox API. Use when tasks require: (1) Converting addresses to coordinates or vice versa, (2) Calculating driving/walking/cycling routes between locations, (3) Computing distance/duration matrices for multiple origins and destinations, (4) Optimizing delivery routes or multi-stop trips. Environment variable MAPBOX_API_KEY must be set."
license: "© 2025 Daisyloop Technologies Inc. See LICENSE.txt"
---

# Mapbox Geospatial Services

## Overview

This skill provides integration with Mapbox's geospatial APIs for geocoding, routing, distance matrices, and route optimization. Use the provided scripts for common operations or write custom implementations following the patterns below.

**API flow**: Prepare coordinates/addresses -> Call API -> Parse structured response

## Quick Start

```python
import os
from mapbox import Geocoder

# Map environment variable (SDK expects MAPBOX_ACCESS_TOKEN)
os.environ['MAPBOX_ACCESS_TOKEN'] = os.environ.get('MAPBOX_API_KEY', '')

geocoder = Geocoder()
response = geocoder.forward("1600 Pennsylvania Ave NW, Washington, DC")
features = response.geojson()['features']
if features:
    coords = features[0]['geometry']['coordinates']
    print(f"Coordinates: {coords[1]}, {coords[0]}")  # lat, lng
```

Or use the provided scripts:

```bash
uv run skills/mapbox/scripts/geocode.py "1600 Pennsylvania Ave NW, Washington, DC"
uv run skills/mapbox/scripts/get_directions.py "38.8977,-77.0365" "40.7484,-73.9857" --profile driving
```

## Task 1: Geocoding

Convert addresses to coordinates (forward) or coordinates to addresses (reverse).

### Forward Geocoding (Address to Coordinates)

```python
import os
from mapbox import Geocoder

os.environ['MAPBOX_ACCESS_TOKEN'] = os.environ.get('MAPBOX_API_KEY', '')

geocoder = Geocoder()
response = geocoder.forward(
    "Empire State Building, New York",
    country=['us'],  # Limit to specific countries
    types=['address', 'poi'],  # Filter result types
    limit=5  # Max results
)

features = response.geojson()['features']
for feature in features:
    name = feature['place_name']
    lng, lat = feature['geometry']['coordinates']
    print(f"{name}: {lat}, {lng}")
```

### Reverse Geocoding (Coordinates to Address)

```python
response = geocoder.reverse(lon=-73.9857, lat=40.7484)
features = response.geojson()['features']
if features:
    address = features[0]['place_name']
    print(f"Address: {address}")
```

### CLI Usage

```bash
# Forward geocoding
uv run skills/mapbox/scripts/geocode.py "350 5th Ave, New York, NY" --json

# Reverse geocoding
uv run skills/mapbox/scripts/geocode.py --reverse "40.7484,-73.9857"

# With filters
uv run skills/mapbox/scripts/geocode.py "Paris" --country fr --types place --limit 3
```

## Task 2: Directions

Calculate routes between two or more waypoints with turn-by-turn instructions.

### Basic Route

```python
import os
from mapbox import Directions

os.environ['MAPBOX_ACCESS_TOKEN'] = os.environ.get('MAPBOX_API_KEY', '')

directions = Directions()
origin = {"type": "Feature", "geometry": {"type": "Point", "coordinates": [-77.0365, 38.8977]}}
destination = {"type": "Feature", "geometry": {"type": "Point", "coordinates": [-73.9857, 40.7484]}}

response = directions.directions([origin, destination], profile='mapbox/driving')
route = response.geojson()['features'][0]

distance_km = route['properties']['distance'] / 1000
duration_min = route['properties']['duration'] / 60
print(f"Distance: {distance_km:.1f} km, Duration: {duration_min:.0f} min")
```

### With Waypoints and Options

```python
waypoints = [
    {"type": "Feature", "geometry": {"type": "Point", "coordinates": [-77.0365, 38.8977]}},
    {"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.1652, 39.9526]}},
    {"type": "Feature", "geometry": {"type": "Point", "coordinates": [-73.9857, 40.7484]}},
]

response = directions.directions(
    waypoints,
    profile='mapbox/driving-traffic',  # Use traffic-aware routing
    geometries='geojson',
    steps=True,  # Include turn-by-turn instructions
    alternatives=True  # Request alternative routes
)
```

### Routing Profiles

| Profile | Use Case |
|---------|----------|
| `mapbox/driving` | Standard car routing |
| `mapbox/driving-traffic` | Traffic-aware car routing |
| `mapbox/walking` | Pedestrian routing |
| `mapbox/cycling` | Bicycle routing |

### CLI Usage

```bash
# Basic route
uv run skills/mapbox/scripts/get_directions.py "38.8977,-77.0365" "40.7484,-73.9857"

# With profile and steps
uv run skills/mapbox/scripts/get_directions.py "38.8977,-77.0365" "40.7484,-73.9857" \
    --profile driving-traffic --steps --json

# Multi-waypoint route
uv run skills/mapbox/scripts/get_directions.py "38.8977,-77.0365" "39.9526,-75.1652" "40.7484,-73.9857"
```

## Task 3: Distance Matrix

Calculate distances and durations between multiple origins and destinations.

### Basic Matrix

```python
import os
from mapbox import DirectionsMatrix

os.environ['MAPBOX_ACCESS_TOKEN'] = os.environ.get('MAPBOX_API_KEY', '')

matrix = DirectionsMatrix()
locations = [
    {"type": "Feature", "geometry": {"type": "Point", "coordinates": [-77.0365, 38.8977]}},
    {"type": "Feature", "geometry": {"type": "Point", "coordinates": [-73.9857, 40.7484]}},
    {"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.1652, 39.9526]}},
]

response = matrix.matrix(locations, profile='mapbox/driving')
data = response.json()

# Access durations matrix (in seconds)
durations = data['durations']
for i, row in enumerate(durations):
    for j, duration in enumerate(row):
        if duration is not None:
            print(f"From {i} to {j}: {duration/60:.0f} min")
```

### Asymmetric Matrix

For asymmetric matrices (many origins to one destination, or vice versa):

```python
# Only compute from first 2 locations to all locations
response = matrix.matrix(
    locations,
    profile='mapbox/driving',
    sources=[0, 1],  # Indices of origin locations
    destinations=[2]  # Indices of destination locations
)
```

### CLI Usage

```bash
# Symmetric matrix
uv run skills/mapbox/scripts/get_matrix.py \
    "38.8977,-77.0365" "40.7484,-73.9857" "39.9526,-75.1652" --json

# Asymmetric matrix
uv run skills/mapbox/scripts/get_matrix.py \
    "38.8977,-77.0365" "40.7484,-73.9857" "39.9526,-75.1652" \
    --sources 0,1 --destinations 2
```

## Task 4: Route Optimization

Optimize multi-stop routes for delivery, field service, or logistics. Solves the Traveling Salesperson Problem.

### Basic Optimization

```python
import os
import httpx

access_token = os.environ.get('MAPBOX_API_KEY', '')

# Coordinates: lng,lat pairs separated by semicolons
coordinates = "-77.0365,38.8977;-73.9857,40.7484;-75.1652,39.9526"

response = httpx.get(
    f"https://api.mapbox.com/optimized-trips/v1/mapbox/driving/{coordinates}",
    params={
        "access_token": access_token,
        "roundtrip": "true",
        "source": "first",
        "geometries": "geojson",
        "overview": "full",
    }
)

result = response.json()
trip = result['trips'][0]
print(f"Optimized distance: {trip['distance']/1000:.1f} km")
print(f"Optimized duration: {trip['duration']/60:.0f} min")

# Get optimized waypoint order
for wp in result['waypoints']:
    print(f"Stop {wp['waypoint_index']}: {wp['name']}")
```

### With Turn-by-Turn Steps

```python
response = httpx.get(
    f"https://api.mapbox.com/optimized-trips/v1/mapbox/driving/{coordinates}",
    params={
        "access_token": access_token,
        "roundtrip": "true",
        "steps": "true",
        "geometries": "geojson",
    }
)

result = response.json()
trip = result['trips'][0]

# Access route legs with instructions
for i, leg in enumerate(trip['legs']):
    print(f"Leg {i+1}: {leg['distance']/1000:.1f} km")
    for step in leg['steps']:
        print(f"  - {step['maneuver']['instruction']}")
```

### CLI Usage

```bash
# Basic optimization (round-trip from first location)
uv run skills/mapbox/scripts/optimize_route.py \
    "38.8977,-77.0365" "40.7484,-73.9857" "39.9526,-75.1652" --json

# With turn-by-turn steps
uv run skills/mapbox/scripts/optimize_route.py \
    "38.8977,-77.0365" "40.7484,-73.9857" "39.9526,-75.1652" --steps

# One-way optimization (no return to start)
uv run skills/mapbox/scripts/optimize_route.py \
    "38.8977,-77.0365" "40.7484,-73.9857" "39.9526,-75.1652" \
    --no-roundtrip
```

## Error Handling

### SDK Error Handling

```python
import os
from mapbox import Geocoder

os.environ['MAPBOX_ACCESS_TOKEN'] = os.environ.get('MAPBOX_API_KEY', '')

geocoder = Geocoder()
response = geocoder.forward("Some address")

if response.status_code == 200:
    data = response.geojson()
    # Process results
elif response.status_code == 401:
    print("Invalid API key")
elif response.status_code == 429:
    print("Rate limit exceeded - back off and retry")
else:
    print(f"API error: {response.status_code}")
```

### httpx Error Handling (for Optimization API)

```python
import httpx

try:
    response = httpx.post(url, json=body, timeout=30.0)
    response.raise_for_status()
    result = response.json()
except httpx.TimeoutException:
    print("Request timed out")
except httpx.HTTPStatusError as e:
    if e.response.status_code == 422:
        print(f"Invalid request: {e.response.json()}")
    elif e.response.status_code == 429:
        print("Rate limit exceeded")
    else:
        print(f"HTTP error: {e}")
```

## Rate Limits

| API | Free Tier | Rate Limit |
|-----|-----------|------------|
| Geocoding | 100,000 requests/month | 600 requests/minute |
| Directions | 100,000 requests/month | 300 requests/minute |
| Matrix | 100,000 elements/month | 60 requests/minute |
| Optimization | 50,000 requests/month | 10 requests/minute |

**Best practices:**
- Implement exponential backoff on 429 errors
- Cache geocoding results for frequently queried addresses
- Batch matrix requests to minimize API calls

## Scripts

This skill includes ready-to-use scripts:

- `scripts/geocode.py` - Forward and reverse geocoding
- `scripts/get_directions.py` - Route calculation with profiles
- `scripts/get_matrix.py` - Distance/duration matrices
- `scripts/optimize_route.py` - Multi-stop route optimization

Run scripts directly via `uv run` or import functions into custom implementations.

## References

For detailed API type definitions, see [references/api_reference.md](references/api_reference.md).
