---
name: risk-assessment
description: Synthesizes lesion data and historical cases into a comprehensive risk profile using WebLLM SmolLM2
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: clinical-pipeline
---

## What I do

I synthesize lesion detection results with historical similar cases to generate a comprehensive risk profile. I use WebLLM (SmolLM2) for offline inference to calculate risk scores with equalized odds correction.

## When to use me

Use this when:

- Similar case search is complete and you need risk scoring
- You need a numerical risk assessment for clinical decision support
- You're combining multiple signals into an overall risk profile

## Key Concepts

- **WebLLM**: Browser-based LLM for offline inference
- **SmolLM2**: Efficient LLM model for risk synthesis
- **Equalized Odds Correction**: Fairness-aware risk calibration
- **Risk Score**: Numerical assessment (Low/Medium/High)
- **risk_assessed**: State flag after assessment complete

## Source Files

- `services/vision.ts`: Risk assessment implementation
- `types.ts`: AnalysisResult interface

## Code Patterns

- Synthesize lesion data with historical patterns
- Apply equalized odds correction for demographic fairness
- Return risk level (Low/Medium/High) with supporting evidence

## Operational Constraints

- Must provide equalized odds across demographics
- Heavy model - must expose unload() method
- Confidence scores required for all risk assessments
