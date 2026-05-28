---
name: accessible-css-and-audit
description: Use this skill when you need to write accessible CSS that meets WCAG 2.2 Level AA standards and perform an accessibility audit of your code.
---

# Skill body

## Generating Accessible CSS

### Protocol and Philosophy

1. **Mobile-First**: Always start styling for the smallest screens. Use `min-width` for media queries.
2. **CSS Variables**: Use CSS Custom Properties (`--variable-name`) for colors, fonts, and spacing.
3. **Preprocessors**: Avoid using Sass/Less/Stylus. Use native CSS Nesting (if supported in `vite.config.js`).

### Accessibility Criteria (WCAG 2.2)

1. **Contrast (1.4.3)**: Always check that the contrast of text to background is at least **4.5:1** (for normal text).
2. **Focus Not Obscured (2.4.11, 2.4.12)**: When creating sticky elements (headers, footers), always add `scroll-padding-top` to the `html` or `body` container equal to the height of the sticky element. This ensures that content is not hidden under the header when tabbing.

   ```css
   html {
     scroll-padding-top: 80px; /* Height of the header */
   }
   ```

3. **Target Size (2.5.8)**: All interactive elements (`button`, `a`, `input`) must have a minimum click area of **24x24px** (recommended **44px** for mobile). If a visual element is small (e.g., a 16px icon), use padding or pseudo-elements to expand the active area.

   ```css
   .icon-btn {
     width: 16px;
     height: 16px;
     padding: 12px; /* Expands click area */
     box-sizing: content-box;
   }
   ```

4. **Visible Focus (2.4.13)**: Focus must always be visible and have high contrast.
   - **FORBIDDEN**: `outline: none;` without a clear and high-contrast replacement.

## Accessibility Audit Checklist

### Criteria for Checking (WCAG 2.2)

1. **Focus Appearance (2.4.13)**: Is there a visible focus indicator? Does it have sufficient contrast?
2. **Focus Not Obscured (2.4.11, 2.4.12)**: Is the focused element not obscured by sticky elements? Check for `scroll-padding-top`.
3. **Target Size (2.5.8)**: Do clickable elements have a size of at least 24x24 CSS pixels (better 44x44)?
4. **Contrast (1.4.3)**: Is the text contrast at least 4.5:1 for normal text?
5. **Labels (3.3.2)**: Do form fields have labels?
6. **Dragging (2.5.7)**: If there is drag-and-drop, is there a one-click alternative?

### Reporting Format

If errors are found, output them in a table:

| Element    | Violation        | WCAG Criterion | Suggested Fix                  |
| ---------- | ---------------- | -------------- | ------------------------------ |
| `<button>` | Low contrast     | 1.4.3          | Change text color to `#000`   |