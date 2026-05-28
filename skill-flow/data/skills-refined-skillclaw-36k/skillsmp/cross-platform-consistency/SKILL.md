---
name: cross_platform_consistency
description: Ensures Android, iOS, and Windows versions match the Web version's UI/UX.
---

# Cross-Platform UI Consistency

This skill ensures that the UI/UX of the Android, iOS, and Windows applications matches the Web version.

## Reference Source
- **Primary Reference**: `web/` directory.
- **Goal**: All other platforms must visually mimic the web version.

## Instructions
1. **Analyze Web UI**: Before making UI changes to Android, iOS, or Windows (Desktop) clients, inspect the corresponding components/pages in the `web/` directory.
2. **Review Styles**: Check `web/src` (or relevant style directories) to understand the color palette, typography, and spacing.
3. **Replicate Behavior**: Ensure animations, hover effects, and layout flow match the web version as closely as the native platform allows.
4. **Validation**: When creating or updating a view, compare it against the web version.

## Workflow
When asked to implement a feature on mobile or desktop:
1. Locate the feature in the `web` codebase.
2. Note the design tokens (colors, sizes).
3. Implement the feature in `composeApp` (for Android/Desktop) or `iosApp` (for iOS) using equivalent styles.
