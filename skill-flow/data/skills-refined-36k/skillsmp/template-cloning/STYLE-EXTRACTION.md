# Style Extraction Guide

How to extract design tokens from reference websites.

---

## Overview

When cloning a design, you need exact values for:
- **Colors** (background, text, accents, borders)
- **Typography** (fonts, weights, sizes, spacing)
- **Spacing** (padding, margins, gaps)
- **Patterns** (layouts, component styles)

---

## Method 1: Browser DevTools (Quick)

### Extract Colors

1. Open DevTools (F12)
2. Select element with color picker
3. Copy color value

```javascript
// Or use Console
getComputedStyle(document.body).backgroundColor
// Returns: "rgb(14, 14, 14)"

getComputedStyle(document.querySelector('.btn-primary')).backgroundColor
// Returns: "rgb(218, 197, 167)"
```

### Convert to HSL

CSS variables work best with HSL (enables opacity modifiers):

```
RGB: rgb(14, 14, 14)
HSL: 0 0% 5.5%

RGB: rgb(218, 197, 167)
HSL: 38 35% 75%
```

**Tools**:
- https://www.rapidtables.com/convert/color/rgb-to-hsl.html
- DevTools color picker (click on color, switch format)

### Extract Typography

```javascript
// Font family
getComputedStyle(document.querySelector('h1')).fontFamily
// "Satoshi, system-ui, sans-serif"

// Font weight
getComputedStyle(document.querySelector('h1')).fontWeight
// "300"

// Letter spacing
getComputedStyle(document.querySelector('h1')).letterSpacing
// "0.05em"

// Font size
getComputedStyle(document.querySelector('h1')).fontSize
// "48px"
```

### Extract Spacing

```javascript
// Section padding
getComputedStyle(document.querySelector('section')).padding
// "96px 0px"

// Container max-width
getComputedStyle(document.querySelector('.container')).maxWidth
// "1280px"

// Gap between items
getComputedStyle(document.querySelector('.grid')).gap
// "24px"
```

---

## Method 2: Playwright Script (Comprehensive)

For systematic extraction:

```python
# analyze_website.py
from playwright.sync_api import sync_playwright
import json

def extract_design_tokens(url: str, output_path: str = "design_tokens.json"):
    """Extract design tokens from a website."""

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url, wait_until="networkidle", timeout=30000)

        tokens = {}

        # Extract colors
        tokens["colors"] = page.evaluate('''() => {
            const body = document.body;
            const styles = getComputedStyle(body);
            return {
                background: styles.backgroundColor,
                text: styles.color,
            };
        }''')

        # Extract heading styles
        tokens["headings"] = page.evaluate('''() => {
            const h1 = document.querySelector('h1');
            if (!h1) return null;
            const styles = getComputedStyle(h1);
            return {
                fontFamily: styles.fontFamily,
                fontWeight: styles.fontWeight,
                fontSize: styles.fontSize,
                letterSpacing: styles.letterSpacing,
                color: styles.color,
            };
        }''')

        # Extract button styles
        tokens["buttons"] = page.evaluate('''() => {
            const btn = document.querySelector('button, .btn, [class*="button"]');
            if (!btn) return null;
            const styles = getComputedStyle(btn);
            return {
                backgroundColor: styles.backgroundColor,
                color: styles.color,
                padding: styles.padding,
                borderRadius: styles.borderRadius,
                fontWeight: styles.fontWeight,
            };
        }''')

        # Take screenshots
        page.screenshot(path="screenshot_full.png", full_page=True)

        # Hero section
        hero = page.query_selector('section, [class*="hero"], header')
        if hero:
            hero.screenshot(path="screenshot_hero.png")

        browser.close()

        # Save tokens
        with open(output_path, 'w') as f:
            json.dump(tokens, f, indent=2)

        return tokens

if __name__ == "__main__":
    import sys
    url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
    tokens = extract_design_tokens(url)
    print(json.dumps(tokens, indent=2))
```

**Usage**:
```bash
python analyze_website.py https://jousefmurad.com
```

---

## Method 3: What Fonts (Typography)

### Identify Fonts

1. Visit https://www.whatfont.com/ (browser extension)
2. Or use DevTools → Fonts tab (Chrome)
3. Or check `<link>` tags in page source

### Find Font Source

| Font Type | Where to Get |
|-----------|--------------|
| Google Fonts | fonts.google.com |
| Adobe Fonts | fonts.adobe.com |
| Fontshare | fontshare.com (free) |
| Custom | Check page source for font files |

### Font Loading Patterns

**Google Fonts**:
```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
```

**Fontshare**:
```html
<link href="https://api.fontshare.com/v2/css?f[]=satoshi@300,400,500,700&display=swap" rel="stylesheet">
```

**Self-hosted**:
```css
@font-face {
  font-family: 'CustomFont';
  src: url('/fonts/custom.woff2') format('woff2');
}
```

---

## Common Design Tokens

### Color Variables Template

```css
:root {
  /* Backgrounds */
  --background: /* main bg */;
  --foreground: /* main text */;

  /* Primary (accent) */
  --primary: /* brand color */;
  --primary-foreground: /* text on primary */;

  /* Cards/Sections */
  --card: /* card bg */;
  --card-foreground: /* card text */;

  /* Borders */
  --border: /* border color */;

  /* Muted (secondary text) */
  --muted: /* muted bg */;
  --muted-foreground: /* muted text */;
}
```

### Typography Variables Template

```javascript
// tailwind.config.js
fontFamily: {
  sans: ['Primary Font', 'system-ui', 'sans-serif'],
  display: ['Accent Font', 'serif'],
  mono: ['Mono Font', 'monospace'],
},
fontWeight: {
  light: '300',
  normal: '400',
  medium: '500',
  bold: '700',
},
letterSpacing: {
  tight: '-0.025em',
  normal: '0em',
  wide: '0.025em',
  elegant: '0.05em',
  widest: '0.1em',
},
```

### Spacing Variables Template

```javascript
// tailwind.config.js (if custom)
spacing: {
  section: '6rem',     // 96px - section padding
  container: '80rem',  // 1280px - max width
  gap: '1.5rem',       // 24px - grid gap
}
```

---

## Extraction Checklist

### Colors
- [ ] Background (body, sections)
- [ ] Text (headings, body, muted)
- [ ] Primary accent (buttons, links)
- [ ] Secondary accent (if any)
- [ ] Borders (cards, inputs)
- [ ] Hover states

### Typography
- [ ] Heading font family
- [ ] Body font family
- [ ] Font weights used (300, 400, 500, 700)
- [ ] Letter-spacing variants
- [ ] Font sizes (h1, h2, h3, body, small)

### Spacing
- [ ] Section padding (vertical)
- [ ] Container max-width
- [ ] Grid gaps
- [ ] Card padding
- [ ] Button padding

### Patterns
- [ ] Hero layout
- [ ] Card styles
- [ ] Button styles (default, hover)
- [ ] Navigation layout
- [ ] Footer layout

---

## Output Format

Document findings in markdown:

```markdown
# Design Tokens: {Site Name}

## Colors
| Role | Hex | HSL |
|------|-----|-----|
| Background | #0E0E0E | 0 0% 5.5% |
| Text | #E8E4DE | 38 25% 90% |
| Primary | #DAC5A7 | 38 35% 75% |
| Border | #2A2520 | 38 15% 18% |

## Typography
| Element | Font | Weight | Size | Spacing |
|---------|------|--------|------|---------|
| H1 | Satoshi | 300 | 48px | 0.05em |
| Body | Satoshi | 400 | 16px | normal |
| Accent | Georgia | 400 italic | varies | normal |

## Spacing
| Element | Value | Tailwind |
|---------|-------|----------|
| Section padding | 96px | py-24 |
| Container width | 1280px | max-w-7xl |
| Card gap | 24px | gap-6 |

## Screenshots
- [Full page](./screenshot_full.png)
- [Hero section](./screenshot_hero.png)
```
