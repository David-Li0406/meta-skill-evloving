---
name: uxui-design
description: Practical UI/UX work within existing design systems. Use for styling, layout, states, accessibility, and design system compliance. Use when working on established products.
---

# UX/UI Design

Practical UI/UX work within an existing design system.

> **When to use**: Working on established products with existing patterns. For new products or landing pages that need to stand out, use `uxui-creative` instead.

**CRITICAL: Think deeply about spacing and layout before writing code.** Analyze spatial relationships and whitespace rhythm. Rushed spacing = amateur UI.

---

## Rules

1. **Analyze the design system first** — spacing scale, type scale, colors, radii, existing patterns
2. **Follow it strictly** — no invented values. Break only with explicit justification
3. **Structure before style** — layout and hierarchy first, then color/shadow/borders
4. **Every value is intentional** — if you can't justify 16px vs 14px, you're guessing
5. **Accessibility is not optional** — semantic HTML, sufficient contrast, keyboard navigable
6. **Mobile-first** — touch targets min 44px, responsive breakpoints, test narrow viewports

---

## Handle All States

Don't just build the happy path:
- **Empty** — no data, first-time user
- **Loading** — skeleton or spinner, preserve layout
- **Error** — clear message, recovery action
- **Edge cases** — long text (truncate), missing images (fallback), overflow

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Inconsistent spacing | Use the scale |
| Too many font sizes | Max 3 per view |
| Borders AND shadows | Pick one |
| No hover/focus states | Clickable = feedback |
| Too tight | Add whitespace |
| Inaccessible | Check contrast, use semantic elements |
| Happy path only | Handle empty, loading, error |

---

## Checklist

- [ ] All spacing/sizing from design system
- [ ] Clear visual hierarchy
- [ ] Hover + focus + disabled states
- [ ] Matches existing patterns
- [ ] Accessible (contrast, keyboard, semantic HTML)
- [ ] All states handled (empty, loading, error)
- [ ] Works on mobile

---

## ULTRATHINK

Trigger: "ULTRATHINK: [question]"

For: component API, layout architecture, new patterns, accessibility deep-dive

---

# UI/UX Review Checklist

## Visual Consistency
- [ ] Colors match design system
- [ ] Typography follows hierarchy
- [ ] Spacing is consistent (use design tokens)
- [ ] Icons are from the same family
- [ ] Borders/shadows follow patterns

## Layout
- [ ] Responsive at all breakpoints (mobile, tablet, desktop)
- [ ] No horizontal scroll on mobile
- [ ] Content doesn't overflow containers
- [ ] Proper alignment (left, center, right)
- [ ] Grid/flex used appropriately

## Interactions
- [ ] Hover states present and consistent
- [ ] Focus states visible (accessibility)
- [ ] Loading states for async actions
- [ ] Error states are clear
- [ ] Success feedback provided

## Usability
- [ ] Actions are discoverable
- [ ] Labels are clear and concise
- [ ] Forms have proper validation feedback
- [ ] Navigation is intuitive
- [ ] Empty states are handled

## Accessibility
- [ ] Sufficient color contrast (WCAG AA)
- [ ] Keyboard navigation works
- [ ] Screen reader friendly (ARIA labels)
- [ ] Focus order is logical
- [ ] Text is resizable

---

## Common Code Issues

### Missing Loading State
```tsx
// BAD - no feedback
<button onClick={submit}>Submit</button>

// GOOD - loading feedback
<button onClick={submit} disabled={loading}>
  {loading ? <Spinner /> : 'Submit'}
</button>
```

### Missing Focus State
```css
/* BAD - removes focus */
button:focus { outline: none; }

/* GOOD - custom focus */
button:focus-visible {
  outline: 2px solid var(--focus-color);
  outline-offset: 2px;
}
```

### Hardcoded Dimensions
```css
/* BAD - fixed width */
.card { width: 300px; }

/* GOOD - responsive */
.card { 
  width: 100%;
  max-width: 300px;
}
```

---

## Review Rules

1. **Test on real devices** — Emulators miss touch issues
2. **Check dark mode** — If supported, test both themes
3. **Keyboard first** — Navigate without mouse
4. **Slow network** — Test with throttling
5. **Content extremes** — Test with very short and very long content
