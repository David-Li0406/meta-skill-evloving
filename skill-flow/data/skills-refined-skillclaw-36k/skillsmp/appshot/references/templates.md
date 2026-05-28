# Template Reference

## v2 Templates (Current)

Fixed layout modes with curated gradients:

| Use Case | Recommended Template |
|----------|----------------------|
| General purpose | `ocean-header` |
| Bold marketing | `sunset-footer` |
| Product-only | `clean-screenshot` |
| Clean + friendly | `pastel-header` |
| Dark + dramatic | `noir-footer` |
| Professional | `silver-header` |
| Playful brand | `tropical-header` |
| Business | `slate-footer` |
| Developer tools | `midnight-header` |

```
appshot_template with template: "ocean-header"
```

---

## v1 Templates (Legacy)

> v1 legacy templates remain as deprecated aliases. See `docs/layout-v2.md` for v2 rules and `docs/migration-v2.md` to upgrade.

8 professional templates for App Store screenshots.

## Template Selection Guide

| App Type | Recommended Template |
|----------|---------------------|
| Developer tools, CLI, OSS | `nerdy` |
| Business, productivity | `corporate` |
| Games, entertainment | `playful` |
| Lifestyle, premium | `elegant` |
| Finance, fintech | `bold` |
| Social, consumer | `modern` |
| Health, wellness | `minimal` |
| Custom backgrounds | `showcase` |

---

## modern

**Modern Vibrant** - Eye-catching gradient with floating device and clean captions

- **Category:** modern
- **Background:** Purple-pink diagonal gradient (`#667eea` → `#764ba2` → `#f093fb`)
- **Caption:** Above device, SF Pro Display, dark text (`#021d2f`)
- **Best for:** Consumer apps, social apps, general-purpose

```
appshot_template with template: "modern"
```

---

## minimal

**Minimal Clean** - Soft pastel background with elegant typography

- **Category:** minimal
- **Background:** Warm peach gradient (`#ffecd2` → `#fcb69f`)
- **Caption:** Above device, Helvetica Neue, dark text (`#1b2a3a`)
- **Best for:** Health apps, wellness, lifestyle

```
appshot_template with template: "minimal"
```

---

## bold

**Bold Impact** - Dark dramatic gradient with large device and overlay captions

- **Category:** bold
- **Background:** Dark purple diagonal gradient (`#0f0c29` → `#302b63` → `#24243e`)
- **Caption:** Overlay at bottom, SF Pro Display, white text
- **Best for:** Finance apps, security, premium features

```
appshot_template with template: "bold"
```

---

## nerdy

**Nerdy OSS** - Grid-lined midnight background with JetBrains Mono captions

- **Category:** bold
- **Background:** Auto-detect (uses background.png if present)
- **Caption:** Overlay at bottom, JetBrains Mono Bold, mint green (`#7CFFCB`)
- **Best for:** Developer tools, CLI apps, open source projects

```
appshot_template with template: "nerdy"
```

**Note:** Place a grid/terminal background image at `screenshots/iphone/background.png` for best results.

---

## elegant

**Elegant Professional** - Sophisticated monochrome with floating device

- **Category:** elegant
- **Background:** Silver gradient (`#8e9eab` → `#eef2f3`)
- **Caption:** Below device, Georgia serif, dark text (`#132235`)
- **Best for:** Luxury apps, premium services, professional tools

```
appshot_template with template: "elegant"
```

---

## showcase

**Showcase** - Feature your app with custom backgrounds

- **Category:** professional
- **Background:** Auto-detect with cyan fallback (`#4facfe` → `#00f2fe`)
- **Caption:** Above device, SF Pro Display, white text
- **Best for:** Apps with strong visual branding, custom marketing assets

```
appshot_template with template: "showcase"
```

**Tip:** Add your branded background to `screenshots/iphone/background.png`

---

## playful

**Playful Energy** - Bright, fun gradients perfect for games and entertainment apps

- **Category:** playful
- **Background:** Pink-yellow diagonal gradient (`#fa709a` → `#fee140` → `#fa709a`)
- **Caption:** Above device, SF Pro Display, white text
- **Best for:** Games, kids apps, entertainment, social

```
appshot_template with template: "playful"
```

---

## corporate

**Corporate Professional** - Clean, professional look for business and productivity apps

- **Category:** professional
- **Background:** Blue-teal gradient (`#0077BE` → `#33CCCC`)
- **Caption:** Above device, Helvetica, dark text (`#0f1e2d`)
- **Best for:** Business apps, B2B, enterprise, productivity

```
appshot_template with template: "corporate"
```

---

## Applying Templates

```
# Apply a template
appshot_template with template: "nerdy"

# Preview without applying
appshot_template with preview: "modern"

# List all templates
appshot_template with list: true
```

## Customizing After Template

Templates set a starting point. Customize further with:

```
# Change gradient
appshot_gradients with action: "apply", preset: "sunset"

# Adjust device positioning
appshot_config with device: "iphone", frameScale: 0.85, framePosition: 30

# Change caption position
appshot_config with device: "iphone", captionPosition: "below"
```
