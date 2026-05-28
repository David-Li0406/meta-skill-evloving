---
name: frontend-design-v2
description: Extended frontend design guidelines with comprehensive mobile responsiveness and cross-element styling consistency. Use alongside /frontend-design for production-grade, mobile-first interfaces.
version: 1.0.0
author: Design Styles Explorer Project
updated: 2025-01-11
---

# Mobile-First Frontend Design Guidelines

This skill extends the core frontend-design principles with critical mobile responsiveness patterns and cross-element styling consistency learned from real-world implementation.

## Mobile Layout Patterns

### Hero Sections

**Problem**: 2-column grid layouts leave empty space when one column is hidden on mobile.

```css
/* Desktop: 2-column grid */
.hero {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 64px;
  align-items: center;
}

/* Mobile: Switch to centered flex */
@media (max-width: 768px) {
  .hero {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 40px 20px;
    gap: 24px;
  }

  .hero-content {
    align-items: center;
  }

  .hero-badge {
    align-self: center;
  }

  .hero-title {
    font-size: 32px;
    text-align: center;
  }

  .hero-subtitle {
    font-size: 14px;
    text-align: center;
  }

  .hero-cta {
    flex-direction: column;
    align-items: center;
    width: 100%;
  }

  .hero-cta .btn {
    width: 100%;
    max-width: 280px;
  }

  .hero-visual {
    display: none;
  }
}
```

**Key Rule**: When hiding grid columns on mobile, switch from `display: grid` to `display: flex` to eliminate reserved empty space.

### Large Selection Lists (Accordion Pattern)

**Problem**: Horizontal scroll for many items (20+) is unusable on mobile - text gets cut off.

**Solution**: Use collapsible accordion with category headers.

```jsx
// Instead of horizontal scroll
function StyleSelector({ items, categories }) {
  const [expandedCategory, setExpandedCategory] = useState(null);

  return (
    <div className="selector">
      {categories.map(category => (
        <div key={category.name} className={`category ${expandedCategory === category.name ? 'expanded' : ''}`}>
          <button
            className="category-header"
            onClick={() => setExpandedCategory(
              expandedCategory === category.name ? null : category.name
            )}
          >
            <span>{category.name}</span>
            <ChevronIcon />
          </button>
          <div className="category-items">
            {category.items.map(item => (
              <button key={item.id} className="item">{item.name}</button>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
```

```css
@media (max-width: 768px) {
  .category-items {
    display: none;
  }

  .category.expanded .category-items {
    display: flex;
    flex-direction: column;
  }

  .chevron-icon {
    transition: transform 0.2s ease;
  }

  .category.expanded .chevron-icon {
    transform: rotate(180deg);
  }
}
```

### Form Layouts

**Problem**: Multi-column form layouts get cut off on mobile.

```css
.form-row {
  display: flex;
  gap: 16px;
}

@media (max-width: 768px) {
  .form-row {
    flex-direction: column;
  }

  .form-group {
    width: 100%;
  }
}
```

### Status/Alert Cards

**Problem**: Inconsistent text alignment when stacking horizontally-laid elements vertically.

```css
.alert {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

@media (max-width: 768px) {
  .alert {
    flex-direction: column;
    align-items: center;  /* Center the flex items */
    text-align: center;   /* Center the text within items */
    gap: 8px;
  }

  .alert strong {
    text-align: center;  /* Explicit for block elements */
  }
}
```

**Key Rule**: Stacked flex items need BOTH `align-items: center` AND `text-align: center` for proper centering.

### Grid Layouts

```css
@media (max-width: 768px) {
  .pricing-grid,
  .feature-grid,
  .team-grid,
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
```

---

## Form Element Consistency

### Always Style as a Group

**Problem**: Styling only `.input` leaves `.select` and `.textarea` unstyled.

```css
/* WRONG - Only targets input */
.style-brutalist .input {
  border: 2px solid var(--border);
  border-radius: 0;
}

/* CORRECT - Targets all form fields */
.style-brutalist .input,
.style-brutalist .select,
.style-brutalist .textarea {
  border: 2px solid var(--border);
  border-radius: 0;
}
```

### Textarea Border Radius Exceptions

Pill-shaped inputs (border-radius: 100px) look wrong on textareas:

```css
.style-kawaii .input,
.style-kawaii .select {
  border-radius: 100px;
}

/* Textarea needs smaller radius */
.style-kawaii .textarea {
  border-radius: 20px;
}
```

### Dropdown Option Styling

`<option>` elements can't inherit backdrop-filter or complex backgrounds:

```css
.style-glassmorphism .select {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  color: white;
}

/* Options need solid backgrounds */
.style-glassmorphism .select option {
  background: #1a1a2e;
  color: white;
}
```

### Transparent Border Styles (Neomorphism, Claymorphism)

**Problem**: Styles with `border: transparent` make form controls invisible.

```css
/* These styles use transparent borders */
.style-neomorphism .radio-mark,
.style-claymorphism .radio-mark {
  border: 2px solid #B8BEC7;  /* Add visible border */
  background: var(--bg-primary);
  box-shadow: inset 2px 2px 4px rgba(163,177,198,0.3),
              inset -2px -2px 4px rgba(255,255,255,0.8);
}
```

---

## Color Contrast Checklist

### Badge/Pill Elements

Always verify badge text contrasts with its background:

```css
/* WRONG - May be invisible on light backgrounds */
.badge {
  color: white;
}

/* CORRECT - Uses semantic variable */
.badge {
  color: var(--bg-primary);  /* Inverts with background */
}
```

### Color Swatches Display

Swatches showing colors need visible borders regardless of swatch color:

```css
.color-swatch {
  border: 2px solid rgba(255, 255, 255, 0.15);
  box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.3);
}
```

### Dark Theme Form Labels

**Problem**: Assuming labels should be white/light on dark themes.

```css
/* WRONG - Hardcoded color */
.label {
  color: white;
}

/* CORRECT - Uses semantic variable */
.label {
  color: var(--text-primary);
}
```

---

## Breakpoint Reference

```css
/* Tablet - Stack sidebars, maintain content width */
@media (max-width: 1200px) { }

/* Mobile - Full single-column, centered hero */
@media (max-width: 768px) { }

/* Small Mobile - Compact spacing, reduced font sizes */
@media (max-width: 480px) { }
```

### Mobile Font Scaling

```css
@media (max-width: 768px) {
  .hero-title {
    font-size: 32px;  /* Down from ~48px */
  }

  .section-title {
    font-size: 24px;  /* Down from ~32px */
  }

  .section-subtitle {
    font-size: 14px;  /* Down from ~16px */
  }
}
```

---

## Pre-Implementation Checklist

Before finalizing any frontend design, verify:

1. [ ] Hero section centers on mobile (not left-aligned with empty space)
2. [ ] All form fields (input, select, textarea) styled consistently
3. [ ] Radio buttons and checkboxes visible (especially for transparent-border styles)
4. [ ] Dropdown options have readable backgrounds
5. [ ] Labels use semantic color variables (not hardcoded)
6. [ ] Status/alert cards center properly on mobile
7. [ ] Large selection lists use accordion on mobile (not horizontal scroll)
8. [ ] Grid layouts collapse to single column on mobile
9. [ ] Badge/pill text contrasts with background
10. [ ] Color swatches have visible borders

---

## Common Mobile Issues Quick Reference

| Issue | Cause | Fix |
|-------|-------|-----|
| Hero left-aligned with empty space | Grid reserves hidden column | Switch to flex on mobile |
| Form fields cut off | Fixed-width grid | Stack vertically with flex |
| Inconsistent alert alignment | Missing align-items | Add `align-items: center` + `text-align: center` |
| Invisible form controls | Transparent borders | Add explicit borders or shadows |
| White text on light background | Hardcoded colors | Use semantic CSS variables |
| Horizontal scroll on selections | Too many items | Use accordion pattern |
| Textarea looks wrong | Pill border-radius | Use smaller radius for textarea |
