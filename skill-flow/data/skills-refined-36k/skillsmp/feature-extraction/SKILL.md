---
name: feature-extraction
description: Extracts vector embeddings for fairness analysis using MobileNetV3 with FairDisCo disentanglement
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: clinical-pipeline
---

## What I do

I extract feature embeddings from segmented skin regions using MobileNetV3 with FairDisCo (Fair Disentangled Continual) disentanglement. This ensures features are suitable for downstream fairness analysis across demographic groups.

## When to use me

Use this when:

- Segmentation is complete and you need feature vectors
- You need embeddings for lesion classification
- Fairness analysis requires disentangled feature representations

## Key Concepts

- **MobileNetV3**: Efficient CNN for feature extraction
- **FairDisCo**: Disentanglement method for fair representations
- **Feature Vector**: Embedding suitable for classification and similarity
- **features_extracted**: State flag after extraction complete

## Source Files

- `services/vision.ts`: Feature extraction implementation
- `types.ts`: FeatureMetadata interface

## Code Patterns

- Run MobileNetV2/V3 on segmented skin regions
- Apply FairDisCo disentanglement for fair representations
- Return feature vector and bias metrics

## Operational Constraints

- Must use tf.tidy() or explicit dispose() for all tensors
- FairDisCo ensures demographic bias is minimized
- Feature quality directly impacts lesion detection accuracy
