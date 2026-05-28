---
name: a2ui-design-bridge
description: Connects A2UI components to the Newfoundation design system. Provides CSS theming variables, styling patterns, and a compliance checklist for the brutalist-editorial aesthetic.
---

# A2UI Design Bridge: Newfoundation Integration

## Purpose

This skill bridges the **A2UI protocol** with the **Newfoundation design DNA**. It ensures that agent-generated components inherit the brutalist-editorial aesthetic defined in the `brand-identity` skill.

---

## CSS Variable Mapping

A2UI components use CSS custom properties that pierce Shadow DOM. Map these to Newfoundation tokens:

```css
:root {
  /* Typography */
  --a2ui-font-family: "Newfoundation Whyte", sans-serif;
  --a2ui-font-weight-normal: 400;
  --a2ui-font-weight-medium: 500;
  --a2ui-font-weight-bold: 600;
  
  /* Colors */
  --a2ui-primary-bg: #FFFFFF;
  --a2ui-primary-text: #000000;
  --a2ui-secondary-text: rgba(0, 0, 0, 0.8);
  --a2ui-accent: #E0FD8C;  /* Newfoundation Green */
  --a2ui-border: rgba(0, 0, 0, 0.1);
  
  /* Glassmorphism */
  --a2ui-glass-bg: rgba(255, 255, 255, 0.6);
  --a2ui-glass-blur: blur(12px);
  
  /* Spacing (8px scale) */
  --a2ui-space-xs: 8px;
  --a2ui-space-sm: 16px;
  --a2ui-space-md: 24px;
  --a2ui-space-lg: 32px;
  --a2ui-space-xl: 48px;
  
  /* Borders */
  --a2ui-border-radius: 12px;  /* Softened Brutalism */
  --a2ui-border-width: 1px;
  
  /* Animation */
  --a2ui-duration-fast: 200ms;
  --a2ui-duration-normal: 300ms;
  --a2ui-easing: ease-out;
}
```

---

## Component Styling Patterns

### Buttons (Brutalist-Technical)

```css
.a2ui-button {
  font-family: var(--a2ui-font-family);
  font-weight: var(--a2ui-font-weight-medium);
  background: var(--a2ui-glass-bg);
  backdrop-filter: var(--a2ui-glass-blur);
  border: var(--a2ui-border-width) solid var(--a2ui-border);
  border-radius: var(--a2ui-border-radius);
  padding: 10px 24px;
  cursor: pointer;
  transition: all var(--a2ui-duration-fast) var(--a2ui-easing);
}

.a2ui-button:hover {
  transform: translateY(-1px);
  background: rgba(200, 200, 200, 0.3);
}
```

### Inputs (Technical Precision)

```css
.a2ui-input {
  font-family: var(--a2ui-font-family);
  background: transparent;
  border: var(--a2ui-border-width) solid var(--a2ui-border);
  border-radius: 0;  /* Sharp corners for inputs */
  padding: var(--a2ui-space-sm);
  outline: none;
  transition: border-color var(--a2ui-duration-fast) var(--a2ui-easing);
}

.a2ui-input:focus {
  border-color: var(--a2ui-primary-text);
}
```

### Cards (Glass-Brutalist)

```css
.a2ui-card {
  background: rgba(255, 255, 255, 0.03);
  border: var(--a2ui-border-width) solid var(--a2ui-border);
  border-radius: var(--a2ui-border-radius);
  padding: var(--a2ui-space-md);
  /* No shadows - use hierarchy and borders */
}
```

---

## Animation Guidelines

> **"Minimal Inertia"** - Quick but weighted

| Property | Value |
|:---------|:------|
| Duration | 200–400ms |
| Easing | `ease-out` (refined, no bounce) |
| Style | `translateY`, opacity fades only |

**Do NOT use:**
- Spring/bounce animations
- Complex multi-axis transforms
- Delays > 100ms

---

## Design Compliance Checklist

When creating an A2UI component, verify:

- [ ] **Font**: Uses `var(--a2ui-font-family)` (Newfoundation Whyte)
- [ ] **Colors**: Black text on white, accents use Newfoundation Green
- [ ] **Borders**: Subtle `rgba(0, 0, 0, 0.1)`, no heavy shadows
- [ ] **Spacing**: Multiples of 8px only
- [ ] **Radius**: 12px for buttons/cards, 0 for inputs
- [ ] **Animation**: 200-400ms, `ease-out`, no bounce
- [ ] **Typography**: Tight line-height (1.3-1.6)

---

## Integration Example

```typescript
import { DynamicComponent } from '@a2ui/core';
import { html, css } from 'lit';
import { customElement } from 'lit/decorators.js';

@customElement('agui-action-button')
export class ActionButton extends DynamicComponent {
  static styles = css`
    button {
      font-family: var(--a2ui-font-family);
      font-weight: var(--a2ui-font-weight-medium);
      background: var(--a2ui-glass-bg);
      backdrop-filter: var(--a2ui-glass-blur);
      border: var(--a2ui-border-width) solid var(--a2ui-border);
      border-radius: var(--a2ui-border-radius);
      padding: 10px 24px;
      cursor: pointer;
      transition: all var(--a2ui-duration-fast) var(--a2ui-easing);
    }
    
    button:hover {
      transform: translateY(-1px);
    }
  `;

  render() {
    const label = this.resolve(this.componentDefinition?.label);
    return html`
      <button @click=${() => this.dispatchUserAction('click')}>
        ${label ?? 'Action'}
      </button>
    `;
  }
}
```

---

## Assets

| File | Purpose |
|:-----|:--------|
| `assets/a2ui-theme.css` | Complete CSS variable definitions |
