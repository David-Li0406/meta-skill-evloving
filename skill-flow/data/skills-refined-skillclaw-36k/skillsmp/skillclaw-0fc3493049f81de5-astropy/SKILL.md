---
name: astropy
description: Use this skill when working with astronomical data, including celestial coordinates, physical units, FITS files, cosmological calculations, time systems, tables, and world coordinate systems (WCS).
---

# Astropy

## Overview

Astropy is the core Python package for astronomy, providing essential functionality for astronomical research and data analysis. Use Astropy for coordinate transformations, unit and quantity calculations, FITS file operations, cosmological calculations, precise time handling, tabular data manipulation, and astronomical image processing.

## When to Use This Skill

Use Astropy when tasks involve:
- Converting between celestial coordinate systems (ICRS, Galactic, FK5, AltAz, etc.)
- Working with physical units and quantities (converting Jy to mJy, parsecs to km, etc.)
- Reading, writing, or manipulating FITS files (images or tables)
- Performing cosmological calculations (luminosity distance, lookback time, Hubble parameter)
- Handling precise time with different time scales (UTC, TAI, TT, TDB) and formats (JD, MJD, ISO)
- Conducting table operations (reading catalogs, cross-matching, filtering, joining)
- Executing WCS transformations between pixel and world coordinates
- Utilizing astronomical constants and calculations

## Quick Start

```python
import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.time import Time
from astropy.io import fits
from astropy.table import Table
from astropy.cosmology import Planck18

# Units and quantities
distance = 100 * u.pc
distance_km = distance.to(u.km)

# Coordinates
coord = SkyCoord(ra=10.5*u.degree, dec=41.2*u.degree, frame='icrs')
coord_galactic = coord.galactic

# Time
t = Time('2023-01-15 12:30:00')
jd = t.jd  # Julian Date

# FITS files
data = fits.getdata('image.fits')
header = fits.getheader('image.fits')

# Tables
table = Table.read('catalog.fits')

# Cosmology
d_L = Planck18.luminosity_distance(z=1.0)
```

## Core Capabilities

### 1. Units and Quantities (`astropy.units`)

Handle physical quantities with units, perform unit conversions, and ensure dimensional consistency in calculations.

**Key operations:**
- Create quantities by multiplying values with units
- Convert between units using `to()`
- Perform arithmetic operations with quantities while maintaining unit consistency