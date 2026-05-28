---
name: responsive-ui-auditor
description: Skill for ensuring components follow mobile-first and responsive best practices.
---

# Responsive UI Auditor

This skill provides an automated and manual way to verify that UI components are optimized for mobile and responsive across devices.

## When to use
- After creating a new UI component.
- When fixing layout issues on mobile devices.
- Before completing a task involving frontend changes.

## Audit Checklist

### 1. Viewport & Layout
- [ ] No `100vh` (use `100dvh` or `inset-0`).
- [ ] No fixed pixel widths on containers (use `w-full`, `max-w-*`).
- [ ] Tailwind classes used correctly (`md:`, `lg:`).

### 2. Interaction
- [ ] Touch targets are at least 44x44px.
- [ ] No critical functionality locked behind hover.
- [ ] Proper `touch-action` on scrollable areas.

### 3. Media
- [ ] Images have `aspect-ratio` or skeleton placeholders.
- [ ] Responsive images (`srcSet`) if applicable.

## Scripts

### `audit-responsive.sh`
Scans a file for common responsive pitfalls using grep.

**Command**:
```bash
./.agent/skills/responsive-ui-auditor/scripts/audit-responsive.sh <path-to-file>
```

## Tips
- Use Chrome DevTools Device Toolbar for quick local checks.
- Test with "Throttling" enabled to see loading states clearly.
