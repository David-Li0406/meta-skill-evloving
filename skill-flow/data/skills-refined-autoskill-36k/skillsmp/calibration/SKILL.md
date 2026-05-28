---
name: calibration
description: Applies decision thresholds for high-confidence inputs or enforces conservative safety margins for low-confidence cases
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: clinical-pipeline
---

## What I do

I apply calibration thresholds that determine how conservatively the pipeline operates. If detection confidence is >= 0.65, I apply standard thresholds (0.65). If confidence < 0.65, I enforce conservative safety margins (0.50) to reduce false positives.

## When to use me

Use this when:

- Skin tone detection is complete and you need to set decision thresholds
- You need to determine whether to use standard or safety calibration
- You're balancing sensitivity vs specificity based on detection confidence

## Key Concepts

- **Standard Calibration**: Threshold = 0.65 for high-confidence inputs
- **Safety Calibration**: Threshold = 0.50 for low-confidence inputs
- **is_low_confidence**: Boolean flag routing to appropriate calibration
- **calibration_complete**: State flag indicating calibration is done

## Source Files

- `services/goap.ts`: Calibration action definitions
- `types.ts`: WorldState interface

## Code Patterns

- Standard-Calibration-Agent: `{ is_low_confidence: false }` preconditions
- Safety-Calibration-Agent: `{ is_low_confidence: true }` preconditions
- Both set `calibration_complete: true` effect

## Operational Constraints

- Safety calibration is MANDATORY for low-confidence cases
- Threshold decisions affect all downstream fairness calculations
- Always log which calibration mode was applied
