# Islands Theme

## Source File

```text
platform/platform-impl/src/com/intellij/openapi/application/impl/islands/IslandsUICustomization.kt
```

## Themeable Properties

| Property                   | Description                      | Default |
|----------------------------|----------------------------------|---------|
| `Islands`                  | Enable Islands mode              | `1`     |
| `Island.arc`               | Corner radius                    | `10`    |
| `Island.borderWidth`       | Border width around islands      | `4`     |
| `Island.borderColor`       | Border color                     | -       |
| `Island.inactiveAlpha`     | Inactive window transparency     | -       |
| `Island.Editor.border`     | Insets around editor island      | -       |
| `Island.ToolWindow.border` | Insets around tool window island | -       |

## Theme JSON Integration

```json
{
  "parentTheme": "Islands Dark",
  "ui": {
    "*": {
      "Island.arc": 20,
      "Island.borderWidth": 5
    }
  }
}
```

## Critical: Parent Theme

Set `"parentTheme": "Islands Dark"` or `"Islands Light"` to inherit Islands styling.

## Transparent Borders

Preserve Islands aesthetic by using transparent borders:

```json
"StatusBar.borderColor": "#00000000",
"ToolWindow.Stripe.borderColor": "#00000000",
"MainToolbar.borderColor": "#00000000"
```

## Search Commands

```bash
# Find all Island properties
grep -rn "Island\." ~/Projects/github.com/JetBrains/intellij-community/platform/platform-impl/src/com/intellij/openapi/application/impl/islands --include="*.kt"

# Find Islands usage in themes
grep -r "Island\." ~/Projects/github.com/JetBrains/intellij-community/platform/platform-resources/src/themes --include="*.json"
```
