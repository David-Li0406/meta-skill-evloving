# Color Tokens Reference

Complete list of theme color tokens from `site/src/index.css`.

## Light Mode (`:root`)

| Token | Value | Usage |
|-------|-------|-------|
| `--background` | `oklch(0.97 0.01 85)` | Page background (off-white/tan) |
| `--foreground` | `oklch(0.20 0.02 250)` | Primary text |
| `--card` | `oklch(0.98 0.008 85)` | Card backgrounds |
| `--card-foreground` | `oklch(0.20 0.02 250)` | Card text |
| `--popover` | `oklch(0.98 0.008 85)` | Popover backgrounds |
| `--popover-foreground` | `oklch(0.20 0.02 250)` | Popover text |
| `--primary` | `oklch(0.45 0.12 250)` | Primary actions (indigo) |
| `--primary-foreground` | `oklch(0.98 0 0)` | Text on primary |
| `--secondary` | `oklch(0.93 0.01 85)` | Secondary backgrounds |
| `--secondary-foreground` | `oklch(0.25 0.02 250)` | Secondary text |
| `--muted` | `oklch(0.93 0.01 85)` | Muted backgrounds |
| `--muted-foreground` | `oklch(0.45 0.02 250)` | Muted text |
| `--accent` | `oklch(0.55 0.10 180)` | Accent color (teal) |
| `--accent-foreground` | `oklch(0.15 0.02 180)` | Text on accent |
| `--destructive` | `oklch(0.55 0.22 27)` | Destructive actions (red) |
| `--border` | `oklch(0.88 0.02 85)` | Border color |
| `--input` | `oklch(0.90 0.015 85)` | Input backgrounds |
| `--ring` | `oklch(0.45 0.12 250)` | Focus ring color |

## Dark Mode (`.dark`)

| Token | Value | Usage |
|-------|-------|-------|
| `--background` | `oklch(0.14 0.02 260)` | Page background (dark purple) |
| `--foreground` | `oklch(0.93 0.01 260)` | Primary text |
| `--card` | `oklch(0.18 0.02 260)` | Card backgrounds |
| `--card-foreground` | `oklch(0.93 0.01 260)` | Card text |
| `--popover` | `oklch(0.18 0.02 260)` | Popover backgrounds |
| `--popover-foreground` | `oklch(0.93 0.01 260)` | Popover text |
| `--primary` | `oklch(0.72 0.16 195)` | Primary actions (neon cyan) |
| `--primary-foreground` | `oklch(0.14 0.02 195)` | Text on primary |
| `--secondary` | `oklch(0.22 0.02 260)` | Secondary backgrounds |
| `--secondary-foreground` | `oklch(0.93 0.01 260)` | Secondary text |
| `--muted` | `oklch(0.22 0.02 260)` | Muted backgrounds |
| `--muted-foreground` | `oklch(0.65 0.02 260)` | Muted text |
| `--accent` | `oklch(0.68 0.18 330)` | Accent color (neon pink) |
| `--accent-foreground` | `oklch(0.14 0.02 330)` | Text on accent |
| `--destructive` | `oklch(0.65 0.20 25)` | Destructive actions |
| `--border` | `oklch(0.28 0.03 260)` | Border color |
| `--input` | `oklch(0.25 0.025 260)` | Input backgrounds |
| `--ring` | `oklch(0.72 0.16 195)` | Focus ring color |

## Border Radius

| Token | Value |
|-------|-------|
| `--radius` | `0.625rem` (10px) |
| `--radius-sm` | `calc(var(--radius) - 4px)` |
| `--radius-md` | `calc(var(--radius) - 2px)` |
| `--radius-lg` | `var(--radius)` |
| `--radius-xl` | `calc(var(--radius) + 4px)` |
| `--radius-2xl` | `calc(var(--radius) + 8px)` |

## Using Tokens in Tailwind

Tokens are mapped to Tailwind classes via `@theme inline`:

```tsx
// Background colors
bg-background    // var(--background)
bg-card          // var(--card)
bg-primary       // var(--primary)
bg-secondary     // var(--secondary)
bg-muted         // var(--muted)
bg-accent        // var(--accent)
bg-destructive   // var(--destructive)

// Text colors
text-foreground        // var(--foreground)
text-card-foreground   // var(--card-foreground)
text-primary-foreground
text-muted-foreground
text-accent-foreground

// Border
border-border    // var(--border)
border-input     // var(--input)

// Ring (focus)
ring-ring        // var(--ring)

// Border radius
rounded-sm       // var(--radius-sm)
rounded-md       // var(--radius-md)
rounded-lg       // var(--radius-lg)
rounded-xl       // var(--radius-xl)
rounded-2xl      // var(--radius-2xl)
```

## Design Intent

**Light Mode:**
- Off-white/tan background for warmth (not pure white)
- Indigo primary for trust and professionalism
- Teal accent for visual interest

**Dark Mode:**
- Dark purple background with subtle hue
- Neon cyan primary for energy and modernity
- Neon pink accent for contrast
- Maintains readability with high contrast text
