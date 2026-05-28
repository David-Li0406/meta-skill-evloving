---
name: pathml
description: Use this skill for advanced analysis of whole-slide images (WSI) in computational pathology, including tasks like multiplexed immunofluorescence, nucleus segmentation, and machine learning model training.
---

# Skill body

## Overview

PathML is a comprehensive Python toolkit designed for computational pathology workflows. It facilitates machine learning and image analysis for whole-slide pathology images, providing modular tools for loading diverse slide formats, preprocessing images, constructing spatial graphs, and analyzing multiparametric imaging data.

## When to Use This Skill

Apply this skill for:
- Loading and processing whole-slide images (WSI) in various proprietary formats (e.g., Aperio SVS, NDPI, DICOM, OME-TIFF).
- Preprocessing H&E stained tissue images with stain normalization.
- Nucleus detection, segmentation, and classification workflows.
- Building cell and tissue graphs for spatial analysis.
- Training or deploying machine learning models (e.g., HoVer-Net, HACTNet) on pathology data.
- Analyzing multiparametric imaging (e.g., CODEX, Vectra) for spatial proteomics.
- Quantifying marker expression from multiplex immunofluorescence.
- Managing large-scale pathology datasets with HDF5 storage.
- Performing tile-based analysis and stitching operations.

## Core Capabilities

PathML provides several major capability areas:

### 1. Image Loading & Formats

Load whole-slide images from 160+ proprietary formats. PathML automatically handles vendor-specific formats and provides unified interfaces for accessing image pyramids, metadata, and regions of interest.

### 2. Preprocessing Pipelines

Build modular preprocessing pipelines by composing transforms for image manipulation, quality control, stain normalization, tissue detection, and mask operations. PathML's Pipeline architecture enables reproducible, scalable preprocessing across large datasets.

### Example Workflow

```python
from pathml import Slide, Pipeline

# Load a slide
slide = Slide("path/to/slide.svs")

# Create a preprocessing pipeline
pipeline = Pipeline([
    'StainNormalizationHE',
    'TissueDetection'
])

# Process the slide
processed_slide = pipeline.run(slide)
```