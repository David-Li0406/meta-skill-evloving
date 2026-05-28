# Advanced Capabilities

This reference covers SAGE's more sophisticated features for power users.

---

## AI-Generated Infographics

Use `generate_infographic` to create custom visuals on-the-fly:
- Org charts showing department structures
- Process flow diagrams for permit procedures
- Comparison charts for zoning districts
- Budget visualizations

**Example prompt**: "Create an organizational chart for Solano County showing the top 5 largest departments by staffing with FTE counts in boxes"

---

## Workforce Analytics

### Position Distribution

`get_position_distribution` shows where a job class is allocated county-wide:

```
Example: "Social Worker" → 159 FTEs across:
- H&SS Child Welfare: 87 FTEs
- H&SS Older/Disabled Adult Services: 53 FTEs
- Probation: 3 FTEs
- Public Defender: 3 FTEs
```

### Department Comparison

`compare_departments` for side-by-side analysis:

```
Example: Compare Sheriff, Probation, Public Defender
→ Shows FTEs, division counts, top 5 positions for each
```

---

## Parcel Search with Aggregations

`search_parcels` returns rich statistical data beyond samples:
- **total_count**: Number of matching parcels
- **total_acres / avg_acres**: Acreage statistics
- **total_value / avg_value**: Assessment value statistics
- **by_use**: Breakdown by property use type

**Example queries**:
- `{ "zoning": "A-40", "min_acres": 100 }` → 276 parcels, 49,337 total acres
- `{ "city": "VALLEJO", "min_acres": 1, "max_acres": 10 }` → 806 parcels with use breakdown

---

## Full Legal Text Retrieval

`get_county_code_sections` returns complete section text including:
- Full regulatory language with subsections
- Development standards tables
- Permit requirements
- Ordinance references

**Key sections for common questions**:
| Topic | Section |
|-------|---------|
| ADU/JADU rules | `28.72.10` (Dwellings - very detailed) |
| Agritourism | `28.75.10` (full requirements) |
| Administrative permits | `28.101` |
| Use permits | `28.106` |
| Variances | `28.107` |

---

## Housing Element Integration

The 2023-2031 Housing Element (Chapter 9) contains:
- ADU potential analysis and sites inventory
- Streamlined permitting policies
- Density and zoning tables
- RHNA allocation data

Search with: `search_general_plan` filtering `chapter: "9"`

---

## Budget Deep Dives

The budget document includes:
- **Section H**: Public Protection (Sheriff, DA, Probation, etc.)
- **Section J**: Health and Public Assistance (H&SS)
- **Section F**: General Government (Admin, IT, HR)

Use `search_budget` with department filter for targeted results:
```javascript
search_budget({ query: "pesticides", department: "Agricultural Commissioner" })
```

---

## Serverless Geoprocessing

Create derived boundary layers from source data using `dissolve_layer`.

### Create School District Boundaries

```javascript
dissolve_layer({
  dataset: "parcels",
  dissolve_field: "f_school",
  output_name: "school_districts"
})
```
→ Merges 152,738 parcels into 9 school district polygons
→ Returns GeoJSON URL: `https://...blob.vercel-storage.com/gis/school_districts.geojson`

### Publishing to ArcGIS Online

The returned GeoJSON URL can be directly added to AGOL:
1. Go to Content → Add Item → From URL
2. Paste the GeoJSON URL
3. Choose "GeoJSON" as type
4. Select "Add data and create a hosted feature layer"
5. Configure title, tags, and sharing

### Available Dissolve Datasets

- `parcels` (152k features) - richest data with 89 fields
- `zoning`, `generalPlan`, `supervisorDistricts`, `cityBoundary`, `countyBoundary`

### Inspect Before Dissolving

Use `inspect_layer` to see available fields and their unique value counts. Fields with 2-100 unique values are good dissolve candidates.

### Common Dissolve Fields (for parcels)

| Field | Description |
|-------|-------------|
| `f_school` / `d_school` | School district code / name |
| `fund_fire` / `desc_fire` | Fire district code / name |
| `fund_water` / `desc_water` | Water district code / name |
| `wa_status` | Williamson Act status |
| `sitecity` | City name (creates city boundaries) |
| `use_desc` | Land use description |

---

## County Overview Visualization

Generate county-wide context maps:

```javascript
capture_map_view({
  extent: 'county',
  layers: { countyBoundary: true, cityBoundary: true }
})
```

Shows all 7 cities within county boundaries.

For user exploration, offer the interactive version:

```javascript
get_interactive_map_url({ preset: 'districts' })
```
