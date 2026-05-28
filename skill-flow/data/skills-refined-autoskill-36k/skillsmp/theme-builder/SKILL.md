---
name: theme-builder
description: Create custom color themes for Tailwind CSS v4 using shadcn/ui conventions. Use when asked to "create a color scheme", "generate a theme for [topic]", "add custom colors", or "build a palette for [brand/mood/concept]".
---

# Theme Builder (shadcn/ui Convention)

Generate custom themes using semantic color tokens following shadcn/ui patterns.

## Theme Structure

```css
@import "tailwindcss";

:root {
  --font-sans: AR One Sans, ui-sans-serif, system-ui, sans-serif;
  --font-serif: Abyssinica SIL, ui-serif, serif;
  --font-mono: Chivo Mono, ui-monospace, monospace;
  --radius: 0.625rem;
  --background: oklch(1 0 0);
  --foreground: oklch(0.145 0 0);
  --card: oklch(1 0 0);
  --card-foreground: oklch(0.145 0 0);
  --popover: oklch(1 0 0);
  --popover-foreground: oklch(0.145 0 0);
  --primary: oklch(0.205 0 0);
  --primary-foreground: oklch(0.985 0 0);
  --secondary: oklch(0.97 0 0);
  --secondary-foreground: oklch(0.205 0 0);
  --muted: oklch(0.97 0 0);
  --muted-foreground: oklch(0.556 0 0);
  --accent: oklch(0.97 0 0);
  --accent-foreground: oklch(0.205 0 0);
  --destructive: oklch(0.577 0.245 27.325);
  --border: oklch(0.922 0 0);
  --input: oklch(0.922 0 0);
  --ring: oklch(0.708 0 0);
  --chart-1: oklch(0.646 0.222 41.116);
  --chart-2: oklch(0.6 0.118 184.704);
  --chart-3: oklch(0.398 0.07 227.392);
  --chart-4: oklch(0.828 0.189 84.429);
  --chart-5: oklch(0.769 0.188 70.08);
  --sidebar: oklch(0.985 0 0);
  --sidebar-foreground: oklch(0.145 0 0);
  --sidebar-primary: oklch(0.205 0 0);
  --sidebar-primary-foreground: oklch(0.985 0 0);
  --sidebar-accent: oklch(0.97 0 0);
  --sidebar-accent-foreground: oklch(0.205 0 0);
  --sidebar-border: oklch(0.922 0 0);
  --sidebar-ring: oklch(0.708 0 0);
  --destructive-foreground: oklch(0.985 0 0);
  --info: oklch(0.646 0.222 41.116);
  --info-foreground: oklch(0.985 0 0);
  --success: oklch(0.398 0.07 227.392);
  --success-foreground: oklch(0.985 0 0);
  --warning: oklch(0.828 0.189 84.429);
  --warning-foreground: oklch(0.985 0 0);
}

.dark {
  --background: oklch(0.145 0 0);
  --foreground: oklch(0.985 0 0);
  --card: oklch(0.205 0 0);
  --card-foreground: oklch(0.985 0 0);
  --popover: oklch(0.269 0 0);
  --popover-foreground: oklch(0.985 0 0);
  --primary: oklch(0.922 0 0);
  --primary-foreground: oklch(0.205 0 0);
  --secondary: oklch(0.269 0 0);
  --secondary-foreground: oklch(0.985 0 0);
  --muted: oklch(0.269 0 0);
  --muted-foreground: oklch(0.708 0 0);
  --accent: oklch(0.371 0 0);
  --accent-foreground: oklch(0.985 0 0);
  --destructive: oklch(0.704 0.191 22.216);
  --border: oklch(1 0 0 / 10%);
  --input: oklch(1 0 0 / 15%);
  --ring: oklch(0.556 0 0);
  --chart-1: oklch(0.488 0.243 264.376);
  --chart-2: oklch(0.696 0.17 162.48);
  --chart-3: oklch(0.769 0.188 70.08);
  --chart-4: oklch(0.627 0.265 303.9);
  --chart-5: oklch(0.645 0.246 16.439);
  --sidebar: oklch(0.205 0 0);
  --sidebar-foreground: oklch(0.985 0 0);
  --sidebar-primary: oklch(0.488 0.243 264.376);
  --sidebar-primary-foreground: oklch(0.985 0 0);
  --sidebar-accent: oklch(0.269 0 0);
  --sidebar-accent-foreground: oklch(0.985 0 0);
  --sidebar-border: oklch(1 0 0 / 10%);
  --sidebar-ring: oklch(0.439 0 0);
  --destructive-foreground: oklch(0.985 0 0);
  --info: oklch(0.646 0.222 41.116);
  --info-foreground: oklch(0.985 0 0);
  --success: oklch(0.398 0.07 227.392);
  --success-foreground: oklch(0.985 0 0);
  --warning: oklch(0.828 0.189 84.429);
  --warning-foreground: oklch(0.985 0 0);
}
```

## Token Reference

| Token                      | Purpose                             |
| -------------------------- | ----------------------------------- |
| `--background`             | Page background                     |
| `--foreground`             | Default text color                  |
| `--card`                   | Card background                     |
| `--card-foreground`        | Card text                           |
| `--popover`                | Popover/dropdown background         |
| `--popover-foreground`     | Popover text                        |
| `--primary`                | Primary buttons, links              |
| `--primary-foreground`     | Text on primary                     |
| `--secondary`              | Secondary buttons                   |
| `--secondary-foreground`   | Text on secondary                   |
| `--muted`                  | Muted backgrounds                   |
| `--muted-foreground`       | Muted/subtle text                   |
| `--accent`                 | Hover highlights                    |
| `--accent-foreground`      | Text on accent                      |
| `--destructive`            | Destructive actions (delete, error) |
| `--border`                 | Default borders                     |
| `--input`                  | Input borders                       |
| `--ring`                   | Focus rings                         |
| `--chart-1` to `--chart-5` | Chart/graph colors                  |
| `--sidebar`                | Sidebar background                  |
| `--sidebar-*`              | Sidebar-specific variants           |
| `--radius`                 | Default border radius               |
| `--font-sans`              | Sans-serif font stack               |
| `--font-serif`             | Serif font stack                    |
| `--font-mono`              | Monospace font stack                |

## Font Selection Examples

Choose fonts that match the theme's personality:

| Style            | Sans                             | Serif                  | Mono           |
| ---------------- | -------------------------------- | ---------------------- | -------------- |
| **Modern/Clean** | Inter, Geist                     | Source Serif 4         | Geist Mono     |
| **Brutalist**    | Helvetica Neue, Akzidenz-Grotesk | None                   | IBM Plex Mono  |
| **Friendly**     | AR One Sans, Nunito              | Merriweather           | Fira Code      |
| **Editorial**    | Archivo, Sora                    | Playfair Display, Lora | JetBrains Mono |
| **Technical**    | IBM Plex Sans                    | IBM Plex Serif         | IBM Plex Mono  |
| **Elegant**      | Cormorant Garamond               | Libre Baskerville      | DM Mono        |

Always include fallbacks: `ui-sans-serif, system-ui, sans-serif`

## OKLCH Format

`oklch(lightness chroma hue)` or `oklch(lightness chroma hue / alpha)`

- **Lightness**: 0 (black) to 1 (white)
- **Chroma**: 0 (gray) to ~0.4 (saturated)
- **Hue**: 0-360 color wheel

### Hue Reference

| Hue     | Color     |
| ------- | --------- |
| 0-30    | Red       |
| 30-60   | Orange    |
| 60-90   | Yellow    |
| 90-150  | Green     |
| 150-200 | Teal/Cyan |
| 200-260 | Blue      |
| 260-300 | Purple    |
| 300-330 | Pink      |
| 330-360 | Rose      |

## Example: Ocean Theme

```css
:root {
  --font-sans: Inter, ui-sans-serif, system-ui, sans-serif;
  --font-serif: Source Serif 4, ui-serif, serif;
  --font-mono: Geist Mono, ui-monospace, monospace;
  --radius: 0.5rem;
  --background: oklch(0.985 0.01 220);
  --foreground: oklch(0.2 0.02 220);
  --card: oklch(1 0 0);
  --card-foreground: oklch(0.2 0.02 220);
  --popover: oklch(1 0 0);
  --popover-foreground: oklch(0.2 0.02 220);
  --primary: oklch(0.55 0.2 220);
  --primary-foreground: oklch(0.98 0 0);
  --secondary: oklch(0.95 0.02 220);
  --secondary-foreground: oklch(0.25 0.02 220);
  --muted: oklch(0.95 0.01 220);
  --muted-foreground: oklch(0.5 0.02 220);
  --accent: oklch(0.92 0.03 220);
  --accent-foreground: oklch(0.25 0.02 220);
  --destructive: oklch(0.577 0.245 27.325);
  --border: oklch(0.9 0.02 220);
  --input: oklch(0.9 0.02 220);
  --ring: oklch(0.55 0.2 220);
  --chart-1: oklch(0.55 0.2 220);
  --chart-2: oklch(0.65 0.15 180);
  --chart-3: oklch(0.6 0.18 260);
  --chart-4: oklch(0.7 0.15 150);
  --chart-5: oklch(0.65 0.2 30);
}

.dark {
  --background: oklch(0.15 0.02 220);
  --foreground: oklch(0.95 0.01 220);
  --card: oklch(0.2 0.02 220);
  --card-foreground: oklch(0.95 0.01 220);
  --popover: oklch(0.22 0.02 220);
  --popover-foreground: oklch(0.95 0.01 220);
  --primary: oklch(0.65 0.18 220);
  --primary-foreground: oklch(0.1 0.02 220);
  --secondary: oklch(0.25 0.02 220);
  --secondary-foreground: oklch(0.95 0.01 220);
  --muted: oklch(0.25 0.02 220);
  --muted-foreground: oklch(0.65 0.02 220);
  --accent: oklch(0.3 0.03 220);
  --accent-foreground: oklch(0.95 0.01 220);
  --destructive: oklch(0.65 0.22 25);
  --border: oklch(1 0 0 / 10%);
  --input: oklch(1 0 0 / 15%);
  --ring: oklch(0.65 0.18 220);
  --chart-1: oklch(0.6 0.2 220);
  --chart-2: oklch(0.65 0.15 180);
  --chart-3: oklch(0.7 0.18 260);
  --chart-4: oklch(0.65 0.15 150);
  --chart-5: oklch(0.7 0.2 30);
}
```

## Example: Forest Theme

```css
:root {
  --font-sans: Nunito, ui-sans-serif, system-ui, sans-serif;
  --font-serif: Merriweather, ui-serif, serif;
  --font-mono: Fira Code, ui-monospace, monospace;
  --radius: 0.75rem;
  --background: oklch(0.98 0.01 145);
  --foreground: oklch(0.2 0.03 145);
  --card: oklch(1 0 0);
  --card-foreground: oklch(0.2 0.03 145);
  --popover: oklch(1 0 0);
  --popover-foreground: oklch(0.2 0.03 145);
  --primary: oklch(0.5 0.15 145);
  --primary-foreground: oklch(0.98 0 0);
  --secondary: oklch(0.94 0.02 145);
  --secondary-foreground: oklch(0.25 0.03 145);
  --muted: oklch(0.94 0.01 145);
  --muted-foreground: oklch(0.5 0.02 145);
  --accent: oklch(0.9 0.03 145);
  --accent-foreground: oklch(0.25 0.03 145);
  --destructive: oklch(0.577 0.245 27.325);
  --border: oklch(0.88 0.02 145);
  --input: oklch(0.88 0.02 145);
  --ring: oklch(0.5 0.15 145);
  --chart-1: oklch(0.5 0.15 145);
  --chart-2: oklch(0.55 0.12 180);
  --chart-3: oklch(0.6 0.1 90);
  --chart-4: oklch(0.45 0.1 30);
  --chart-5: oklch(0.65 0.15 120);
}

.dark {
  --background: oklch(0.15 0.02 145);
  --foreground: oklch(0.95 0.01 145);
  --card: oklch(0.2 0.02 145);
  --card-foreground: oklch(0.95 0.01 145);
  --popover: oklch(0.22 0.02 145);
  --popover-foreground: oklch(0.95 0.01 145);
  --primary: oklch(0.6 0.15 145);
  --primary-foreground: oklch(0.1 0.02 145);
  --secondary: oklch(0.25 0.02 145);
  --secondary-foreground: oklch(0.95 0.01 145);
  --muted: oklch(0.25 0.02 145);
  --muted-foreground: oklch(0.65 0.02 145);
  --accent: oklch(0.3 0.03 145);
  --accent-foreground: oklch(0.95 0.01 145);
  --destructive: oklch(0.65 0.22 25);
  --border: oklch(1 0 0 / 10%);
  --input: oklch(1 0 0 / 15%);
  --ring: oklch(0.6 0.15 145);
  --chart-1: oklch(0.55 0.15 145);
  --chart-2: oklch(0.6 0.12 180);
  --chart-3: oklch(0.65 0.1 90);
  --chart-4: oklch(0.5 0.1 30);
  --chart-5: oklch(0.7 0.15 120);
}
```

## Usage in Components

```tsx
<div className="bg-background text-foreground">
  <div className="rounded-lg border bg-card text-card-foreground">
    <button className="bg-primary text-primary-foreground">Action</button>
    <button className="bg-secondary text-secondary-foreground">Cancel</button>
    <p className="text-muted-foreground">Helper text</p>
  </div>
</div>
```

## Design Guidelines

1. **Foreground tokens** always pair with their background (e.g., `--primary` with `--primary-foreground`)
2. **Light mode**: Higher lightness for backgrounds (~0.95-1), lower for foregrounds (~0.15-0.3)
3. **Dark mode**: Invert the pattern, use subtle opacity for borders (`oklch(1 0 0 / 10%)`)
4. **Keep chroma consistent** within a theme for visual harmony
5. **Destructive** should always be red-ish (hue ~25-30) for universal recognition
6. **Charts** should have distinct hues for accessibility
7. **Fonts** should match theme personality - brutalist uses heavy grotesks, elegant uses serifs
