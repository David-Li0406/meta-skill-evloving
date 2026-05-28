# Tailwind 4.1+ — Patterns

## Anti-Patterns

| Avoid | Use |
|-------|-----|
| `tailwind.config.js` | `@theme` in CSS |
| `@tailwind base/utilities` | `@import "tailwindcss"` |
| `@apply` | `@utility` or raw CSS |
| `dark:bg-zinc-900` | Semantic `bg-background` |
| `group` class | `in-*` variant |
| Viewport for component layout | `@container` queries |
| `@utility` for single property | `@theme` namespace |

## Built-in Utilities — Don't Redefine

Tailwind 4 ships with these. Never redefine in `@theme`:

- `rounded-*` (sm, md, lg, xl, 2xl, 3xl, full)
- `shadow-*` (xs, sm, md, lg, xl, 2xl)
- `blur-*` (sm, md, lg, xl, 2xl, 3xl)
- `ease-*` (linear, in, out, in-out)
- `duration-*` (75, 100, 150, 200, 300, 500, 700, 1000)

Only use `@theme` for **custom** tokens.

## Dark Mode

```css
@custom-variant dark (&:where(.dark, .dark *));

:root { --primary: var(--color-blue-600); }
.dark { --primary: var(--color-blue-400); }

@theme inline { --color-primary: var(--primary); }
```

Usage: `bg-primary` — no `dark:` needed.

## Palette Overrides

```css
body:has(.claude-code) { --primary: var(--color-orange-600); }
.dark body:has(.claude-code) { --primary: var(--color-orange-400); }
```

## @theme vs :root vs @theme inline

| Directive | Purpose |
|-----------|---------|
| `@theme` | Creates utilities, static values |
| `:root` / `.dark` | CSS variables, cascadable, no utilities |
| `@theme inline` | Maps `:root` vars to utilities, runtime resolution |

## Entry Animation

```css
starting:opacity-0 starting:translate-y-2 transition-[opacity,transform]
```

## Gradients

`bg-linear-*` not `bg-gradient-*`

## Text Shadows

`text-shadow-lg` `text-shadow-primary/30`

Sizes: `2xs` `xs` `sm` `md` `lg`

## Masks

`mask-b-from-50%` `mask-t-from-20%` `mask-radial-from-70% mask-radial-at-center`

## Popover Animation

`transition-discrete open:opacity-100 starting:open:opacity-0`

## Field Sizing

`field-sizing-content` — auto-resize textarea

## Theme Functions

```css
--color-overlay: --alpha(var(--background) / 80%);
padding: --spacing(4) --spacing(6);
```
