---
name: histolab
description: Use this skill for lightweight whole slide image (WSI) tile extraction and preprocessing, including tissue detection and stain normalization for H&E images.
---

# Skill body

## Overview

Histolab is a Python library designed for processing whole slide images (WSI) in digital pathology. It automates tissue detection, extracts informative tiles from gigapixel images, and prepares datasets for deep learning pipelines. The library supports multiple WSI formats, implements sophisticated tissue segmentation, and provides flexible tile extraction strategies.

## Installation

```bash
uv pip install histolab
```

## Quick Start

Basic workflow for extracting tiles from a whole slide image:

```python
from histolab.slide import Slide
from histolab.tiler import RandomTiler

# Load slide
slide = Slide("slide.svs", processed_path="output/")

# Configure tiler
tiler = RandomTiler(
    tile_size=(512, 512),
    n_tiles=100,
    level=0,
    seed=42
)

# Preview tile locations
tiler.locate_tiles(slide, n_tiles=20)

# Extract tiles
tiler.extract(slide)
```

## Core Capabilities

### 1. Slide Management

Load, inspect, and work with whole slide images in various formats.

**Common operations:**
- Loading WSI files (SVS, TIFF, NDPI, etc.)
- Accessing slide metadata (dimensions, magnification, properties)
- Generating thumbnails for visualization
- Working with pyramidal image structures
- Extracting regions at specific coordinates

**Key classes:** `Slide`

**Example workflow:**

```python
from histolab.data import prostate_tissue

# Load sample data
prostate_svs, prostate_path = prostate_tissue()

# Initialize slide
slide = Slide(prostate_path, processed_path="output/")

# Inspect properties
print(f"Dimensions: {slide.dimensions}")
print(f"Levels: {slide.levels}")
print(f"Magnification: {slide.properties.get('openslide.objective-power')}")
```