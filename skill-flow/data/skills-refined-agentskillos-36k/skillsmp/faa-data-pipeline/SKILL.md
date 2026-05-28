---
name: faa-data-pipeline
description: Parse FAA aviation data sources (NASR, CIFP, d-TPP, DOF) into SQLite databases. Use when processing 28-day subscription data, building automated data pipelines, implementing AIRAC cycle updates, or working with FAA fixed-width file formats. Includes parsers for airports, runways, navaids, fixes, airways, frequencies, procedures (SIDs/STARs/approaches), obstacles, and approach plate manifests.
---

# FAA Data Pipeline

## Overview

Parse all FAA aviation data sources into SQLite databases for the MagentaLine EFB.

## Data Sources

| Source | URL | Cycle | Format |
|--------|-----|-------|--------|
| NASR | https://nfdc.faa.gov/webContent/28DaySub/ | 28 days | Fixed-width ASCII |
| CIFP | https://www.faa.gov/air_traffic/flight_info/aeronav/digital_products/cifp/ | 28 days | ARINC 424 |
| d-TPP | https://www.faa.gov/air_traffic/flight_info/aeronav/digital_products/dtpp/ | 28 days | PDF + XML |
| DOF | https://www.faa.gov/air_traffic/flight_info/aeronav/digital_products/dof/ | Daily | Fixed-width ASCII |

## Quick Start

### Download FAA Data
```bash
python scripts/download_faa_data.py --cycle 2513 --output ./faa_raw/
```

### Parse NASR Data
```bash
# Parse airports
python scripts/parse_nasr_apt.py --input faa_raw/APT.txt --output aviation.db

# Parse runways
python scripts/parse_nasr_rwy.py --input faa_raw/RWY.txt --output aviation.db

# Parse all NASR files
for script in parse_nasr_*.py; do
    python scripts/$script --input faa_raw/ --output aviation.db
done
```

### Parse CIFP Procedures
```bash
python scripts/parse_cifp.py --input faa_raw/FAACIFP18 --output aviation.db
```

### Parse Obstacles
```bash
python scripts/parse_dof.py --input faa_raw/DOF.DAT --output aviation.db
```

### Parse d-TPP Chart Manifest
```bash
python scripts/parse_dtpp_xml.py --input faa_raw/d-TPP_Metafile.xml --output aviation.db
```

### Validate Data
```bash
python scripts/validate_data.py --database aviation.db --expected-airports 19000
```

## File Format References

- NASR field specifications: See `references/nasr_field_specs.md`
- ARINC 424 record types: See `references/cifp_record_types.md`
- AIRAC schedule: See `references/airac_schedule.md`
- Data source URLs: See `references/data_sources.md`

## Schema

The complete SQLite schema is in `assets/aviation_schema.sql`

## Scripts

| Script | Description |
|--------|-------------|
| `download_faa_data.py` | Download FAA data files for a given AIRAC cycle |
| `parse_nasr_apt.py` | Parse APT.txt (airports) |
| `parse_nasr_rwy.py` | Parse RWY.txt (runways) |
| `parse_nasr_nav.py` | Parse NAV.txt (navaids) |
| `parse_nasr_fix.py` | Parse FIX.txt (fixes/waypoints) |
| `parse_nasr_awy.py` | Parse AWY*.txt (airways) |
| `parse_nasr_twr.py` | Parse TWR.txt (frequencies) |
| `parse_cifp.py` | Parse ARINC 424 CIFP data |
| `parse_dof.py` | Parse DOF.DAT (obstacles) |
| `parse_dtpp_xml.py` | Parse d-TPP metafile XML |
| `validate_data.py` | Data integrity validation |

## Usage Examples

### Building a Complete Aviation Database

```bash
# 1. Download current cycle data
python scripts/download_faa_data.py --cycle current --output ./faa_raw/

# 2. Initialize database with schema
sqlite3 aviation.db < assets/aviation_schema.sql

# 3. Parse all NASR files
python scripts/parse_nasr_apt.py --input faa_raw/APT.txt --output aviation.db
python scripts/parse_nasr_rwy.py --input faa_raw/RWY.txt --output aviation.db
python scripts/parse_nasr_nav.py --input faa_raw/NAV.txt --output aviation.db
python scripts/parse_nasr_fix.py --input faa_raw/FIX.txt --output aviation.db
python scripts/parse_nasr_awy.py --input faa_raw/ --output aviation.db
python scripts/parse_nasr_twr.py --input faa_raw/TWR.txt --output aviation.db

# 4. Parse CIFP procedures
python scripts/parse_cifp.py --input faa_raw/FAACIFP18 --output aviation.db

# 5. Parse obstacles
python scripts/parse_dof.py --input faa_raw/DOF.DAT --output aviation.db

# 6. Parse chart manifest
python scripts/parse_dtpp_xml.py --input faa_raw/d-TPP_Metafile.xml --output aviation.db

# 7. Validate
python scripts/validate_data.py --database aviation.db
```

### Incremental Updates

```bash
# Update only obstacles (daily)
python scripts/download_faa_data.py --type dof --output ./faa_raw/
python scripts/parse_dof.py --input faa_raw/DOF.DAT --output aviation.db --mode update

# Update for new AIRAC cycle
python scripts/download_faa_data.py --cycle 2514 --output ./faa_raw/
# ... run all parsers
```

## Data Integrity

The `validate_data.py` script checks:
- Expected record counts (airports, runways, navaids, etc.)
- Foreign key relationships
- Coordinate ranges (latitude: -90 to 90, longitude: -180 to 180)
- Required field presence
- Identifier format validation
