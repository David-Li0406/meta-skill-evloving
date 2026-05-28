# nimiq-css Design System

## Installation

```bash
pnpm add -D nimiq-css
```

## Configuration

```ts
import { presetNimiq } from 'nimiq-css'

export default defineConfig({
  presets: [
    presetOnmax(),
    presetNimiq({
      utilities: true,           // nq-* utilities
      attributifyUtilities: true, // attribute mode
      typography: true,          // prose styles
      staticContent: true,       // markdown styles
      scrollbar: false,          // custom scrollbar
      fonts: false,              // use @nuxt/fonts
      icons: true,               // i-nimiq:* icons
    }),
  ],
})
```

## Color System

### Base Colors
```
neutral, blue, green, orange, gold, red, purple
```

### Color Scale (0-1100)
```vue
<div bg-neutral-0>      <!-- lightest -->
<div bg-neutral-50>
<div bg-neutral-100>
<div bg-neutral-200>
<!-- ... -->
<div bg-neutral-900>
<div bg-neutral-1000>
<div bg-neutral-1100>   <!-- darkest -->
```

### With Opacity
```vue
<div bg="neutral/20">           <!-- 20% opacity -->
<div text="neutral-800/50">
<div outline="neutral-0/15">
```

## Typography Utilities

```vue
<h1 nq-heading>Main Heading</h1>
<h2 nq-heading-lg>Large Heading</h2>
<span nq-label>Label Text</span>
<p nq-raw>Raw text without prose</p>
```

## Prose Styles

```vue
<article nq-prose>
  <!-- Styled markdown content -->
</article>

<article nq-prose-compact>
  <!-- Tighter prose spacing -->
</article>
```

## Button Utilities

```vue
<!-- Size variants -->
<button nq-button-s>Small</button>
<button nq-button>Default</button>

<!-- Color variants -->
<button nq-button-s nq-button-blue>Primary</button>
<button nq-button-s nq-button-secondary>Secondary</button>
<button nq-button-s nq-button-tertiary>Tertiary</button>

<!-- Ghost -->
<button nq-ghost-btn>Ghost</button>
```

## Pills/Badges

```vue
<span nq-pill>Default</span>
<span nq-pill nq-pill-blue>Blue</span>
<span nq-pill nq-pill-secondary>Secondary</span>
<span nq-pill nq-pill-tertiary>Tertiary</span>
<span nq-pill nq-pill-red>Red</span>
<span nq-pill nq-pill-lg>Large</span>
```

## Arrow/Link Utilities

```vue
<a nq-arrow>Link with arrow →</a>
<a nq-arrow-back>← Back link</a>
```

## Interactive Utilities

```vue
<div nq-hoverable>
  <!-- Hover effect card -->
</div>

<div nq-hoverable-cta>
  <!-- CTA hover effect -->
</div>
```

## Input Utilities

```vue
<input nq-input-box>
<input nq-input-box-s>  <!-- small variant -->
<div nq-switch>         <!-- toggle switch -->
```

## Layout Utilities

```vue
<section nq-section-gap>
  <!-- Standard section spacing -->
</section>
```

## Stack Utility

Centers children in overlapping grid:

```vue
<div stack>
  <img>           <!-- Both centered, overlapping -->
  <div>Overlay</div>
</div>
```

Generates:
```css
.stack { display: grid; place-content: center; }
.stack > * { grid-area: 1/1; justify-self: center; align-self: center; }
```

## Scrollbar Utilities

```vue
<div nq-scrollbar-hide>    <!-- Hide scrollbar -->
<div of-x-auto>            <!-- Horizontal scroll -->
```

## Icons (i-nimiq:*)

```vue
<i i-nimiq:logos-nimiq-mono />
<i i-nimiq:globe />
<i i-nimiq:verified-filled />
<i i-nimiq:spinner animate-spin />
<i i-nimiq:arrow-right />
<i i-nimiq:duotone-fluctuations />
```

## CSS Variables

```css
--colors-neutral
--colors-blue
--colors-green
/* etc */

--nq-max-width      /* Container max width */
--nq-ease           /* Easing function */
--nq-prose-max-width
```

## Grid Shortcuts (Custom)

```ts
// Add to config
shortcuts: {
  'nq-grid-2': 'grid grid-cols-1 md:grid-cols-2 gap-24',
  'nq-grid-3': 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-24',
  'nq-grid-4': 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-24',
}
```
