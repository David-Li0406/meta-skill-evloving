# Tailwind 4.1+ — Utilities

## @theme Namespaces → Auto-Generated Utilities

| Namespace | Generates |
|-----------|-----------|
| `--color-*` | `bg-*`, `text-*`, `border-*`, `fill-*` |
| `--font-*` | `font-*` |
| `--spacing-*` | `p-*`, `m-*`, `gap-*`, `w-*`, `h-*` |
| `--radius-*` | `rounded-*` |
| `--shadow-*` | `shadow-*` |
| `--ease-*` | `ease-*` |
| `--animate-*` | `animate-*` (keyframes inside @theme) |
| `--breakpoint-*` | `sm:`, `md:`, `3xl:` |
| `--container-*` | `@sm:`, `@md:` |

**Prefer @theme** when namespace exists. Use `@utility` only for multi-property compositions.

## @theme vs @utility

| Need | Use |
|------|-----|
| Animation | `--animate-*` in `@theme` |
| Color | `--color-*` in `@theme` |
| Multi-property | `@utility` with `--value()` |

## @utility

Wildcard `*` at end of name. Don't use for component shortcuts (use React).

## --value() Modes

| Mode | Syntax | Matches |
|------|--------|---------|
| Theme | `--value(--namespace-*)` | `tab-2` → `--tab-size-2` |
| Bare | `--value(integer)` | `indent-4` → `4` |
| Literal | `--value("a", "b")` | `wrap-balance` → `balance` |
| Arbitrary | `--value([length])` | `perspective-[30rem]` → `30rem` |

Combine left-to-right: `--value(--repeat-*, integer, "infinite")`

→ See `examples/utility-value-modes.css`

## --modifier()

Slash syntax: `utility-value/modifier`

→ See `examples/utility-modifiers.css`

## Examples

| Pattern | File |
|---------|------|
| Functional + OKLCH | `examples/utility-functional.css` |
| Negative pairs | `examples/utility-negative.css` |
| Nesting (pseudo, states) | `examples/utility-nesting.css` |
| Fractions (ratio type) | `examples/utility-fractions.css` |
| Dark mode (@theme inline) | `examples/theme-dark-mode.css` |

## @layer / @source

`@layer base` for defaults. `@layer components` — escape hatch only.

`@source "../path"` to include, `@source not "./path"` to exclude.
