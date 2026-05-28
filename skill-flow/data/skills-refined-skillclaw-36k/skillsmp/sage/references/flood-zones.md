# FEMA Flood Zone Interpretation Guide

## Overview

FEMA's National Flood Hazard Layer (NFHL) maps flood risk across the United States. These maps determine flood insurance requirements and building regulations.

## Special Flood Hazard Areas (SFHA)

SFHAs are areas with a 1% annual chance of flooding (often called "100-year flood"). These zones have the most significant regulatory implications.

### Zone A
- **Definition**: 1% annual chance flood, no Base Flood Elevation determined
- **Insurance**: Required for federally-backed mortgages
- **Building**: Must elevate to BFE (determined by community or engineer)
- **Common in**: Unmapped detailed areas

### Zone AE
- **Definition**: 1% annual chance flood WITH Base Flood Elevation determined
- **Insurance**: Required for federally-backed mortgages
- **Building**: Must elevate lowest floor to or above BFE
- **Common in**: Detailed study areas along major waterways

### Zone AH
- **Definition**: 1% annual chance of shallow flooding (1-3 feet), ponding
- **Insurance**: Required for federally-backed mortgages
- **Building**: Must elevate to BFE
- **Common in**: Flat areas with poor drainage

### Zone AO
- **Definition**: 1% annual chance of shallow flooding, sheet flow
- **Insurance**: Required for federally-backed mortgages
- **Building**: Must elevate above highest adjacent grade
- **Common in**: Alluvial fans, sheet flow areas

### Zone VE
- **Definition**: Coastal high hazard area with velocity (wave action)
- **Insurance**: Required, higher rates
- **Building**: Strictest requirements, must be elevated on pilings
- **Common in**: Not typically in Solano County (no ocean coast)

## Non-SFHA Zones

### Zone X (shaded)
- **Definition**: 0.2% annual chance flood (500-year) OR 1% with average depth <1 foot
- **Insurance**: Not required but recommended
- **Building**: Standard codes apply
- **Risk level**: Moderate

### Zone X (unshaded)
- **Definition**: Areas outside 500-year floodplain
- **Insurance**: Not required, available at lower rates
- **Building**: Standard codes apply
- **Risk level**: Minimal (but not zero)

### Zone D
- **Definition**: Undetermined flood hazard
- **Insurance**: Available but not required
- **Building**: Local codes apply
- **Note**: No flood study performed for this area

## Insurance Implications

### Mandatory Purchase
For properties in SFHA zones (A, AE, AH, AO, V, VE):
- Required if mortgage is from federally-regulated or insured lender
- Must maintain for life of loan
- Private flood insurance may satisfy requirement

### Recommended Purchase
For properties in Zone X:
- Not required but strongly recommended
- About 25% of flood claims come from Zone X
- Rates are typically lower (Preferred Risk Policy)

### NFIP vs. Private Insurance
- **NFIP**: Federal program, standardized coverage limits
- **Private**: May offer higher limits, different terms
- Both can satisfy lender requirements

## Building Requirements in SFHA

### Lowest Floor Elevation
New construction and substantial improvement must have lowest floor:
- At or above BFE in Zone AE
- Above highest adjacent grade + depth number in Zone AO
- Determined by engineer/community if no BFE (Zone A)

### Substantial Improvement
If improvement cost ≥ 50% of building value:
- Must bring entire structure into compliance
- Includes cumulative improvements over time in some communities

### Enclosures Below BFE
- Allowed only for parking, storage, building access
- Must have flood openings (vents)
- Cannot be finished living space

## Letters of Map Change

### LOMA (Letter of Map Amendment)
- For naturally high ground incorrectly mapped in SFHA
- Requires elevation certificate showing above BFE
- Removes flood insurance requirement

### LOMR (Letter of Map Revision)
- For changes to floodplain due to physical changes
- Requires engineering study
- Can result from fill, levee construction, channel improvements

### LOMR-F (Letter of Map Revision based on Fill)
- For properties elevated by fill material
- Requires documentation of compliant fill placement

## Solano County Context

### Major Flood Sources
- Sacramento River and tributaries
- Suisun Marsh and sloughs
- Local creeks (Green Valley, Suisun, Ulatis)
- Delta waterways

### Levee-Protected Areas
Many areas in Solano County are protected by levees:
- Behind levees may be Zone X or "protected by levee"
- Levee failure would result in significant flooding
- FEMA may map as Zone AE if levee doesn't meet standards

### Historical Floods
- 1986: Significant flooding in multiple areas
- 1997: Major Sacramento River flooding
- 2017: Oroville Dam spillway incident affected region

## Common Questions

**Q: My property has never flooded. Why am I in a flood zone?**
A: Flood zones are based on statistical probability, not flood history. A 1% annual chance means flooding is possible in any year, regardless of past experience.

**Q: Can I remove my property from the flood zone?**
A: Possibly, through a LOMA or LOMR. You'll need an elevation certificate showing your property is above the BFE. Consult a surveyor and contact FEMA.

**Q: What if I disagree with my flood zone?**
A: You can appeal through the LOMA/LOMR process. Contact your local floodplain administrator (typically the Building Department) for guidance.

**Q: Does flood insurance cover everything?**
A: No. NFIP has coverage limits ($250K building, $100K contents for residential). It doesn't cover temporary housing, business interruption, or vehicles.

## GIS Layer URLs for Visualization

When using `capture_map_view` to visualize flood zones:

| Layer | URL | Source |
|-------|-----|--------|
| FEMA NFHL (Official) | `https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer/28` | FEMA |
| California 100-Year Floodplain | `https://services.gis.ca.gov/arcgis/rest/services/InlandWaters/Flood_Risk_State/MapServer/0` | CA DWR |
| California 200-Year Floodplain | `https://services.gis.ca.gov/arcgis/rest/services/InlandWaters/Flood_Risk_State/MapServer/1` | CA DWR |
| County Floodplains (Local) | `https://services2.arcgis.com/SCn6czzcqKAFwdGU/ArcGIS/rest/services/Floodplains/FeatureServer/0` | Solano County |

**Map Rendering Tips:**
- Use opacity 0.4-0.6 for good visibility while still seeing parcels
- FEMA layer uses blue tints (darker = higher risk zones like AE, lighter = Zone X)
- State layers show simplified 100/200-year boundaries
- County layer may have more local detail for smaller drainages
- Consider county-wide view first to see flood patterns (concentrated along waterways, delta, marsh)
