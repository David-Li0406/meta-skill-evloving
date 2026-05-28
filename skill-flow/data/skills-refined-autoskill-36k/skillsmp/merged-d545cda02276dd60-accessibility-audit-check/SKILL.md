---
name: accessibility-audit-check
description: Use this skill to evaluate and audit UI components and pages for accessibility compliance with WCAG guidelines, ensuring inclusive design practices.
---

# Accessibility Audit and Check Skill

Evaluate and audit UI accessibility against WCAG 2.1/2.2 guidelines to ensure inclusive design for all users.

## When to Use

- Reviewing UI components for accessibility compliance
- Auditing pages for WCAG conformance
- Identifying keyboard navigation issues
- Checking color contrast
- Pre-launch accessibility verification
- Before releasing new features
- Ensuring legal compliance
- Improving user inclusivity

## Core Workflow

### Phase 1: Visual Accessibility Analysis

```
Perform a comprehensive accessibility audit:

1. COLOR CONTRAST
   - Check text/background contrast ratios
   - WCAG AA: 4.5:1 normal text, 3:1 large text
   - Identify failing elements

2. VISUAL HIERARCHY
   - Heading structure (logical H1-H6)
   - Visual grouping of related elements
   - Touch targets (44x44px minimum)

3. CONTENT ACCESSIBILITY
   - Images needing alt text
   - Icons without text labels
   - Color-only information

4. INTERACTIVE ELEMENTS
   - Buttons/links with unclear purpose
   - Form fields without labels
   - Missing error states

5. MOTION
   - Auto-playing content
   - Potential vestibular triggers

Provide WCAG criterion references for each issue.
```

### Phase 2: Component Checklist

For each interactive component:

```markdown
## Component: [Name]

### Keyboard Navigation

- [ ] Focusable with Tab
- [ ] Visible focus indicator
- [ ] Operable with Enter/Space
- [ ] Escape closes modals
- [ ] Arrow keys for menus

### Screen Reader

- [ ] Meaningful accessible name
- [ ] Role announced correctly
- [ ] State changes announced
- [ ] Errors associated with inputs

### Visual

- [ ] 4.5:1 contrast ratio (text)
- [ ] 3:1 contrast ratio (UI)
- [ ] 44x44px touch targets
- [ ] No color-only information

### Motion

- [ ] Respects prefers-reduced-motion
- [ ] No auto-play >5 seconds
```

## WCAG 2.1 Checklist

### Level A (Minimum)

#### Perceivable
- [ ] **1.1.1 Non-text Content**: Images have alt text
- [ ] **1.3.1 Info and Relationships**: Semantic HTML structure
- [ ] **1.3.2 Meaningful Sequence**: Logical reading order
- [ ] **1.4.1 Use of Color**: Color not sole indicator

#### Operable
- [ ] **2.1.1 Keyboard**: All functionality via keyboard
- [ ] **2.1.2 No Keyboard Trap**: Can navigate away
- [ ] **2.4.1 Bypass Blocks**: Skip to content link
- [ ] **2.4.2 Page Titled**: Descriptive page titles
- [ ] **2.4.3 Focus Order**: Logical tab sequence
- [ ] **2.4.4 Link Purpose**: Links describe destination

#### Understandable
- [ ] **3.1.1 Language of Page**: `lang` attribute set
- [ ] **3.2.1 On Focus**: No unexpected changes
- [ ] **3.2.2 On Input**: No unexpected changes
- [ ] **3.3.1 Error Identification**: Errors clearly described
- [ ] **3.3.2 Labels**: Form inputs have labels

#### Robust
- [ ] **4.1.1 Parsing**: Valid HTML
- [ ] **4.1.2 Name, Role, Value**: ARIA correctly used

### Level AA (Standard Target)

#### Perceivable
- [ ] **1.4.3 Contrast (Minimum)**: 4.5:1 for text
- [ ] **1.4.4 Resize Text**: Readable at 200% zoom
- [ ] **1.4.5 Images of Text**: Avoid where possible

#### Operable
- [ ] **2.4.5 Multiple Ways**: Multiple navigation paths
- [ ] **2.4.6 Headings and Labels**: Descriptive headings
- [ ] **2.4.7 Focus Visible**: Clear focus indicators

#### Understandable
- [ ] **3.2.3 Consistent Navigation**: Same nav location
- [ ] **3.2.4 Consistent Identification**: Same icons/labels
- [ ] **3.3.3 Error Suggestion**: Suggest corrections
- [ ] **3.3.4 Error Prevention**: Confirm destructive actions

## Testing Methods

### 1. Automated Testing
```bash
# Using axe-core via Playwright
npx playwright test --grep accessibility

# Using pa11y
npx pa11y http://localhost:5176
```

### 2. Manual Keyboard Testing
1. Tab through entire page
2. Verify focus visibility
3. Test Enter/Space activation
4. Check Escape closes modals
5. Verify arrow key navigation in menus

### 3. Screen Reader Testing
- Test with VoiceOver (Mac)
- Test with NVDA (Windows)
- Verify announcements make sense
- Check form label associations

### 4. Visual Testing
- Check color contrast ratios
- Test at 200% zoom
- Verify without color
- Check reduced motion

## Common Fixes

### Missing Alt Text
```jsx
// Bad
<img src="logo.png" />

// Good
<img src="logo.png" alt="LogiDocs Certify logo" />
```

### Missing Form Labels
```jsx
// Bad
<input type="email" placeholder="Email" />

// Good
<label htmlFor="email">Email</label>
<input id="email" type="email" />
```

### Low Contrast Fix
```css
/* Bad: 2.5:1 ratio */
.button { color: #999; background: #fff; }

/* Good: 4.5:1+ ratio */
.button { color: #595959; background: #fff; }
```

### Focus Indicator
```css
/* Ensure visible focus */
:focus {
  outline: 2px solid #16a34a;
  outline-offset: 2px;
}
```

## Report Template

```markdown
# Accessibility Audit Report

**Date:** [Date]
**Page:** [Name]
**WCAG Level:** AA

## Summary

- Critical Issues: X
- Major Issues: X
- Minor Issues: X

## Issues

### [Issue Title]

- **Severity:** Critical/Major/Minor
- **WCAG:** [X.X.X]
- **Element:** [selector]
- **Issue:** [Description]
- **Fix:** [Recommendation]
```

## Storage

Save audit reports to `.opencode/memory/design/accessibility/`

## Related Skills

| Need           | Skill                 |
| -------------- | --------------------- |
| Design quality | `frontend-design` |
| UI research    | `ui-ux-research`      |