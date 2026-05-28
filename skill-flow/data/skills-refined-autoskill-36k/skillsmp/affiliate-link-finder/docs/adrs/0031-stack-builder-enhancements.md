# ADR 0031: Stack Builder Enhancements (Search & Customization)

## Status
Proposed

## Context
The initial `StackBuilderScreen` was a simple drag-and-drop interface with No discoverability (search) and limited customization. ADHD users need faster ways to find items (reducing cognitive load) and the ability to set specific dosages per routine slot to ensure accuracy and engagement.

## Decision
We implemented several enhancements to the Stack Builder:
1.  **Integrated Library Search**: Added a real-time search bar within the `StackBuilderScreen` that filters the `availableSupplements` list in the `StackBuilderViewModel`.
2.  **Per-Item Dosage Customization**: Modified the `StackItem` entity and `StackBuilderViewModel` to support `customDosage`. Users can tap an item in their stack to open a customization bottom sheet.
3.  **Visual Contextualization**: Added emojis to slot tabs (🌅, ☀️, 🌇, 🌙) to provide faster visual recognition of the current routine being edited.
4.  **Action labeling**: Renamed the primary action from "Save" to "Activate Routine" to create a stronger psychological link between the configuration and the usage of the routine.
5.  **Dopamine-Positive Feedback**: Updated the success feedback to use celebratory micro-copy ("Routine optimization active! 🎉") to reinforce the positive behavior of organizing health routines.

## Consequences
-   **Usability**: Significant reduction in time-to-completion for building routines due to search and better visual cues.
-   **Flexibility**: Users can now have different dosages for the same supplement across different times of day.
-   **State Management**: `StackBuilderViewModel` now manages more transient state (search query) and deeper object updates (per-item dosage), slightly increasing its internal complexity.
-   **Design Consistency**: The enhancements follow the "Rule of One" and other ADHD-friendly principles defined in our design system.
