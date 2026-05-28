# Shadows

Tenzir uses a layered shadow system with four sizes. Each shadow consists of two
layers to create a more realistic depth effect.

## Shadow Sizes

| Token       | Usage                 |
| ----------- | --------------------- |
| `shadow-l`  | Sidepanels and modals |
| `shadow-m`  | Popups                |
| `shadow-s`  | Tooltips and toasts   |
| `shadow-xs` | Subtle elevation      |

## Shadow Specifications

All shadows use `neutral-800` (`#0E1017`) as the base color with varying opacity.

### Shadow L (Large)

For sidepanels and modals - highest elevation.

```css
box-shadow:
  0px 20px 40px -16px #0e101733,
  0px 8px 16px -8px #0e101733;
```

| Layer | Y Offset | Blur | Spread | Color     | Opacity |
| ----- | -------- | ---- | ------ | --------- | ------- |
| 1     | 20px     | 40px | -16px  | `#0E1017` | 20%     |
| 2     | 8px      | 16px | -8px   | `#0E1017` | 20%     |

### Shadow M (Medium)

For popups - medium elevation.

```css
box-shadow:
  0px 10px 20px -8px #0e101733,
  0px 4px 8px -6px #0e101733;
```

| Layer | Y Offset | Blur | Spread | Color     | Opacity |
| ----- | -------- | ---- | ------ | --------- | ------- |
| 1     | 10px     | 20px | -8px   | `#0E1017` | 20%     |
| 2     | 4px      | 8px  | -6px   | `#0E1017` | 20%     |

### Shadow S (Small)

For tooltips and toasts - low elevation.

```css
box-shadow:
  0px 8px 16px -8px #0e101733,
  0px 3px 6px -3px #0e101733;
```

| Layer | Y Offset | Blur | Spread | Color     | Opacity |
| ----- | -------- | ---- | ------ | --------- | ------- |
| 1     | 8px      | 16px | -8px   | `#0E1017` | 20%     |
| 2     | 3px      | 6px  | -3px   | `#0E1017` | 20%     |

### Shadow XS (Extra Small)

For subtle elevation - minimal shadow.

```css
box-shadow:
  0px 8px 16px -8px #0e10171a,
  0px 3px 6px -3px #0e10171a;
```

| Layer | Y Offset | Blur | Spread | Color     | Opacity |
| ----- | -------- | ---- | ------ | --------- | ------- |
| 1     | 8px      | 16px | -8px   | `#0E1017` | 10%     |
| 2     | 3px      | 6px  | -3px   | `#0E1017` | 10%     |

## CSS Custom Properties

Use the `--tnz-` prefix for all custom properties:

```css
:root {
  --tnz-shadow-l: 0px 20px 40px -16px #0e101733, 0px 8px 16px -8px #0e101733;
  --tnz-shadow-m: 0px 10px 20px -8px #0e101733, 0px 4px 8px -6px #0e101733;
  --tnz-shadow-s: 0px 8px 16px -8px #0e101733, 0px 3px 6px -3px #0e101733;
  --tnz-shadow-xs: 0px 8px 16px -8px #0e10171a, 0px 3px 6px -3px #0e10171a;
}
```

**Usage example:**

```css
.card {
  box-shadow: var(--tnz-shadow-xs);
}

.card:hover {
  box-shadow: var(--tnz-shadow-s);
}

.modal {
  box-shadow: var(--tnz-shadow-l);
}
```

## Tailwind Configuration

```js
// tailwind.config.js
module.exports = {
  theme: {
    boxShadow: {
      l: "0px 20px 40px -16px #0E121733, 0px 8px 16px -8px #0E121733",
      m: "0px 10px 20px -8px #0E121733, 0px 4px 8px -6px #0E121733",
      s: "0px 8px 16px -8px #0E121733, 0px 3px 6px -3px #0E121733",
      xs: "0px 8px 16px -8px #0E12171A, 0px 3px 6px -3px #0E12171A",
      none: "none",
    },
  },
};
```

## Dim Overlays

Modals and sidepanels use a fullpage dim overlay to increase focus. The dim uses
`neutral-800` at varying opacities.

| Token                | Opacity | Usage         |
| -------------------- | ------- | ------------- |
| `neutral-800-dim-50` | 50%     | Full page dim |
| `neutral-800-dim-20` | 20%     | Medium dim    |
| `neutral-800-dim-8`  | 8%      | Subtle dim    |

See [colors.md](./colors.md#overlays) for the complete overlay specification.

## Usage Guidelines

1. **Match shadow to component type** - Use the designated shadow size for each
   component category
2. **Consistency** - Don't mix shadow sizes within similar component types
3. **Background** - Shadows are optimized for `neutral-50` (#FDFDFE) backgrounds
4. **Layering** - Both shadow layers are required for the correct depth effect
5. **Combine with dim** - Modals and sidepanels should use both `shadow-l` and a
   dim overlay (typically 50%) for proper elevation
