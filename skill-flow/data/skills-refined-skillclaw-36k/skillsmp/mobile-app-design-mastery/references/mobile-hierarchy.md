# Mobile Visual Hierarchy

Hierarchy principles adapted for mobile screens where space is limited.

---

## Critical on Mobile

On desktop, multiple elements can coexist. On mobile, every pixel counts. Poor hierarchy makes apps feel cluttered and unusable.

**Three-tier system:**

| Tier | Treatment | Example |
|------|-----------|---------|
| Primary | Large, bold, dark | Screen title, main action |
| Secondary | Medium, regular, gray-600 | Supporting text, dates |
| Tertiary | Small, light, gray-400 | Metadata, timestamps |

---

## Size Matters More (But Don't Overdo It)

- Mobile already has size constraints—don't make primary text huge
- Body text: 14-16sp is comfortable
- Titles: 20-28sp is usually sufficient
- Use weight (semibold/bold) before increasing size
- Use color (gray levels) for de-emphasis

---

## Emphasize by De-emphasizing

When the main element doesn't stand out:

- Don't make it bigger/bolder
- Make competing elements softer/lighter/smaller

**Example:** List item titles not standing out?

- Don't increase title size
- Reduce subtitle color to gray-500

---

## Labels on Mobile

Screen real estate is precious. Labels add visual weight.

**Strategies:**

1. **Format speaks for itself:** Email, phone, price don't need labels
2. **Combine label + value:** "Stock: 12" → "12 in stock"
3. **Use icons instead of labels:** Location pin, calendar, clock
4. **De-emphasize labels:** Smaller, lighter, uppercase tracking

---

## Icon Weight Balance

Icons (especially filled) are heavy and compete with text.

**Solution:** Give icons softer colors than text

- Text: gray-900
- Icons: gray-500 or brand color at 60% opacity

**Exception:** Primary action icons (FAB) should be prominent.

---

## Mobile Button Hierarchy

| Level | Style | Placement |
|-------|-------|-----------|
| Primary | Filled, high contrast | Bottom of screen, single per view |
| Secondary | Outlined or tonal | Near primary or in toolbars |
| Tertiary | Text only | Inline, navigation |

**Destructive actions:** Tertiary style on normal screens, primary red only on confirmation dialogs.
