---
name: lesion-detection
description: Classifies skin conditions including Melanoma and Basal Cell Carcinoma using TF.js MobileNetV3
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: clinical-pipeline
---

## What I do

I classify skin conditions using TensorFlow.js with MobileNetV3. I identify patterns consistent with various skin conditions including Melanoma, Basal Cell Carcinoma (BCC), and other dermatoses. I return confidence scores for each classification.

## When to use me

Use this when:

- Feature extraction is complete and you need lesion classification
- You need confidence scores for risk assessment
- You're identifying potential areas of concern in skin images

## Key Concepts

- **MobileNetV3**: TF.js model for skin condition classification
- **Confidence Score**: 0-1 probability for each condition
- **Lesion Types**: Melanoma, BCC, Actinic Keratosis, etc.
- **lesions_detected**: State flag after detection complete

## Source Files

- `services/vision.ts`: Lesion detection implementation
- `types.ts`: AnalysisResult interface with lesions array

## Code Patterns

- Load MobileNetV3 model via TF.js
- Run inference on feature vectors
- Return array of detected lesions with confidence and risk levels

## Operational Constraints

- MUST use tf.tidy() or explicit dispose() for all tensors
- Confidence scores required for all detections
- High-risk detections trigger elevated scrutiny in downstream
