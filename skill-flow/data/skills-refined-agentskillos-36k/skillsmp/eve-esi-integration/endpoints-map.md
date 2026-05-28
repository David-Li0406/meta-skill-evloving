# ESI Map & Navigation Endpoints

All endpoints for building map/navigation applications.

## Universe Structure (Public, No Auth)

### Systems

```
GET /universe/systems/
```
Returns: Array of all system IDs (8,285 systems)
Cache: 24 hours
Use: Initial data load

```
GET /universe/systems/{system_id}/
```
Returns:
```json
{
  "system_id": 30000142,
  "name": "Jita",
  "constellation_id": 20000020,
  "security_status": 0.9459,
  "security_class": "A",
  "star_id": 40009077,
  "stargates": [50001248, 50001249],
  "stations": [60003760],
  "planets": [{"planet_id": 40009078, "moons": [40009079]}],
  "position": {
    "x": -1.29e+17,
    "y": 6.07e+16,
    "z": 1.12e+17
  }
}
```
Cache: 1 hour

### Stargates

```
GET /universe/stargates/{stargate_id}/
```
Returns:
```json
{
  "stargate_id": 50001248,
  "name": "Stargate (Perimeter)",
  "system_id": 30000142,
  "type_id": 29624,
  "destination": {
    "stargate_id": 50001247,
    "system_id": 30000144
  },
  "position": {
    "x": 3.31e+11,
    "y": 4.36e+10,
    "z": -5.86e+11
  }
}
```
Cache: 1 hour
Use: Build connection graph

### Constellations

```
GET /universe/constellations/
```
Returns: Array of constellation IDs

```
GET /universe/constellations/{constellation_id}/
```
Returns:
```json
{
  "constellation_id": 20000020,
  "name": "Kimotoro",
  "region_id": 10000002,
  "systems": [30000142, 30000143, 30000144],
  "position": {"x": ..., "y": ..., "z": ...}
}
```

### Regions

```
GET /universe/regions/
```
Returns: Array of region IDs

```
GET /universe/regions/{region_id}/
```
Returns:
```json
{
  "region_id": 10000002,
  "name": "The Forge",
  "description": "...",
  "constellations": [20000020, 20000021, ...]
}
```

## Live Activity Data (Public, No Auth)

### System Kills

```
GET /universe/system_kills/
```
Returns:
```json
[
  {
    "system_id": 30000142,
    "ship_kills": 5,
    "npc_kills": 89,
    "pod_kills": 0
  },
  ...
]
```
Cache: 1 hour
Use: Kill heatmap layer

### System Jumps

```
GET /universe/system_jumps/
```
Returns:
```json
[
  {
    "system_id": 30000142,
    "ship_jumps": 12847
  },
  ...
]
```
Cache: 1 hour
Use: Traffic heatmap layer

## Route Planning (Public, No Auth)

### Calculate Route

```
GET /route/{origin}/{destination}/
```

Query params:
- `flag`: `shortest` (default), `secure`, `insecure`
- `avoid`: Array of system IDs to avoid

Returns: Array of system IDs representing path

Example:
```
GET /route/30000142/30002187/?flag=secure&avoid=30002768
```

Returns:
```json
[30000142, 30000144, 30000145, ..., 30002187]
```

Cache: 24 hours (but changes with sovereignty)

## Sovereignty Data (Public, No Auth)

### Sovereignty Map

```
GET /sovereignty/map/
```
Returns:
```json
[
  {
    "system_id": 30000001,
    "alliance_id": 99000001,
    "corporation_id": 98000001,
    "faction_id": null
  },
  ...
]
```

### Sovereignty Campaigns

```
GET /sovereignty/campaigns/
```
Returns active sovereignty fights

## Incursions (Public, No Auth)

```
GET /incursions/
```
Returns:
```json
[
  {
    "constellation_id": 20000001,
    "faction_id": 500019,
    "has_boss": true,
    "infested_solar_systems": [30000001, 30000002],
    "influence": 0.5,
    "staging_solar_system_id": 30000001,
    "state": "established",
    "type": "Incursion"
  }
]
```

## Character Location (Auth Required)

### Current Location

```
GET /characters/{character_id}/location/
```
Scope: `esi-location.read_location.v1`

Returns:
```json
{
  "solar_system_id": 30000142,
  "station_id": 60003760,
  "structure_id": null
}
```

### Online Status

```
GET /characters/{character_id}/online/
```
Scope: `esi-location.read_online.v1`

Returns:
```json
{
  "online": true,
  "last_login": "2025-01-01T12:00:00Z",
  "last_logout": "2025-01-01T10:00:00Z",
  "logins": 1247
}
```

### Set Waypoint

```
POST /ui/autopilot/waypoint/
```
Scope: `esi-ui.write_waypoint.v1`

Query params:
- `destination_id`: System/station/structure ID
- `add_to_beginning`: bool
- `clear_other_waypoints`: bool

Returns: 204 No Content (waypoint set in client)

## ID Resolution

### Names to IDs

```
POST /universe/ids/
```
Body: `["Jita", "The Forge", "Rifter"]`

Returns:
```json
{
  "systems": [{"id": 30000142, "name": "Jita"}],
  "regions": [{"id": 10000002, "name": "The Forge"}],
  "inventory_types": [{"id": 587, "name": "Rifter"}]
}
```

### IDs to Names

```
POST /universe/names/
```
Body: `[30000142, 10000002, 587]`

Returns:
```json
[
  {"id": 30000142, "name": "Jita", "category": "solar_system"},
  {"id": 10000002, "name": "The Forge", "category": "region"},
  {"id": 587, "name": "Rifter", "category": "inventory_type"}
]
```

## Best Practices for Map Apps

1. **Initial load**: Use SDE for bulk system/stargate data, not ESI
2. **Live layers**: Poll `/universe/system_kills/` and `system_jumps/` every 5-10 min
3. **Route caching**: Cache routes for 15 min minimum
4. **Connection graph**: Build once from SDE stargates, update on patch day
5. **2D projection**: Use x/z coordinates (y is "up" in EVE's 3D space)
