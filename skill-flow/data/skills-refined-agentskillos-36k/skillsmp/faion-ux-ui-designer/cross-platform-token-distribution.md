# Cross-Platform Token Distribution

### Problem

Design tokens must work across iOS, Android, Web.

### Solution: Token Transformation Pipeline

**Tools:**

| Tool | Function |
|------|----------|
| Style Dictionary | Token transformation |
| Tokens Studio | Figma plugin + sync |
| Supernova | Design system platform |
| Specify | Token distribution |

**Pipeline:**
```
Figma Tokens
    ↓
Token Studio export (JSON)
    ↓
Style Dictionary transform
    ↓
Platform outputs:
  → CSS variables
  → SCSS maps
  → iOS Swift
  → Android XML
  → React Native
```

**Output Examples:**

```css
/* CSS */
:root {
  --color-primary: #3B82F6;
  --spacing-md: 16px;
}
```

```swift
// iOS
struct Colors {
  static let primary = UIColor(hex: "#3B82F6")
}
```

```xml
<!-- Android -->
<color name="primary">#3B82F6</color>
<dimen name="spacing_md">16dp</dimen>
```
