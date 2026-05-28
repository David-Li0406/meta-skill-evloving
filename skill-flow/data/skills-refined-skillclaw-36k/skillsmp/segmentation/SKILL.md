---
name: segmentation
description: Isolates skin regions from background clutter using calibrated thresholds for downstream analysis
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: clinical-pipeline
---

## What I do

I isolate skin regions from the background to focus analysis on the relevant areas. I use calibrated thresholds based on skin tone classification to create accurate skin masks.

## When to use me

Use this when:

- Image preprocessing is complete and you need to segment skin regions
- You need to remove background noise for feature extraction
- You need a binary mask of skin vs non-skin pixels

## Key Concepts

- **Skin Mask**: Binary image where skin pixels are 1, background is 0
- **Calibrated Thresholds**: Thresholds adjusted based on Fitzpatrick type
- **segmentation_complete**: State flag after segmentation complete
- **Background Removal**: Eliminate non-skin pixels for focused analysis

## Source Files

- `services/vision.ts`: Segmentation implementation
- `types.ts`: WorldState interface

## Code Patterns

- Apply calibrated color thresholds based on fitzpatrick_type
- Generate binary mask of skin regions
- Validate segmentation quality before marking complete

## Operational Constraints

- Thresholds MUST be calibrated to Fitzpatrick type
- Poor segmentation affects all downstream accuracy
- Consider fallback to manual region selection if auto-segmentation fails
