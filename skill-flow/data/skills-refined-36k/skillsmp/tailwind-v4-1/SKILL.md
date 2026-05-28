---
name: tailwind-v4
description: Tailwind v4 custom color detection and usage rules.
---

# Tailwind v4 Custom Color Detection

## Protocol

When using Tailwind CSS v4, check for custom theme configuration first:

1. Read `src/index.css` (or main CSS entry point).
2. Look for the `@theme { ... }` directive with color variables.
3. If found, use the defined semantic names (e.g., `bg-brand`, `text-primary`).
4. If not found, use Tailwind default color classes (e.g., `bg-blue-500`).
5. Never hardcode hex colors in class names (e.g., `bg-[#3b82f6]`).

## Detection

- Tailwind v4 if `package.json` has `tailwindcss: ^4.x`.
- Load this skill when working with React/Angular/Tailwind projects.

## Documentation Access

When you need to verify v4 `@theme` syntax, CSS variable usage, or migration breaking changes:

1. **Primary (Context7)**: `/websites/tailwindcss`
2. **Fallback**: <https://tailwindcss.com/docs>

**Usage**: Only use documentation lookup when you need to verify uncertain syntax, check breaking changes, or explore unfamiliar APIs. Apply this skill's established rules directly for routine tasks.
