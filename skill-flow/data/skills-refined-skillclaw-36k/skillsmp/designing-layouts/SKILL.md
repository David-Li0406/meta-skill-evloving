---
name: designing-layouts
description: Guides design decisions for a low-code CSS layout generator. Use this skill when the user asks for help with UI/UX choices, component architecture, layout presets, canvas interactions, or design system decisions. Generates creative, polished code that avoids generic AI aesthetics.
---

# Design Engineer

Bridges design thinking with technical implementation for the layout application.
This skill focuses on design principles and decision-making criteria.

## Scope

Use for: Dashboards, admin panels, SaaS apps, tools, settings pages, data interfaces.
Not for: Landing pages, marketing sites, campaigns. For those, use the official Claude skill: [frontend-design](https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design).

## Responsibilities

1. **Design System Decisions**: Choose appropriate patterns, spacing, colors, and component structures
2. **Component Architecture**: Design reusable, accessible, and maintainable components
3. **Layout Expertise**: CSS Grid, Flexbox, and responsive design patterns
4. **User Experience**: Consider how users interact with the canvas editor
5. **Preset Creation**: Design reusable layout templates that solve real-world problems

---

# Styling Approach

**Prefer Tailwind CSS** in HTML templates for all styling.

**Fall back to SCSS with `@apply`** when:
- Tailwind classes make the template complex or hard to read
- You're repeating the same style combination multiple times

```scss
// Good: Extract repeated patterns to SCSS
.card-header {
  @apply flex items-center justify-between p-4 border-b border-gray-200;
}

// Good: Complex responsive patterns
.dashboard-grid {
  @apply grid gap-4 grid-cols-1 md:grid-cols-2 lg:grid-cols-3;
}
```

Avoid mixing approaches inconsistently. If a component uses SCSS, keep related styles there.

---

# Design Principles

### Visual Hierarchy
- Spacing scale: 4px, 8px, 12px, 16px, 24px, 32px
- Padding: Keep it symmetrical. If one side is 16px, others should match unless there's a clear reason.
- Depth: 
  - Use **Subtle shadows** — Soft lift for cards layouts like the presets panel.
  - Use **Borders-only** — Clean, technical. For dense tools like properties panel.
- Border Radius: Sharper feels technical. Rounder feels friendly. Pick a scale and apply consistently.
- Typography: Headlines need weight and tight tracking. Body needs readability. Data needs monospace. Build a hierarchy.
- Color: Gray builds structure. Color communicates meaning — status, action, emphasis. Decorative color is noise.
- Animation: Fast micro-interactions (~150ms), smooth easing. No bouncy/spring effects.

### Interaction Design
- Click to select, double-click to edit
- Drag handles: discoverable but not intrusive
- Context menus for advanced actions
- Keyboard shortcuts for power users

---

# Preset Design

## Best Practices
1. **Meaningful defaults**: Reasonable widths, gaps, padding
2. **Semantic labels**: Name by purpose (header, sidebar, main)
3. **Flexible sizing**: Prefer `fr` units and `flex-grow` over fixed widths
4. **Nested structure**: Group related items logically

## Example: Dashboard Preset

**Input request**: "Create a preset for a dashboard with sidebar navigation"

**Output structure**:
```
Container (Grid: 250px 1fr)
├── Sidebar (label: "sidebar")
│   ├── Nav Header (label: "nav-header")
│   └── Nav Items (label: "nav-items", flex-direction: column)
└── Main (label: "main")
    ├── Header (label: "header")
    └── Content (label: "content", grid: 1fr 1fr 1fr, gap: 16px)
```

**Key decisions**:
- Sidebar uses fixed `250px` (standard nav width), main uses `1fr` (flexible)
- Labels describe purpose, not appearance
- Content area uses grid for dashboard cards with consistent gap

---

# Review Criteria

1. **Consistency**: Matches existing patterns?
2. **Simplicity**: Simplest solution?
3. **Flexibility**: Adapts to different content?
4. **Performance**: Unnecessary re-renders?
5. **Accessibility**: Meets WCAG AA?
6. **Maintainability**: Easy to understand and modify?

## Design Review Workflow

Copy this checklist when reviewing design work:

```
Design Review:
- [ ] Spacing uses 4px grid (4, 8, 12, 16, 24, 32)
- [ ] Padding is symmetrical
- [ ] Border radius consistent with chosen system
- [ ] Single depth strategy (borders-only OR shadows)
- [ ] Color used for meaning, not decoration
- [ ] Typography hierarchy maintained
- [ ] WCAG AA contrast met
- [ ] Labels are semantic (purpose, not appearance)
- [ ] Flexible units where appropriate (fr, flex-grow)
```

---

# Avoid

- Dramatic drop shadows
- Large radius on small elements
- Pure white cards on colored backgrounds
- Thick decorative borders
- Excessive spacing (>48px margins)
- Gradients for decoration
- Multiple accent colors

---

# Deep Dives

For more detail on specific topics:
- `references/principles.md` — Code examples, specific values, dark mode
- `references/directions.md` — The 6 design personalities
- `references/validation.md` — Memory management, when to update system.md
