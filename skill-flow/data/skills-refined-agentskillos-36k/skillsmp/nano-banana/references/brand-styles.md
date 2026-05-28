# Brand Styles Reference

This file contains brand color palettes and style guidelines for generating on-brand imagery.

---

## TrendLife

Corporate brand identity for Trend Micro's "TrendLife" product line.

### Color Palette

**Primary Colors:**

| Color Name | Hex Code | Usage |
|------------|----------|-------|
| **Trend Red** | `#D71920` | Primary brand color, accents |
| **Guardian Red** | `#6F0000` | Supporting elements, intensity |
| Trend Red 80% | `#DE543B` | Tinted variations |
| Trend Red 40% | `#EDA389` | Light tinted variations |
| Black | `#000000` | Strong contrast |
| White | `#FFFFFF` | Clean backgrounds |

**Grays (Neutral Palette):**

| Gray Level | Hex Code |
|------------|----------|
| Dark Gray | `#57585B` |
| Medium Gray | `#808285` |
| Light Gray | `#E7E6E6` |

### Prompt Template

When `style: "trendlife"` is detected, append this to the user's prompt:

```
Use TrendLife brand colors for Trend Micro presentations:
- IMPORTANT: Title text and all headings MUST be in Trend Red (#D71920)
- Primary accents and highlights: Trend Red (#D71920)
- Guardian Red (#6F0000) for supporting elements and depth
- Neutral palette: Dark gray (#57585B), medium gray (#808285), light gray (#E7E6E6)
- Black (#000000) for body text, white (#FFFFFF) for backgrounds
Keep the design clean, professional, and suitable for corporate presentations.
DO NOT include any logos or brand text - these will be added separately.
```

### Logo Configuration

**Logo Asset:**
- Path: `assets/logos/trendlife-logo.png`
- Source: Extracted and cropped from TrendLife PowerPoint template (image3.png)
- Format: PNG with transparency (RGBA)
- Dimensions: 4768×1490 pixels (3.2:1 aspect ratio)
- Size: Pre-cropped to match PowerPoint's display aspect ratio
- Note: Original image3.png (12532×1490) was cropped to remove tagline

**Logo Positioning (All Layouts):**

**Based on actual TrendLife PowerPoint template master slide configuration:**

| Property | Value |
|----------|-------|
| Position | Bottom-right corner (fixed for all layouts) |
| Size | 17.2% of slide width (330px at 1920×1080) |
| Padding | 14px from right edge, 1px from bottom |
| Opacity | 100% |

**Position Calculations (16:9, 1920×1080 reference):**
- Logo width: `slide_width × 0.172 = 330px`
- Logo position: `x = slide_width - logo_width - 14px = 1576px`
- Logo position: `y = slide_height - logo_height - 1px = 976px`

**Note:** Unlike the original template draft assumptions, all slide layouts (title, content, divider, end) use the **same logo size and position** in the master slide.

### Style Guidelines

1. **Color Usage:**
   - Trend Red (#D71920) as primary accent
   - Guardian Red (#6F0000) for intensity
   - Neutral grays for backgrounds and structure
   - High contrast with black/white

2. **Design Principles:**
   - Clean, professional corporate aesthetic
   - Minimal text, maximum visual impact
   - Suitable for executive presentations

3. **Logo Treatment:**
   - Never distort or skew logo
   - Maintain minimum clear space around logo
   - Always use transparent PNG with full color
   - Logo automatically overlaid after AI generation

### Style Trigger Keywords

**Explicit:**
- `style: "trendlife"`

**Natural Language:**
- "trendlife style"
- "use trendlife"
- "trendlife brand"
- "trendlife presentation"

---

## Adding New Brand Styles

To add new brands, follow this structure:

```markdown
## [Brand Name]

### Color Palette
[Primary, secondary, accent colors with hex codes]

### Style Guidelines
[Design principles, usage rules]

### Prompt Template
[Text to append when style is detected]
```
