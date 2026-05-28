# Aumentum Property Tax System & Parcel Data

Solano County uses **Aumentum Technologies** as their Computer Assisted Mass Appraisal (CAMA) and property tax management system. The parcel data available through SAGE comes directly from this system.

---

## System Overview

### What is Aumentum?

Aumentum is an enterprise property tax platform that manages the complete property tax lifecycle:
- **Valuation (CAMA)**: Appraisal tools, cost/market/income approaches, mass valuation
- **Assessment Administration**: Exemptions, value caps (Prop 13), penalties
- **Records Management**: Property and owner database
- **GIS Integration**: Esri ArcGIS Server integration (Aumentum GeoAnalyst)
- **Tax Collection**: Billing, collection, distribution

### Solano County Implementation

- **Go-Live**: 2023 (replaced legacy SCIPS system)
- **Internal Name**: CATS (County Assessment Tax System)
- **Investment**: ~$10 million multi-year project
- **Annual Hosting**: $616,000/year (DoIT budget line item)
- **Assessment Roll**: $77.96 billion (FY2025-26)
- **Parcels**: ~152,738 parcels
- **Stakeholders**: Assessor-Recorder, Auditor-Controller, Treasurer-Tax Collector, DoIT

### Aumentum Market Context

Aumentum Technologies (acquired by Harris Computer in 2019) serves hundreds of jurisdictions across 29 US states. In California, other Aumentum users include Riverside County and Mendocino County. The CAMA market is fragmented—competitors include Tyler Technologies (iasWorld), Thomson Reuters, and various legacy systems. Aumentum tends to target mid-to-large counties with complex assessment needs.

### How Data Flows

```
Building Permits, Deeds → Assessor (Valuation) → Assessment Roll (July 1)
                                                        ↓
                                              Auditor-Controller (Tax Rate)
                                                        ↓
                                              Tax Collector (Bills/Collection)
                                                        ↓
                                              Revenue Distribution
                                              (County, Schools, Cities, Districts)
```

### GIS-CAMA Integration Workflow

The parcel data involves coordination between multiple departments and contractors:

**Staffing (from FY2025-26 Budget):**

| Department | Role | Staff |
|------------|------|-------|
| Assessor/Recorder | Appraisal & valuation | 49 FTE (16 Appraisers, 2 Cadastral Mapping Techs) |
| DoIT GIS Division | Parcel geometry, map services | 5 FTE (incl. 1 Cadastral Mapping Tech) |
| GTG Contractor | QA/QC, parcel maintenance | $416,000/year contract |
| County Surveyor | Legal boundary surveys | 1 FTE (in Public Works) |

**Likely Parcel Maintenance Flow:**

```
     DEED RECORDED (Recorder Division)
                  │
    ┌─────────────┴─────────────┐
    ▼                           ▼
┌─────────────────┐    ┌─────────────────┐
│ ASSESSOR        │    │ DoIT GIS + GTG  │
│ Cadastral (2)   │    │ Cadastral (1+)  │
│ • New APNs      │    │ • Edit polygons │
│ • Legal desc    │    │ • Split/merge   │
│ • Update CATS   │    │ • QA/QC         │
└────────┬────────┘    └────────┬────────┘
         │                      │
         ▼                      ▼
   ┌───────────┐         ┌───────────┐
   │ AUMENTUM  │         │ ArcGIS    │
   │ (CATS)    │◄───────►│ Enterprise│
   │ SQL Server│  APN    │ Geodatabase│
   └─────┬─────┘  Join   └─────┬─────┘
         │                     │
         └──────────┬──────────┘
                    ▼
         ┌─────────────────────┐
         │  MONTHLY SYNC (ETL) │
         │  Join on parcelid   │
         └──────────┬──────────┘
                    ▼
         ┌─────────────────────┐
         │ Parcels_Public_     │
         │ Aumentum (ArcGIS    │
         │ Feature Service)    │
         └─────────────────────┘
```

**Evidence for this workflow:**
- `c_user`, `last_edit` fields show GTG contractor emails (e.g., ecolaiacomo@geotg.com)
- `gtg_review`, `gtg_notes` fields exist for QA tracking
- Budget shows separate line items: $616K Aumentum hosting (DoIT) + $416K GIS consulting (GTG)
- Two cadastral mapping techs in Assessor, one in DoIT GIS—suggests split responsibility
- `gis_acre` vs `acres` fields indicate GIS-calculated vs legal/deeded values maintained separately

---

## Parcel Data Layer

**Layer Name**: Parcels_Public_Aumentum
**Service**: `https://services5.arcgis.com/rDlqVjMA0Gtex3Mg/arcgis/rest/services/Parcels_Public_Aumentum/FeatureServer/1`
**Features**: 152,738 parcels
**Fields**: 89 attributes
**Update Frequency**: Monthly
**Data Steward**: Solano County DoIT GIS Division + Geographic Technologies Group (GTG)

**Related Budget Items (FY2025-26):**
- $416,000 - GIS consulting services (GTG)
- $249,000 - GIS flyover (aerial imagery)
- $160,000 - NV5 Geospatial cloud services
- $128,000 - ESRI software maintenance
- $96,000 - GIS derivative products

---

## Field Reference

### Identification Fields

| Field | Alias | Description |
|-------|-------|-------------|
| `parcelid` | APN Number | Assessor's Parcel Number - primary identifier (format: XXXXXXXXXX) |
| `lowparceli` | APN for Multi-unit | APN for the lot in multi-unit dwellings |
| `asmtnum` | PIN | Assessment number (same as parcelid in most cases) |
| `taxmapno` | Tax Map Number | Reference to the tax map page |

### GIS/Geometry Fields

| Field | Alias | Description |
|-------|-------|-------------|
| `gis_acre` | Measured Acreage | GIS-calculated acreage from polygon |
| `acres` | Recorded Acreage | Deeded/recorded acreage (may differ from GIS) |
| `lotsize` | Lot Size Sq Ft | Lot size in square feet |
| `xcentroid` | X Centroid | Longitude of parcel centroid |
| `ycentroid` | Y Centroid | Latitude of parcel centroid |
| `acre_diff` | Acreage Difference | Difference between GIS and recorded acres |
| `Shape__Area` | Shape Area | Polygon area (internal) |
| `Shape__Length` | Shape Length | Polygon perimeter (internal) |

### Administrative Fields

| Field | Alias | Description |
|-------|-------|-------------|
| `c_user` | Created User | Who created the parcel record |
| `c_date` | Created Date | When parcel was created |
| `last_edit` | Last Edited User | Last editor |
| `last_edate` | Last Edited Date | Last edit date |
| `gtg_review` | GTG Review Notes | Quality review notes |
| `gtg_notes` | GTG Team Notes | Data steward notes |
| `countynote` | County GIS Notes | County staff notes |
| `data_note` | Data Notes | General data notes |
| `floororder` | Building Floor | Floor order for multi-story |
| `status` | PIN Status | Active (AC) or inactive status |
| `rollyear` | Tax Roll Year | Current assessment roll year |
| `p_create` | Parcel Creation Date | Original parcel creation |
| `p_inactive` | Parcel Inactivation | When parcel was retired |

### Address/Site Fields

| Field | Alias | Description |
|-------|-------|-------------|
| `situs` | Site Address | Whether situs address exists |
| `sitenum` | Site Number | Street number |
| `siteroad` | Site Street | Street name |
| `p_address` | Full Site Address | Complete street address |
| `sitecity` | Site City | City name (for grouping/dissolving) |
| `unitbldg` | Unit/Building | Unit or building identifier |

### Property Use Fields

| Field | Alias | Description |
|-------|-------|-------------|
| `usecode` | Use Code | Numeric use classification |
| `use_desc` | Use Description | Human-readable use type |
| `subdiv` | Subdivision | Subdivision name |
| `qclass` | Quality Class | Building quality rating |
| `yrbuilt` | Year Built | Construction year |

**Common Use Codes:**
- `0100-0199`: Residential
- `0200-0299`: Multi-family
- `0300-0399`: Commercial
- `0400-0499`: Industrial
- `0500-0599`: Rural/Agricultural
- `0600-0699`: Recreational
- `9800`: Governmental/Miscellaneous

### Valuation Fields (Prop 13 Assessed Values)

| Field | Alias | Description |
|-------|-------|-------------|
| `valland` | Land Value | Assessed value of land |
| `valimp` | Improvement Value | Assessed value of structures |
| `valtv` | Trees & Vines Value | Value of permanent plantings |
| `valfme` | Fixed Machinery Value | Fixed machinery & equipment |
| `valpp` | Personal Property | Business personal property |
| `valpen` | Penalty Value | Any penalty assessments |

**Note**: These are **assessed values** under Prop 13, NOT market values. Long-held properties may have assessed values far below market value due to the 2% annual cap.

### Building Characteristics

| Field | Alias | Description |
|-------|-------|-------------|
| `firs_floor` | First Floor Area | First floor sq ft |
| `sec_floor` | Second Floor Area | Second floor sq ft |
| `thir_floor` | Third Floor Area | Third floor sq ft |
| `other_area` | Other Area | Other building area |
| `garage` | Garage Area | Garage sq ft |
| `total_area` | Total Area | Total building sq ft |
| `stories` | Stories | Number of stories |
| `bedroom` | Bedrooms | Bedroom count |
| `bathroom` | Bathrooms | Bathroom count |
| `dining` | Dining Room | YS (Yes), NO, or blank |
| `family` | Family Room | YS (Yes), NO, or blank |
| `other_room` | Other Rooms | Count of other rooms |
| `utility` | Utility Room | YS (Yes), NO, or blank |
| `rooms` | Total Rooms | Total room count |
| `fireplc` | Fireplace | Count or YS/NO |
| `hvac` | HVAC Code | Heating/cooling type |
| `pool` | Swimming Pool | YS (Yes), NO, or blank |
| `solar` | Solar | YS (Yes), NO, or blank |

### Williamson Act (Agricultural Preserves)

| Field | Alias | Description |
|-------|-------|-------------|
| `wa` | Williamson Act | In WA contract? |
| `wa_status` | WA Status Code | Contract status |
| `wacontno` | WA Contract Number | Contract identifier |
| `wa_prime` | Prime Acreage | Prime farmland acres |
| `noprimacre` | Nonprime Acreage | Non-prime acres |
| `exacre` | Excluded Acreage | Acres excluded from WA |

**Williamson Act Status Codes:**
- `AC`: Active contract
- `NR`: Non-renewal filed
- `CA`: Cancelled

### Tax District/Fund Fields (Key for Dissolving)

| Field | Alias | Description |
|-------|-------|-------------|
| `tac` | TAC | Tax Area Code |
| `tac_city` | TAC City | Tax Area Code city name |
| `fund_fire` | Fire District Code | Fire district fund number |
| `desc_fire` | Fire District Name | Fire district description |
| `f_school` | School District Code | School district fund number |
| `d_school` | School District Name | School district description |
| `fund_water` | Water District Code | Water district fund number |
| `desc_water` | Water District Name | Water district description |
| `f_airboard` | Air Board Code | Air quality district code |
| `d_airboard` | Air Board Name | Air quality district name |
| `f_soilcons` | Soil Conservation Code | Soil conservation district code |
| `d_soilcons` | Soil Conservation Name | Soil conservation district name |
| `govt_owned` | Government Owned | YES/NO government ownership |
| `hotype` | Homeowner Exemption | Exemption type code |

### Zoning Fields

| Field | Alias | Description |
|-------|-------|-------------|
| `zone1` | Zone 1 | Primary zoning code |
| `zone2` | Zone 2 | Secondary/overlay zoning |
| `zone3` | Zone 3 | Tertiary zoning |

**Note**: These zoning fields reflect Aumentum's internal copy. For authoritative zoning, use the `get_zoning` tool which queries the official zoning layers.

### Links

| Field | Alias | Description |
|-------|-------|-------------|
| `taxmaplink` | Tax Map Link | URL to tax map image |
| `propurl` | Property Link | URL to property details on Public Access |
| `taxinfo` | Tax Info Link | URL to tax information |

---

## Using Parcel Data

### Common Query Patterns

**By APN:**
```
search_parcels({ apn: "0030251020" })
get_parcel_details({ apn: "0030251020" })
```

**By Criteria:**
```
search_parcels({ zoning: "A-40", min_acres: 20 })
search_parcels({ city: "FAIRFIELD", use_desc: "SINGLE FAMILY RESIDENTIAL" })
search_parcels({ min_value: 1000000, max_acres: 5 })
```

### Dissolving Parcels into Boundaries

The parcel data contains district codes that can be dissolved to create boundary layers:

| Field to Dissolve | Creates | Example Result |
|-------------------|---------|----------------|
| `f_school` | School district boundaries | 9 districts |
| `desc_fire` | Fire district boundaries | ~6-8 districts |
| `fund_water` | Water district boundaries | Varies |
| `sitecity` | City boundaries from parcels | 7 cities |
| `wa_status` | Williamson Act areas | AC/NR/CA zones |
| `use_desc` | Land use categories | ~50+ categories |

**Example Dissolve:**
```
dissolve_layer({
  dataset: "parcels",
  dissolve_field: "f_school",
  output_name: "school_districts"
})
```

### Understanding Values

**When reporting assessed values, always note:**
1. These are Prop 13 assessed values, NOT market values
2. Long-held properties show values far below market
3. Base year determines when last reassessed
4. Land + Improvement = Total Assessed Value

**Example explanation:**
> "The assessed value is $285,000 (land: $120,000, improvements: $165,000). Note that this is the Prop 13 assessed value for tax purposes, which increases maximum 2% annually. A property purchased decades ago will have an assessed value significantly below current market value."

### Building Data Caveats

The building characteristics (bedrooms, bathrooms, sq ft) come from Assessor records:
- May be incomplete for older properties
- Updated when permits are pulled or properties sold
- Accessory structures may not be fully captured
- Use for general reference, not official records

---

## Data Quality Notes

### Monthly Updates
The parcel layer is updated monthly. Recent property transfers, new construction, or boundary changes may take 1-2 months to appear. The Assessor's office has noted ongoing work to reduce backlogs from the 2023 CATS implementation.

### GTG Review
Geographic Technologies Group (GTG) is a Raleigh, NC-based GIS consulting firm (Esri Gold Partner) that provides outsourced cadastral mapping services to local governments. GTG maintains geometry quality and attribute accuracy under a $416K annual contract with Solano County.

Review notes in `gtg_review` indicate parcels needing attention:
- "Needs further review"
- "Topology exception"
- "Adjacent parcel missing"
- "No GIS Primary Table APN Match"

The `gtg_notes` field captures specific issues like "In Water", "Condo/Business Park", or "Encroachment".

### Known Data Quality Issues
The `sitecity` field has inconsistent spelling (37 values instead of ~8 expected):
- BENICIA vs BENECIA
- FAIRFIELD vs FAIFIELD vs FAIRIFLED
- BIRDS LANDING vs BIRDS LNDG vs BIRDSLANDING

This is typical CAMA data entry drift—use `tac_city` for cleaner city groupings.

### Coordinate Accuracy
Parcel boundaries are maintained in California State Plane III (NAD83), EPSG:6418. Centroid coordinates (`xcentroid`, `ycentroid`) are in WGS84 for GIS compatibility.

---

## Related Resources

- **Property Lookup Portal**: https://ca-solano.publicaccessnow.com/
- **Assessor Contact**: (707) 784-6210
- **GIS Data Download**: Available through Solano Regional GIS Consortium (ReGIS)
- **Tax Collector**: (707) 784-7485

### Key Personnel (FY2025-26)
- **Glenn Zook** - Assessor/Recorder (elected)
- **Timothy P. Flanagan** - Chief Information Officer (DoIT)
- **Charles Lomeli** - Tax Collector/County Clerk

### Vendor Information
- **Aumentum Technologies** - CAMA software vendor (owned by Harris Computer since 2019)
- **Geographic Technologies Group (GTG)** - GIS data steward contractor
- **NV5 Geospatial** - Cloud GIS services

---

## Common Questions

**Q: Why does my property show a low assessed value?**
A: Due to Prop 13, assessed values increase max 2% annually from purchase/construction. Long-held properties show values far below market.

**Q: Why are building details missing?**
A: Older properties may have incomplete records. Data is updated when permits are pulled or properties are reassessed.

**Q: Why doesn't my address match the parcel?**
A: The `sitecity` field is mailing address city, which may differ from legal jurisdiction. A "Fairfield" address might be in unincorporated county.

**Q: How can I create district boundary layers?**
A: Use `dissolve_layer` with fields like `f_school`, `desc_fire`, or `fund_water` to merge parcels into boundary polygons.

**Q: Where do the district codes come from?**
A: District fund codes are maintained by the Auditor-Controller's office and linked to parcels in Aumentum for tax apportionment.

**Q: What is CATS?**
A: CATS (County Assessment Tax System) is Solano County's internal name for their Aumentum implementation.

**Q: Who maintains the parcel geometry vs attributes?**
A: It's split—the Assessor's Office cadastral techs maintain the assessment data in Aumentum, while DoIT GIS and the GTG contractor maintain the polygon geometry in ArcGIS. The two systems sync monthly using the APN (parcelid) as the join key.

**Q: Why does Solano outsource GIS to GTG?**
A: Many mid-size counties use contractors like GTG to supplement limited in-house GIS staff. GTG specializes in cadastral mapping for local governments. Solano's DoIT GIS division has only 5 FTE covering all county GIS needs—the $416K GTG contract provides additional capacity for parcel maintenance.

---

## Etymology

The name "Aumentum" derives from Latin *augmentum* meaning "increase, growth, augmentation" (from *augere* - to increase, enlarge). The company was founded in 1972 and was acquired by Harris Computer Corporation in 2019.
