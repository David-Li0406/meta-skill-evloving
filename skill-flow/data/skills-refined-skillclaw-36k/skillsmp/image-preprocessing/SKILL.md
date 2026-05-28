---
name: image-preprocessing
description: Normalizes image histograms to preserve melanin features using Canvas API before analysis
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: clinical-pipeline
---

## What I do

I preprocess images to normalize histograms while preserving melanin features critical for skin analysis. I use the Canvas API for efficient pixel manipulation and contrast enhancement.

## When to use me

Use this when:

- Calibration is complete and you need to prepare the image
- You need to enhance contrast for better lesion detection
- Histogram normalization is required before segmentation

## Key Concepts

- **Histogram Equalization**: Spreads out pixel intensity values
- **Melanin Preservation**: Enhances features without losing skin pigmentation info
- **Canvas API**: Browser canvas for image manipulation
- **image_preprocessed**: State flag after preprocessing complete

## Source Files

- `services/vision.ts`: Preprocessing implementation
- `components/AnalysisIntake.tsx`: Image upload component

## Code Patterns

- Use Canvas API for pixel-level operations
- Apply histogram equalization that preserves melanin contrast
- Ensure output is suitable for segmentation algorithms

## Operational Constraints

- Must preserve features critical for dermatological analysis
- Use tf.tidy() or explicit dispose() for any tensor operations
- Work in Canvas pixel space, not tensor space
