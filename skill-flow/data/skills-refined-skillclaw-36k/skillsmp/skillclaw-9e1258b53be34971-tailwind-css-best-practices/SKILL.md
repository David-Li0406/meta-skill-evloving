---
name: tailwind-css-best-practices
description: Use this skill when styling with Tailwind CSS, especially for managing class names, dynamic styles, and avoiding common pitfalls.
---

# Tailwind CSS Best Practices

This document outlines best practices for using Tailwind CSS, focusing on class usage, dynamic styles, and critical rules to follow.

## Styling Decision Tree

```
Tailwind class exists?   → className="..."
Dynamic value?          → style={{ width: `${x}%` }}
Conditional styles?     → cn("base", condition && "variant")
Static only?            → className="..." (no cn() needed)
Library can't use class?→ style prop with var() constants
```

## Critical Rules

### Never Use var() in className

```typescript
// ❌ NEVER: var() in className
<div className="bg-[var(--color-primary)]" />
<div className="text-[var(--text-color)]" />

// ✅ ALWAYS: Use Tailwind semantic classes
<div className="bg-primary" />
<div className="text-slate-400" />
```

### Never Use Hex Colors

```typescript
// ❌ NEVER: Hex colors in className
<p className="text-[#ffffff]" />
<div className="bg-[#1e293b]" />

// ✅ ALWAYS: Use Tailwind color classes
<p className="text-white" />
<div className="bg-slate-800" />
```

## The cn() Utility

```typescript
import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

### When to Use cn()

```typescript
// ✅ Conditional classes
<div className={cn("base-class", isActive && "active-class")} />

// ✅ Merging with potential conflicts
<button className={cn("px-4 py-2", className)} />  // className might override

// ✅ Multiple conditions
<div className={cn(
  "rounded-lg border",
  variant === "primary" && "bg-blue-500 text-white",
  variant === "secondary" && "bg-gray-200 text-gray-800",
  disabled && "opacity-50 cursor-not-allowed"
)} />
```

### When NOT to Use cn()

```typescript
// ❌ Static classes - unnecessary wrapper
<div className={cn("flex items-center gap-2")} />

// ✅ Just use className directly
<div className="flex items-center gap-2" />
```

## Style Constants for Libraries

When libraries don't accept className (like Recharts):

```typescript
// ✅ Constants with var() - ONLY for library props
const CHART_COLORS = {
  primary: "var(--color-primary)",
  secondary: "var(--color-secondary)",
  text: "var(--color-text)",
  gridLine: "var(--color-border)",
};

// Usage with Recharts (can't use className)
<XAxis tick={{ fill: CHART_COLORS.text }} />
<CartesianGrid stroke={CHART_COLORS.gridLine} />
```

## Dynamic Values

```typescript
// Example of dynamic values
```