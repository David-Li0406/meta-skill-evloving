# 3. ADHD-Friendly UI Design Strategy

Date: 2026-01-18

## Status

Accepted

## Context

The target audience for this application consists of individuals with ADHD. Users with ADHD often struggle with visual clutter, sensory overload, and decision paralysis. Standard UI patterns may be too distracting or overwhelming.

## Decision

We will implement a specialized **ADHD-Friendly Design System** adhering to the following principles:

1.  **High Contrast Dark Mode**: Use a dark background (`#121212`) with high-contrast accent colors to reduce eye strain and visual noise.
2.  **Focus Level Badges**: Use a clear, color-coded 1-5 scale for supplements to allow for quick scanning and decision making (Red to Green spectrum).
3.  **Card-Based Layout**: Group information into distinct, bordered cards to separate concepts visually.
4.  **Bite-Sized Information**: Use "Chips" for benefits and short, bulleted lists instead of long paragraphs.
5.  **Clear Calls to Action**: Use large, distinct "Buy Now" buttons that match the color theme of the item's focus level.

## Consequences

### Positive
- **Accessibility**: Improves usability for the core demographic by reducing cognitive load.
- **Engagement**: A clean, visually appealling interface encourages extended use.
- **Clarity**: Critical information (warnings, benefits) matches visual hierarchy patterns.

### Negative
- **Design Constraints**: Strict adherence to high-contrast dark mode limits generic theming options.
