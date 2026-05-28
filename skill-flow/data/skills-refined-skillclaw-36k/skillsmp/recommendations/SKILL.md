---
name: recommendations
description: Generates actionable clinical advice (max 25 words) calibrated for patient skin tone using WebLLM or Gemini
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: clinical-pipeline
---

## What I do

I generate concise, actionable clinical recommendations based on the diagnosis, risk assessment, and web verification. I calibrate advice for the patient's specific skin tone and ensure recommendations are evidence-based.

## When to use me

Use this when:

- Web verification is complete and you need clinical recommendations
- You need patient-appropriate, skin-tone-calibrated advice
- You're generating the final output for clinical decision support

## Key Concepts

- **25 Word Limit**: Concise recommendations for easy comprehension
- **Skin-Tone Calibration**: Advice appropriate for Fitzpatrick type
- **Evidence-Based**: Grounded in verified web sources
- **recommendations_generated**: State flag after generation complete

## Source Files

- `services/vision.ts`: Recommendation generation
- `types.ts`: AnalysisResult with recommendations array

## Code Patterns

- Synthesize diagnosis, risk, and web evidence
- Calibrate language for patient demographics
- Generate concise, actionable advice

## Operational Constraints

- Maximum 25 words per recommendation
- Must be calibrated to Fitzpatrick type
- Must clearly differentiate AI reasoning from web-grounded advice
