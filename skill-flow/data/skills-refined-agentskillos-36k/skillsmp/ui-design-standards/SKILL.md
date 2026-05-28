---
name: ui-design-standards
description: UI design quality standards and principles for frontend implementation and code review. Use when (1) implementing UI from design specs or mockups, (2) reviewing frontend/UI code, (3) creating new UI components, (4) building user interfaces for web or mobile apps. Complements frontend-design skills with quality enforcement.
---

# UI Design Standards

Quality standards for implementing and reviewing user interfaces. Apply these principles regardless of framework (React, Vue, SwiftUI, Flutter, etc.).

## Core Principles

### 1. Visual Fidelity

Match design specifications exactly:

- **Layout**: Precise positioning, alignment, and structure
- **Spacing**: Exact margins, padding, and gaps
- **Typography**: Font family, size, weight, line-height, letter-spacing
- **Colors**: Exact color values (no approximations)
- **Component shapes**: Border radius, shadows, borders
- **Visual hierarchy**: Element prominence matches design intent

**Rule**: Do not introduce new UI elements or redesign. Follow the design precisely.

### 2. Component Architecture

Apply OOP principles to UI development:

- **Single Responsibility**: Each component does one thing well
- **Open/Closed**: Extend via props/composition, not modification
- **Encapsulation**: Internal state hidden, clean public interface
- **Composition over Inheritance**: Compose small components

```
// Good: Reusable, props-driven, single responsibility
<Button variant="primary" size="lg">Submit</Button>

// Bad: One-off, hardcoded, mixed concerns
<button style="background: #3b82f6; padding: 12px 24px;">Submit</button>
```

- Break UI into logical, single-responsibility components
- Components should be composable and testable
- Avoid deep nesting (max 3-4 levels)

### 3. Theme System

Use a single global theme file for all design tokens:

```
theme/
├── colors.ts      # Color palette
├── typography.ts  # Font styles
├── spacing.ts     # Spacing scale
├── shadows.ts     # Shadow definitions
└── index.ts       # Unified export
```

**Required tokens**:
- Colors (primary, secondary, neutral, semantic)
- Typography (font families, sizes, weights)
- Spacing (consistent scale: 4, 8, 12, 16, 24, 32...)
- Border radius
- Shadows/elevation
- Breakpoints (responsive)

**Rule**: No hardcoded styles inside components. All values from theme.

### 4. Functional Completeness

UI must be fully functional:

- **Navigation**: Working routes and transitions
- **State handling**: Proper state management for all interactions
- **Interactions**: Hover, focus, active, disabled states
- **Loading states**: Skeleton, spinner, or placeholder
- **Error states**: Clear error feedback
- **Empty states**: Meaningful empty state UI

### 5. Asset Generation

When assets are missing (icons, images, avatars, illustrations):

- Generate in a style that matches the design language
- Maintain consistent visual weight and style
- Use appropriate formats (SVG for icons, optimized images)
- Provide fallbacks where needed

## Implementation Checklist

Before marking UI implementation complete:

- [ ] Layout matches design exactly
- [ ] All spacing values from theme
- [ ] Typography matches design specs
- [ ] Colors are exact (use color picker to verify)
- [ ] All interactive states implemented
- [ ] Responsive behavior works correctly
- [ ] No hardcoded style values
- [ ] Components are reusable
- [ ] Loading/error/empty states handled

## Code Review Checklist

When reviewing UI code:

| Area | Check |
|------|-------|
| Visual | Does it match the design? |
| Theme | Are all values from theme system? |
| Components | Reusable and properly abstracted? |
| States | All interaction states handled? |
| Accessibility | Proper semantics and ARIA? |
| Performance | No unnecessary re-renders? |
| Hardcoding | Any magic numbers or colors? |

### Common Issues to Flag

```
// Flag: Hardcoded color
color: '#3b82f6'  // Should use theme.colors.primary

// Flag: Magic number
padding: 13px  // Should use spacing scale

// Flag: Inline styles for reusable patterns
style={{ display: 'flex', gap: 8 }}  // Should be component/class

// Flag: Missing states
<Button>Submit</Button>  // Where is disabled/loading state?
```

## Quality Levels

| Level | Description |
|-------|-------------|
| A | Pixel-perfect, fully themed, all states, accessible |
| B | Visually accurate, mostly themed, core states work |
| C | Functional but visual inconsistencies, some hardcoding |
| D | Major visual deviations, significant hardcoding |

Target: Level A for production, Level B minimum for review approval.
