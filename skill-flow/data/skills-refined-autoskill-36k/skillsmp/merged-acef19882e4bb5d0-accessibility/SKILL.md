---
name: accessibility
description: Use this skill to implement web accessibility best practices following WCAG 2.1 guidelines, ensuring inclusive and accessible user interfaces for all users.
---

# Accessibility Best Practices

This skill provides comprehensive guidance for creating accessible web experiences that comply with WCAG standards and serve users of all abilities effectively.

## When to Use This Skill

Use this skill when:
- Auditing websites for accessibility compliance
- Implementing WCAG 2.1 Level AA or AAA standards
- Fixing accessibility violations and errors
- Testing with screen readers (NVDA, JAWS, VoiceOver)
- Ensuring keyboard navigation works correctly
- Implementing ARIA attributes and landmarks
- Designing inclusive user experiences
- Conducting accessibility audits and reviews

## Core Accessibility Principles

1. **Perceivable** - Users must be able to perceive the information being presented.
2. **Operable** - Users must be able to operate the interface.
3. **Understandable** - Users must be able to understand the information and interface.
4. **Robust** - Content must be robust enough to work with current and future technologies.

## Semantic HTML

### Structural Elements
- Use semantic elements like `<header>`, `<main>`, `<footer>`, `<nav>`, `<article>`, `<section>`, `<aside>`.
- Employ `<button>` for interactive elements, not `<div>` or `<span>`.
- Use proper heading hierarchy (h1-h6) without skipping levels.
- Use landmarks for screen reader navigation.

### Form Accessibility
- Associate labels with form inputs using `for` and `id` attributes.
- Group related form elements with `<fieldset>` and `<legend>`.
- Provide clear error messages and validation feedback.

## ARIA Implementation

### When to Use ARIA
- Use ARIA roles and attributes to enhance accessibility where semantic HTML is insufficient.
- Prefer native HTML elements over ARIA when possible.
- Use `aria-label` for elements without visible text labels.

### Common ARIA Patterns
- Use `role="button"` only when a non-button element must act as a button.
- Implement `aria-expanded` for collapsible content.
- Use `aria-hidden="true"` for decorative elements.

## Color Contrast Requirements

### WCAG AA Minimum Ratios
- Normal text: **4.5:1** minimum
- Large text (≥ 18px or ≥ 14px bold): **3:1** minimum
- UI components and graphics: **3:1** minimum

### Calculating Contrast
```bash
# Use a contrast validator
npm run validate:design
```

## Keyboard Navigation

### Focus Requirements
All interactive elements must be:
1. Reachable via Tab key
2. Visually focused (visible outline)
3. Activatable via Enter/Space

### Keyboard Patterns
| Element | Keys | Action |
|---------|------|--------|
| Link/Button | Enter | Activate |
| Button | Space | Activate |
| Checkbox | Space | Toggle |
| Radio group | Arrow keys | Select |

### Skip Links
```html
<a href="#main-content" class="skip-link">Skip to main content</a>
<main id="main-content" tabindex="-1">...</main>
```

## Testing and Validation

### Automated Testing
- Use tools like Lighthouse for accessibility audits.
- Integrate axe-core for automated accessibility testing.

### Manual Testing
- Test with screen readers (NVDA, JAWS, VoiceOver).
- Navigate entirely by keyboard.
- Verify focus indicators are visible.

## Common Accessibility Issues & Fixes

### 1. Missing Alt Text for Images
**Problem:**
```html
<img src="/products/shoes.jpg">
```
**Solution:**
```html
<img src="/products/shoes.jpg" alt="Red Nike Air Max running shoes with white swoosh">
```

### 2. Low Color Contrast
**Problem:**
```css
.text {
  color: #767676;
  background: #ffffff;
}
```
**Solution:**
```css
.text {
  color: #595959;
  background: #ffffff;
}
```

### 3. Non-Semantic HTML
**Problem:**
```html
<div class="button" onclick="submitForm()">Submit</div>
```
**Solution:**
```html
<button type="submit" onclick="submitForm()">Submit</button>
```

### 4. Missing Form Labels
**Problem:**
```html
<input type="email" placeholder="Enter your email">
```
**Solution:**
```html
<label for="email">Email Address</label>
<input type="email" id="email" name="email">
```

### 5. Keyboard Navigation Issues
**Problem:**
```html
<div onclick="handleClick()">Click me</div>
```
**Solution:**
```html
<button onclick="handleClick()">Click me</button>
```

## Accessibility Statement

Include on website:
```markdown
# Accessibility Statement

We are committed to ensuring digital accessibility for people with disabilities. We continually improve the user experience for everyone and apply relevant accessibility standards.
```

## Resources

**Tools:**
- axe DevTools (browser extension)
- WAVE (web accessibility evaluation tool)
- Lighthouse (Chrome DevTools)

**Guidelines:**
- WCAG 2.1: https://www.w3.org/WAI/WCAG21/quickref/
- ARIA Authoring Practices: https://www.w3.org/WAI/ARIA/apg/

Accessibility is not optional—it's a fundamental requirement for creating inclusive web experiences. Prioritize it from the start of every project, not as an afterthought.