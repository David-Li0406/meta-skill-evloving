---
name: daisyui
description: Build UIs with DaisyUI component library. Use when creating interfaces with DaisyUI, styling Tailwind projects with semantic components, or customizing DaisyUI themes.
---

Use semantic DaisyUI classes over raw Tailwind utilities. DaisyUI provides 65 components with built-in variants.

## Idiomatic Usage

```html
<!-- Prefer semantic classes -->
<button class="btn btn-primary">Click</button>
<div class="card bg-base-100 shadow-xl">...</div>
<input class="input input-bordered" />

<!-- NOT raw Tailwind -->
<button class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded">
  This is bad design
</button>
```

**Customization priority**: DaisyUI variants → Tailwind utilities → CSS `@apply`

**Theme application**:

```html
<html data-theme="dark">
  <div data-theme="light"><!-- nested themes supported --></div>
</html>
```

## Theme Customization

**Config** (CSS file):

```css
@plugin "daisyui" {
  themes:
    light --default,
    dark --prefersdark;
}
```

**Custom theme**:

```css
@plugin "daisyui/theme" {
  name: "mytheme";
  default: true;
  --color-primary: oklch(55% 0.3 240);
  --color-secondary: oklch(70% 0.25 200);
  --color-accent: oklch(65% 0.28 150);
  --color-neutral: oklch(30% 0.02 260);
  --color-base-100: oklch(98% 0.01 260);
  --color-base-200: oklch(94% 0.01 260);
  --color-base-300: oklch(90% 0.02 260);
}
```

**Color variables**:
| Variable | Purpose |
|----------|---------|
| `--color-primary/secondary/accent` | Brand colors |
| `--color-neutral` | Low-saturation UI |
| `--color-base-100/200/300` | Backgrounds (light→dark) |
| `--color-info/success/warning/error` | Feedback |
| `*-content` | Foreground on each background |

## Components (65)

| Category         | Components                                                                                                                |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------- |
| **Actions**      | btn, dropdown, modal, swap, theme-controller                                                                              |
| **Data Display** | accordion, avatar, badge, card, carousel, chat, collapse, countdown, diff, kbd, list, stat, status, table, timeline       |
| **Navigation**   | breadcrumbs, dock, link, menu, navbar, pagination, steps, tabs                                                            |
| **Feedback**     | alert, loading, progress, radial-progress, skeleton, toast, tooltip                                                       |
| **Input**        | calendar, checkbox, fieldset, file-input, filter, label, radio, range, rating, select, input, textarea, toggle, validator |
| **Layout**       | divider, drawer, footer, hero, indicator, join, mask, stack                                                               |
| **Mockup**       | browser, code, phone, window                                                                                              |

## Built-in Themes (35)

light, dark, cupcake, bumblebee, emerald, corporate, synthwave, retro, cyberpunk, valentine, halloween, garden, forest, aqua, lofi, pastel, fantasy, wireframe, black, luxury, dracula, cmyk, autumn, business, acid, lemonade, night, coffee, winter, dim, nord, sunset, caramellatte, abyss, silk

for real applications, you usually want to design your own color schema.

## Common Patterns

Use semantic HTML elements with DaisyUI classes:

```html
<!-- Card -->
<article class="card bg-base-100 shadow-xl">
  <section class="card-body">
    <h2 class="card-title">Title</h2>
    <p>Content</p>
    <footer class="card-actions justify-end">
      <button class="btn btn-primary">Action</button>
    </footer>
  </section>
</article>

<!-- Navigation -->
<nav class="navbar bg-base-100">
  <a class="navbar-start btn btn-ghost text-xl" href="/">Logo</a>
  <menu class="navbar-end">
    <li><button class="btn btn-primary">Login</button></li>
  </menu>
</nav>

<!-- Form -->
<form>
  <fieldset class="fieldset">
    <label class="label" for="email">Email</label>
    <input id="email" type="email" class="input input-bordered" required />
  </fieldset>
</form>
```
