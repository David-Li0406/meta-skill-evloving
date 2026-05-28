# Hyperlinks

Hyperlinks use an underline style that changes on hover.

## Props

| Prop       | Values                         |
| ---------- | ------------------------------ |
| `fontSize` | `10px`, `12px`, `14px`, `16px` |
| `state`    | `default`, `hover`             |

## Specifications

| Size | Line Height |
| ---- | ----------- |
| 10px | 14px        |
| 12px | 16.5px      |
| 14px | 19px        |
| 16px | 22px        |

## State Specifications

| State   | Text Color    | Underline Color |
| ------- | ------------- | --------------- |
| Default | `neutral-800` | `neutral-300`   |
| Hover   | `neutral-800` | `neutral-400`   |

## CSS Implementation

```css
/* Hyperlink Default */
.hyperlink {
  color: var(--neutral-800);
  text-decoration: none;
  border-bottom: 1px solid var(--neutral-300);
}

.hyperlink:hover {
  border-bottom-color: var(--neutral-400);
}
```

## CSS Custom Properties

```css
:root {
  --hyperlink-underline-default: var(--neutral-300);
  --hyperlink-underline-hover: var(--neutral-400);
}
```

## Usage Guidelines

1. **Use consistent sizing** - Match the hyperlink font size to the surrounding text
2. **Underline style** - Use bottom border (not text-decoration) for consistent styling
3. **Color changes on hover** - Only the underline color changes, text remains `neutral-800`
4. **Accessibility** - Ensure sufficient contrast between link and surrounding text
