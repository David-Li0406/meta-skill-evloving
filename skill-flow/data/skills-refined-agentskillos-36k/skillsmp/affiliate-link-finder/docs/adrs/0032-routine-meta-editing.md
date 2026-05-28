# ADR 0032: Routine Meta-Editing (Personalization)

## Status
Accepted

## Context
The initial routine management system (Stack Builder) used hardcoded slot names (Morning, Afternoon, etc.) for display purposes. ADHD users often have unique routine triggers (e.g., "Post-Workout", "Deep Work Preamble") that don't always map to a simple time-of-day category. To increase user agency and reduce friction, we needed a way to allow users to rename these routines while preserving their underlying slot categorization for scheduling purposes.

## Decision
We implemented a routine-level "Meta-Editing" capability:
1.  **Direct Header Editing**: Added an edit affordance next to the routine name in the `StackBuilderScreen`.
2.  **Specialized Bottom Sheet**: Introduced a focused metadata editor that allows changing the stack's public name and its associated time metadata.
3.  **ViewModel-Driven Updates**: The `StackBuilderViewModel` was extended with `updateStackMeta` to manage these transient name changes before persistence.
4.  **Schema Support**: Utilized the existing `name` field in the `SupplementStack` entity to store these custom labels, which are now correctly propagated to the Dashboard and History views.

## Consequences
- **User Agency**: Users can now tailor the app's vocabulary to their personal life triggers.
- **Cognitive Ease**: Faster recognition of routines in lists when using personally meaningful names.
- **Persistence Quality**: Stack metadata is now as customizable as the item list within it.
