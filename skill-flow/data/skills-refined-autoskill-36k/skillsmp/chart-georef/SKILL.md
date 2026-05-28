---
name: chart-georef
description: Georeferencing approach plates and airport diagrams. Use when adding location awareness to FAA d-TPP charts, creating moving map overlays for approach plates, or correlating CIFP procedures to chart images.
---

# Chart Georeferencing

## Overview

Add geographic coordinate references to approach plates and airport diagrams for moving map display.

## Process

1. **Extract Control Points** - Identify reference points on the chart
2. **Calculate Transform** - Compute affine transformation matrix
3. **Apply Georef** - Transform pixel coordinates to lat/lon
4. **Validate Accuracy** - Verify against known points

## Quick Start

### Extract Control Points

```python
from extract_control_points import extract_points

# Automatically find control points
points = extract_points('KLAX_ILS_25L.pdf')
# Returns: [(pixel_x, pixel_y, lat, lon), ...]
```

### Calculate Transformation

```python
from calculate_transform import PlateGeoreference

# From 3+ control points
georef = PlateGeoreference.from_control_points([
    (100, 200, 33.9425, -118.4081),  # Airport reference point
    (500, 150, 33.9500, -118.3800),  # Navaid
    (300, 600, 33.9200, -118.4200),  # Fix
])

# Transform pixel to lat/lon
lat, lon = georef.pixel_to_latlon(350, 400)
```

### Validate Accuracy

```python
from validate_accuracy import validate_georef

results = validate_georef(
    georef=georef,
    known_points=known_points,
    max_error_nm=0.1
)
print(f"RMS Error: {results['rms_error_nm']:.3f} nm")
```

## Control Point Types

| Type | Description | Accuracy |
|------|-------------|----------|
| Airport Reference | ARP coordinates | Highest |
| Runway Threshold | Threshold coordinates | High |
| NAVAID | VOR/NDB location | High |
| Fix | Named waypoint | Medium |
| DME Arc | Arc center | Medium |
| Procedure Turn | PT fix | Medium |

## References

- Affine transformation: `references/affine_transform.md`
- Control point types: `references/control_point_types.md`
- CIFP correlation: `references/cifp_correlation.md`
- Accuracy standards: `references/accuracy_standards.md`

## Scripts

| Script | Description |
|--------|-------------|
| `extract_control_points.py` | Find reference points in plates |
| `calculate_transform.py` | Compute affine transformation |
| `apply_georef.py` | Apply georef to plate image |
| `validate_accuracy.py` | Check georef accuracy |
| `correlate_cifp.py` | Match CIFP procedures to plates |
