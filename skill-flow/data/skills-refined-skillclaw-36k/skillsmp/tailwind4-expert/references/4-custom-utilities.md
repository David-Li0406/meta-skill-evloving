# 4. Custom Utilities & @utility

**Impact: MEDIUM**

Tailwind 4 replaces the old `@layer utilities` pattern with the much more powerful `@utility` directive.

## 4.1 The `@utility` Directive

The `@utility` directive registers a custom utility class with the Tailwind engine, ensuring it's treated exactly like a built-in utility (including support for variants like `hover:`, `md:`, and `@md:`).

**Incorrect (v3 style):**
```css
@layer utilities {
  .neon-text {
    color: #00f0ff;
    text-shadow: 0 0 5px #00f0ff;
  }
}
```

**Correct (v4 style):**
```css
@utility neon-text {
  color: #00f0ff;
  text-shadow: 0 0 5px #00f0ff;
}
```

## 4.2 Functional Utilities

You can define utilities that accept values, similar to how `bg-[color]` works.

```css
@utility mask-size-* {
  mask-size: --value();
}
```
The `--value()` function automatically extracts the value from the utility name (e.g., `mask-size-cover` or `mask-size-[50%]`).

## 4.3 Avoiding Arbitrary Value Bloat

While Tailwind 4 supports arbitrary values via `[value]`, the "Oxide" engine encourages using local theme variables for cleaner templates.

**Avoid:**
```tsx
<div className="bg-[#ff00ea] p-[4.75rem] border-[#00ff00]">
```

**Prefer (Local Theme):**
```css
/* In your CSS */
@theme {
  --color-hot-pink: #ff00ea;
  --spacing-extra: 4.75rem;
}

/* In your Template */
<div className="bg-hot-pink p-extra border-green-500">
```

## 4.4 Composition and `@apply`

While `@apply` is still supported, Tailwind 4 encourages using standard CSS variables or the `@utility` directive to keep the CSS readable and compatible with Lightning CSS optimizations.

**Pro Tip**: If you find yourself using `@apply` heavily inside many components, consider if you should be creating a reusable React component instead of a "utility" that is actually a "component style".
