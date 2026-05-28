---
name: css
description: Modern CSS features. Use for @function, style queries, range comparisons, if(), relative colors. (project)
---

# Modern CSS (Chrome 139+)

## @function Rule

Custom functions that accept arguments and return computed values.

- **Syntax**: `@function --name(--param) { result: value; }`
- **Calling**: `--function-name(args)` (double-dash prefix)
- **Default params**: `--param: default-value`

### Patterns

- **Negation**: flip sign of numeric values → `examples/function-negate.css`
- **Opacity**: oklch relative color → `examples/function-opacity.css`
- **Fluid scaling**: clamp with container units → `examples/function-fluid-type.css`
- **Responsive layout**: media query branching → `examples/function-layout.css`

## Style Queries with Range Syntax

Compare numeric custom property values using operators.

- **Operators**: `>`, `<`, `>=`, `<=`
- **Requirement**: both sides must be same numeric type (length, percentage, angle, time)

### Patterns

- **Container style query**: `@container style(--prop > value)` → `examples/style-query-range.css`
- **if() function**: inline conditionals → `examples/if-conditional.css`
- **Data attributes**: `attr(data-*, type(<type>))` with range queries → `examples/style-query-attr.css`

## Anchor Positioning

Position elements relative to named anchors.

- **anchor-name**: name an element as target
- **position-anchor**: attach to named anchor
- **anchor()**: reference anchor coordinates
- **position-area**: logical placement (top, bottom, etc.)

### Patterns

- **Follow hover**: dynamic anchor switching → `examples/anchor-follow.css`
- **Fallback detection**: style based on flip state → `examples/anchor-fallback.css`

## Scroll State Queries

Style based on scroll direction. Requires `container-type: scroll-state`.

- **Values**: `top`, `bottom`, `left`, `right`, `block-start`, `inline-end`, `none`

### Patterns

- **Hide on scroll**: header slides away on scroll down → `examples/scroll-state.css`

## Tree Counting

Index-based styling without hard-coded values.

- **sibling-index()**: 1-based position among siblings
- **sibling-count()**: total number of siblings

### Patterns

- **Staggered animation**: delay based on position → `examples/sibling-index.css`

## Customizable Select

Style native `<select>` with full CSS control.

- **appearance: base-select**: opt into new rendering
- **::picker(select)**: style dropdown container
- **<selectedcontent>**: reflect selected option

## Scroll Markers

CSS-only carousel navigation.

- **::scroll-button(direction)**: prev/next buttons
- **::scroll-marker**: per-item indicators
- **:target-current**: active marker state

## type() Function

Specify CSS data types for `attr()` and `@function` parameters.

- **Types**: `<angle>`, `<color>`, `<integer>`, `<length>`, `<length-percentage>`, `<number>`, `<percentage>`, `<string>`, `<time>`, `<url>`, `*`
- **Combinators**: `+` (space-separated), `#` (comma-separated), `|` (either)

### Patterns

- **Typed attr()**: read data attributes as CSS values → `examples/style-query-attr.css`
- **Typed @function params**: enforce parameter types → `examples/type-function.css`

## Relative Color Syntax

Modify color channels using `oklch`.

```css
oklch(from var(--color) l c h / 50%)          /* opacity */
oklch(from var(--color) l c calc(h + 30))     /* shift hue */
oklch(from var(--color) calc(l * 1.2) c h)    /* lighten */
```
