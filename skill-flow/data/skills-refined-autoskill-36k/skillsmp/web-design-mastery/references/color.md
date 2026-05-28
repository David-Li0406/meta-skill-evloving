# Color

Detailed principles for effective color usage in UI design.

---

## Ditch Hex for HSL

Hex and RGB don't represent colors intuitively.

**HSL components:**

- **Hue** (0-360°): Position on color wheel (0°=red, 120°=green, 240°=blue)
- **Saturation** (0-100%): How colorful (0%=grey, 100%=vibrant)
- **Lightness** (0-100%): How close to black/white (50%=pure color)

**HSL vs HSB:** Don't confuse them. In HSB, 100% brightness at 100% saturation is NOT white. Use HSL for web.

---

## You Need More Colors Than You Think

5 hex codes won't work. You need comprehensive palettes.

**What you actually need:**

| Category | Shades | Purpose |
|----------|--------|---------|
| Greys | 8-10 | Text, backgrounds, panels, borders |
| Primary | 5-10 | Actions, active states, links |
| Accents | 5-10 each | Success, warning, error, feature highlights |

**Grey notes:** True black looks unnatural. Start with really dark grey.

**Primary notes:** Ultra-light for tinted backgrounds (alerts), dark for text.

---

## Define Your Shades Up Front

Don't use CSS preprocessor functions (lighten, darken). Define fixed shades.

**Process:**

1. **Choose base color (500):** Should work as button background
2. **Find the edges:**
   - Darkest (900): Works for text on light background
   - Lightest (100): Works as tinted background
3. **Fill the gaps:**
   - First pass: 700, 300 (middle of gaps)
   - Second pass: 800, 600, 400, 200

**Result:** 9 shades (100-900), well-balanced, no more exhaustive decisions.

**For greys:** Same process. Darkest for darkest text, lightest for subtle off-white.

---

## Don't Let Lightness Kill Your Saturation

As lightness approaches 0% or 100%, saturation appears weaker.

**Solution:** Increase saturation as lightness moves away from 50%.

**Perceived brightness hack:** Different hues have different perceived brightness.

- Yellow, cyan, magenta = bright
- Red, green, blue = dark

**Adjusting brightness via hue:**

- To lighten: Rotate hue toward 60°, 180°, or 300°
- To darken: Rotate hue toward 0°, 120°, or 240°
- Don't rotate more than 20-30° (looks like different color)

**Example - Yellow palette:** Rotate toward orange as you decrease lightness. Darker shades feel warm and rich instead of dull brown.

---

## Greys Don't Have to Be Grey

True grey has 0% saturation. Real "grey" palettes are often saturated.

**Color temperature:**

- **Cool greys:** Saturate with blue
- **Warm greys:** Saturate with yellow/orange

**Important:** Increase saturation for lighter/darker shades too, or they look washed out compared to middle greys.

---

## Accessible Doesn't Have to Mean Ugly

**WCAG recommendations:**

- Normal text (<18px): 4.5:1 contrast ratio
- Large text: 3:1 contrast ratio

**Problem with white on color:** Often needs very dark color to meet 4.5:1.

**Solution 1 - Flip the contrast:**

- Instead of light text on dark color
- Use dark colored text on light colored background
- Less in-your-face, doesn't interfere with other actions

**Solution 2 - Rotate the hue:**

- Hard to meet contrast with colored text on colored background
- Rotate hue toward brighter color (cyan, magenta, yellow)
- Increases contrast while staying colorful

---

## Don't Rely on Color Alone

Color blind users can't distinguish some colors.

**Examples to fix:**

- Metric cards with red/green trends: Add icons (up/down arrows)
- Graph lines with different colors: Use contrast (light/dark) instead

**Rule:** Color should support what design is already saying, never be the only communication.
