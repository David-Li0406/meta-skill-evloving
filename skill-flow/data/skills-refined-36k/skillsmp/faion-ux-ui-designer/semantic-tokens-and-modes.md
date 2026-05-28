# Semantic Tokens and Modes

### Problem

Tokens need to adapt to different contexts (themes, platforms, breakpoints).

### Solution: Token Collections with Modes

**Mode Types:**

| Collection | Modes Example |
|------------|---------------|
| Color | Light, Dark, High contrast |
| Typography | Desktop, Mobile, Compact |
| Density | Default, Compact, Comfortable |
| Brand | Brand A, Brand B, White-label |

**Figma Variables Implementation:**
```
Collection: Colors
  Mode: Light
    surface.primary → #FFFFFF
    text.primary → #1A1A1A
  Mode: Dark
    surface.primary → #1A1A1A
    text.primary → #FFFFFF
```

**Multi-platform Tokens:**
```json
{
  "spacing": {
    "button": {
      "padding": {
        "value": "16px",
        "ios": "14px",
        "android": "12px"
      }
    }
  }
}
```
