# FAA Data Sources

Official FAA data download URLs and documentation.

## Primary Data Sources

### NASR (National Airspace System Resources)

28-day subscription containing airports, runways, NAVAIDs, fixes, airways, frequencies.

**Download URL:**
```
https://nfdc.faa.gov/webContent/28DaySub/28DaySubscription_Effective_{YYYY-MM-DD}.zip
```

**Contents:**
| File | Description | Records |
|------|-------------|---------|
| APT.txt | Airports | ~19,000 |
| RWY.txt | Runways | ~25,000 |
| NAV.txt | NAVAIDs | ~4,000 |
| FIX.txt | Fixes/Waypoints | ~60,000 |
| AWY.txt | Airways | ~6,000 segments |
| TWR.txt | Tower Frequencies | ~25,000 |
| AFF.txt | Air Route Traffic Control | - |
| ARB.txt | ARTCC Boundaries | - |
| ATS.txt | ATS Routes | - |
| WXL.txt | Weather Locations | - |

**Documentation:**
- https://nfdc.faa.gov/webContent/28DaySub/28DaySubLayout.html

### CIFP (Coded Instrument Flight Procedures)

ARINC 424 format data for SIDs, STARs, and approaches.

**Download URL:**
```
https://aeronav.faa.gov/Upload_313-d/cifp/CIFP_{CYCLE}.zip
```

Example: `CIFP_2513.zip` for cycle 2513

**Contents:**
- `FAACIFP18` - Main CIFP data file (ARINC 424 format)

**Documentation:**
- ARINC 424 Specification (requires purchase)
- https://www.faa.gov/air_traffic/flight_info/aeronav/digital_products/cifp/

### d-TPP (Digital Terminal Procedures Publication)

Approach plates, airport diagrams, departure procedures.

**Manifest URL:**
```
https://aeronav.faa.gov/d-tpp/{CYCLE}/xml_data/d-TPP_Metafile.xml
```

**Individual Charts:**
```
https://aeronav.faa.gov/d-tpp/{CYCLE}/{PDF_NAME}
```

Example: `https://aeronav.faa.gov/d-tpp/2513/00058IL25L.PDF`

**Documentation:**
- https://www.faa.gov/air_traffic/flight_info/aeronav/digital_products/dtpp/

### DOF (Digital Obstacle File)

Daily-updated obstacle data (towers, buildings, antennas).

**Download URL:**
```
https://aeronav.faa.gov/Obst_Data/DAILY_DOF_DAT.ZIP
```

**Contents:**
- `DOF.DAT` - All obstacles (~600,000 records)

**Documentation:**
- https://www.faa.gov/air_traffic/flight_info/aeronav/digital_products/dof/

## VFR/IFR Charts

### VFR Sectional Charts

**Raster (GeoTIFF):**
```
https://aeronav.faa.gov/visual/{CYCLE}/sectional_files/
```

**Vector (coming soon via AeroNav):**
- Currently not available in vector format

### IFR Enroute Charts

**Low Altitude:**
```
https://aeronav.faa.gov/enroute/{CYCLE}/
```

**High Altitude:**
```
https://aeronav.faa.gov/enroute/{CYCLE}/
```

## Weather Data

### Aviation Weather Center

**METARs:**
```
https://aviationweather.gov/api/data/metar?ids={STATION}&format=json
```

**TAFs:**
```
https://aviationweather.gov/api/data/taf?ids={STATION}&format=json
```

**NEXRAD Radar:**
```
https://aviationweather.gov/data/cache/nexrad/
```

**Documentation:**
- https://aviationweather.gov/data/api/

### TFRs (Temporary Flight Restrictions)

**XML Feed:**
```
https://tfr.faa.gov/tfr2/list.xml
```

**GeoJSON:**
```
https://tfr.faa.gov/tfr2/list.geojson
```

## API Endpoints

### FAA SWIM (System Wide Information Management)

Enterprise-level data feeds (requires registration):
- https://www.faa.gov/air_traffic/technology/swim

### AeroAPI (FlightAware)

Commercial API for real-time flight data:
- https://flightaware.com/commercial/aeroapi/

## Data Formats

| Source | Format | Encoding |
|--------|--------|----------|
| NASR | Fixed-width ASCII | Latin-1 |
| CIFP | ARINC 424 (fixed-width) | ASCII |
| d-TPP Manifest | XML | UTF-8 |
| DOF | Fixed-width ASCII | Latin-1 |
| Weather | JSON/XML | UTF-8 |
| TFRs | XML/GeoJSON | UTF-8 |

## Update Frequency

| Data | Update Frequency | Typical Availability |
|------|------------------|----------------------|
| NASR | 28 days | 14 days before effective |
| CIFP | 28 days | 14 days before effective |
| d-TPP | 28 days | 14 days before effective |
| Charts | 56 days | 14 days before effective |
| DOF | Daily | Same day |
| METARs | Hourly | Real-time |
| TAFs | 6 hours | Real-time |
| TFRs | As issued | Real-time |

## License & Usage

All FAA data is **public domain** and can be freely used, redistributed, and modified.

However, note:
- Data may not be current or accurate
- Always verify against official sources before flight
- Commercial redistribution may have practical limitations (bandwidth, etc.)
