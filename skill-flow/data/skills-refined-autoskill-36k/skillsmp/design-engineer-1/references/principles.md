# Core Craft Principles

These principles apply across any visual direction. They're the foundation of professional interface work.

## Surface & Token Systems

Build from primitives:
- **Foreground** — Text and icons
- **Background** — Page canvas
- **Border** — Dividers and containers
- **Brand** — Primary action color
- **Semantic** — Success, warning, error, info

Create a numbered elevation hierarchy:
```
surface-0: Base canvas
surface-1: Raised cards
surface-2: Modals, dropdowns
surface-3: Tooltips, popovers
```

Each elevation should be only a few percentage points of lightness different. Whisper-quiet shifts that you feel rather than see.

## The Subtlety Principle

**The Squint Test:** Blur your eyes or step back. You should still perceive the hierarchy — what's above what, where regions begin and end. If borders are the first thing you notice, reduce opacity. If you can't find where regions end, increase slightly.

### Borders

Use rgba, not solid colors. Low opacity borders blend with their background:
```css
/* Good */
border: 1px solid rgba(255, 255, 255, 0.08);

/* Harsh */
border: 1px solid #333;
```

Border intensity matches boundary importance:
- **Standard** — 0.05-0.08 alpha
- **Subtle** — 0.03-0.05 alpha
- **Strong** — 0.10-0.12 alpha
- **Stronger** — 0.15-0.20 alpha

### Text Contrast Progression

Four levels of text contrast:
```
primary:   1.0 alpha — Headings, important content
secondary: 0.7 alpha — Body text
tertiary:  0.5 alpha — Supporting text
muted:     0.4 alpha — Disabled, hints
```

## Spacing System

Establish a consistent base unit (4px or 8px) with multiples:
```
micro:     4px  — Icon gaps, tight groups
component: 8px  — Within components
element:   16px — Between elements
section:   24px — Between sections
major:     32px — Major divisions
```

Use symmetrical padding. Maintain deliberate border radius scale.

## Depth Strategies

**Choose one and commit:**

1. **Borders-only** — Technical, information-dense (Linear, GitHub)
   - No shadows
   - Borders define containers
   - Clean, fast

2. **Subtle shadows** — Approachable (Notion)
   - Very light shadows
   - Some border use
   - Soft hierarchy

3. **Layered shadows** — Premium (Stripe)
   - Multiple shadow layers
   - Clear depth perception
   - Rich, elevated

4. **Surface color shifts** — Hierarchical (Supabase)
   - Background colors change with elevation
   - Minimal shadows
   - Color-driven depth

## Typography

- Weight and letter-spacing combined with size
- Monospace with `tabular-nums` for numerical data
- System fonts for utility focus
- Geometric/humanist for personality

## Interaction States

Every interactive element needs:
- Default
- Hover
- Focus (accessible focus rings)
- Active/pressed
- Disabled
- Loading (where applicable)
- Error (for form elements)

## Animation

Keep it functional:
- **Micro-interactions:** 150ms
- **Transitions:** 200-250ms
- **Easing:** Smooth deceleration (`ease-out`)

## Form Controls

Native form elements can't be styled consistently. Build custom:
- Selects/dropdowns
- Date pickers
- Checkboxes/radios
- Switches

Inputs should feel "inset" — slightly darker background signals "type here" without heavy borders.
