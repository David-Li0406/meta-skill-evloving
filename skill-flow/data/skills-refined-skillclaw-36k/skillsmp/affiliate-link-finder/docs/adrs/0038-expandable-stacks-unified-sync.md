# ADR 0038: Expandable Stacks & Standardized Dashboard Sync

## Status
Proposed

## Context
As users add more supplements to their routines, the Dashboard (Home) and Daily Stack (Today) screens can become cluttered. Users with ADHD benefit from a "Focus mode" where non-immediate tasks are hidden. Additionally, there was a discrepancy between how the Library saved stacks (dynamic IDs) and how the Dashboard retrieved them (fixed slots like 'morning').

## Decision
1. **Expandable Sections**: Implement a unified expand/collapse state in `DailyStackViewModel` to manage the visibility of supplement groups.
2. **Unified State**: Shared the expansion state across all screens (Dashboard and Today) for a consistent user experience.
3. **Standardized ID Mapping**: The sync logic now maps dynamic routine titles (e.g., "Morning Stack") to fixed slot IDs ('morning', 'afternoon', etc.) used for high-reliability dashboard rendering.
4. **Global Toggle**: Provide "Expand All" and "Collapse All" functionality to quickly manage screen real estate.

## Consequences
- **Positive**: Reduced cognitive load; cleaner UI; improved cross-screen consistency.
- **Negative**: Adds a small amount of complexity to the ViewModel state.
- **Neutral**: Requires `DailyStackViewModel` to be initialized with both dynamic and static IDs for the "Collapse All" feature to work across divergent UI designs.

## Compliance
- **ADHD UI Optimizer**: Enhances "Clutter Reduction" and "Focus Management" principles.
- **Architecture**: Maintains SOLID by keeping state logic in the ViewModel and presentation in the View.
