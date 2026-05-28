# Accessibility Guide (WCAG 2.1 AA)

Comprehensive accessibility guidelines for the LucidData application, targeting WCAG 2.1 Level AA compliance.

## WCAG 2.1 AA Requirements

### 1. Perceivable

#### 1.1 Text Alternatives
- **Images**: All images must have `alt` text
  ```tsx
  // Decorative images
  <img src="logo.svg" alt="" />

  // Informative images
  <img src="chart.png" alt="Revenue growth chart showing 25% increase" />
  ```

#### 1.3 Adaptable
- **Semantic HTML**: Use proper heading hierarchy (h1 → h2 → h3)
  ```tsx
  <h1>Dashboard</h1>
  <section>
    <h2>Vault Entries</h2>
    <h3>Recent Additions</h3>
  </section>
  ```

#### 1.4 Distinguishable

**Color Contrast** (critical):
- Normal text (< 18px): **4.5:1** minimum
- Large text (≥ 18px or 14px bold): **3:1** minimum
- UI components: **3:1** minimum

**Check contrast**:
```tsx
// Bad: Low contrast
<p className="text-gray-400 bg-white">Text</p> // ~2.6:1 ❌

// Good: High contrast
<p className="text-gray-900 bg-white">Text</p> // 15:1 ✅

// Use muted colors (designed for 4.5:1+)
<p className="text-muted-foreground">Text</p> ✅
```

**Tools**:
- Chrome DevTools → Accessibility → Contrast ratio
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Stark Plugin](https://www.getstark.co/)

### 2. Operable

#### 2.1 Keyboard Accessible

**All interactive elements must be keyboard accessible**:
- Tab navigation works
- Enter/Space activate buttons/links
- Escape closes modals/dropdowns
- Arrow keys navigate lists/menus

```tsx
// Custom interactive element (needs tabindex)
<div
  role="button"
  tabIndex={0}
  onClick={handleClick}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      handleClick();
    }
  }}
>
  Custom Button
</div>

// Use native button instead (preferred)
<button onClick={handleClick}>
  Native Button
</button>
```

#### 2.4 Navigable

**Focus Indicators** (critical):
```tsx
// All focusable elements need visible focus
<Button className="focus-visible:ring-2 focus-visible:ring-offset-2">
  Click me
</Button>

// Custom focus styles
<a className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary">
  Link
</a>

// Never disable focus outlines without replacement
❌ <button className="outline-none">Bad</button>
✅ <button className="focus-visible:ring-2">Good</button>
```

**Skip Links** (for keyboard users):
```tsx
// Add at top of page
<a href="#main-content" className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4">
  Skip to main content
</a>

<main id="main-content">
  {/* content */}
</main>
```

**Page Titles**:
```tsx
// Next.js metadata
export const metadata = {
  title: 'Vault - Lucid',
  description: 'Manage your personal data vault'
};
```

### 3. Understandable

#### 3.2 Predictable

**Consistent Navigation**:
- Navigation is in the same location across pages
- Icons and labels are consistent

**No Context Changes on Focus**:
```tsx
// Bad: Focus triggers navigation
❌ <input onFocus={() => navigate('/search')} />

// Good: User explicitly triggers navigation
✅ <input onSubmit={() => navigate('/search')} />
```

#### 3.3 Input Assistance

**Labels for Form Fields**:
```tsx
// Always associate labels with inputs
<div>
  <Label htmlFor="email">Email</Label>
  <Input id="email" type="email" />
</div>

// Or use aria-label if visual label not desired
<Input type="search" aria-label="Search vault entries" />
```

**Error Identification**:
```tsx
<div>
  <Label htmlFor="password">Password</Label>
  <Input
    id="password"
    type="password"
    aria-invalid={!!errors.password}
    aria-describedby={errors.password ? "password-error" : undefined}
  />
  {errors.password && (
    <p id="password-error" className="text-sm text-destructive mt-1">
      {errors.password.message}
    </p>
  )}
</div>
```

### 4. Robust

#### 4.1 Compatible

**Valid HTML**:
- No duplicate IDs
- Proper nesting (buttons inside buttons, etc.)
- Close all tags

**ARIA Usage**:
```tsx
// Dialog
<div role="dialog" aria-labelledby="dialog-title" aria-describedby="dialog-desc">
  <h2 id="dialog-title">Create Entry</h2>
  <p id="dialog-desc">Fill out the form below</p>
</div>

// Button that controls something
<button aria-expanded={isOpen} aria-controls="menu">
  Menu
</button>
<div id="menu" hidden={!isOpen}>
  {/* menu items */}
</div>
```

## Testing Checklist

### Automated Testing

```bash
# Install axe-core for automated tests (future)
npm install --save-dev @axe-core/playwright

# Run in Playwright tests
test('should have no accessibility violations', async ({ page }) => {
  await page.goto('/dashboard');
  const results = await page.evaluate(() => {
    return window.axe.run();
  });
  expect(results.violations).toHaveLength(0);
});
```

### Manual Testing

**Keyboard Navigation**:
1. Tab through entire page
2. Verify focus indicators visible
3. Test Enter/Space on buttons
4. Test Escape on modals
5. Verify logical tab order

**Screen Reader** (NVDA/JAWS):
1. Navigate by headings (H key)
2. Navigate by landmarks (D key)
3. Read form fields and labels
4. Verify ARIA labels announced

**Color Contrast**:
1. Use browser DevTools
2. Check all text colors
3. Check button states (hover, focus, disabled)
4. Check links

**Zoom**:
1. Zoom to 200% (Ctrl/Cmd +)
2. Verify no horizontal scroll
3. Verify content reflows
4. Test at 400% zoom

### Testing Tools

**Browser Extensions**:
- axe DevTools
- WAVE Evaluation Tool
- Lighthouse (Chrome DevTools)

**Commands**:
```bash
# Lighthouse accessibility audit
npx lighthouse http://localhost:3000 --only-categories=accessibility --view
```

## Common Fixes for LucidData

### Missing Alt Text

```tsx
// Find images without alt
<img src="icon.svg" />

// Fix
<img src="icon.svg" alt="Settings icon" />
// Or if decorative
<img src="decoration.svg" alt="" />
```

### Missing Form Labels

```tsx
// Find inputs without labels
<Input placeholder="Email" />

// Fix
<Label htmlFor="email">Email</Label>
<Input id="email" placeholder="you@example.com" />
```

### Poor Focus Indicators

```tsx
// Find elements with outline:none
<button className="outline-none">

// Fix with focus-visible
<button className="focus-visible:ring-2 focus-visible:ring-offset-2">
```

### Color-Only Information

```tsx
// Bad: Color only indicates state
<Badge className="bg-green-500">Active</Badge>
<Badge className="bg-red-500">Revoked</Badge>

// Good: Text + color
<Badge variant="default">Active</Badge>
<Badge variant="destructive">Revoked</Badge>
// Or add icon
<Badge><CheckIcon /> Active</Badge>
```

### Non-Descriptive Link Text

```tsx
// Bad
<a href="/vault/123">Click here</a>

// Good
<a href="/vault/123">View passport entry</a>
```

## ARIA Attributes Quick Reference

```tsx
// Landmarks
<header role="banner">
<nav role="navigation">
<main role="main">
<aside role="complementary">
<footer role="contentinfo">

// Widgets
<div role="button" tabIndex={0}>
<div role="dialog" aria-modal="true">
<div role="alert">
<div role="status"> // For live regions

// States
aria-expanded={isOpen}
aria-selected={isSelected}
aria-checked={isChecked}
aria-disabled={isDisabled}
aria-hidden={isHidden}
aria-current="page"

// Properties
aria-label="Close dialog"
aria-labelledby="title-id"
aria-describedby="desc-id"
aria-controls="controlled-element-id"
aria-live="polite"  // For dynamic content
```

## Resources

**Standards**:
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)

**Testing Tools**:
- [axe DevTools](https://www.deque.com/axe/devtools/)
- [WAVE](https://wave.webaim.org/extension/)
- [Lighthouse](https://developers.google.com/web/tools/lighthouse)

**Learning**:
- [WebAIM](https://webaim.org/)
- [The A11Y Project](https://www.a11yproject.com/)

---

**For more information:**
- [Tailwind Patterns](tailwind-patterns.md)
- [shadcn Components](shadcn-components.md)
- [Main Skill Documentation](../SKILL.md)
