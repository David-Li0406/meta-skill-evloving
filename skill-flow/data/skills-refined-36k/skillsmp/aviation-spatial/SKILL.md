---
name: aviation-spatial
description: SpatiaLite database operations for aviation data. Use when building spatial indexes, running proximity queries, importing airspace GeoJSON, or performing geometric calculations on aviation features like finding airports within radius, airspace containment, or obstacle corridor searches.
---

# Aviation Spatial Database

## Overview

SpatiaLite-based spatial database operations for aviation data in the MagentaLine EFB.

## Quick Start

### Initialize SpatiaLite Database
```bash
python scripts/init_spatialite.py --output aviation.db
```

### Import Airspace Data
```bash
python scripts/import_airspace.py --input airspace.geojson --output aviation.db
```

### Build Spatial Indexes
```bash
python scripts/build_indexes.py --database aviation.db
```

## Features

- **Proximity queries** - Find airports/navaids within radius
- **Containment tests** - Check if point is within airspace
- **Corridor searches** - Find obstacles along route
- **R-Tree indexing** - Fast spatial lookups

## Schema

Full SpatiaLite schema in `assets/aviation_schema.sql`

## References

| Document | Description |
|----------|-------------|
| `references/schema.md` | Complete aviation schema |
| `references/spatial_queries.md` | Query patterns with examples |
| `references/coordinate_systems.md` | EPSG codes, projections |
