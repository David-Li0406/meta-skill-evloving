# presetOnmax Configuration

## Installation

```bash
pnpm add -D unocss-preset-onmax
```

## Basic Config

```ts
// uno.config.ts
import { defineConfig } from 'unocss'
import { presetOnmax } from 'unocss-preset-onmax'

export default defineConfig({
  presets: [
    presetOnmax(),
  ],
})
```

## Included Sub-Presets

| Preset | Purpose |
|--------|---------|
| `presetWind4` | Tailwind v4 compatibility (attributifyPseudo) |
| `presetAttributify` | HTML attribute-based utilities |
| `presetScalePx` | 1px base unit (1rem = 4px) |
| `presetFluidSizing` | Responsive clamp() utilities |
| `presetCSSVar` | CSS variable generation |
| `presetEasingGradient` | Advanced gradient functions |
| `presetUnoVue` | Vue/Reka UI integration |
| `transformerDirectives` | @apply support |

## Configuration Options

```ts
presetOnmax({
  baseFontSize: '0.0625rem', // 1px base (default)
  presets: {
    wind4: { attributifyPseudo: true }, // or false to disable
    attributify: {},
    fluidSizing: {
      minContainerWidth: 320,
      maxContainerWidth: 1920,
      prefix: 'f-',
      attributify: true,
    },
    scalePx: {}, // or false
    unoVue: {
      reka: true,
      shadcn: false,
    },
    easingGradient: {},
    cssVar: {},
    animations: {},
  },
})
```

## Scale-to-Pixel System

**NOT a 4x multiplier** - it's a 1/4 divisor.

```
p-4  = 0.25rem = 4px   (1px × 4)
p-8  = 0.5rem  = 8px   (1px × 8)
p-16 = 1rem    = 16px  (1px × 16)
gap-24 = 1.5rem = 24px
```

All rem values divided by 4 with 0.0625rem (1px) base font.

## With nimiq-css

```ts
import { presetNimiq } from 'nimiq-css'
import { presetOnmax } from 'unocss-preset-onmax'

export default defineConfig({
  presets: [
    presetOnmax(),
    presetNimiq({
      utilities: true,
      attributifyUtilities: true,
      typography: true,
      fonts: false, // use @nuxt/fonts instead
    }),
  ],
})
```

## Custom Rules Example

```ts
export default defineConfig({
  presets: [presetOnmax()],
  rules: [
    ['shadow-sm', { 'box-shadow': '0 1px 2px 0 rgba(0, 0, 0, 0.05)' }],
    [/^area-(.+)$/, ([, name]) => ({ 'grid-area': name })],
  ],
  shortcuts: {
    'nq-grid-3': 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-24',
  },
})
```

## Disabling Sub-Presets

```ts
presetOnmax({
  presets: {
    animations: false,     // disable animations
    easingGradient: false, // disable gradient functions
  },
})
```
