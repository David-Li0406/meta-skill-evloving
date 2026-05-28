# GIS Layer Reference

This document covers how to discover and query Solano County GIS layers.

---

## Layer Discovery Tools

SAGE now has a **67-layer catalog** with metadata, service URLs, and field definitions. Use these tools to discover layers dynamically rather than hardcoding URLs.

### Discovery Tools

| Tool | Purpose |
|------|---------|
| `list_gis_categories` | Browse 11 categories with layer counts |
| `list_gis_layers` | List layers by category or priority |
| `search_gis_layers` | Keyword search across all layers |
| `get_gis_layer_details` | Full metadata, fields, service URL, downloads |
| `suggest_layers` | Match user questions to relevant layers |
| `list_gis_downloads` | List datasets with file downloads (Shapefile, GDB, LiDAR) |

### Categories Available

| Category | Layers | Examples |
|----------|--------|----------|
| property | 3 | Parcels, Address Points, Building Footprints |
| zoning | 16 | County zoning + all 7 city zoning/general plan layers |
| hazards | 7 | FEMA flood, CAL FIRE severity, fault zones, liquefaction |
| districts | 6 | BOS, Congressional, State Assembly/Senate, School |
| services | 3 | Garbage, Water, Fire Response |
| poi | 10 | Schools, Parks, Libraries, Hospitals, Transit |
| infrastructure | 5 | Road closures, bridges, culverts |
| emergency | 4 | OES real-time incidents |
| environmental | 3 | Farmland, conservation, soils |
| demographics | 2 | Census tracts, zip codes |
| basemap | 1 | 2025 aerial imagery |

### Example Discovery Workflow

```
User: "Is there a layer for fire stations?"

1. search_gis_layers({ query: "fire stations" })
   → Returns: solano-fire-stations (POI category)

2. get_gis_layer_details({ layerId: "solano-fire-stations" })
   → Returns: serviceUrl, fields, geometry type

3. Use URL with capture_map_view additionalLayers or direct query
```

---

## Data Downloads

Many layers offer both **live service URLs** (for real-time queries) AND **file downloads** (for bulk analysis, offline work, desktop GIS).

### Using list_gis_downloads

```javascript
// List all downloadable datasets
list_gis_downloads()

// Filter by format
list_gis_downloads({ format: "shapefile" })
list_gis_downloads({ format: "lidar" })

// Filter by category
list_gis_downloads({ category: "property" })
```

### Available Download Formats

| Format | Extension | Best For |
|--------|-----------|----------|
| `shapefile` | .shp/.dbf/.shx in .zip | Industry standard, ArcGIS/QGIS |
| `geodatabase` | .gdb in .zip | Esri workflows, richer data model |
| `geojson` | .geojson | Web applications, JavaScript |
| `csv` | .csv | Spreadsheets, tabular analysis |
| `lidar` | .laz | Elevation analysis, 3D modeling |
| `kml` | .kml/.kmz | Google Earth |

### Key Downloadable Datasets

- **Parcels** (shapefile/GDB) - 152k parcels with 89 fields
- **Address Points** (shapefile) - Address geocoding data
- **Road Centerlines** (shapefile) - Street network
- **Zoning** (shapefile) - Unincorporated zoning districts
- **General Plan** (shapefile) - Land use designations
- **Supervisor Districts** (shapefile) - BOS district boundaries
- **LiDAR** (LAZ) - 2023 USGS 3DEP point cloud data

### Download Workflow

```
1. list_gis_downloads() → Find available datasets
2. get_gis_layer_details({ layerId }) → Get download URLs
3. Provide URL to user for direct download
```

---

## Data Sources

The catalog includes layers from:

| Source | Type | Coverage |
|--------|------|----------|
| Solano County AGOL | County | Parcels, zoning, services, POI |
| Solano County Hosted | County | Roads, OES incidents |
| FEMA NFHL | Federal | Flood hazard zones |
| CAL FIRE | State | Fire hazard severity |
| CGS | State | Fault zones, liquefaction |

---

## Query Methods

### Attribute Queries (by value)

For layers with unique identifiers like APN:

```
WHERE parcelid = '0030251020'
WHERE fulladdress LIKE '675 TEXAS%'
```

**Best for:** Address Points, Parcels

### Spatial Queries (by location)

For layers where you need to find what polygon contains a point:

```json
{
  "geometry": {"x": -122.0, "y": 38.25},
  "geometryType": "esriGeometryPoint",
  "inSR": 4326,
  "spatialRel": "esriSpatialRelIntersects"
}
```

**Best for:** Zoning, flood zones, fire hazard, districts, service areas

### Using with capture_map_view

Once you have a service URL from `get_gis_layer_details`, use it with `capture_map_view`:

```javascript
capture_map_view({
  apn: "003-025-1020",
  additionalLayers: [{
    url: "https://services2.arcgis.com/.../Fire_Stations/FeatureServer/0",
    title: "Fire Stations"
  }]
})
```

---

## Lookup Strategy

### Standard Property Lookup Flow

```
Address Input
     │
     ▼
┌─────────────────────────────────────┐
│ 1. Address Points (Attribute Query) │
│    WHERE fulladdress LIKE '...'     │
│    → Returns: APN, lat, long        │
└─────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────┐
│ 2. Parcels (Attribute Query)        │
│    WHERE parcelid = 'APN'           │
│    → Returns: property details      │
└─────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────┐
│ 3. Overlay Layers (Spatial Queries) │
│    Point-in-polygon at lat/long     │
│    - Zoning, Flood, Fire, Districts │
└─────────────────────────────────────┘
```

### Why This Order?

1. **Address Points have pre-linked APNs** - no spatial matching errors
2. **Parcels have all property data** - values, use codes, districts
3. **Spatial queries needed for zones/districts** - they don't store APNs

---

## Key Layer Details

### Address Points
- **Lookup:** Attribute query on `fulladdress`
- **Key fields:** `apn`, `fulladdress`, `lat`, `long`, `post_comm`
- **Returns:** APN + coordinates for subsequent queries

### Parcels (Parcels_Public_Aumentum)
- **Lookup:** Attribute query on `parcelid` (APN from Address Points)
- **Key fields:** `parcelid`, `acres`, `use_desc`, `yrbuilt`, `valland`, `valimp`, `zone1`
- **Geometry:** Polygon (parcel boundary)
- **Links:** `propurl`, `taxinfo`, `taxmaplink`

### Zoning (County vs City)
- **County:** `SolanoCountyZoning_092322/FeatureServer/4` - unincorporated only
- **Cities:** Separate layer per city (Benicia, Dixon, Fairfield, Rio Vista, Suisun City, Vacaville, Vallejo)
- **Use `get_zoning` tool** - it handles jurisdiction routing automatically

### FEMA Flood Zones
- **URL:** `https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer/28`
- **Key fields:** `FLD_ZONE`, `SFHA_TF`
- **Zones:** A/AE/AH/AO (high risk), X shaded (moderate), X unshaded (low)

### CAL FIRE FHSZ
- **SRA:** `https://services.gis.ca.gov/.../Fire_Severity_Zones/MapServer/0`
- **LRA:** `https://services.gis.ca.gov/.../Fire_Severity_Zones/MapServer/1`
- **Key fields:** `HAZ_CODE` (1=Moderate, 2=High, 3=Very High)
- **Query both** - SRA covers rural, LRA covers cities

---

## Coordinate Systems

| System | EPSG | Usage |
|--------|------|-------|
| WGS84 | 4326 | GPS, web maps, always use for input |
| CA State Plane III | 103004 | Solano County internal storage |

Always specify `inSR: 4326` when querying with lat/long coordinates.

---

## Common Patterns

### "What layers answer this question?"

```javascript
suggest_layers({
  question: "Is this property in a flood zone?"
})
// Returns: FEMA flood zones, local floodplains
```

### "What GIS data is available for zoning?"

```javascript
list_gis_layers({ category: "zoning" })
// Returns: 16 layers (county + 7 cities, zoning + general plan)
```

### "Get the service URL for rendering"

```javascript
get_gis_layer_details({ layerId: "fema-flood-zones" })
// Returns: full serviceUrl, fields, geometry type
```

### "Add a layer to my map"

```javascript
// After getting URL from get_gis_layer_details:
capture_map_view({
  apn: "003-025-1020",
  additionalLayers: [{
    url: result.serviceUrl,
    title: "FEMA Flood Zones",
    opacity: 0.6
  }]
})
```

### "Download parcel data"

```javascript
// List downloadable datasets
list_gis_downloads({ format: "shapefile" })
// Returns: parcels, addresses, roads, etc.

// Get specific download URL
get_gis_layer_details({ layerId: "solano-parcels" })
// Returns: downloads array with format, url, size
```

---

## Quick Reference: Priority Layers

These are the most commonly needed layers (use `list_gis_layers({ priority: "high" })`):

| Layer | Purpose | Lookup |
|-------|---------|--------|
| Address Points | Address → APN | Attribute |
| Parcels | Property details | Attribute |
| County Zoning | Land use (uninc) | Spatial |
| City Zoning (7) | Land use (cities) | Spatial |
| FEMA Flood | Insurance/disclosure | Spatial |
| Fire Hazard | Disclosure/building | Spatial |
| Garbage Service | "Who picks up trash?" | Spatial |
| Water Districts | "Who provides water?" | Spatial |
| BOS Districts | Supervisor lookup | Spatial |
| Schools | Nearby school lookup | Spatial |
