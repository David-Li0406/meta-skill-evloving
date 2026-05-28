---
name: maintaining-ui-standards
description: Maintain consistent UI/UX, enforce design system usage, and ensure accessibility/responsiveness. Use when designing screens, styling components, or reviewing UI implementation.
---

# UI/UX Standards

## When to use this skill
- When implementing new UI screens or components.
- When applying styles or themes.
- When reviewing UI/UX design choices.
- When debugging layout or responsiveness issues.

## Design System
- **Single Source of Truth**: Always use the defined theme variables for colors, typography, and spacing. Do not hardcode values.
- **Color Palette**:
    - Use `Primary`, `Secondary`, and `Accent` colors from the theme.
    - Use semantic names like `Error`, `Success`, `Warning`, `Info`.
- **Typography**:
    - Use defined font families and weights.
    - Follow the type scale (e.g., `Heading1`, `Body`, `Caption`).
- **Spacing Scale**:
    - Stick to the 8px grid system: `4px` (0.5x), `8px` (1x), `16px` (2x), `24px` (3x), `32px` (4x), `48px` (6x).
- **Border Radius**: Use consistent radii for related components (e.g., 4px for buttons, 8px for cards).

## Components
- **Consistency**: Use the project's reusable components from `/components` first. Avoid creating custom one-offs.
- **Platform Conventions**: Respect platform differences where it matters (e.g., navigation styles), but maintain brand unity.
- **Accessibility (A11y)**:
    - Ensure minimum touch target size (44x44 points).
    - Provide `accessibilityLabel` and `accessibilityHint`.
    - Support dynamic type (scaling fonts).
    - ensure sufficient color contrast (WCAG AA).
- **Dark Mode**: All components must support dark mode. Use semantic colors that adapt automatically.

## Responsive Design
- **Mobile First**: Design for the smallest screen first, then scale up.
- **Safe Areas**: Always respect notches, status bars, and home indicators (use `SafeAreaView`).
- **Layouts**: Use Flexbox for layout. Use percentages or flex ratios, rarely fixed pixels for width/height.
- **Testing**: Verify UI on small phones, large phones, and tablets if supported.

## User Experience
- **Feedback**:
    - Show skeleton loaders or activity indicators during data fetching.
    - Display clear, helpful error messages (not "Something went wrong").
    - Provide toast notifications for success states.
- **Interaction**:
    - Add active states to buttons (opacity change or background darkening).
    - Use haptic feedback for significant actions (success, error, impact).
- **Navigation**: Ensure navigation flow is intuitive and follows standard patterns (Stack, Tab, Drawer).
