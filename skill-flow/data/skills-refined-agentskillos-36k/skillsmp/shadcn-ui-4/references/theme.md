# Algoma Jobs Theme Reference

Complete CSS theme variables for the public-facing application.

## Color Philosophy

| Color Role | Light Mode | Dark Mode | Semantic Use |
|------------|------------|-----------|--------------|
| **Primary** | Copper orange | Lighter copper | CTAs, active states, focus rings |
| **Secondary** | Teal | Teal | Secondary buttons, badges |
| **Muted** | Light gray | Dark gray | Backgrounds, disabled states |
| **Accent** | Near white | Medium gray | Hover backgrounds |
| **Destructive** | Red | Teal (dark) | Errors, warnings, delete |

## Complete Theme CSS

Copy this to `resources/css/app.css`:

```css
:root {
  --background: oklch(1.0000 0 0);
  --foreground: oklch(0.2101 0.0318 264.6645);
  --card: oklch(1.0000 0 0);
  --card-foreground: oklch(0.2101 0.0318 264.6645);
  --popover: oklch(1.0000 0 0);
  --popover-foreground: oklch(0.2101 0.0318 264.6645);
  --primary: oklch(0.6716 0.1368 48.5130);
  --primary-foreground: oklch(1.0000 0 0);
  --secondary: oklch(0.5360 0.0398 196.0280);
  --secondary-foreground: oklch(1.0000 0 0);
  --muted: oklch(0.9670 0.0029 264.5419);
  --muted-foreground: oklch(0.5510 0.0234 264.3637);
  --accent: oklch(0.9491 0 0);
  --accent-foreground: oklch(0.2101 0.0318 264.6645);
  --destructive: oklch(0.6368 0.2078 25.3313);
  --border: oklch(0.9276 0.0058 264.5313);
  --input: oklch(0.9276 0.0058 264.5313);
  --ring: oklch(0.6716 0.1368 48.5130);
  --chart-1: oklch(0.5940 0.0443 196.0233);
  --chart-2: oklch(0.7214 0.1337 49.9802);
  --chart-3: oklch(0.8721 0.0864 68.5474);
  --chart-4: oklch(0.6268 0 0);
  --chart-5: oklch(0.6830 0 0);
  --sidebar: oklch(0.9670 0.0029 264.5419);
  --sidebar-foreground: oklch(0.2101 0.0318 264.6645);
  --sidebar-primary: oklch(0.6716 0.1368 48.5130);
  --sidebar-primary-foreground: oklch(1.0000 0 0);
  --sidebar-accent: oklch(1.0000 0 0);
  --sidebar-accent-foreground: oklch(0.2101 0.0318 264.6645);
  --sidebar-border: oklch(0.9276 0.0058 264.5313);
  --sidebar-ring: oklch(0.6716 0.1368 48.5130);
  --radius: 0.625rem;
}

.dark {
  --background: oklch(0.1797 0.0043 308.1928);
  --foreground: oklch(0.8109 0 0);
  --card: oklch(0.1822 0 0);
  --card-foreground: oklch(0.8109 0 0);
  --popover: oklch(0.1797 0.0043 308.1928);
  --popover-foreground: oklch(0.8109 0 0);
  --primary: oklch(0.7214 0.1337 49.9802);
  --primary-foreground: oklch(0.1797 0.0043 308.1928);
  --secondary: oklch(0.5940 0.0443 196.0233);
  --secondary-foreground: oklch(0.1797 0.0043 308.1928);
  --muted: oklch(0.2520 0 0);
  --muted-foreground: oklch(0.6268 0 0);
  --accent: oklch(0.3211 0 0);
  --accent-foreground: oklch(0.8109 0 0);
  --destructive: oklch(0.5940 0.0443 196.0233);
  --border: oklch(0.2520 0 0);
  --input: oklch(0.2520 0 0);
  --ring: oklch(0.7214 0.1337 49.9802);
  --chart-1: oklch(0.5940 0.0443 196.0233);
  --chart-2: oklch(0.7214 0.1337 49.9802);
  --chart-3: oklch(0.8721 0.0864 68.5474);
  --chart-4: oklch(0.6268 0 0);
  --chart-5: oklch(0.6830 0 0);
  --sidebar: oklch(0.1822 0 0);
  --sidebar-foreground: oklch(0.8109 0 0);
  --sidebar-primary: oklch(0.7214 0.1337 49.9802);
  --sidebar-primary-foreground: oklch(0.1797 0.0043 308.1928);
  --sidebar-accent: oklch(0.3211 0 0);
  --sidebar-accent-foreground: oklch(0.8109 0 0);
  --sidebar-border: oklch(0.2520 0 0);
  --sidebar-ring: oklch(0.7214 0.1337 49.9802);
}
```

## Tailwind Usage

### Backgrounds

```tsx
bg-background      // Page background
bg-card            // Card surfaces
bg-popover         // Dropdowns, modals
bg-muted           // Subtle backgrounds
bg-accent          // Hover states
bg-primary         // Primary buttons
bg-secondary       // Secondary buttons
bg-destructive     // Error/danger
```

### Text Colors

```tsx
text-foreground         // Primary text
text-card-foreground    // Text on cards
text-muted-foreground   // Secondary/subtle text
text-primary            // Branded text
text-primary-foreground // Text on primary bg
text-destructive        // Error text
```

### Borders

```tsx
border-border      // Default borders
border-input       // Form input borders
border-ring        // Focus rings (via ring-ring)
```

### Charts

```tsx
bg-chart-1  // Teal
bg-chart-2  // Copper
bg-chart-3  // Gold
bg-chart-4  // Gray
bg-chart-5  // Light gray
```

## Example Component Styling

### Primary Button

```tsx
<Button className="bg-primary text-primary-foreground hover:bg-primary/90">
  Submit
</Button>
```

### Card

```tsx
<Card className="bg-card text-card-foreground border-border">
  <CardContent>Content here</CardContent>
</Card>
```

### Form Input

```tsx
<Input className="border-input bg-background text-foreground focus:ring-ring" />
```

### Error State

```tsx
<p className="text-sm text-destructive">This field is required</p>
```

## OKLCH Color Reference

OKLCH format: `oklch(lightness chroma hue)`

- **Lightness**: 0 (black) to 1 (white)
- **Chroma**: 0 (gray) to ~0.4 (vivid)
- **Hue**: 0-360 degrees (red=0, yellow=90, green=150, cyan=195, blue=265, purple=310)

### Key Hues in Theme

| Hue | Color | Usage |
|-----|-------|-------|
| 48-50 | Copper/Orange | Primary |
| 196 | Teal | Secondary |
| 264-265 | Blue-violet | Foreground text |
| 308 | Purple-gray | Dark backgrounds |
| 25 | Red-orange | Destructive |
| 68 | Gold | Charts |
