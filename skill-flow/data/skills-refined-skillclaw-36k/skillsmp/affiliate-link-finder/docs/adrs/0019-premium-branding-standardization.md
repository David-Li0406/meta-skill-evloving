# ADR 0019: Premium Branding Standardization

**Date:** 2026-01-20  
**Status:** Accepted  
**Deciders:** Development Team

## Context

The application previously used a mix of colors (Blue, Green, Purple) for different features, leading to an inconsistent "vibe" that didn't feel premium or cohesive. The "Developer Handoff" wireframes introduced a a "Gold Standard" aesthetic that needed systematic enforcement.

## Decision

Standardize the entire application on the **"Deep Focus Gold"** branding system.

Core requirements:
1. **Typography**: Mandatory use of `GoogleFonts.lexend` for all UI text.
2. **Colors**: Primary brand color is `AppColors.primaryGold` (#D4AF37).
3. **Themes**: Light/Dark themes use premium cream/dark card backgrounds instead of standard material defaults.
4. **Badging**: Use of "Gold Standard" badges for verified content and high-value features.

## Rationale
- **Brand Identity**: Establishes a premium, high-trust identity suitable for health and wellness supplements.
- **ADHD Friendliness**: Lexend typography is specifically designed for improved readability.
- **Visual Hierarchy**: Gold on dark/light backgrounds provides high contrast for call-to-action elements.
- **Market Positioning**: Distinguishes the app as a "Pro" tool compared to generic hobbyist trackers.

## Consequences

**Positive:**
- Cohesive visual style that feels like a single, finished product.
- Improved readability and accessibility via standardized fonts and weights.
- Simple theme maintenance by referencing a centralized `AppColors` and `AppTheme` system.

**Negative:**
- Potential over-reliance on a single accent color might reduce semantic clarity (e.g., using gold for both "Success" and "Discovery").
- Performance overhead from loading multiple Google Font weights (mitigated by font bundling).

## Alternatives Considered

| Option | Rejected Because |
|--------|------------------|
| Functional Color Coding | Hard for users to remember what orange vs purple meant; felt "busy" and less premium. |
| System Font Default | Lacks the brand distinctiveness and ADHD-specific benefits of Lexend. |
| Mixed Theme (Gold & Blue) | Blue was retained only for "Utility" screens (e.g., Help) to separate support from the core habit-forming experience. |
