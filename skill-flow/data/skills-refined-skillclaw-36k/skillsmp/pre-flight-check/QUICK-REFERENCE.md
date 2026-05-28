# Pre-Flight Quick Reference Card

One-page reference for common pre-flight checks.

## Before Writing ANY File

```
1. What exists already? (Glob, Read)
2. What patterns apply? (Check skills)
3. What validators will run? (hooks)
4. What could go wrong? (red flags)
```

## HTML Quick Check

| Requirement | How to Verify |
|-------------|---------------|
| XHTML syntax | Self-closing voids, lowercase, quoted attrs |
| Semantic structure | `<header>`, `<main>`, `<footer>` present |
| Single `<h1>` | Only one per page |
| Accessibility | Labels, alt text, ARIA |
| Metadata | Title, description, Open Graph |

## CSS Quick Check

| Requirement | How to Verify |
|-------------|---------------|
| Layer declared | `@layer` at top |
| Tokens used | Custom properties for values |
| Nesting depth | Max 3 levels |
| No classes for state | Use `data-*` attributes |
| No duplicate properties | Each property once per block |

## JavaScript Quick Check

| Requirement | How to Verify |
|-------------|---------------|
| `const`/`let` only | No `var` |
| Named exports | No `export default` |
| JSDoc present | Classes and public methods |
| Cleanup defined | `disconnectedCallback` cleans up |
| Complexity < 10 | Simple, focused functions |

## Common Patterns by Task

### Adding a Page
```
1. Check .claude/patterns/pages/ for similar page type
2. Use patterns skill for structure
3. Apply metadata profile
4. Include skip link and landmarks
```

### Adding a Form
```
1. Use <form-field> pattern
2. Every input needs <label>
3. Add <output> for errors
4. Include autocomplete attributes
```

### Adding an Image
```
1. Generate WebP/AVIF with optimize:images
2. Use <picture> for multiple formats
3. Add loading="lazy" for below-fold
4. Include width/height attributes
```

### Adding a Component
```
1. Create component directory structure
2. Separate template, styles, i18n
3. Use Web Component pattern
4. Export with named export
```

### Adding Interactivity
```
1. Can CSS do this? (progressive-enhancement)
2. If not, use Web Component
3. Follow functional core pattern
4. Add cleanup in disconnectedCallback
```

## Red Flag Quick Reference

| If you think... | Instead do... |
|-----------------|---------------|
| "Use a div" | Find the semantic element |
| "Add a class" | Use data-* attribute |
| "Inline style" | Add to CSS file |
| "Skip validation" | Fix the issue |
| "Copy paste this" | Check for existing pattern |

## Validation Commands

```bash
npm run lint          # HTML
npm run lint:css      # CSS
npm run lint:js       # JavaScript
npm run lint:all      # Everything
npm run a11y          # Accessibility
```
