# Mobile Color

Color principles adapted for mobile apps with dark mode support.

---

## Color System for Mobile

Same structure as web, but must work in both light AND dark modes.

**Categories:**

| Role | Light Mode | Dark Mode |
|------|------------|-----------|
| Background | White/Gray-50 | Gray-900/Black |
| Surface | White | Gray-800 |
| Primary | Brand color 600 | Brand color 400 |
| On-Primary | White | Gray-900 |
| Secondary | Gray-600 | Gray-400 |
| Disabled | Gray-300 | Gray-700 |

---

## Define Shade Palettes

9 shades per color (same process as web):

1. **Base (500):** Works as primary button background
2. **Darkest (900):** Text on light backgrounds
3. **Lightest (50-100):** Subtle backgrounds, tints
4. Fill gaps systematically

**Important:** In dark mode, lighter shades become primary (invert logic).

---

## Semantic Colors

Always define for both themes:

| Semantic | Light | Dark |
|----------|-------|------|
| Success | Green-700 | Green-400 |
| Warning | Amber-600 | Amber-400 |
| Error | Red-600 | Red-400 |
| Info | Blue-600 | Blue-400 |

---

## Dark Mode Considerations

- **Don't just invert:** Black backgrounds + white text is too harsh
- **Use gray-900 or gray-950:** Softer than pure black
- **Reduce saturation:** Vibrant colors glare on dark backgrounds
- **Elevation with lightness:** Higher surfaces = slightly lighter gray
- **Surface colors:** Gray-800 for cards on gray-900 background

---

## Contrast Requirements

| Content | Minimum Ratio |
|---------|---------------|
| Normal text | 4.5:1 |
| Large text (18sp+) | 3:1 |
| UI components | 3:1 |

**Test both themes** for contrast compliance.

---

## Don't Rely on Color Alone

Mobile accessibility is critical:

- Use icons with status colors
- Add text labels for colorblind users
- Shape differences for states (outlined vs filled)
