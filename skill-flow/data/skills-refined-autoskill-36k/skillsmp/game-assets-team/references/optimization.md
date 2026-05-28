# Asset Optimization Reference

## Image Compression Pipeline

### Recommended Tools

| Tool | Use Case | Command/Usage |
|------|----------|---------------|
| Squoosh (web) | One-off optimization | squoosh.app |
| sharp (Node) | Build pipeline | `npm install sharp` |
| imagemin | Batch processing | CI/CD integration |
| SVGO | SVG optimization | `npx svgo input.svg` |

### Format Selection Guide

```
Decision Tree:

Is it a simple icon/logo?
├─ Yes → SVG (infinite scale, tiny size)
└─ No → Continue...

Does it need transparency?
├─ Yes → PNG-24 or WebP
└─ No → Continue...

Is it a photograph or complex gradient?
├─ Yes → WebP (lossy) or AVIF
└─ No → PNG-8 or WebP (lossless)

Is animation required?
├─ Yes → Lottie (vector) or WebP (raster)
└─ No → Static format above
```

### Compression Settings

**WebP (Recommended Default):**
```javascript
// sharp configuration
sharp(input)
  .webp({
    quality: 80,        // 75-85 for game assets
    effort: 6,          // compression effort (0-6)
    smartSubsample: true
  })
  .toFile(output);
```

**PNG (When Transparency Needed):**
```javascript
sharp(input)
  .png({
    compressionLevel: 9,
    palette: true,      // Enable for <256 colors
    quality: 80,
    effort: 10
  })
  .toFile(output);
```

**AVIF (Best Compression, Limited Support):**
```javascript
sharp(input)
  .avif({
    quality: 65,        // AVIF is efficient, can go lower
    effort: 7
  })
  .toFile(output);
```

### Sprite Sheet Generation

**TexturePacker Settings:**
```json
{
  "algorithm": "MaxRects",
  "maxWidth": 2048,
  "maxHeight": 2048,
  "padding": 2,
  "extrude": 1,
  "allowRotation": false,
  "trimMode": "Trim",
  "outputFormat": "json-array"
}
```

**Manual Sprite Sheet Layout:**
```
┌────────────────────────────────┐
│ idle_0 │ idle_1 │ idle_2 │ ... │  ← Row per animation
├────────┼────────┼────────┼─────┤
│ walk_0 │ walk_1 │ walk_2 │ ... │
├────────┼────────┼────────┼─────┤
│ action_0│action_1│action_2│... │
└────────────────────────────────┘
   64px    64px     64px
```

## Performance Budgets

### Per-Screen Budget

| Screen Type | Total Assets | Max Load Time |
|-------------|--------------|---------------|
| Main Menu | 500KB | <1s |
| Game Board | 1MB | <2s |
| Card Table | 800KB | <1.5s |
| Shop/Store | 600KB | <1s |

### Critical Path Assets

Load immediately (above the fold):
- UI chrome/frame
- Primary game board
- Essential icons

Lazy load:
- Backgrounds beyond viewport
- Animation variations
- Audio assets
- Shop item previews

## Resolution Strategy

### Device Pixel Ratio Handling

```css
/* CSS approach */
.game-bg {
  background-image: url('bg-1x.webp');
}

@media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {
  .game-bg {
    background-image: url('bg-2x.webp');
  }
}
```

```html
<!-- HTML approach -->
<picture>
  <source srcset="hero-2x.avif" type="image/avif" media="(min-resolution: 2dppx)">
  <source srcset="hero-1x.avif" type="image/avif">
  <source srcset="hero-2x.webp" type="image/webp" media="(min-resolution: 2dppx)">
  <source srcset="hero-1x.webp" type="image/webp">
  <img src="hero-1x.png" alt="Hero image">
</picture>
```

### Asset Naming Convention

```
[category]_[name]_[variant]_[size].[ext]

Examples:
icon_tulip_red_64.png
sprite_simulin_harvester_idle_256.webp
bg_field_sunset_1x.avif
card_ace_hearts_180x252.png
```

## Build Pipeline Integration

### Vite Plugin Example

```javascript
// vite.config.ts
import { imagetools } from 'vite-imagetools';

export default {
  plugins: [
    imagetools({
      defaultDirectives: new URLSearchParams({
        format: 'webp',
        quality: '80',
        w: '1920'
      })
    })
  ]
}
```

### Usage in Code

```tsx
// Automatic optimization via import
import heroImage from './hero.png?w=1920&format=webp';
import heroImage2x from './hero.png?w=3840&format=webp';
```
