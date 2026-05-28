# ADR 0026: Insights V2 Refactor & Gamification Polish

**Date:** 2026-01-21  
**Status:** Accepted  
**Deciders:** Development Team

## Context

The initial gamification strategy (ADR 0010) proposed a multi-screen "celebration" system (StreakRecovery, LevelUp, etc.). while effective for major milestones, users reported that for daily usage, a "Low-Dose" information display was preferred to reduce cognitive load. The original `InsightsScreen` specifically suffered from:
1.  **Anti-patterns**: Logic mixed inside UI widgets.
2.  **Visual Clutter**: Too many competing data points.
3.  **Lack of Dopamine**: Static text didn't provide immediate positive feedback.

## Decision

We have refactored the `InsightsScreen` into a streamlined **Insights V2** architecture:

1.  **MVVM Architecture**:
    - Introduced `InsightsViewModel` to handle all data fetching (Logs, Streaks) and logic (Consistency Scores).
    - The View (`InsightsScreen`) is now purely reactive, listening to the ViewModel via `Provider`.

2.  **"Low-Dose" UI Design**:
    - Removed complex charts in favor of a single "Hero Streak Card" and a broad "Consistency Bar".
    - Focuses on just two key metrics: **Current Streak** (Motivation) and **30-Day Consistency** (Discipline).

3.  **Subtle Gamification (The "Ember" System)**:
    - Instead of full-screen confetti for every interaction, implemented a `_StreakEmberAnimation`.
    - Uses a local `AnimationController` and `CustomPainter` to render floating "golden embers" behind the streak icon.
    - Provides a "premium" feel without overwhelming the user.

4.  **Doctor Export Integration**:
    - Added direct access to the `DoctorExportScreen` (ADR 0021) from the Insights dashboard, linking personal progress with professional care.

## Implementation Details

-   **State Management**: `ChangeNotifierProvider` with `get_it` injection.
-   **Animation**: `Computed` particle system in `_EmberPainter` to avoid heavy asset loading.
-   **Testing**: Fully covered by `insights_view_model_test.dart` (Unit) and verified via manual UI checks (Widget tests skipped due to environment complexity).

## Consequences

**Positive:**
-   **Reduced Cognitive Load**: Users see their status at a glance.
-   **Improved Maintainability**: Logic is isolated in the ViewModel, making it testable.
-   **Premium Aesthetic**: The ember animation adds delight without distraction.

**Negative:**
-   **Migration**: Older analytics widgets (e.g., specific symptom charts) were temporarily removed to focus on the "Core Two" metrics; these may need to be reintroduced later as "Advanced Insights".
