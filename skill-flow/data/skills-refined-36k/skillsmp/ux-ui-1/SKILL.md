---
name: ux-ui
description: "UX/UI review process and accessibility assessment. Use when reviewing UI implementations, implementing WCAG accessibility, creating design system components, evaluating usability, or building responsive designs. Also use when images lack alt text, color is the only way to convey information, interactive elements aren't keyboard accessible, form inputs lack labels, or focus states are missing. Essential for accessibility audits, a11y compliance, and usability heuristic evaluations."
---

# UX/UI Skill

## Overview

Good UX is invisible. Users should accomplish their goals without thinking about the interface. This skill guides systematic review of UI implementations for accessibility, usability, and consistency.

**Core principle:** Accessibility is not optional. WCAG compliance is a legal requirement in many jurisdictions and benefits all users—not just those with disabilities.

## The UX/UI Review Process

### Phase 1: Check Accessibility First

**Accessibility is the foundation. Start here:**

1. **Perceivable**
   - Can screen readers access all content?
   - Is there sufficient color contrast?
   - Are images described?

2. **Operable**
   - Can everything be done with keyboard?
   - Are focus states visible?
   - Is there enough time for interactions?

3. **Understandable**
   - Is language clear?
   - Are errors explained?
   - Is behavior predictable?

4. **Robust**
   - Is HTML valid and semantic?
   - Are ARIA attributes correct?
   - Does it work across browsers?

### Phase 2: Check Usability

**Then verify usability heuristics:**

1. **System Status**
   - Does the user know what's happening?
   - Are loading states shown?
   - Is progress indicated?

2. **Error Prevention**
   - Are dangerous actions confirmed?
   - Is input validated early?
   - Can mistakes be undone?

3. **Efficiency**
   - Can experts use shortcuts?
   - Is the most common path optimized?
   - Is navigation consistent?

### Phase 3: Check Consistency

**Finally, verify design system adherence:**

1. **Visual Consistency**
   - Following spacing system?
   - Using design tokens?
   - Matching typography scale?

2. **Behavioral Consistency**
   - Same interactions behave same way?
   - Consistent feedback patterns?
   - Predictable navigation?

## Red Flags - STOP and Fix

### Accessibility Red Flags

```html
<!-- ❌ CRITICAL: No alt text -->
<img src="chart.png">

<!-- ❌ CRITICAL: Non-semantic button -->
<div onclick="submit()">Submit</div>

<!-- ❌ HIGH: Color-only information -->
<span style="color: red">Required</span>

<!-- ❌ HIGH: No form label -->
<input type="email" placeholder="Email">

<!-- ❌ HIGH: Hidden focus state -->
*:focus { outline: none; }

<!-- ❌ MEDIUM: Auto-playing media -->
<video autoplay>
```

### Usability Red Flags

```html
<!-- ❌ HIGH: No loading state -->
<button onclick="slowAction()">Save</button>
<!-- User has no idea if click worked -->

<!-- ❌ HIGH: No error explanation -->
<input class="error">  <!-- Why is it error? -->

<!-- ❌ HIGH: Destructive action without confirm -->
<button onclick="deleteAll()">Delete All</button>

<!-- ❌ MEDIUM: Tiny touch target -->
<a style="font-size: 10px;">Click me</a>
```

### Design Consistency Red Flags

```css
/* ❌ HIGH: Hardcoded values */
padding: 13px;  /* Should use spacing token */
font-size: 15px;  /* Should use type scale */
color: #337ab7;  /* Should use color token */

/* ❌ MEDIUM: Inconsistent spacing */
.card { padding: 16px; }
.card-similar { padding: 20px; }  /* Why different? */
```

## Common Rationalizations - Don't Accept These

| Excuse | Reality |
|--------|---------|
| "Accessibility is for blind people" | It benefits everyone: SEO, mobile, aging users. |
| "We'll add a11y later" | Retrofitting is 10x harder. Build it in. |
| "No one uses keyboard" | Many do. And it's legally required. |
| "The design doesn't have alt text" | Write it yourself. You understand the content. |
| "Our users don't have disabilities" | You don't know that. And they might in the future. |
| "Focus outlines are ugly" | Design better ones. Don't remove them. |

## UX/UI Quality Checklist

Before approving UI changes:

**Accessibility (WCAG 2.1 AA):**
- [ ] All images have alt text
- [ ] Color contrast meets 4.5:1 (text), 3:1 (large/UI)
- [ ] All interactive elements keyboard accessible
- [ ] Form inputs have associated labels
- [ ] Focus states visible and meaningful
- [ ] Heading hierarchy is logical (h1 → h2 → h3)
- [ ] ARIA used correctly (or not at all)

**Usability:**
- [ ] Loading states shown for async operations
- [ ] Error messages explain how to fix
- [ ] Destructive actions require confirmation
- [ ] Touch targets are 44x44px minimum
- [ ] Most common paths are optimized

**Consistency:**
- [ ] Uses design system tokens
- [ ] Follows established patterns
- [ ] Spacing/typography from scale

## Quick Patterns

### Accessible Button

```html
<!-- ✅ Semantic, keyboard accessible, described -->
<button
  type="submit"
  aria-label="Submit contact form"
  disabled={isSubmitting}
>
  {isSubmitting ? 'Submitting...' : 'Submit'}
</button>
```

### Accessible Form Field

```html
<!-- ✅ Labeled, described, with error handling -->
<div class="field">
  <label for="email">
    Email address
    <span aria-hidden="true">*</span>
  </label>
  <input
    type="email"
    id="email"
    required
    aria-required="true"
    aria-describedby="email-hint email-error"
    aria-invalid={hasError}
  >
  <span id="email-hint" class="hint">
    We'll never share your email.
  </span>
  {hasError && (
    <span id="email-error" class="error" role="alert">
      Please enter a valid email address.
    </span>
  )}
</div>
```

### Accessible Image

```html
<!-- ✅ Informative image with description -->
<img
  src="sales-chart.png"
  alt="Sales chart showing 25% growth in Q4 2024"
>

<!-- ✅ Decorative image (skip for screen readers) -->
<img src="decorative-line.png" alt="" role="presentation">
```

### Skip Link

```html
<!-- ✅ Skip to main content for keyboard users -->
<a href="#main" class="skip-link">
  Skip to main content
</a>

<style>
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  padding: 8px;
  background: #000;
  color: #fff;
  z-index: 100;
}
.skip-link:focus {
  top: 0;
}
</style>
```

### Focus Styles

```css
/* ✅ Visible, high-contrast focus indicator */
:focus {
  outline: 2px solid #005fcc;
  outline-offset: 2px;
}

/* ✅ Only hide for mouse users */
:focus:not(:focus-visible) {
  outline: none;
}
:focus-visible {
  outline: 2px solid #005fcc;
  outline-offset: 2px;
}
```

## Quick Commands

```bash
# Accessibility testing
npx axe-core-cli <url>             # Automated a11y scan
npx pa11y <url>                    # Page accessibility
npx lighthouse <url> --view        # Full audit

# Visual testing
npx storybook                      # Component testing
npx chromatic                      # Visual regression

# Validation
npx html-validate <file>           # HTML validation
```

## WCAG Quick Reference

| Level | Requirement | Ratio |
|-------|-------------|-------|
| AA | Normal text contrast | 4.5:1 |
| AA | Large text contrast | 3:1 |
| AA | UI component contrast | 3:1 |
| AAA | Normal text contrast | 7:1 |
| AAA | Large text contrast | 4.5:1 |

**Large text:** 18pt+ regular OR 14pt+ bold

## References

Detailed patterns and examples in `references/`:
- `wcag-checklist.md` - Complete WCAG 2.1 AA checklist
- `aria-patterns.md` - Correct ARIA usage
- `design-tokens.md` - Design system patterns
