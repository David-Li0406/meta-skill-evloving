# 4. Safety Guard System Implementation

Date: 2026-01-18

## Status

Accepted

## Context

Supplement interactions with prescription ADHD medications (specifically stimulants) pose a significant health/efficacy risk. For example, Vitamin C can drastically reduce the effectiveness of amphetamines. Users need a reliable way to check these interactions.

## Decision

We will implement a **SafetyGuard** logic engine and UI component.

### Logic (`ADHDInteractionGuard`)
- **Mechanism**: Cross-reference user-selected medications against a database of interaction rules.
- **Critical Rule**: Explicitly flag **High-Dose Vitamin C (>500mg) + Amphetamine Stimulants**.
- **Explanation**: Warnings must explain *why* the interaction occurs (e.g., "Increased GI/urinary acidity flushes medication faster").

### UI (`SafetyGuardWidget`)
- **Input**: specific dropdowns for "Your Medication" (e.g. Adderall, Vyvanse) and "Supplement".
- **Feedback**: Immediate visual feedback.
    - **Safe**: Green Checkmark (`#00E676`).
    - **Interaction**: Amber Warning (`#FFAB40`) with explicit "Timing Tip" (space by 2 hours).
- **Legitimacy**: Include direct links to medical sources (e.g., PubMed) for verification.
- **Disclaimer**: Mandatory standard medical disclaimer on all results.

## Consequences

### Positive
- **User Safety**: Proactively prevents common efficacy issues with medication.
- **Trust**: Providing medical reasoning and source links builds authority and trust.

### Negative
- **Liability Risk**: Providing health information carries risk. We mitigate this with strict disclaimers stating "this is not medical advice."
- **Maintenance**: Interaction rules must be kept up-to-date with medical research.
