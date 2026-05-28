# Tailwind CSS Methodology

## Tailwind Architecture

### Principles

1. **Utility-first** - Compose styles from atomic classes
2. **Design tokens** - Centralize in tailwind.config.js
3. **Component extraction** - Abstract repeated patterns to components, not @apply
4. **JIT compilation** - Only ship used CSS

### Configuration

```js
// tailwind.config.js
export default {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#eff6ff",
          500: "#3b82f6",
          900: "#1e3a8a",
        },
      },
      spacing: {
        18: "4.5rem",
        88: "22rem",
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [
    require("@tailwindcss/forms"),
    require("@tailwindcss/typography"),
  ],
}
```

### Class Ordering (Concentric CSS)

Follow consistent order for readability:

```tsx
<div
  className="
    {/* 1. Layout/Position */}
    relative flex flex-col
    {/* 2. Box Model */}
    w-full max-w-md p-6 m-4
    {/* 3. Borders */}
    border border-gray-200 rounded-lg
    {/* 4. Background */}
    bg-white shadow-lg
    {/* 5. Typography */}
    text-gray-900 text-sm font-medium
    {/* 6. Effects/Other */}
    transition-all duration-200 hover:shadow-xl
  "
/>
```

**Auto-sort with Prettier plugin:**
```bash
npm install -D prettier-plugin-tailwindcss
```

### Component Patterns

**1. cn() helper (clsx + tailwind-merge):**
```ts
// lib/utils.ts
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

// Usage
<div className={cn(
  "base-styles",
  isActive && "active-styles",
  className
)} />
```

**2. Variant patterns:**
```tsx
const variants = {
  primary: "bg-blue-600 text-white hover:bg-blue-700",
  secondary: "bg-gray-200 text-gray-900 hover:bg-gray-300",
  ghost: "bg-transparent hover:bg-gray-100",
}

<button className={cn("px-4 py-2 rounded", variants[variant])} />
```

**3. Responsive design:**
```tsx
// Mobile-first approach
<div className="
  flex flex-col          {/* mobile: stack */}
  md:flex-row            {/* tablet+: row */}
  lg:justify-between     {/* desktop+: space between */}
" />
```

### Design Tokens

```js
// tailwind.config.js
theme: {
  extend: {
    // Semantic colors
    colors: {
      background: "hsl(var(--background))",
      foreground: "hsl(var(--foreground))",
      primary: {
        DEFAULT: "hsl(var(--primary))",
        foreground: "hsl(var(--primary-foreground))",
      },
    },
    // Semantic spacing
    spacing: {
      section: "6rem",
      container: "1280px",
    },
    // Semantic radii
    borderRadius: {
      card: "0.75rem",
      button: "0.5rem",
    },
  },
}
```

### @apply Usage (Sparingly)

```css
/* Only for truly repeated patterns that can't be components */
@layer components {
  .btn-base {
    @apply inline-flex items-center justify-center rounded-md
           font-medium transition-colors focus-visible:outline-none
           focus-visible:ring-2 disabled:pointer-events-none
           disabled:opacity-50;
  }
}

/* DON'T: Create utility aliases */
.text-big { @apply text-2xl; }  /* Bad! */
```

### Performance

1. **Purge unused CSS** - Automatic with content paths
2. **Avoid arbitrary values** - `w-[347px]` → use design tokens
3. **Limit @apply** - Increases CSS size
4. **Use CSS layers** - Proper specificity management

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  /* Reset, typography defaults */
}

@layer components {
  /* Reusable component classes */
}

@layer utilities {
  /* Custom utilities */
}
```

### Common Patterns

**Container:**
```tsx
<div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
```

**Card:**
```tsx
<div className="rounded-lg border bg-card p-6 shadow-sm">
```

**Stack:**
```tsx
<div className="flex flex-col gap-4">
```

**Center:**
```tsx
<div className="flex items-center justify-center">
```

**Truncate:**
```tsx
<p className="truncate">Long text...</p>
<p className="line-clamp-2">Multi-line truncate...</p>
```

### Anti-patterns

| Don't | Do Instead |
|-------|------------|
| `style={{ width: 100 }}` | `w-[100px]` or design token |
| Random hex in classes | Define in config |
| `@apply` for everything | Component extraction |
| Long unreadable class strings | Extract to component |
| Inline arbitrary colors | CSS variables |

### Dark Mode

```js
// tailwind.config.js
module.exports = {
  darkMode: "class", // or "media"
}
```

```tsx
<div className="bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100">
```

### Plugins

```js
plugins: [
  require("@tailwindcss/forms"),       // Form resets
  require("@tailwindcss/typography"),  // Prose styling
  require("@tailwindcss/aspect-ratio"), // Aspect ratios
  require("@tailwindcss/container-queries"), // Container queries
]
```

---

*Tailwind Architecture*
*Sources: [Tailwind Best Practices 2025](https://www.frontendtools.tech/blog/tailwind-css-best-practices-design-system-patterns), [Infinum Handbook](https://infinum.com/handbook/frontend/react/tailwind/best-practices)*
