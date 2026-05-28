---
name: geopandas
description: Use this skill when working with geospatial vector data for spatial analysis, geometric operations, and coordinate transformations. It supports various file formats and integrates with mapping libraries for visualization.
---

# GeoPandas

GeoPandas extends pandas to enable spatial operations on geometric types. It combines the capabilities of pandas and shapely for geospatial data analysis.

## Installation

```bash
pip install geopandas
```

### Optional Dependencies

```bash
# For interactive maps
pip install folium

# For classification schemes in mapping
pip install mapclassify

# For faster I/O operations (2-4x speedup)
pip install pyarrow

# For PostGIS database support
pip install psycopg2 geoalchemy2

# For basemaps
pip install contextily

# For cartographic projections
pip install cartopy
```

## Quick Start

```python
import geopandas as gpd

# Read spatial data
gdf = gpd.read_file("data.geojson")

# Basic exploration
print(gdf.head())
print(gdf.crs)
print(gdf.geometry.geom_type)

# Simple plot
gdf.plot()

# Reproject to different CRS
gdf_projected = gdf.to_crs("EPSG:3857")

# Calculate area (use projected CRS for accuracy)
gdf_projected['area'] = gdf_projected.geometry.area

# Save to file
gdf.to_file("output.gpkg")
```

## Core Concepts

### Data Structures

- **GeoSeries**: Vector of geometries with spatial operations.
- **GeoDataFrame**: Tabular data structure with a geometry column.

### Reading and Writing Data

GeoPandas reads/writes multiple formats: Shapefile, GeoJSON, GeoPackage, PostGIS, Parquet.

```python
# Read with filtering
gdf = gpd.read_file("data.gpkg", bbox=(xmin, ymin, xmax, ymax))

# Write with Arrow acceleration
gdf.to_file("output.gpkg", use_arrow=True)
```

### Coordinate Reference Systems

Always check and manage CRS for accurate spatial operations:

```python
# Check CRS
print(gdf.crs)
```