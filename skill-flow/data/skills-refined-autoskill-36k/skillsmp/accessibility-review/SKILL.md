---
name: accessibility-review
description: Audit for WCAG 2.1 AA compliance including keyboard navigation, ARIA usage, color contrast, and screen reader support. Use when building UI components, reviewing forms, or checking accessibility of new features.
---

# Accessibility Review

Audit components and pages for WCAG 2.1 AA compliance as specified in AGENTS.md.

## Scope

Review the specified files for:

### 1. Semantic HTML
- Proper heading hierarchy (h1 -> h2 -> h3, no skipping)
- Use of semantic elements (nav, main, article, section, aside)
- Lists for list content (ul, ol, dl)
- Buttons for actions, links for navigation
- Tables with proper headers and scope

### 2. Keyboard Accessibility
- All interactive elements focusable
- Logical tab order
- Visible focus indicators (check for `outline-none` without replacement)
- No keyboard traps
- Skip links for navigation
- Escape key closes modals/dialogs

### 3. ARIA Usage
- ARIA only when semantic HTML insufficient
- Proper ARIA roles, states, and properties
- ARIA labels on icon-only buttons
- Live regions for dynamic content
- Proper dialog/modal ARIA patterns

### 4. Forms
- Labels associated with inputs (htmlFor/id or wrapping)
- Error messages linked to fields (aria-describedby)
- Required fields indicated (aria-required)
- Fieldset/legend for radio/checkbox groups
- Autocomplete attributes where appropriate

### 5. Visual Design
- Color contrast ratios (4.5:1 text, 3:1 UI components)
- Not relying on color alone for meaning
- Respects `prefers-reduced-motion`
- Respects `prefers-color-scheme`
- Text resizable to 200% without loss

### 6. Images & Media
- Alt text on images (empty alt="" for decorative)
- Captions/transcripts for video/audio
- No auto-playing media with sound

### 7. Component-Specific (shadcn/Radix)
- Radix primitives used correctly (they handle a11y)
- Custom overrides don't break accessibility
- Tooltips accessible to keyboard users
- Dropdown menus with proper ARIA

## Output Format

For each finding:
```
[WCAG: 1.1.1|2.1.1|etc] [LEVEL: A|AA|AAA]
File: path/to/component.tsx:lineNumber
Issue: Brief description
Impact: Who is affected and how
Fix: Code example or recommendation
```

## Actions

1. Read component files in scope
2. Check for Radix/shadcn primitive usage
3. Verify keyboard interaction patterns
4. Analyze color usage and contrast
5. Review form patterns

## Post-Review

Generate:
- Findings grouped by WCAG principle (Perceivable, Operable, Understandable, Robust)
- Priority fixes (Level A before AA)
- Component-specific recommendations
- Testing checklist for manual verification
