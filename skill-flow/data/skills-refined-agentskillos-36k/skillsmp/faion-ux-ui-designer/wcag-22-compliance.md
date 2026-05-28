# WCAG 2.2 Compliance

### What's New in WCAG 2.2

Released October 2023, baseline compliance standard by 2025-2026.

**9 New Success Criteria:**

| Criterion | Level | Requirement |
|-----------|-------|-------------|
| Focus Not Obscured (Min) | AA | Focus indicator must be at least partially visible |
| Focus Not Obscured (Enhanced) | AAA | Focus indicator fully visible |
| Focus Appearance | AAA | 2px minimum focus indicator |
| Dragging Movements | AA | All drag actions have non-drag alternative |
| Target Size (Minimum) | AA | 24x24 CSS pixels minimum |
| Consistent Help | A | Help mechanism in same location across pages |
| Redundant Entry | A | Don't ask for same info twice |
| Accessible Authentication (Min) | AA | No cognitive function tests for login |
| Accessible Authentication (Enhanced) | AAA | No object/image recognition for login |

**Target Size Examples:**
```css
/* Minimum 24x24px */
.button {
  min-width: 24px;
  min-height: 24px;
  /* Or 44x44px for touch targets (recommended) */
}
```

**Dragging Alternatives:**
| Drag Action | Alternative Required |
|-------------|---------------------|
| Drag to reorder | Up/down buttons |
| Drag to resize | Input field for value |
| Drag to select area | Click corners |
