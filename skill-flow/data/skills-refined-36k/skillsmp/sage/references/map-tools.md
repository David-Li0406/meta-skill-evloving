# Map Tools Reference

SAGE provides two distinct mapping tools for different purposes:

| Tool | Output | Purpose | Best For |
|------|--------|---------|----------|
| `capture_map_view` | Static image | AI spatial analysis | Verifying locations, assessing spatial relationships |
| `get_interactive_map_url` | URL to live map | User exploration | Panning, zooming, toggling layers, detailed exploration |

---

## When to Use Which Tool

### Use `capture_map_view` when:
- You need to visually verify a location or parcel
- You're assessing spatial relationships ("is this near the freeway?")
- You want to see the layout of parcels in a buffer/notification area
- You need to confirm what layers/features are present in an area
- You're making a spatial decision that requires visual context
- User needs a static image for a document or report

### Use `get_interactive_map_url` when:
- User wants to explore the map themselves
- User needs to toggle layers on/off
- User wants to change basemaps
- User is looking at multiple properties and wants to navigate
- After showing a static map, offer the interactive link for further exploration

---

## capture_map_view (Static Maps)

Generates a map image that is returned directly to you (the AI) for visual analysis. An imageUrl is also generated for sharing with the user.

### Location Input (provide ONE)

| Parameter | Description | Example |
|-----------|-------------|---------|
| `apn` | Center on and highlight a single parcel | `"0030-251-020"` |
| `apns` | Highlight multiple parcels | `["0030-251-020", "0030-251-021"]` |
| `center` | Center on coordinates (shows marker if no APN) | `{ latitude: 38.25, longitude: -122.04 }` |
| `bbox` | Explicit bounding box in WGS84 | `{ xmin, ymin, xmax, ymax }` |
| `buffer` | Buffer visualization for notification maps | See buffer section |
| `extent` | Full county view | `"county"` |

### Layer Options

```javascript
layers: {
  parcels: true,       // Parcel boundaries WITH APN labels (default: true at zoom >= 14)
  aerial2025: false,   // Solano County 2025 high-res aerial imagery
  addressPoints: false,
  cityBoundary: false,
  countyBoundary: false,
  garbageAreas: false
}
```

**Tip**: Enable `aerial2025` when zoomed in on individual parcels - it provides much clearer detail than the default basemap imagery.

### Basemap Options

| Basemap | Description | Best For |
|---------|-------------|----------|
| `topographic` | Default - hillshade + topo labels | General use, orientation |
| `imagery` | World satellite imagery | Regional context |
| `imagery-hybrid` | Satellite + labels | Satellite with reference labels |
| `navigation` | Street map style | Address/road context |

### Buffer Visualization

For notification radius maps (e.g., "parcels within 300 feet"):

```javascript
// Using APN as center
capture_map_view({
  buffer: {
    apn: "0030-251-020",
    radius_feet: 300,
    show_ring: true  // default: true
  }
})

// Using coordinates as center
capture_map_view({
  buffer: {
    latitude: 38.25,
    longitude: -122.04,
    radius_feet: 500
  }
})
```

The buffer visualization shows:
- **Orange fill**: Source parcel (if APN provided)
- **Dashed orange ring**: Buffer radius circle
- **Blue highlight**: Target parcels within buffer (if also specified via `apns`)

### Adding External Layers

Overlay any ArcGIS service using `additionalLayers`:

```javascript
capture_map_view({
  apn: "0030-251-020",
  additionalLayers: [
    {
      url: "https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer/28",
      title: "FEMA Flood Zones",
      opacity: 0.6
    }
  ]
})
```

**Layer types** (auto-detected from URL, or specify):
- `ArcGISFeatureLayer` - FeatureServer layers
- `ArcGISMapServiceLayer` - MapServer dynamic layers
- `ArcGISTiledMapServiceLayer` - Tiled/cached layers

**Optional `where` clause** to filter features:
```javascript
additionalLayers: [{
  url: "https://..../Fire_Stations/FeatureServer/0",
  title: "Fire Stations",
  where: "CITY='Fairfield'"
}]
```

### Using Layer Extent

Set map extent based on a layer's features:

```javascript
capture_map_view({
  extentLayer: {
    url: "https://.../SomeLayer/FeatureServer/0",
    where: "DISTRICT='5'",  // optional filter
    padding: 0.1            // 10% padding (default)
  },
  additionalLayers: [...] // the layer to display
})
```

### Layout Templates

For maps with scale bars and titles:

```javascript
capture_map_view({
  apn: "0030-251-020",
  layout: "Letter ANSI A Landscape",  // or "A4 Landscape"
  layoutOptions: {
    title: "Property Location Map",
    author: "Solano County GIS",
    scalebarUnit: "Feet"  // Feet, Miles, Meters, Kilometers
  }
})
```

| Layout | Output |
|--------|--------|
| `MAP_ONLY` | Just the map (default) |
| `Letter ANSI A Landscape` | 8.5x11" with title, scale bar, north arrow |
| `A4 Landscape` | A4 size with marginalia |

### What You Get Back

The tool returns:
1. **Image**: Displayed directly for your visual analysis
2. **Spatial context metadata**:
   - `extent`: Bounding box coordinates
   - `scale`: Approximate map scale (e.g., "1:5K")
   - `layersShown`: List of visible layers
   - `highlightedApns`: APNs highlighted on map
   - `approximateArea`: Area shown (e.g., "~25 acres")
3. **imageUrl**: Public URL for sharing with user

### Common Patterns

**Verify a parcel location:**
```javascript
capture_map_view({ apn: "0030-251-020" })
```

**Notification buffer map:**
```javascript
capture_map_view({
  buffer: { apn: "0030-251-020", radius_feet: 300 }
})
```

**Check flood zones:**
```javascript
capture_map_view({
  apn: "0030-251-020",
  additionalLayers: [{
    url: "https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer/28",
    title: "Flood Zones"
  }]
})
```

**Detailed aerial view:**
```javascript
capture_map_view({
  apn: "0030-251-020",
  layers: { aerial2025: true }
})
```

**County overview:**
```javascript
capture_map_view({
  extent: "county",
  layers: { countyBoundary: true, cityBoundary: true }
})
```

---

## get_interactive_map_url (Live Maps)

Generates a URL to open the SAGE interactive map application where users can pan, zoom, toggle layers, and explore.

### Map Presets

| Preset | Name | Layers Included |
|--------|------|-----------------|
| `base` | Property Research | Parcels, addresses, basic layers (default) |
| `hazards` | Hazard Assessment | Flood zones, fire hazard severity, risk layers |
| `zoning` | Zoning Analysis | Zoning districts, land use designations |
| `environmental` | Environmental Review | Wetlands, habitat, environmental constraints |
| `districts` | District Lookup | Supervisor districts, special districts, service areas |

### Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `preset` | Map preset/theme | `"hazards"` |
| `apns` | Array of APNs to highlight (supports multiple!) | `["0027030010", "0027040010"]` |
| `address` | Geocode and highlight | `"675 Texas St, Fairfield, CA"` |
| `center` | Initial map center | `{ longitude: -122.0, latitude: 38.25 }` |
| `zoom` | Initial zoom (1-20) | `17` |
| `origin` | Route start point | `{ longitude, latitude, label? }` |
| `destination` | Route end point | `{ longitude, latitude, label? }` |

### Examples

**Single parcel view:**
```javascript
get_interactive_map_url({ apns: ["0001-011-180"] })
// → Opens map centered on parcel, highlighted
```

**Multiple parcels (site selection results):**
```javascript
get_interactive_map_url({
  apns: ["0027030010", "0027040010", "0031010500"],
  preset: "planning"
})
// → Opens map with all candidate parcels highlighted, zoomed to fit all
// Great for presenting search results or site selection candidates!
```

**Hazard assessment:**
```javascript
get_interactive_map_url({
  apns: ["0001-011-180"],
  preset: "hazards"
})
// → Opens hazard layers, centered on parcel
```

**Address lookup:**
```javascript
get_interactive_map_url({
  address: "675 Texas St, Fairfield, CA"
})
// → Geocodes address, highlights parcel
```

**Show driving route:**
```javascript
get_interactive_map_url({
  origin: { longitude: -122.0, latitude: 38.2, label: "Start" },
  destination: { longitude: -122.1, latitude: 38.3, label: "End" }
})
// → Opens map with route and distance/time overlay
```

### Using list_map_presets

To show available presets:
```javascript
list_map_presets()
// Returns all presets with descriptions
```

---

## Combining Map Tools

A typical workflow:

1. **Quick verification** with `capture_map_view`:
   ```javascript
   capture_map_view({ apn: "0030-251-020" })
   ```
   "I can see this parcel is located north of Texas Street..."

2. **Offer interactive exploration** with `get_interactive_map_url`:
   ```javascript
   get_interactive_map_url({ apn: "0030-251-020", preset: "hazards" })
   ```
   "Here's an interactive map where you can explore the hazard layers in more detail: [URL]"

---

## Technical Notes

### Coordinate Systems

| System | EPSG | Usage |
|--------|------|-------|
| WGS84 | 4326 | All tool inputs/outputs (lat/long) |
| Web Mercator | 3857 | Internal rendering |
| CA State Plane III | 103004 | County internal storage |

### Zoom Levels

| Zoom | Approximate Scale | View |
|------|-------------------|------|
| 10 | 1:600K | County overview |
| 12 | 1:150K | City area |
| 14 | 1:40K | Neighborhood |
| 16 | 1:10K | Blocks |
| 17 | 1:5K | Parcel detail (default) |
| 18 | 1:2.5K | Building detail |
| 19 | 1:1.2K | Maximum detail |

### Available Aerial Imagery Years

Solano County has historical aerial imagery available (though currently only 2025 is exposed in the tool):

| Year | Coverage |
|------|----------|
| 2025 | Countywide (current) |
| 2024 | Urban areas |
| 2023 | Urban areas |
| 2022 | Countywide |
| 2021 | Urban areas |
| 2019 | Countywide |
| 2017 | Countywide |
| 2015 | Countywide |
| 2008 | Countywide |
| 2004 | Countywide (oldest) |

### Print Service

Static maps are rendered using ESRI's hosted print service:
```
https://utility.arcgisonline.com/arcgis/rest/services/Utilities/PrintingTools/GPServer/Export%20Web%20Map%20Task/execute
```

The service composites:
1. Basemap tiles
2. Operational layers (parcels, boundaries, etc.)
3. Graphics layers (highlights, buffers, markers)
4. Layout elements (scale bar, title, north arrow)

### Symbol Colors

| Element | Color | RGBA |
|---------|-------|------|
| Highlighted parcel fill | Blue 30% | [59, 130, 246, 77] |
| Highlighted parcel outline | Blue solid | [59, 130, 246, 255] |
| Buffer source fill | Orange 40% | [249, 115, 22, 100] |
| Buffer ring | Orange dashed | [249, 115, 22, 230] |
| Center marker | Red | [220, 38, 38, 255] |

---

## Multi-Scale Analysis: Thinking Like a GIS Analyst

Maps render quickly and cheaply - don't hesitate to generate multiple views. Humans instinctively zoom in and out; as an AI, you need to deliberately work at multiple scales to get proper context.

### The Scale Problem

A single map view often fails to give complete context:
- **Zoomed in** (parcel level): You see detail, labels, building footprints - but can't tell where in the county this is, or what surrounds it
- **Zoomed out** (county level): You see regional patterns and layer coverage - but can't read parcel labels or see fine detail

**Solution: Generate multiple maps at different scales, just like a human analyst would pan and zoom.**

### Recommended Multi-Scale Workflow

#### For Property/Parcel Questions

1. **Parcel view (zoom 17-18)**: Start here for the specific property
   ```javascript
   capture_map_view({ apn: "012-805-010", zoom: 17 })
   ```
   - What: Parcel shape, neighboring parcels, street access
   - Labels: APN labels visible, street names

2. **Neighborhood view (zoom 14-15)**: Context
   ```javascript
   capture_map_view({ apn: "012-805-010", zoom: 14 })
   ```
   - What: Surrounding development pattern, distance to services
   - Missing: Fine detail, may lose some labels

3. **City/regional view (zoom 11-12)**: When relevant
   ```javascript
   capture_map_view({ apn: "012-805-010", zoom: 11, layers: { cityBoundary: true } })
   ```
   - What: City context, major roads, regional position

#### For Hazard Assessment

**Always start with county-wide view to understand layer coverage:**

```javascript
// First: County-wide hazard context
capture_map_view({
  extent: "county",
  additionalLayers: [{
    url: "https://services2.arcgis.com/SCn6czzcqKAFwdGU/ArcGIS/rest/services/FireHazardSeverityZone/FeatureServer/0",
    title: "Fire Hazard Severity"
  }],
  layers: { cityBoundary: true, countyBoundary: true }
})
// This shows: Where are the high-risk areas in the county?
// Is this property in a hotspot or isolated pocket?
```

```javascript
// Then: Parcel-specific view
capture_map_view({
  apn: "012-805-010",
  zoom: 15,
  additionalLayers: [{
    url: "https://services2.arcgis.com/SCn6czzcqKAFwdGU/ArcGIS/rest/services/FireHazardSeverityZone/FeatureServer/0",
    title: "Fire Hazard Severity"
  }]
})
// This shows: What exactly is this parcel's classification?
```

**Why this matters for hazards:**
- Fire and flood zones have distinct spatial patterns
- A parcel might be in a Very High fire zone, but so is half the county's western hills
- Or it might be an isolated high-risk pocket surrounded by moderate areas
- County view gives you interpretive context the parcel view can't provide

### Key GIS Analyst Habits to Adopt

1. **Verify layer coverage**: Before interpreting results, check if the layer even covers your area. Some layers have gaps.

2. **Check neighboring parcels**: A property's context matters. Is this the only agricultural parcel in a residential area? Is it at the edge of a fire zone?

3. **Use aerial for detail**: When zoomed in (17+), `aerial2025` gives much better visual context than basemap imagery.
   ```javascript
   capture_map_view({ apn: "012-805-010", zoom: 18, layers: { aerial2025: true } })
   ```

4. **Trust labels at appropriate zoom**: Parcel labels (APNs) become readable at zoom 16+. If you need to identify specific parcels, zoom in enough.

5. **Multiple hazard layers together**: Fire and flood often affect different areas - show them together for complete assessment:
   ```javascript
   capture_map_view({
     apn: "012-805-010",
     zoom: 14,
     additionalLayers: [
       { url: "...FireHazardSeverityZone...", title: "Fire", opacity: 0.4 },
       { url: "https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer/28", title: "Flood", opacity: 0.4 }
     ]
   })
   ```

### Scale Reference Table

| Question Type | Start Zoom | Also Check |
|--------------|------------|------------|
| "What's the zoning for this parcel?" | 17 | 14 (neighborhood pattern) |
| "Is this in a flood zone?" | 15, then county | County view first |
| "Is this in a fire hazard zone?" | 15, then county | County view first |
| "Where exactly is this property?" | 17 (detail), 12 (regional) | Both needed |
| "What's around this parcel?" | 14-15 | - |
| "Show me the buffer/notification area" | 17 | - |
| "What's the development pattern here?" | 13-14 | - |
| "County-wide overview of X" | 10 (county extent) | - |

### Example: Complete Hazard Assessment

For a thorough hazard assessment, generate 3 maps:

```javascript
// 1. County fire hazard context
capture_map_view({
  extent: "county",
  additionalLayers: [{ url: "...FireHazardSeverityZone...", opacity: 0.5 }],
  layers: { cityBoundary: true }
})
// "Looking at the county-wide fire hazard map, high-risk areas (red/orange)
// are concentrated in the western hills and Suisun Marsh edges..."

// 2. Property fire hazard detail
capture_map_view({
  apn: "012-805-010",
  zoom: 15,
  additionalLayers: [{ url: "...FireHazardSeverityZone...", opacity: 0.5 }]
})
// "Your specific parcel is in the Moderate zone (yellow), at the transition
// between the High zone to the west and the urban area to the east..."

// 3. Property flood hazard detail
capture_map_view({
  apn: "012-805-010",
  zoom: 15,
  additionalLayers: [{ url: "https://hazards.fema.gov/.../NFHL/MapServer/28", opacity: 0.5 }]
})
// "The FEMA flood map shows this parcel is in Zone X (minimal flood hazard)..."
```

### Available Hazard Layers

For reference, these hazard layers are available for visualization:

| Hazard | Layer URL | Notes |
|--------|-----------|-------|
| Fire (Current) | `services2.arcgis.com/SCn6czzcqKAFwdGU/.../FireHazardSeverityZone/FeatureServer/0` | CAL FIRE FHSZ |
| Fire (2025 Phase 2) | `services2.arcgis.com/SCn6czzcqKAFwdGU/.../FireHazardSeverityZone_Phase2_2025/FeatureServer/0` | Latest data |
| FEMA Flood | `hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer/28` | Official NFHL |
| CA 100-Year Flood | `services.gis.ca.gov/arcgis/rest/services/InlandWaters/Flood_Risk_State/MapServer/0` | State data |
| CA 200-Year Flood | `services.gis.ca.gov/arcgis/rest/services/InlandWaters/Flood_Risk_State/MapServer/1` | State data |
| County Floodplains | `services2.arcgis.com/SCn6czzcqKAFwdGU/.../Floodplains/FeatureServer/0` | Local data |
| Earthquake Faults | `services2.arcgis.com/zr3KAIbsRSUyARHG/.../CGS_Alquist_Priolo_Fault_Zones/FeatureServer/0` | CGS data |
| Wildlife Hazard | `services2.arcgis.com/SCn6czzcqKAFwdGU/.../BirdStrikeHazardZone/FeatureServer/0` | Travis AFB |

---

## Troubleshooting

### "APN not found"
- Verify APN format (e.g., "003-025-1020" or "0030251020")
- The tool normalizes APNs internally, but unusual formats may fail
- Try using coordinates instead: `center: { latitude, longitude }`

### Buffer map not showing parcels
- Buffer visualization only shows the ring and source parcel
- To highlight parcels WITHIN the buffer, use `find_nearby_parcels` first to get APNs, then pass them to `capture_map_view` via `apns`

### Layer not appearing
- Check that the service URL is accessible
- Verify the layerType matches the service type
- Check opacity isn't set too low
- Some layers only render at certain zoom levels

### Map extent too tight/loose
- Explicitly set `zoom` to override auto-calculation
- Use `bbox` for precise extent control
- For `extentLayer`, adjust `padding` (default: 0.1 = 10%)
