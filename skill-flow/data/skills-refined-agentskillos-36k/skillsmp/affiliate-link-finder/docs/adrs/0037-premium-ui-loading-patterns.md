# ADR 0037: Premium UI Loading Patterns (Shimmers)

## Status
Accepted

## Context
Standard Flutter loading indicators (like `CircularProgressIndicator`) create high visual contrast and perceived "stop-and-go" motion, which can be distracting for ADHD users. Furthermore, generic loaders do not provide context about the layout being loaded, leading to potential "layout shift" once data arrives. To align with our premium design standards and ADHD-friendly UX, a more cohesive loading strategy was needed.

## Decision
We implemented a standardized "Shimmer" loading pattern using the `SkeletonLoader` widget:
1.  **Layout-Matching Skeletons**: Loading states are now designed to mirror the final UI structure (e.g., circular shimmers for avatars, rectangular bars for titles).
2.  **Tiered Loading**: Screens like `LibraryScreen` and `DailyStackScreen` now use multi-sized skeletons to provide an "instant-load" feeling.
3.  **Low-Contrast Motion**: Used wide `LinearGradient` animations with subtle color offsets (e.g., 5% to 10% opacity) to ensure the motion is helpful but not overstimulating for neurodivergent users.
4.  **Reusable Component**: Refactored the shimmer logic into a standalone `SkeletonLoader` widget in the presentation layer to ensure design consistency across all domains.

## Consequences
- **Perceived Performance**: Users experience significantly shorter "wait times" because the screen structure is visible immediately.
- **Visual Stability**: Reduced layout shifts (jank) once the actual data is rendered.
- **Design Aesthetic**: Elevated the app's professional feel, moving beyond basic "MVP" aesthetics.
