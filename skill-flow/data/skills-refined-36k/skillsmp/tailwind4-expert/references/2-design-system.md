# 2. The @theme Block & Design Systems

**Impact: CRITICAL**

In Tailwind 4, the design system is defined using standard CSS variables inside the `@theme` block.

## 2.1 Defining Design Tokens

Tailwind 4 maps CSS variables starting with `--color-`, `--spacing-`, `--font-`, etc., directly to utility classes.

```css
@theme {
  /* Colors: creates text-brand, bg-brand, border-brand */
  --color-brand: #3b82f6;
  --color-brand-muted: #60a5fa;

  /* Spacing: creates p-18, m-18, h-18 */
  --spacing-18: 4.5rem;

  /* Fonts: creates font-display */
  --font-display: "Clash Display", "Inter", sans-serif;
  
  /* Radii: creates rounded-xl-plus */
  --radius-xl-plus: 1.25rem;
}
```

## 2.2 Overriding vs. Extending

By default, adding a variable to `@theme` **extends** the default theme. To **override** the entire category, use the `reference` keyword or clear the default block.

### To Extend (Standard):
```css
@theme {
  --color-custom: #ff00ff; /* Existing colors stay, 'custom' is added */
}
```

### To Reset/Override a Category:
If you want to *only* have your custom colors and remove the default Tailwind palette:
```css
@theme {
  --color-*: initial; /* Resets all default colors */
  --color-primary: #000;
  --color-secondary: #fff;
}
```

## 2.3 Using CSS Variables in the Browser

Since Tailwind 4 uses native CSS variables, you can now interact with your theme in real-time using JS or standard CSS without the `theme()` function.

**❌ Old Pattern (Avoid):**
```css
.my-card {
  background-color: theme('colors.brand');
}
```

**✅ New Pattern (Standard):**
```css
.my-card {
  background-color: var(--color-brand);
}
```

## 2.4 Dynamic Theme Variables

You can now use local CSS variables within utilities:

```tsx
function DynamicGrid({ count }) {
  return (
    <div 
      style={{ '--grid-count': count } as any}
      className="grid grid-cols-(--grid-count)"
    >
      {/* ... */}
    </div>
  )
}
```
Tailwind 4 automatically recognizes the `(--variable-name)` syntax for arbitrary values mapped to variables.
