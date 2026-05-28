# Mapbox API Reference

Request and response data types for Mapbox APIs.

## Table of Contents

- [Geocoding](#geocoding)
- [Directions](#directions)
- [Matrix](#matrix)
- [Optimization](#optimization)
- [Error Codes](#error-codes)

---

## Geocoding

### GeocodingResult

| Field | Type | Description |
|-------|------|-------------|
| `type` | `str` | Always "FeatureCollection" |
| `query` | `list[str]` | Original query tokens |
| `features` | `list[Feature]` | List of matching features |
| `attribution` | `str` | Mapbox attribution string |

### Feature

| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | Unique feature identifier |
| `place_type` | `list[str]` | Feature types (address, poi, place, region, country) |
| `relevance` | `float` | Relevance score (0-1) |
| `text` | `str` | Primary name |
| `place_name` | `str` | Full formatted place name |
| `center` | `list[float]` | [longitude, latitude] |
| `geometry` | `Geometry` | GeoJSON geometry |
| `context` | `list[Context]` | Hierarchical context |
| `bbox` | `list[float] \| None` | Bounding box |

### Context

| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | Context type and ID (e.g., "place.123456") |
| `text` | `str` | Display name |
| `short_code` | `str \| None` | ISO code |

### Feature Types

| Type | Description |
|------|-------------|
| `country` | Country |
| `region` | State/province |
| `postcode` | Postal code |
| `district` | District/county |
| `place` | City/town |
| `locality` | Neighborhood |
| `address` | Street address |
| `poi` | Point of interest |

---

## Directions

### DirectionsResult

| Field | Type | Description |
|-------|------|-------------|
| `type` | `str` | Always "FeatureCollection" |
| `features` | `list[Route]` | List of routes |
| `waypoints` | `list[Waypoint]` | Snapped waypoint locations |

### Route Properties

| Field | Type | Description |
|-------|------|-------------|
| `distance` | `float` | Total distance (meters) |
| `duration` | `float` | Total duration (seconds) |
| `weight` | `float` | Route weight |
| `legs` | `list[Leg]` | Route legs |

### Leg

| Field | Type | Description |
|-------|------|-------------|
| `distance` | `float` | Leg distance (meters) |
| `duration` | `float` | Leg duration (seconds) |
| `summary` | `str` | Road names |
| `steps` | `list[Step]` | Turn-by-turn steps |

### Step

| Field | Type | Description |
|-------|------|-------------|
| `distance` | `float` | Step distance (meters) |
| `duration` | `float` | Step duration (seconds) |
| `name` | `str` | Road/street name |
| `maneuver` | `Maneuver` | Turn instruction |

### Maneuver

| Field | Type | Description |
|-------|------|-------------|
| `type` | `str` | Maneuver type |
| `modifier` | `str \| None` | Direction (left, right, straight) |
| `instruction` | `str` | Human-readable instruction |
| `bearing_before` | `float` | Bearing before |
| `bearing_after` | `float` | Bearing after |
| `location` | `list[float]` | [longitude, latitude] |

### Maneuver Types

| Type | Description |
|------|-------------|
| `depart` | Starting the route |
| `turn` | Turn at intersection |
| `merge` | Merge onto road |
| `fork` | Road splits |
| `roundabout` | Enter roundabout |
| `arrive` | Arrive at destination |
| `continue` | Continue straight |

---

## Matrix

### MatrixResult

| Field | Type | Description |
|-------|------|-------------|
| `code` | `str` | Response code ("Ok" on success) |
| `durations` | `list[list[float \| None]]` | Duration matrix (seconds) |
| `distances` | `list[list[float \| None]]` | Distance matrix (meters) |
| `sources` | `list[Waypoint]` | Source waypoints |
| `destinations` | `list[Waypoint]` | Destination waypoints |

---

## Optimization (v1 API)

### Request Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `profile` | `str` | mapbox/driving, mapbox/walking, mapbox/cycling, mapbox/driving-traffic |
| `coordinates` | `str` | Semicolon-separated lng,lat pairs (2-12 max) |
| `roundtrip` | `bool` | Return to start (default: true) |
| `source` | `str` | Start point: "first", "last", or "any" |
| `destination` | `str` | End point: "first", "last", or "any" |
| `steps` | `bool` | Include turn-by-turn instructions |
| `geometries` | `str` | geojson, polyline, polyline6 |
| `overview` | `str` | full, simplified, false |

### OptimizationResult

| Field | Type | Description |
|-------|------|-------------|
| `code` | `str` | "Ok" on success |
| `trips` | `list[Trip]` | Optimized trips |
| `waypoints` | `list[Waypoint]` | Waypoints with optimized order |

### Trip

| Field | Type | Description |
|-------|------|-------------|
| `distance` | `float` | Total distance (meters) |
| `duration` | `float` | Total duration (seconds) |
| `geometry` | `Geometry` | Route geometry |
| `legs` | `list[Leg]` | Route legs |
| `weight` | `float` | Route weight |
| `weight_name` | `str` | Weight type used |

### Optimization Waypoint

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` | Street/location name |
| `location` | `list[float]` | [longitude, latitude] |
| `waypoint_index` | `int` | Position in optimized order |
| `trips_index` | `int` | Index of associated trip |

---

## Error Codes

### HTTP Status Codes

| Code | Description | Action |
|------|-------------|--------|
| `200` | Success | Process response |
| `401` | Unauthorized | Check API key |
| `403` | Forbidden | Check permissions |
| `422` | Invalid parameters | Check request |
| `429` | Rate limit | Back off and retry |

### Response Codes

| Code | Description |
|------|-------------|
| `Ok` | Success |
| `NoRoute` | No route found |
| `NoSegment` | Cannot snap to road |
| `ProfileNotFound` | Invalid profile |
| `InvalidInput` | Invalid coordinates |

---

## Additional Resources

- [Geocoding API](https://docs.mapbox.com/api/search/geocoding/)
- [Directions API](https://docs.mapbox.com/api/navigation/directions/)
- [Matrix API](https://docs.mapbox.com/api/navigation/matrix/)
- [Optimization v2 API](https://docs.mapbox.com/api/navigation/optimization-v2/)
