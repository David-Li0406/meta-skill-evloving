# Dosage Intelligence System

This document covers the dosage logic and calculation tools that help users find their optimal supplement intake levels.

## Overview
The Dosage Intelligence system provides personalized recommendations based on user-provided metrics (like body weight) and clinical data stored in the `Supplement` entity.

## Components

### 1. `Supplement` (Domain Entity)
**Location**: `lib/domain/entities/supplement.dart`

The base entity now contains several fields for dosage logic:
- `dosageByWeight`: A map of weight ranges (kg) to dosage strings (e.g., `"40-60": "500-1000mg"`).
- `dosageFrequency`: Instructions on how often to take the dose.
- `dosageWarnings`: Specific clinical warnings related to dosage (e.g., bleeding risk for high-dose Omega-3).
- `bestTimeToTake`: Timing suggestions (Morning, Evening, With Food).

### 2. `DosageCalculatorCard` (UI Widget)
**Location**: `lib/presentation/widgets/dosage_calculator_card.dart`

An interactive calculator displayed on the `SupplementDetail` screen.

**Features:**
- **Dynamic Calculation**: Uses a `Slider` to take user weight input and cross-references it with `dosageByWeight`.
- **Real-time Feedback**: Updates the recommended dosage string immediately as the slider moves.
- **Safety Context**: Displays the `dosageFrequency` and `dosageWarnings` alongside the calculated dose.
- **Fall-through**: If the user's weight is outside the clinically typical range, it displays a standard disclaimer.

## Logic Flow

1. **Initialization**: The `SupplementDetail` screen checks if `supplement.dosageByWeight` is present.
2. **Personalization**: If data exists, the `DosageCalculatorCard` is rendered instead of a static dosage string.
3. **Calculation**: 
    - The widget parses the keys of `dosageByWeight` (ranges like `X-Y`).
    - It matches the slider value against these ranges.
    - It retrieves the corresponding value (e.g., `1000mg`).
4. **Safety**: All warnings associated with the supplement's dosage are rendered below the result.

## UI Styling (Gold Standard)
- **Contrast**: High-clarity typography using `Lexend`.
- **Interactivity**: Accessible slider with immediate visual state changes.
- **Branding**: Uses `primaryGold` for the current recommendation to denote clinical authority.

## Verification & Tests
- Unit tests for range parsing and value retrieval in `DosageCalculatorCard` logic.
- UI validation for overflow and slider responsiveness.
