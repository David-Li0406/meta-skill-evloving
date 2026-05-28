---
name: skin-tone-detection
description: Classifies patient skin tone using Fitzpatrick/Monk scale with Gemini 3 Flash and outputs confidence score
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: clinical-pipeline
---

## What I do

I classify patient skin tone using the Fitzpatrick (I-VI) and Monk (1-10) scales. I use Gemini 3 Flash for classification and return a confidence score that determines downstream calibration decisions.

## When to use me

Use this when:

- An image has been verified and needs skin tone classification
- You need to determine the appropriate fairness calibration threshold
- Confidence score is needed for safety routing decisions

## Key Concepts

- **Fitzpatrick Scale**: I-VI classification (very fair to darkest)
- **Monk Scale**: 1-10 numerical skin tone representation
- **Confidence Score**: 0-1 float determining if standard or safety calibration applies
- **Threshold**: 0.65 - below this triggers safety calibration

## Source Files

- `services/vision.ts`: Vision model integration
- `types.ts`: FitzpatrickType enum

## Code Patterns

- Use Gemini 3 Flash API for classification
- Return confidence with classification result
- Route to Safety-Calibration-Agent if confidence < 0.65

## Operational Constraints

- All inference must return confidence score (0-1)
- If low confidence, MUST route through Safety-Calibration-Agent
- Store fitzpatrick_type in WorldState for downstream agents
