# Safety & Interaction System

This document covers the safety mechanisms that prevent harmful supplement-medication interactions.

## Overview
The app has a **layered safety system** designed for ADHD users who take stimulant medications alongside supplements. 

## Components

### 1. `SafetyGuard` (Domain Service)
**Location**: `lib/domain/services/safety_guard.dart`

A comprehensive rule-based engine for detecting supplement-medication interactions.

**Key Classes:**
- `Medication`: Represents the user's ADHD medication (e.g., Adderall, Vyvanse).
    - `Medication.fromName(String name)`: Static helper to create medication typed data from simple strings (used in onboarding).
- `MedicationType`: Enum categorizing medications (`stimulant`, `nonStimulant`, `antidepressant`).
- `InteractionWarning`: A structured warning with severity, message, recommendation.
- `WarningSeverity`: Enum (`info`, `caution`, `warning`, `danger`).

**Key Methods:**
- `checkSupplement(Supplement)`: Returns a list of `InteractionWarning` for a given supplement.
- `getHighestSeverity(List<InteractionWarning>)`: Utility to find the most critical warning.

**Rule Examples:**
| Medication Type | Supplement | Severity | Reason |
|-----------------|------------|----------|--------|
| Stimulant | Vitamin C | Caution | Acidic supplements increase medication excretion. |
| SSRI | St. John's Wort | Danger | Risk of Serotonin Syndrome. |

**3. Supplement-Driven Interactions**
In addition to global rules, the system checks the `adhdMedInteractions` map on each `Supplement` entity for clinical-specific notes tailored to a user's exact prescription.

### 2. `ADHDInteractionGuard` (Domain Service)
**Location**: `lib/domain/services/adhd_interaction_guard.dart`

A **lightweight, quick-check** utility focused specifically on the `Stimulant + Acidic Supplement` interaction, which is the most common concern for ADHD users.

**Key Methods:**
- `checkInteraction(String med, String supplement)`: Returns a `Map` with `risk`, `warning`, `message`, `recommendation`.
- `isAmphetamineStimulant(String medication)`: Check if a med is affected.
- `isAcidicSupplement(String supplement)`: Check if a supplement is acidic.
- `getPotentialInteractionsFor(String supplement)`: Get list of meds that interact.

**Hardcoded Lists:**
- `stimulantMeds`: Adderall, Vyvanse, Mydayis, etc.
- `acidicSupplements`: Vitamin C, Multivitamins, Orange Extract, etc.

**Usage:**
Used by `SafetyGuardWidget` (UI) to provide instant feedback when a user selects a medication/supplement pair.

### 3. `SafetyViewModel` (Application Layer)
**Location**: `lib/application/view_models/safety_view_model.dart`

Manages state for safety-related screens (overrides, triage).
- Fetches known interactions for the user.
- Logs when a user overrides a safety warning (for audit trail).

## UI Screens
- `SafetyInteractionDetailScreen`: Shows a specific interaction (Warning + PubMed Source).
- `SafetyOverrideConfirmationScreen`: "I understand the risks" override flow.
- `LateDoseTriageScreen`: Decision tree for "Should I still take this dose?" scenarios.
- `SafetyGuardWidget`: Inline widget for the on-demand interaction checker.
- `MedicationSafetyAlert`: High-contrast alert card displayed on the Supplement Detail screen when an interaction is detected with the user's profile med.

## ADR Reference
See [ADR-001: Safety First Architecture](file:///Users/lycanbeats/Desktop/adhd_supplement_app/docs/adrs/001-safety-first-architecture.md).
