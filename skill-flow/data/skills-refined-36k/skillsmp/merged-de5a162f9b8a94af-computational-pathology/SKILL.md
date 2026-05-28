---
name: computational-pathology
description: Use this skill for advanced analysis of whole-slide images (WSI) and multiparametric imaging data in computational pathology workflows, including tissue segmentation, graph construction, and machine learning model training.
---

# Computational Pathology

## Overview

This skill combines capabilities from histolab and pathml to provide a comprehensive toolkit for processing and analyzing whole slide images (WSI) in digital pathology. It supports a variety of tasks including tissue detection, tile extraction, image preprocessing, and machine learning model training across multiple slide formats.

## Core Capabilities

### 1. Image Loading & Formats

Load whole-slide images from over 160 proprietary formats including Aperio SVS, NDPI, DICOM, and OME-TIFF. The toolkit provides unified interfaces for accessing image pyramids, metadata, and regions of interest.

### 2. Preprocessing Pipelines

Build modular preprocessing pipelines for image manipulation, quality control, stain normalization, tissue detection, and mask operations. Key transforms include:
- **StainNormalizationHE**: Macenko/Vahadane stain normalization
- **TissueDetectionHE**: Tissue segmentation
- **NucleusDetectionHE**: Nucleus segmentation

### 3. Tissue Detection and Masks

Automatically identify tissue regions and filter background/artifacts. Common operations include:
- Creating binary tissue masks
- Detecting largest tissue regions
- Custom tissue segmentation

### 4. Tile Extraction

Extract smaller regions from large WSI using different strategies:
- **RandomTiler**: Extracts a fixed number of randomly positioned tiles.
- **GridTiler**: Systematically extracts tiles in a grid pattern.
- **ScoreTiler**: Extracts top-ranked tiles based on scoring functions.

### 5. Graph Construction

Construct spatial graphs representing cellular and tissue-level relationships. Extract features from segmented objects to create graph-based representations suitable for spatial analysis.

### 6. Machine Learning

Train and deploy deep learning models for nucleus detection, segmentation, and classification. The toolkit integrates with PyTorch and supports models like HoVer-Net and HACTNet.

### 7. Multiparametric Imaging

Analyze spatial proteomics and gene expression data from multiplex imaging platforms like CODEX and Vectra. This includes specialized slide classes and transforms for processing multiparametric data.

### 8. Data Management

Efficiently store and manage large pathology datasets using HDF5 format. This includes handling tiles, masks, metadata, and extracted features in unified storage structures optimized for machine learning workflows.

## Quick Start

### Installation

```bash
# Install the toolkit
uv pip install pathml
```

### Basic Workflow Example

```python
from pathml.core import SlideData
from pathml.preprocessing import Pipeline, StainNormalizationHE, TissueDetectionHE

# Load a whole-slide image
wsi = SlideData.from_slide("path/to/slide.svs")

# Create preprocessing pipeline
pipeline = Pipeline([
    TissueDetectionHE(),
    StainNormalizationHE(target='normalize', stain_estimation_method='macenko')
])

# Run pipeline
pipeline.run(wsi)

# Access processed tiles
for tile in wsi.tiles:
    processed_image = tile.image
    tissue_mask = tile.masks['tissue']
```

## Common Workflows

### H&E Image Analysis
1. Load WSI with appropriate slide class.
2. Apply tissue detection and stain normalization.
3. Perform nucleus detection or train segmentation models.
4. Extract features and build spatial graphs.
5. Conduct downstream analysis.

### Multiparametric Imaging (CODEX)
1. Load CODEX slide with `CODEXSlide`.
2. Segment cells using Mesmer model.
3. Quantify marker expression.
4. Export to AnnData for single-cell analysis.

### Training ML Models
1. Prepare dataset with public pathology data.
2. Create PyTorch DataLoader with PathML datasets.
3. Train models like HoVer-Net or custom models.
4. Evaluate on held-out test sets.

## Best Practices

- Always inspect slide properties before processing.
- Use appropriate masks for tissue detection.
- Preview tile locations before extraction.
- Monitor tile quality and adjust extraction parameters as needed.

## Troubleshooting

- If no tiles are extracted, verify the presence of tissue and adjust thresholds.
- For slow extraction, consider reducing the number of tiles or extracting at a lower pyramid level.
- If tiles contain artifacts, implement custom annotation-exclusion masks.

## Resources

This skill includes comprehensive reference documentation organized by capability area. Each reference file contains detailed API information, workflow examples, best practices, and troubleshooting guidance for specific functionalities.

### references/

- `image_loading.md` - Whole-slide image formats and loading strategies.
- `preprocessing.md` - Transform catalog and preprocessing workflows.
- `graphs.md` - Graph construction methods and spatial analysis.
- `machine_learning.md` - Model architectures and training workflows.
- `multiparametric.md` - CODEX and multiplex IF analysis.
- `data_management.md` - HDF5 storage and dataset organization.