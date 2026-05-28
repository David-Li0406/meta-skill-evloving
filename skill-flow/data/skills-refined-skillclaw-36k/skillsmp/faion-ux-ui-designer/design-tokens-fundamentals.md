# Design Tokens Fundamentals

### What Are Design Tokens?

Design tokens are named values that store design decisions (colors, spacing, typography) in a platform-agnostic format. They bridge design and development.

**Token Types:**

| Type | Examples | Use Case |
|------|----------|----------|
| Global/Primitive | `#3B82F6`, `16px` | Raw values |
| Semantic/Alias | `color.primary`, `spacing.md` | Meaningful names |
| Component | `button.background`, `card.padding` | Component-specific |

### Token Structure

```json
{
  "color": {
    "primary": {
      "value": "#3B82F6",
      "type": "color",
      "description": "Primary brand color"
    },
    "text": {
      "default": { "value": "{color.gray.900}" },
      "muted": { "value": "{color.gray.600}" }
    }
  },
  "spacing": {
    "xs": { "value": "4px" },
    "sm": { "value": "8px" },
    "md": { "value": "16px" },
    "lg": { "value": "24px" },
    "xl": { "value": "32px" }
  }
}
```

### Benefits

| Benefit | Description |
|---------|-------------|
| Consistency | Same values across platforms |
| Scalability | Update once, apply everywhere |
| Collaboration | Shared language designers/devs |
| Theming | Easy mode switching (dark/light) |
| Maintenance | Single source of truth |
